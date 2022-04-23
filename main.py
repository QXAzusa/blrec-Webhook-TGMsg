from flask import Flask, request
import json
import httpx
import urllib.parse
app = Flask(__name__)


@app.route("/", methods=['POST'])
async def recvMsg():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if json_data["type"] == "LiveBeganEvent":
        username = json_data["data"]["user_info"]["name"]
        roomid = json_data["data"]["room_info"]["room_id"]
        roomurl = 'https://live.bilibili.com' + roomid
        roomurl = urllib.parse.quote(roomurl)
        tittle = json_data["data"]["room_info"]["tittle"]
        print("I:" + username + "开播了")
        msg = username + '开播了%0A标题:' + tittle + '%0A' + roomurl
        url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + UID + '&text=' + msg
        await httpx.AsyncClient().post(url)
    elif json_data["type"] == "LiveEndedEvent":
        username = json_data["data"]["user_info"]["name"]
        print("I:" + username + "下播了")
        msg = username + '下播了'
        url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + UID + '&text=' + msg
        await httpx.AsyncClient().post(url)
    elif json_data["type"] == "SpaceNoEnoughEvent":
        print("W:磁盘空间不足")
        msg = urllib.parse.quote('警告：磁盘空间不足，请及时处理！')
        url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + UID + '&text=' + msg
        await httpx.AsyncClient().post(url)
    elif json_data["type"] == "Error":
        print("W:程序发生错误")
        msg = urllib.parse.quote('警告：程序出现异常，请及时检查！')
        url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + UID + '&text=' + msg
        await httpx.AsyncClient().post(url)
    return "200 OK"


if __name__ == '__main__':
    TOKEN = ''
    UID = ''
    app.run(host="0.0.0.0", port=5000)
