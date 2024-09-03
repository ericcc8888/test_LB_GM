from bs4 import BeautifulSoup
import requests
from line_flex import generate_star_icons

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