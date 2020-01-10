import argparse
import json
import os
import sys

import live_monitor


def valid_file(arg):
    if os.path.isfile(arg):
        return arg
    raise argparse.ArgumentTypeError("{} is not a existing file!".format(arg))


def main(args):
    parser = argparse.ArgumentParser(description="Start monitoring.")
    parser.add_argument(
        "config", type=valid_file, help="Config file with necessary tokens"
    )
    parser.add_argument(
        "--live", action="store_true", help="Run live power data monitoring"
    )

    args = parser.parse_args()

    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    config["header"] = {"Authorization": "Bearer {}".format(config["token"])}
    config["ws_header"] = {"Sec-WebSocket-Protocol": "graphql-subscriptions"}

    if args.live:
        live_monitor.config = config
        live_monitor.start()


if __name__ == "__main__":
    main(sys.argv[1:])
