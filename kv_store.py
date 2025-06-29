#!/usr/bin/python3
"""Simple key value store application"""
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

# Initialize empty dataset for kv
kvstore = dict()

# Queue for event stream
msg_queue = queue.Queue()

# For /watch user count
WATCHERS_COUNT = 0


@app.route("/")
def test_run():
    """Return all available routes."""
    return 'you can hit your request on "/get", "/set" or "/sub".'


@app.route("/get/<key>", methods=["GET"])
def get_key(key):
    """Route for getting key from kv store"""
    if key in kvstore.keys():
        app.logger.info("%s - Key exists", key)
        return {'value': kvstore.get(key)}
    else:
        app.logger.info("%s - Key does not exist", key)
        return ({'value': 'Error - Key not found'}, 404)


@app.route("/set", methods=["PUT"])
def update_dataset():
    """Route for creating/updating key"""
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
    """Yield events from the event queue for watch functionality."""
    try:
        while True:
            message = msg_queue.get()
            print("yield test %s", message, flush=True)
            yield "{}\n".format(message)
    except GeneratorExit:
        global WATCHERS_COUNT
        WATCHERS_COUNT -= 1
        print("on exit", WATCHERS_COUNT, flush=True)


@app.route("/watch")
def subscribe_to_events():
    """Consumes queue events and stream to clients."""
    app.logger.info("Event consumer initialized.")
    global WATCHERS_COUNT
    WATCHERS_COUNT += 1
    print("on entry", WATCHERS_COUNT, flush=True)
    return Response(stream_with_context(event_stream()),
                    mimetype="text/event-stream")


@click.command(no_args_is_help=True)
@click.option('--server', '-s', default=False, is_flag=True,
              help='Runs KV app in server mode')
@click.option('--serverip', '-i', default="0.0.0.0",
              help='Listen server IP [default: 0.0.0.0]')
@click.option('--serverport', '-p', default=8080,
              type=click.IntRange(80, 49151), help='Listen port [default: 8080]')
@click.option('--get', '-G', default=None, help='Gets key from server')
@click.option('--put', '-P', default=None, type=(str, str),
              help='Stores key to server')
@click.option('--watch', '-W', default=False, is_flag=True,
              help='Watch for key changes')
@click.option('--endpoint', '-e', default="http://localhost:8080",
              help='Server endpoint [default: http://localhost:8080]')
def server_kv(server=False, serverip="0.0.0.0", serverport="8080", get=None,
              put=None, watch=False, endpoint="http://localhost:8080"):
    """Simple Key/Value Store"""
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
    """Triggers /get on server and fetches value for the key."""
    response = requests.get(f"{endpoint}/get/{key}")
    resp = response.json()
    click.echo(resp['value'])


def cli_put(key, endpoint):
    """
    Triggers /set on server and create a key
    or update value for existing key
    """
    key, value = key
    response = requests.put(f"{endpoint}/set",
                            data=json.dumps({key: value}))
    resp = response.json()
    click.echo(resp['value'])


def cli_watch(endpoint):
    """Streams KV changes from server"""
    word = []
    with requests.get(f'{endpoint}/watch', stream=True) as response:
        for data in response.iter_content(decode_unicode=True):
            word.append(data)
            if data == '\n':
                print(''.join(word), flush=True)
                word.clear()


if __name__ == "__main__":
    server_kv()
