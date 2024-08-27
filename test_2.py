from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, LocationMessage, TextSendMessage, FlexSendMessage,
    RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, PostbackAction, MessageAction, URIAction,
    PostbackEvent
)
from linebot.exceptions import InvalidSignatureError

from handle_keys import get_secret_and_token
from flex_message_formmat import locations_flexmessage, store_message
from line_flex import line_store_flex
import sys, googlemaps, requests

app = Flask(__name__)

business_time = '營業時間'
telephone = 'tel:+1234556789'

def get_photo_url(photo_reference, max_width=400):
    """构建照片请求 URL"""
    base_url = 'https://maps.googleapis.com/maps/api/place/photo'
    params = {
        'photoreference': photo_reference,
        'maxwidth': max_width,
        'key': keys['GOOGLE_API_KEY']
    }
    url = f"{base_url}?{requests.compat.urlencode(params)}"
    return url

# 获取环境变量中的 channel_secret 和 channel_access_token
keys = get_secret_and_token()
channel_secret = keys['LINEBOT_SECRET_KEY']
channel_access_token = keys['LINEBOT_ACCESS_TOKEN']
gmaps = googlemaps.Client(key=keys['GOOGLE_API_KEY'])

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
    # 获取 X-Line-Signature 头信息
    signature = request.headers['X-Line-Signature']

    # 获取请求体内容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 处理 webhook 请求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# 处理文字消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "台灣美食":
        flex_message = FlexSendMessage(
            alt_text='This is a Flex Message',
            contents=line_store_flex(photo_url, name, place_rate, detailed_address, business_time, telephone)
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        reply_text = TextSendMessage(text='請輸入"台灣美食"')
        line_bot_api.reply_message(event.reply_token, reply_text)

# 处理位置消息
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    location = event.message
    flex_message = FlexSendMessage(
        alt_text='This is a Flex Message',
        contents=get_store_info(location)
    )
    line_bot_api.reply_message(event.reply_token, flex_message)

def get_store_info(location):
    # 获取用户的地理位置
    origin_location = {'lat': location.latitude, 'lng': location.longitude}

    # 使用 Places API 搜索附近的餐厅
    places_result = gmaps.places_nearby(location=origin_location, radius=100, type='restaurant')

    places_locations = []
    for place in places_result['results']:
        place_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
        places_locations.append(place_location)

    # 使用 Distance Matrix API 计算距离
    distances = gmaps.distance_matrix(origins=[(origin_location['lat'], origin_location['lng'])],
                                      destinations=places_locations,
                                      units='metric')

    places_text = ""
    for i, place in enumerate(places_result['results']):
        name = place.get('name')  # 获取餐厅名称
        place_location = place['geometry']['location']  # 获取餐厅的经纬度
        lat = place_location['lat']
        lng = place_location['lng']
        place_id = place.get('place_id')
        place_photos = place.get('photos', [])
        place_rate = place.get('rating')

        if place_photos:
            photo_reference = place_photos[0].get('photo_reference')
            photo_url = get_photo_url(photo_reference)
        else:
            photo_url = ""

        # 获取距离信息
        distance_info = distances['rows'][0]['elements'][i]
        distance_text = distance_info.get('distance', {}).get('value', '未知')

        # 使用 Geocoding API 获取中文地址
        reverse_geocode_result = gmaps.reverse_geocode((lat, lng), language='zh-TW')

        if reverse_geocode_result:
            detailed_address = reverse_geocode_result[0]['formatted_address']
            places_text = line_store_flex(photo_url, name, place_rate, detailed_address, business_time, telephone)
        else:
            places_text = line_store_flex(photo_url, name, place_rate, '無法獲取地址', business_time, telephone)
        return places_text

def create_rich_menu():
    # 主菜單
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Main Menu",
        chat_bar_text="Tap here",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=PostbackAction(data="action=first_layer_text")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=PostbackAction(data="action=first_layer_url")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=PostbackAction(data="action=first_layer_location")
            ),
        ]
    )

    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    # 為主菜單上傳圖片
    with open("static/rich_menu.png", 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

    line_bot_api.set_default_rich_menu(rich_menu_id)

    print(f"Rich menu created and set as default: {rich_menu_id}")

# 創建子選單
def create_submenu(menu_type):
    if menu_type == "text":
        sub_menu_name = "Text Submenu"
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=MessageAction(text="Text Option 1")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=MessageAction(text="Text Option 2")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=MessageAction(text="Text Option 3")
            ),
        ]
    elif menu_type == "url":
        sub_menu_name = "URL Submenu"
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=URIAction(uri="https://example.com/page1")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=URIAction(uri="https://example.com/page2")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=URIAction(uri="https://example.com/page3")
            ),
        ]
    elif menu_type == "location":
        sub_menu_name = "Location Submenu"
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=PostbackAction(data="action=location_option1")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
                action=PostbackAction(data="action=location_option2")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
                action=PostbackAction(data="action=location_option3")
            ),
        ]

    sub_menu = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name=sub_menu_name,
        chat_bar_text="Tap here",
        areas=areas
    )

    sub_menu_id = line_bot_api.create_rich_menu(rich_menu=sub_menu)

    # 這裡可以選擇為子選單上傳圖片
    with open(f"static/{menu_type}_submenu.png", 'rb') as f:
        line_bot_api.set_rich_menu_image(sub_menu_id, "image/png", f)

    return sub_menu_id

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if data == "action=first_layer_text":
        submenu_id = create_submenu("text")
        line_bot_api.link_rich_menu_to_user(event.source.user_id, submenu_id)
        flex_message = TextSendMessage(text="You selected text. Here's your text submenu.")
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif data == "action=first_layer_url":
        submenu_id = create_submenu("url")
        line_bot_api.link_rich_menu_to_user(event.source.user_id, submenu_id)
        uri_message = TextSendMessage(text="You selected a URL. Here's your URL submenu.")
        line_bot_api.reply_message(event.reply_token, uri_message)
    elif data == "action=first_layer_location":
        submenu_id = create_submenu("location")
        line_bot_api.link_rich_menu_to_user(event.source.user_id, submenu_id)
        location_message = TextSendMessage(text="You selected location. Here's your location submenu.")
        line_bot_api.reply_message(event.reply_token, location_message)
    elif data.startswith("action=location_option"):
        location_message = TextSendMessage(text="You selected a location option.")
        line_bot_api.reply_message(event.reply_token, location_message)

if __name__ == "__main__":
    create_rich_menu()
    app.run(debug=True)
