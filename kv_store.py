#!/usr/bin/python
"""Key Value."""
import queue
import logging
import ipaddress
import json
import os
import requests
import click
from flask import Flask, request, Response
from flask.helpers import stream_with_context


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Initialize empty dataset
kvstore = dict()

# Queue for event stream
msg_queue = queue.Queue()

WATCHERS_COUNT = 0


@app.route("/")
def test_run():
    """sf."""
    return 'you can hit your request on "/get", "/set" or "/sub".'


@app.route("/get/<key>", methods=["GET"])
def get_key(key):
    """sad."""
    if key in kvstore.keys():
        app.logger.info("%s - Key exists", key)
        return {'value': kvstore.get(key)}
    else:
        app.logger.info("%s - Key does not exist", key)
        return ({'value': 'Error - Key not found'}, 404)


@app.route("/set", methods=["PUT"])
def update_dataset():
    """asd."""
    fetch_request_data = request.get_json(force=True)
    app.logger.info("Processing set request.")
    for key in fetch_request_data.keys():
        key_operation = "Creating"
        if key in kvstore.keys():
            key_operation = "Updating"
            if WATCHERS_COUNT:
                msg_queue.put("Updated key  - {}".format(key))
        else:
            if WATCHERS_COUNT:
                msg_queue.put("Created key  - {}".format(key))
        app.logger.info("%s key - %s", key_operation, key)
    kvstore.update(fetch_request_data)
    app.logger.info("Processed set request successfully.")
    return {'value': 'published'}


def event_stream():
    """Yield Events from the event queue for watch functionality."""
    try:
        while True:
            message = msg_queue.get()
            print("aa gya watch me")
            print("yield test %s", message)
            yield "{}\n".format(message)
    except GeneratorExit:
        print("bahr mu mai ab watch se")
        global WATCHERS_COUNT
        WATCHERS_COUNT -= 1
        print("on exit", WATCHERS_COUNT)


@app.route("/watch")
def subscribe_to_events():
    """Consume Queue events FIFO with exactly once delivery for events."""
    app.logger.info("Event consumer initialized.")
    global WATCHERS_COUNT
    WATCHERS_COUNT += 1
    print("on entry", WATCHERS_COUNT)
    return Response(stream_with_context(event_stream()),
                    mimetype="text/event-stream")


@click.command(no_args_is_help=True)
@click.option('--server', '-s', default=False, is_flag=True,
              help='Runs KV app in server mode')
@click.option('--serverip', '-i', default="0.0.0.0",
              help='Number of greetings.')
@click.option('--serverport', '-p', default=80,
              type=click.IntRange(1024, 49151), help='The person to greet.')
@click.option('--get', '-G', default=None, help='Runs KV app in server mode')
@click.option('--put', '-P', default=None, type=(str, str),
              help='Runs KV app in server mode')
@click.option('--watch', '-W', default=False, is_flag=True,
              help='Runs KV app in server mode')
@click.option('--endpoint', '-e', default="http://localhost",
              help='Runs KV app in server mode')
def server_kv(server=False, serverip="0.0.0.0", serverport="80", get=None,
              put=None, watch=False, endpoint="http://localhost"):
    """sad."""
    if os.environ.get("KV_SERVER_IP") is not None:
        serverip = os.environ.get("KV_SERVER_IP")
    if os.environ.get("KV_SERVER_PORT") is not None:
        serverport = os.environ.get("KV_SERVER_PORT")
    if server:
        try:
            ipaddress.ip_address(serverip)
        except ValueError:
            click.echo('Invalid IP address is invalid')
            return
        app.run(
            host=serverip,
            port=serverport,
            threaded=True
        )
        return
    if get:
        cli_get(get, endpoint)
        return
    if put:
        cli_put(put, endpoint)
        return
    if watch:
        cli_watch(endpoint)
        return


def cli_get(key, endpoint):
    """sad."""
    response = requests.get(f"{endpoint}/get/{key}")
    resp = response.json()
    click.echo(resp['value'])


def cli_put(key, endpoint):
    """sad."""
    key, value = key
    response = requests.put(f"{endpoint}/set",
                            data=json.dumps({key: value}))
    resp = response.json()
    click.echo(resp['value'])


def cli_watch(endpoint):
    """asd."""
    word = []
    with requests.get(f'{endpoint}/watch', stream=True) as response:
        for data in response.iter_content(decode_unicode=True):
            word.append(data)
            if data == '\n':
                print(''.join(word))
                word.clear()


if __name__ == "__main__":
    server_kv()
