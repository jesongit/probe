import requests
from .utils import now
from .config import CONFIG, update

corpid = CONFIG["corpid"]
base_url = CONFIG["proxy"]
corpsecret = CONFIG["corpsecret"]
send_url = f"{base_url}/cgi-bin/message/send?access_token="
post_body = {"msgtype": "text", "agentid": 1000005, "touser": "@all"}
token_url = f"{base_url}/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"


def get_token():
    if now() >= CONFIG["expired_time"]:
        return new_token()
    return CONFIG["token"]


def new_token():
    req = requests.get(token_url)
    json = req.json()
    token, expired_time = json["access_token"], now() + json["expires_in"] - 10
    print(req.status_code, expired_time, token)
    update(token=json["access_token"], expired_time=expired_time)
    return token


def notify(title, content, retry=True):
    try:
        print(title, content)
        content = f"{title}\n{content}"
        url = send_url + get_token()
        post_body["text"] = {"content": content}
        req = requests.post(url, json=post_body)
    except Exception as e:  # 捕获所有异常
        print("Exception:", e)
        if retry:
            new_token()
            notify(content, False)
