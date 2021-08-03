# Simple KV Store

Python(Flask) based minimal Key/Value store

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.6 or greater
```

### Installing

Install the dependecies

```
python3 -m pip install -r requirements.txt
```

## Running on Local

```
$ ./kv_store.py
Usage: kv_store.py [OPTIONS]

  Simple Key/Value Store

Options:
  -s, --server                    Runs KV app in server mode
  -i, --serverip TEXT             Listen server IP [default: 0.0.0.0]
  -p, --serverport INTEGER RANGE  Listen port [default: 80]  [80<=x<=49151]
  -G, --get TEXT                  Gets key from server
  -P, --put <TEXT TEXT>...        Stores key to server
  -W, --watch                     Watch for key changes
  -e, --endpoint TEXT             Server endpoint [default: http://localhost]
  --help                          Show this message and exit.
```

### Starting the Server


```
$ ./kv_store.py -s
```

### Using client
Create or update a key:value pair 
```
$ ./kv_store.py -P a 5
published
```
Get value for a key 
```
$ ./kv_store.py -G a
5
```

Watch for updates 
```
$ ./kv_store.py -W
Created key  - b

Updated key  - a
```

## AWS Deployment

* [CDK Deployment docs](cdk-kv) 

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

