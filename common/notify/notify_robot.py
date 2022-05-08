import requests
import os

# "2aac663c6d2f"
def NotifyRobot(title, name, content):
    notify_token = os.getenv('notify_token') 
    resp = requests.post("https://www.autodl.com/api/v1/wechat/message/push",
                        json={
                            "token": notify_token,
                            "title": title,
                            "name": name,
                            "content": content
                        })
    print(resp.content.decode())

