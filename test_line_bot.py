from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, LocationMessage, TextSendMessage, FlexSendMessage, PostbackEvent
from linebot.exceptions import InvalidSignatureError
from API_KEYS import get_api_keys
from line_flex import line_store_flex, flex_formmat, big_food_class, rice_class, noodle_class, dessert_class, hot_pot_class, line_bot_scraper_ifoodie, ifoodie_class, no_search
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
user_states = 0
food_preference = ''
# user_functions = {} # 用戶選擇的功能
# user_food_preferences = {} # 用戶想吃的食物

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_states
    global food_preference
    user_message = event.message.text.strip()
    # 讓使用者選擇使用的功能
    if user_message == "美食推薦":
        flex_message = FlexSendMessage(
            alt_text='This is a Flex Message',
            contents=ifoodie_class()
            )
        line_bot_api.reply_message(event.reply_token, flex_message)
        user_states = 1  # 設定用戶選擇的功能為「美食推薦」

    elif user_message == "附近美食":
        flex_message = FlexSendMessage(
            alt_text='This is a Flex Message',
            contents=big_food_class()
            )
        line_bot_api.reply_message(event.reply_token, flex_message)
        text = "請點擊想要查詢的食物類型"
        text_message = TextSendMessage(text=text)
        line_bot_api.push_message(event.source.user_id, text_message)
        user_states = 2  # 設定用戶選擇的功能為「附近美食」

    elif user_states == 3:
        food_preference =  event.message.text  # 保存用戶的偏好
        text = "請傳送定位資訊"
        text_message = TextSendMessage(text)
        line_bot_api.push_message(event.source.user_id, text_message)

    #根據使用者選擇的功能來運行
    elif user_states == 1:       
        area = user_message
        ifoodie = line_bot_scraper_ifoodie(area)
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
            user_states = 0            
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="沒有找到相關餐廳資訊。"))
            user_states = 0

    else:
        text = "請點擊圖卡上的食物種類"
        text_message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, text_message)

    # print(user_functions[user_id])


@handler.add(PostbackEvent)
#傳送食物細分的圖卡
def handle_postback(event):
    global user_states
    data = event.postback.data
    if data == "rice_class":
        flex_message = FlexSendMessage(alt_text="米飯類選擇", contents=rice_class())
        line_bot_api.reply_message(event.reply_token, flex_message)
        text = "請點選圖卡告訴我你想吃甚麼飯，上述沒有想吃的也可以打字輸入呦"
        text_message = TextSendMessage(text=text)
        line_bot_api.push_message(event.source.user_id, text_message)
        user_states = 3
        
    elif data == "noodle_class":
        flex_message = FlexSendMessage(alt_text="麵類選擇", contents=noodle_class())
        line_bot_api.reply_message(event.reply_token, flex_message)
        text = "請點選圖卡告訴我你想吃甚麼麵，上述沒有想吃的也可以打字輸入呦"
        text_message = TextSendMessage(text=text)
        line_bot_api.push_message(event.source.user_id, text_message)
        user_states = 3
    elif data == "hot_pot_class":
        flex_message = FlexSendMessage(alt_text="火鍋選擇", contents=hot_pot_class())
        line_bot_api.reply_message(event.reply_token, flex_message)
        text = "請點選圖卡告訴我你想吃甚麼火鍋，上述沒有想吃的也可以打字輸入呦"
        text_message = TextSendMessage(text=text)
        line_bot_api.push_message(event.source.user_id, text_message)
        user_states = 3

    elif data == "dessert_class":
        flex_message = FlexSendMessage(alt_text="點心選擇", contents=dessert_class())
        line_bot_api.reply_message(event.reply_token, flex_message)
        text = "請點選圖卡告訴我你想吃甚麼風格的點心，上述沒有想吃的也可以打字輸入呦"
        text_message = TextSendMessage(text=text)
        line_bot_api.push_message(event.source.user_id, text_message)
        user_states = 3

# 處理位置訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    global user_states
    global food_preference
    location = event.message

    if user_states == 3:
        flex_message = FlexSendMessage(
            alt_text='This is a Flex Message',
            contents=get_store_info(location, food_preference)  # 使用用戶的食物偏好
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
        user_states = 0
    else:
        text_message = TextSendMessage(text="請先選擇「附近美食」以傳送您的定位資訊。")
        line_bot_api.reply_message(event.reply_token, text_message)

#==============================================================
def get_store_info(location, food_preference):
    global user_states
    try:
        max_results=10
        origin_location = {'lat': location.latitude, 'lng': location.longitude}
        places_result = gmaps.places_nearby(location=origin_location, radius=500, keyword=food_preference, language="zh-TW")

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
        user_states = 0
        return flex_message
    except:
        flex_message = no_search()
        user_states = 0
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

def delete_all_rich_menus():
    try:
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print(f"正在刪除 Rich Menu: {rich_menu.rich_menu_id}")
            delete_rich_menu(rich_menu.rich_menu_id)
    except Exception as e:
        print(f"獲取 Rich Menu 列表時發生錯誤: {e}")
    # 刪除指定的 Rich Menu
def delete_rich_menu(rich_menu_id):
    try:
        line_bot_api.delete_rich_menu(rich_menu_id)
        print(f"Rich Menu {rich_menu_id} 已成功刪除")
    except Exception as e:
        print(f"刪除 Rich Menu 時發生錯誤: {e}")

if __name__ == "__main__":
    delete_all_rich_menus()
    app.run(debug=True)



