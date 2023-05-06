import sys

from sanic.response import json, html
from sanic import Request, Websocket
from sanic import Sanic
from sanic.response import json
from sanic import Blueprint

from conf import conf
from controller import gpt
from utils.log import loger

app = Sanic(__name__)

app.config.global_user = dict()

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_PING_INTERVAL = 30
app.config.WEBSOCKET_PING_TIMEOUT = 30

app.config.REQUEST_TIMEOUT = 180
app.config.RESPONSE_TIMEOUT = 180
app.config.KEEP_ALIVE_TIMEOUT = 180
app.config.KEEP_ALIVE = True


@app.websocket("/ws")
async def ws(request: Request, ws: Websocket):
    await gpt.ws(request, ws, app.config.global_user)


# mpcbot route group
mpcbot = Blueprint("mpcbot", url_prefix="/mpcbot")
mpcbot.add_route(gpt.http, "/sendchat", methods=["POST"])
mpcbot.add_route(gpt.http4gpt4, "/sendchat_gpt4", methods=["POST"])

app.blueprint(mpcbot)


@app.route("/")
async def index(request):
    return html("<h1>Welcome to the Sanic server!</h1>")


@app.route("/api")
async def api(request):
    return json({"message": "Hello, World!"})


if __name__ == "__main__":
    if not conf.OPEN_API_KEY or not conf.OPEN_API_KEY_GPT4 or not conf.DEVICE_ID_AES_KEY or not conf.RSA_PRIVATE:
        loger.error("Missing config")
        sys.exit(0)
    app.run(host="0.0.0.0", port=15010, fast=True)
