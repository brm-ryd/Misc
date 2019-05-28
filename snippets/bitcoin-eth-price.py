from websocket import WebSocketApp
from json import dumps, loads

URL = "wss://ws-feed.gdax.com"

def on_message(_, message):
    json_message = loads(message)
    print(json_message)

def on_open(socket):
    products = ["BTC-IDR","ETH-IDR"]
    channels = [
        {
            "name" : "ticker",
            "product_ids" : products,
        },
    ]
    params = {
        "type" : "subscribe",
        "channels" : channels,
    }
    socket.send(dumps(params))

def main():
    ws = WebSocketApp(URL, on_open=on_open, on_message=on_message)
    ws.run_forever()

if __name__ == "__main__":
    main()
