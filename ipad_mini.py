from json import JSONDecodeError

import requests

from push import push


def queryQuote(a, b):
    cookie = "${YOUR_COOKIE}"

    headers = {
        'authority': 'www.apple.com.cn',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.apple.com.cn/shop/buy-iphone/iphone-13-pro/MLH83CH/A',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie,
    }
    params = {
        'pl': 'true',
        'mt': 'compact',
        'parts.0': 'MLWR3CH/A',
        'location': '\u4E0A\u6D77 \u4E0A\u6D77 \u6D66\u4E1C\u65B0\u533A'
    }

    models = [{
        "key": "MLWR3CH/A",
        "describe": "星光色"
    }, {
        "key": "MK7T3CH/A",
        "describe": "深空灰色"
    },
        {
            "key": "MLWR3CH/A",
            "describe": "粉色"
        }]
    for model in models:
        params['parts.0'] = model["key"]
        response = requests.get('https://www.apple.com.cn/shop/fulfillment-messages', headers=headers, params=params)

        if response.status_code != 200:
            print(f"Query failed: {response.text}")
            push(f"Query failed: {response.text}")

        try:
            response.json()
        except JSONDecodeError as e:
            print(f"JSONDecodeError!!! {e}")
            push(f"JSONDecodeError!!! {e}")

        json_data = response.json()
        stores = json_data["body"]["content"]["pickupMessage"]["stores"]
        print("\n\n\n" + "All stores quote:" + model["describe"])
        for idx, item in enumerate(stores):
            if idx < 7:
                quote = item["partsAvailability"][model["key"]]["pickupSearchQuote"]
                msg = item["storeName"] + ": " + quote
                print(msg)
                if quote != "暂无供应":
                    msg = "GOT ONE!!!\n" + item["storeName"] + ": " + model["describe"] + " " + quote
                    push(msg)


if __name__ == '__main__':
    result = queryQuote("a", "b")
