from flask import Flask, app, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, CarouselContainer,LocationMessage, TextSendMessage ,FlexSendMessage,ImageComponent,ImageComponent, TextComponent, BoxComponent, ButtonComponent, URIAction
from linebot.models.flex_message import BubbleContainer, TextComponent, BoxComponent
from linebot.exceptions import InvalidSignatureError

from API_KEYS import get_api_keys
from flex_message_formmat import store_message
import sys,googlemaps

# 替换为你的 Google Maps API 密钥
app = Flask(__name__)

keys = get_api_keys()

# 初始化 Google Maps 客户端
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


# 搜索店家
places_result = gmaps.places(query='嘉園小上海點心總匯店', location=(24.1401689, 120.6811455), radius=500)
store_name = '嘉園小上海點心總匯店'

# 获取第一个店家的 Place ID
place_id = places_result['results'][0]['place_id']



# 获取店家的详细信息
place_details = gmaps.place(place_id=place_id)

store_type = place_details['result'].get('opening_hours')
open_now = store_type.get('open_now')
store_status = ""

if open_now is True:
    store_status = "營業中"
else:
    store_status = "已打烊"

# 提取评分星数
rate_star = place_details['result'].get('rating')

if rate_star:
    print(f'The rating for the place is {rate_star} stars.')
else:
    print('No rating information available for this place.')

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


bubbles_data = [
    {
        'image_url': 'https://example.com/image1.jpg',
        'title': 'Title 1',
        'description': 'Description 1',
        'button_label': 'Button 1',
        'button_uri': 'https://example.com'
    },
    {
        'image_url': 'https://example.com/image2.jpg',
        'title': 'Title 2',
        'description': 'Description 2',
        'button_label': 'Button 2',
        'button_uri': 'https://example.com'
    }
]

# 动态生成 bubbles
bubbles = []
for data in bubbles_data:
    bubble = BubbleContainer(size='micro',
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text=data['title'],
                    weight='bold',
                    size='lg',  # 可以调整为 'sm', 'md', 'lg', 'xl'
                    margin='md'  # 控制文本与其他元素的间距
                ),
                TextComponent(
                    text=data['description'],
                    size='sm',
                    color='#999999',
                    margin='sm'  # 控制文本与其他元素的间距
                )
            ],
            padding_all='20px'  # 控制 body 部分的内边距
        ),
        footer=BoxComponent(
            layout='horizontal',
            contents=[
                ButtonComponent(
                    action=URIAction(label=data['button_label'], uri=data['button_uri'])
                )
            ],
            padding_all='10px'  # 控制 footer 部分的内边距
        )
    )
    bubbles.append(bubble)

# 创建 Carousel 布局
carousel = CarouselContainer(contents=bubbles)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # reply_text = TextSendMessage(text=event.message.text)

    # # 使用 reply_message 方法回應使用者
    # line_bot_api.reply_message(event.reply_token, reply_text)

    if event.message.text == "台灣美食":
        print("=======================")
        flex_message = FlexSendMessage(
        alt_text='This is a Flex Message',
        contents= carousel
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    else:
        reply_text = TextSendMessage(text='請輸入"台灣美食"')

        # 使用 reply_message 方法回應使用者
        line_bot_api.reply_message(event.reply_token, reply_text)


if __name__ == "__main__":
    app.run(debug=True)
