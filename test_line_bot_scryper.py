from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.exceptions import InvalidSignatureError
from bs4 import BeautifulSoup
from API_KEYS import get_api_keys
from line_flex import generate_star_icons
import sys, googlemaps, requests

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
keys = get_api_keys()
channel_secret = keys['LINE_BOT_SECRET']
channel_access_token = keys['LINE_BOT_ACCESS_TOKEN']
gmaps = googlemaps.Client(key=keys['GOOGLEMAPS_API_KEY'])

if channel_secret is None:
    print('Specify LINE_BOT_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_BOT_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)

# 愛食記爬蟲類別
class IFoodie:
    def __init__(self, area):
        self.area = area

    def scrape(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area + "/list?sortby=popular&opening=true", headers=headers)

        if response.status_code != 200:
            print("Failed to retrieve the webpage. Status Code:", response.status_code)
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all('div', {'class': 'restaurant-item'}, limit=4)

        if not cards:
            print("沒有抓取到資料")
            return []

        flex_message_datas = []

        for card in cards:
            title = card.find("a", {"class": "title-text"}).getText()
            stars = card.find("div", {"class": "jsx-2373119553 text"}).getText()
            address = card.find("div", {"class": "address-row"}).getText()
            url = card.find("a", {"class": "title-text"}).get("href")
            photo = card.find("img").get("src")

            # 確保 URL 以 https:// 開頭
            if not url.startswith("http"):
                url = "https://ifoodie.tw" + url
            if not photo.startswith("http"):
                photo = "https:" + photo

            try:
                stars = float(stars)
            except ValueError:
                stars = 0

            flex_message_datas.append({
                "type": "bubble",
                "size": "deca",
                "hero": {
                    "type": "image",
                    "url": photo,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "320:213",
                    "action": {
                        "type": "uri",
                        "uri": url
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "size": "sm",
                            "maxLines": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "offsetTop": "sm",
                            "contents": generate_star_icons(stars)
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "offsetTop": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "地址",
                                            "wrap": True,
                                            "color": "#8c8c8c",
                                            "size": "xs",
                                            "flex": 2
                                        },
                                        {
                                            "type": "text",
                                            "text": address,
                                            "size": "xs"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            })

        return flex_message_datas

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    area = event.message.text.strip()
    ifoodie = IFoodie(area)
    flex_message_datas = ifoodie.scrape()

    if flex_message_datas:
        flex_message = FlexSendMessage(
            alt_text="美食推薦",
            contents={
                "type": "carousel",
                "contents": flex_message_datas
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有找到相關餐廳資訊。"))

if __name__ == "__main__":
    app.run(debug=True)
