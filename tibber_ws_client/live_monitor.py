# -*- coding: utf-8 -*-
import sys
import websocket
import ssl
import json
import _thread
import time
import argparse
import logging

import logging
import sys

header = {
    'Sec-WebSocket-Protocol': 'graphql-subscriptions'
}

def console_handler(ws, message):
    data = json.loads(message)
    if 'payload' in data:
        measurement = data['payload']['data']['liveMeasurement']
        timestamp = measurement['timestamp']
        power = measurement['power']
        min_power = measurement['minPower']
        max_power = measurement['maxPower']
        avg_power = measurement['averagePower']
        accumulated = measurement['accumulatedConsumption']
        accumulated_cost = measurement['accumulatedCost']
        currency = measurement['currency']

        output = {
            "timestamp": timestamp,
            "power": {
                "power": power,
                "min power": min_power,
                "max power": max_power,
                "avg power": avg_power,
            },
            "consumption": accumulated,
            "cost": accumulated_cost,
            "currency": currency,
        }

        print(output)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        init_data = {
            'type':'init',
            'payload':'token={token}'.format(token=config.token)
        }
        init = json.dumps(init_data)
        ws.send(init)

        query = """
        subscription {{
            liveMeasurement(homeId:"{home_id}"){{
                timestamp
                power
                accumulatedConsumption
                accumulatedCost
                currency
                minPower
                averagePower
                maxPower
            }}
        }}
        """.format(home_id=config.home_id)

        subscribe_data = {
            'query': query,
            'type':'subscription_start',
            'id': 0
        }
        subscribe = json.dumps(subscribe_data)
        ws.send(subscribe)

    _thread.start_new_thread(run, ())


def initialize_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(config.api_url,
                              header = header,
                              on_message = console_handler,
                              on_error = on_error,
                              on_close = on_close)
    websocket_logger = logging.getLogger('websocket')
    websocket_logger.setLevel(logging.WARN)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})
