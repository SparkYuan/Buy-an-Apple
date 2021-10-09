import time
import hmac
import hashlib
import base64
import requests, json


def push(text):
    timestamp = str(round(time.time() * 1000))
    app_secret = '${YOUR_AS}'
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    print(sign)
    headers = {'Content-Type': 'application/json'}
    ding_web_hook = '${DING_WEB_HOOK}' + '&timestamp=' + timestamp + "&sign=" + sign
    wechat_hook = "${Wechat_WEB_HOOK}"

    data = {
        "msgtype": "text",
        "text": {"content": text},
        "at": {
            "atMobiles": [
                "${PhoneNumber}"
            ],
        }
    }
    requests.post(ding_web_hook, data=json.dumps(data), headers=headers)
    res = requests.post(wechat_hook, data=json.dumps(data), headers=headers)
    print(res.text)


if __name__ == '__main__':
    result = push("Test")
