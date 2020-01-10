# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import pprint
import ssl
import sys
import time

import pandas as pd
import websocket
from pandas.io.json import json_normalize

import _thread

config = {}

result = []


def start():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        config["api_url"],
        header=config["ws_header"],
        on_message=console_handler,
        on_error=on_error,
        on_close=on_close,
    )
    # websocket_logger = logging.getLogger('websocket')
    # websocket_logger.setLevel(logging.WARN)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})


def console_handler(ws, message):
    data = json.loads(message)

    if "payload" in data:
        measurement = data["payload"]["data"]["liveMeasurement"]
        keys = list(measurement.keys())
        if len(result) == 0:
            result.append(keys)
        values = list(measurement.values())
        result.append(values)
        df = pd.DataFrame(result)
        print(df)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        init_data = {
            "type": "init",
            "payload": "token={token}".format(token=config["token"]),
        }
        init = json.dumps(init_data)
        ws.send(init)

        query = """
        subscription {{
            liveMeasurement(homeId:"{home_id}"){{
                timestamp
                power
                lastMeterConsumption
                accumulatedConsumption
                accumulatedCost
                currency
                averagePower
                maxPower
                minPower
                voltagePhase1
                voltagePhase2
                voltagePhase3
                currentPhase1
                currentPhase2
                currentPhase3
            }}
        }}
        """.format(
            home_id=config["home_id"]
        )

        subscribe_data = {"query": query, "type": "subscription_start", "id": 0}
        subscribe = json.dumps(subscribe_data)
        ws.send(subscribe)

    _thread.start_new_thread(run, ())


# Timestamp when usage occured
# Consumption at the moment (Watt)
# Last meter active import register state (kWh)
# kWh consumed since midnight
# net kWh produced since midnight
# Accumulated cost since midnight; requires active Tibber power deal
# Accumulated reward since midnight; requires active Tibber power deal
# Currency of displayed cost; requires active Tibber power deal
# Min consumption since midnight (Watt)
# Average consumption since midnight (Watt)
# Peak consumption since midnight (Watt)
# Net production at the moment (Watt)
# Min net production since midnight (Watt)
# Max net production since midnight (Watt)
# Last meter active export register state (kWh)
# Power factor (active power / apparent power)
# Voltage on phase 1; on Kaifa and Aidon meters the value is not part of every HAN data frame therefore the value is null at timestamps with second value other than 0, 10, 20, 30, 40, 50. There can be other deviations based on concrete meter firmware.
# Current on phase 1; on Kaifa and Aidon meters the value is not part of every HAN data frame therefore the value is null at timestamps with second value other than 0, 10, 20, 30, 40, 50. There can be other deviations based on concrete meter firmware.

#  timestamp
#  power
#  lastMeterConsumption
#  accumulated
#  accumulatedProduction
#  accumulated_cost
#  accumulatedReward
#  currency
#  min_power
#  avg_power
#  max_power
#  powerProduction
#  minPowerProduction
#  maxPowerProduction
#  lastMeterProduction
#  powerFactor
#  voltagePhase1
#  voltagePhase2
#  voltagePhase3
#  currentPhase1
#  currentPhase2
#  currentPhase3
