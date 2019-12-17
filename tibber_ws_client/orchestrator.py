import argparse
import live_monitor
import ws_client

class Config():
    def __init__(self):
        self.api_url = "wss://api.tibber.com/v1-beta/gql/subscriptions"

    def init(self, token, home_id):
        self.token = token 
        self.home_id = home_id

config = Config()


def main():
    parser = argparse.ArgumentParser(description='Start monitoring.')
    parser.add_argument('--token', type=str, help='Personal token')
    parser.add_argument('--home-id', type=str, help='Home id')
    parser.add_argument('--config', type=str, help="Config file with necessary tokens")

    args = parser.parse_args()


    config.init(args.token, args.home_id)
    live_monitor.initialize_websocket()