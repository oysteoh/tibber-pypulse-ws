import sys
import argparse
import live_monitor
import ws_client


class Config:
    def __init__(self, token, home_id):
        self.api_url = "wss://api.tibber.com/v1-beta/gql/subscriptions"
        self.token = token
        self.home_id = home_id


def main():
    parser = argparse.ArgumentParser(description="Start monitoring.")
    parser.add_argument("--token", type=str, help="Personal token")
    parser.add_argument("--home-id", type=str, help="Home id")
    parser.add_argument("--config", type=str, help="Config file with necessary tokens")

    args = parser.parse_args()

    config = Config(args.token, args.home_id)

    ws_client.headers = {"Authorization": "Bearer {}".format(args.token)}

    print("Hei!")
    ws_client.name()
    #ws_client.home_price_consumption()
    live_monitor.config = config
    live_monitor.start()


if __name__ == "__main__":
    main()
