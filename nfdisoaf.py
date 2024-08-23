import requests
from API_KEYS import get_api_keys
import sys,googlemaps


# 店家圖片
# 評論分數
# 地址
# 營業時間
# 電話



keys = get_api_keys()
channel_secret = keys['LINE_BOT_SECRET']
channel_access_token = keys['LINE_BOT_ACCESS_TOKEN']
gmaps = googlemaps.Client(key=keys['GOOGLEMAPS_API_KEY'])
# 替换为你的 Google Maps API Key

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

places_result = gmaps.places_nearby(location='24.139353,120.6837809', radius=300, keyword = '德利')


places_locations = []
for place in places_result['results']:
    place_location = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
    places_locations.append(place_location)

for place in places_result['results']:
    name = place.get('name')  # 獲取餐廳名稱
    place_location = place['geometry']['location']  # 獲取餐廳的經緯度
    lat = place_location['lat']
    lng = place_location['lng']
    store_id = place.get('place_id')
    store_photo = place.get('photos',[])

    if store_photo:
            photo_reference = store_photo[0].get('photo_reference')
            print(f"Photo Reference: {photo_reference}")

    photo_url = get_photo_url(photo_reference)
    print(f"Photo URL: {photo_url}")

            
