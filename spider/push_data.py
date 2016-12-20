import hashlib
import logging
import time

import requests

from spider.config import default_key, default_u


def md5(data):
    m = hashlib.md5(data)
    return m.hexdigest()


def get_k(u, t, key):
    str_total = (u + str(t) + key).encode("gb2312")
    return md5(str_total)


def push_request(url, data):
    response = requests.post(url, data=data)
    # response = requests.get(url, params=payload)
    logging.info(response)
    print(response.content)
    return response


def push_data(url, data):
    u = default_u
    t = int(time.time())
    key = default_key
    k = get_k(u, t, key)

    payload = data

    payload.update({
        "t": t,
        "u": u,
        "k": k,
    })
    logging.info(payload.get("companyName"))
    logging.debug(payload)
    return push_request(url, payload)


# if __name__ == "__main__":
#     # from init_logging import init_logging
#
#     # init_logging()
#     url = "https://data.api.zhironghao.com/update/job"
#     # logging.debug(time.time())
#     response = push_data(url, {u"companyName": u"123"})
#     logging.info(response)
#     logging.info(response.content)
