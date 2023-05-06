import websocket
import _thread
import time
import rel
import json

# WebSocket服务器的URL

msg = json.dumps({
    "opt": "chat_gpt",
    "content": ["你好,你是谁?", "你叫什么名字"]
}, ensure_ascii=False)

# WebSocket服务器的URL
url = "ws://localhost:15010/ws"


def on_message(ws, message):
    chinese_str = message.encode('utf-8').decode('unicode_escape')

    print('收到消息: ', chinese_str)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    print('发送消息: ', msg)
    ws.send(msg)


if __name__ == "__main__":
    # websocket.enableTrace(True)

    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    # wss.run_forever(dispatcher=rel, reconnect=5)
    ws.run_forever(ping_interval=2)
    # rel.signal(2, rel.abort)  # Keyboard Interrupt
    # rel.dispatch()
