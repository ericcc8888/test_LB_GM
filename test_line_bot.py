from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, LocationMessage, TextSendMessage, FlexSendMessage, PostbackEvent
from linebot.exceptions import InvalidSignatureError
from API_KEYS import get_api_keys
from line_flex import line_store_flex, flex_formmat
import sys, googlemaps, requests
import line_flex

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

#==============================================================
line_bot_scraper = line_flex.line_bot_scraper_ifoodie
user_states = {}
user_functions = {} # 用戶選擇的功能
user_food_preferences = {} # 用戶想吃的食物

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text.strip()
    # 讓使用者選擇使用的功能
    if user_message == "美食推薦":
        text = "請主人輸入想查找的地區"
        text_message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, text_message)
        user_functions[user_id] = "美食推薦"  # 設定用戶選擇的功能為「美食推薦」

    elif user_message == "附近美食":
        text = "請輸入想要查詢的食物類型"
        text_message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, text_message)
        user_functions[user_id] = "附近美食"  # 設定用戶選擇的功能為「附近美食」
    # 根據使用者選擇的功能來運行
    elif user_id in user_functions:
        if user_functions[user_id] == "附近美食":
            user_food_preferences[user_id] = user_message  # 保存用戶的食物偏好
            text = "請傳送主人的定位資訊"
            text_message = TextSendMessage(text=text)
            line_bot_api.reply_message(event.reply_token, text_message)

        elif user_functions[user_id] == "美食推薦":
            area = user_message
            ifoodie = line_bot_scraper(area)
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

    else:
        text = "請主人輸入想使用的功能"
        text_message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, text_message)

# 處理位置訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    user_id = event.source.user_id
    location = event.message
    user_function = user_functions.get(user_id, None)
    food_preference = user_food_preferences.get(user_id, "美食")  # 默認為「美食」

    if user_function == "附近美食":
        flex_message = FlexSendMessage(
            alt_text='This is a Flex Message',
            contents=get_store_info(location, food_preference)  # 使用用戶的食物偏好
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        text_message = TextSendMessage(text="請先選擇「附近美食」以傳送您的定位資訊。")
        line_bot_api.reply_message(event.reply_token, text_message)

#==============================================================
def get_store_info(location, need_food, max_results=10):
    origin_location = {'lat': location.latitude, 'lng': location.longitude}
    places_result = gmaps.places_nearby(location=origin_location, radius=500, keyword=need_food, language="zh-TW")

    places_text = []
    flex_message_datas = []

    for place in places_result['results'][:max_results]:
        name = place.get('name')
        place_location = place['geometry']['location']
        lat = place_location['lat']
        lng = place_location['lng']
        address = place.get('vicinity')
        place_phtot = place.get('photos', [])
        place_rate = place.get('rating')
        opening_hours = place.get('opening_hours', {})
        business_time = opening_hours.get('open_now', '無營業時間')
        place_id = place.get('place_id')
        store_result = gmaps.place(place_id)
        googlemap_url = store_result["result"]['url']
        telephone = 'tel:' + store_result["result"].get("formatted_phone_number", "0000").replace(" ", "")

        if business_time:
            business_status = '營業中'
            business_color = "#00A600"
        else:
            business_status = '已打烊'
            business_color = "#CE0000"

        if place_phtot:
            photo_reference = place_phtot[0].get('photo_reference')
            photo_url = get_photo_url(photo_reference)
        else:
            photo_reference = ""
            photo_url = "https://www.post.gov.tw/post/internet/images/NoResult.jpg"

        reverse_geocode_result = gmaps.reverse_geocode((lat, lng), language='zh-TW')
        detailed_address = reverse_geocode_result[0]['address_components'][4]['long_name'] + reverse_geocode_result[0]['address_components'][3]['long_name'] + address
        places_text.append(line_store_flex(photo_url, name, place_rate, detailed_address, business_status, telephone, googlemap_url, business_color, flex_message_datas))

    flex_message = flex_formmat(places_text[0])
    return flex_message

def get_photo_url(photo_reference, max_width=400):
    base_url = 'https://maps.googleapis.com/maps/api/place/photo'
    params = {
        'photoreference': photo_reference,
        'maxwidth': max_width,
        'key': keys['GOOGLEMAPS_API_KEY']
    }
    url = f"{base_url}?{requests.compat.urlencode(params)}"
    return url

if __name__ == "__main__":
    app.run(debug=True)