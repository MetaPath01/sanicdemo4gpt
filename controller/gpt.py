import time
from concurrent.futures import ThreadPoolExecutor
import asyncio
import openai
import json
from sanic import Request, Websocket

from conf import conf
from utils import aes_util
from utils.log import loger
from utils.tool import rsa_decrypt
from sanic import Sanic, response

executor = ThreadPoolExecutor(max_workers=10)


async def http4gpt4(request: Request):
    data = request.json
    device_id = data.get("device_id", "")
    opt = data.get("opt", "")
    product = data.get("product", "")
    content = data.get("content", "")
    loger.info('http4gpt4 收到请求 %s', data)
    resp_msg = {
        'opt': 'gpt',
        'content': "",
    }
    if opt not in {"gpt"}:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    if product not in {"swft", "path"}:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    if not device_id:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    device_id = aes_util.decrypt_ecb_pkcs7(conf.DEVICE_ID_AES_KEY, device_id)
    if not device_id:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    # 请求 gpt4
    loger.info("######################## 准备请求 gpt4 " + request.ip)
    r = await call_gpt4(content)

    # 回复消息
    resp_msg['content'] = r

    return response.json({"code": 0, "msg": "success", "data": resp_msg})


async def http(request: Request):
    data = request.json
    device_id = data.get("device_id", "")
    opt = data.get("opt", "")
    product = data.get("product", "")
    content = data.get("content", "")
    loger.info('http4gpt3 收到请求 %s', data)
    resp_msg = {
        'opt': 'gpt',
        'content': "",
    }
    if opt not in {"gpt"}:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    if product not in {"swft", "path"}:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    if not device_id:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    device_id = aes_util.decrypt_ecb_pkcs7(conf.DEVICE_ID_AES_KEY, device_id)
    if not device_id:
        return response.json({"code": 10003, "msg": "参数错误", "data": ""})

    # 请求 gpt3
    loger.info("######################## 准备请求 gpt3 " + request.ip)
    r = await call_gpt3(content)

    # 回复消息
    resp_msg['content'] = r

    return response.json({"code": 0, "msg": "success", "data": resp_msg})


async def ws(request: Request, ws_handler: Websocket, users: dict):
    mp = {
        "ip": "",
        "device_id": "",
        "type": "",
        "answer": "",
        "question": "",
    }

    while True:

        device = request.headers['device']
        if not device:
            loger.info('device_id empty' + request.ip)
            return

        device = rsa_decrypt(device, conf.RSA_PRIVATE)
        if not device:
            loger.info('device_id 解密失败 ' + device + " " + request.ip)
            return

        message = await ws_handler.recv()

        if message == 'ping':
            loger.info('ping:', request.ip)
            await ws_handler.send("pong")
            continue

        params = json.loads(message)
        if params['opt'] != 'chat_gpt':
            await ws_handler.send("参数错误")
            loger.info("opt != chat_gpt")
            return

        if not params['content']:
            await ws_handler.send("参数错误")
            loger.info("content empty")
            return

        resp_msg = {
            'opt': 'chat_gpt',
            'content': "",
        }

        # 检查用户字典中是否已存在 device 以及时间差是否小于XX
        current_time = time.time()
        if device in users and current_time - users[device] < 3:
            loger.info("请求太过频繁 ip: " + request.ip)

            resp_msg['content'] = "请静待回复,稍作休息"
            await ws_handler.send(json.dumps(resp_msg, ensure_ascii=False))
            return

        mp['ip'] = request.ip
        mp['type'] = "question"
        mp['device_id'] = device
        mp['question'] = params['content'][-1]
        loger.info(mp)

        # 请求 gpt3
        r = await call_gpt3(params['content'])

        users[device] = time.time()

        mp['type'] = "answer"
        mp['answer'] = r
        loger.info(mp)

        # 回复消息
        resp_msg['content'] = r
        await ws_handler.send(json.dumps(resp_msg))


async def call_gpt3(msg):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, gpt, msg, "gpt-3.5-turbo", conf.OPEN_API_KEY)
    return result


async def call_gpt4(msg):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, gpt, msg, "gpt-4", conf.OPEN_API_KEY_GPT4)
    return result


def gpt(msg: list, model: str, open_api_key: str):
    openai.api_key = open_api_key
    msg.insert(0, {
        "role": "system",
        "content": "You are a helpful assistant."
    })

    try:
        loger.debug(
            '######################## 开始请求 gpt, model: ' + model + " msg: " + json.dumps(msg, ensure_ascii=False))
        response = openai.ChatCompletion.create(
            model=model,
            messages=msg,
            temperature=0.9,  # 值在[0,1]之间，越大表示回复越具有不确定性
            top_p=1,
            frequency_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            presence_penalty=0.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
        )
        loger.info("######################## 收到响应 gpt: %s", json.dumps(response, ensure_ascii=False))

        result = ''
        for choice in response.choices:
            result += choice.message.content

        return result

    except openai.error.RateLimitError as e:
        loger.error("openai.error.RateLimitError: %s", e)
        return "提问太快啦，请休息一下再问我吧"
    except openai.error.APIConnectionError as e:
        loger.error("openai.error.APIConnectionError: %s", e)
        return "我连接不到网络，请稍后重试"
    except openai.error.Timeout as e:
        loger.error("openai.error.Timeout: %s", e)
        return "我没有收到消息，请稍后重试"
    except Exception as e:
        loger.error("Exception: %s", e)
        return "系统繁忙"

    return ""
