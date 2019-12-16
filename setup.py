#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="tibber-ws-client",
    version="0.1",
    packages=['tibber_ws_client'],
    install_requires=["websocket-client", "argparse"],
    author="Øystein Olai Heggen",
    author_email="oystein.heggen@gmail.com",
    description="Python websocket client for Tibber providing real time power data",
    url="https://github.com/websocket-client/websocket-client",
    entry_points = {
        'console_scripts': ['tibber-ws-client=tibber_ws_client.live_monitor:main'],
    }
)