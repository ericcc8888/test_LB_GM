from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, LocationMessage, TextSendMessage ,FlexSendMessage
from linebot.models.flex_message import BubbleContainer, TextComponent, BoxComponent
from linebot.exceptions import InvalidSignatureError

from API_KEYS import get_api_keys
from flex_message_formmat import locations_flexmessage,store_message
from line_flex import line_store_flex , flex_formmat
import sys,googlemaps,requests

app = Flask(__name__)

business_time = '營業時間'
telephone = 'tel:+1234556789'

def get_photo_url(photo_reference, max_width=400):
    """构建照片请求 URL"""
    base_url = 'https://maps.googleapis.com/maps/api/place/photo'
    params = {
        'photoreference': photo_reference,
        'maxwidth': max_width,
        'key': keys['GOOGLEMAPS_API_KEY']
    }
    url = f"{base_url}?{requests.compat.urlencode(params)}"
    return url

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
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

#==============================================================

#處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # reply_text = TextSendMessage(text=event.message.text)

    # # 使用 reply_message 方法回應使用者
    # line_bot_api.reply_message(event.reply_token, reply_text)

    # if event.message.text == "台灣美食":
    #     flex_message = FlexSendMessage(
    #     alt_text='This is a Flex Message',
    #     contents= line_store_flex(image_url, story_name, star_num, store_address, business_time, telephone)
    #     )
    #     line_bot_api.reply_message(event.reply_token, flex_message)

    # else:
    reply_text = TextSendMessage(text='請輸入"台灣美食"')

        # 使用 reply_message 方法回應使用者
    line_bot_api.reply_message(event.reply_token, reply_text)

#==============================================================

#處理位置訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    location = event.message

    flex_message = FlexSendMessage(
    alt_text='This is a Flex Message',
    contents= get_store_info(location)
    )

    print(f"====================={flex_message}==================")
    line_bot_api.reply_message(event.reply_token, flex_message)
# ==============================================================

def get_store_info(location):
    # Geocoding an address
    origin_location = {'lat':location.latitude, 'lng':location.longitude}
    # 使用 Places API 搜尋附近500公尺內的餐廳
    places_result = gmaps.places_nearby(location=origin_location, radius=100, keyword='滷肉飯')

    places_locations = []
    for place in places_result['results']:
        place_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
        places_locations.append(place_location)
    # 使用 Distance Matrix API 計算距離
    distances = gmaps.distance_matrix(origins=[(origin_location['lat'], origin_location['lng'])],
                                    destinations=places_locations,
                                    units='metric')

    places_text = []
    # 列印每個餐廳的名稱、中文地址和距離
    for i, place in enumerate(places_result['results']):
        name = place.get('name')  # 獲取餐廳名稱
        place_location = place['geometry']['location']  # 獲取餐廳的經緯度
        lat = place_location['lat']
        lng = place_location['lng']
        place_id = place.get('place_id')
        place_phtot = place.get('photos',[])
        place_rate = place.get('rating')

        if place_phtot:
            photo_reference = place_phtot[0].get('photo_reference')
            photo_url = get_photo_url(photo_reference)
        else:
            photo_reference = ""
            photo_url = "no photos"
        
        # 獲取距離資訊
        distance_info = distances['rows'][0]['elements'][i]
        distance_text = distance_info.get('distance', {}).get('value', '未知')

        # 使用 Geocoding API 獲取中文地址
        reverse_geocode_result = gmaps.reverse_geocode((lat, lng), language='zh-TW')
        
        if reverse_geocode_result:
            detailed_address = reverse_geocode_result[0]['formatted_address']
            places_text.append(line_store_flex(photo_url, name, place_rate, detailed_address, business_time, telephone))
        else:
            detailed_address = "無地址"
            places_text.append(line_store_flex(photo_url, name, place_rate, detailed_address, business_time, telephone))
    flex_message = flex_formmat(places_text[0])
    return flex_message


if __name__ == "__main__":
    app.run(debug=True)