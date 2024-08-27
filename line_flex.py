def generate_star_icons(store_rateing_star):
    # 將星數值轉換為整數（四捨五入）
    if store_rateing_star == None:
        rounded_star_num = 0
    else:
        rounded_star_num = round(store_rateing_star)

    # 設定最大星數（5顆星）
    max_stars = 5

    # 計算金星和灰星的數量
    num_gold_stars = min(rounded_star_num, max_stars)
    num_gray_stars = max_stars - num_gold_stars

    # 生成星星圖示的URL
    gold_star_url = "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
    gray_star_url = "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"


    rateing_star = []

    for i in range(num_gold_stars):
        rateing_star.append({"type": "icon", "size": "xs", "url": gold_star_url}) 

    for i in range(num_gray_stars):
        rateing_star.append({"type": "icon", "size": "xs", "url": gray_star_url})

    rateing_star.append({
                                    "type": "text",
                                    "text": str(store_rateing_star),
                                    "size": "xs",
                                    "color": "#8c8c8c",
                                    "margin": "md",
                                    "flex": 0
                                })
    return rateing_star

flex_message_datas = []
    # # 生成星星圖示內容
    # return rateing_star

def line_store_flex(photo_url, name, place_rate, detailed_address, business_time, telephone):
    flex_message_datas.append({
            "type": "bubble",
            "size": "micro",
            "hero": {
                "type": "image",
                "url": photo_url,
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "320:213"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": name,
                        "weight": "bold",
                        "size": "sm",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": generate_star_icons(place_rate)
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "地址",
                                        "wrap": True,
                                        "color": "#8c8c8c",
                                        "size": "xxs",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": detailed_address,
                                        "size": "xs"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "營業時間",
                                        "size": "xxs",
                                        "flex": 1,
                                        "color": "#8c8c8c"
                                    },
                                    {
                                        "type": "text",
                                        "text": business_time,
                                        "size": "xs"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "撥打電話",
                                    "uri": telephone
                                }
                            }
                        ]
                    }
                ],
                "spacing": "sm",
                "paddingAll": "13px"
            }
        })
    return flex_message_datas

def flex_formmat(places_text):
    
    flex_message = {
        "type": "carousel",
        "contents": places_text
        }
    return flex_message

# result = ee[:]  # 複製 ee 的內容作為返回值
# ee.clear()  # 清空 ee
# return result

    

# if __name__ == '__main__':
#     xx()