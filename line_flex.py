from bs4 import BeautifulSoup
import requests


# 將星數數值轉換成星星圖片url
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

    # # 生成星星圖示內容
    # return rateing_star

# 將獲取的資訊轉換成flex message格式
def line_store_flex(photo_url, name, place_rate, detailed_address, business_status, telephone, googlemap_url, business_color, flex_message_datas):
    flex_message_datas.append({
            "type": "bubble",
            "size": "deca",
            "hero": {
                "type": "image",
                "url": photo_url,
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "320:213",
                "action":{
                    "type":"uri",
                    "uri": googlemap_url
                }
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
                        "maxLines": 1,
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "offsetTop": "sm",
                        "contents": generate_star_icons(place_rate)
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
                                        "text": detailed_address,
                                        "size": "xs"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "offsetTop": "md",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": business_status,
                                        "size": "sm",
                                        "flex": 1,
                                        "color": business_color
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
                ]
            }
        })
    return flex_message_datas

def flex_formmat(places_text):
    
    flex_message = {
        "type": "carousel",
        "contents": places_text
        }
    return flex_message

# 愛食記爬蟲以及將爬蟲資料轉換成flex message
class line_bot_scraper_ifoodie:
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

# 食物大分類的flex message格式
def big_food_class():
    contents ={
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2020/09/05/1/8488743.jpg&x=0&y=0&sw=0&sh=0&exp=3600",
            "size": "5xl",
            "aspectMode": "cover",
            "aspectRatio": "150:196",
            "gravity": "center",
            "flex": 1,
            "action": {
              "type": "postback",
              "data": "rice_class"
            }
          },
          {
            "type": "image",
            "url": "https://d3l76hx23vw40a.cloudfront.net/material/53.jpg",
            "size": "5xl",
            "aspectMode": "cover",
            "aspectRatio": "150:196",
            "gravity": "center",
            "flex": 1,
            "action": {
              "type": "postback",
              "data": "noodle_class"
            }
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://tw.savorjapan.com/gg/content_image/t0268_001.jpg",
            "size": "5xl",
            "aspectMode": "cover",
            "aspectRatio": "150:196",
            "gravity": "center",
            "flex": 1,
            "action": {
              "type": "postback",
              "data": "hot_pot_class"
            }
          },
          {
            "type": "image",
            "url": "https://blackmomo.tw/wp-content/uploads/221213-P000.jpg",
            "size": "5xl",
            "aspectMode": "cover",
            "aspectRatio": "150:196",
            "gravity": "center",
            "flex": 1,
            "action": {
              "type": "postback",
              "data": "dessert_class"
            }
          }
        ]
      }
    ],
    "paddingAll": "0px"
  }
}
    return contents

# 美食推薦地區選擇的flex message #需要改圖片
def ifoodie_class(): 
    contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://line.me/"
    }
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "台北",
          "text": "台北"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "台中",
          "text": "台中"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "台南",
          "text": "台南"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "台東",
          "text": "台東"
        }
      }
    ],
    "flex": 0
  }
}
    return contents

def rice_class():
    contents = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://i.epochtimes.com/assets/uploads/2022/09/id13816945-shutterstock_1730946862.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "炒飯"
                }
              },
              {
                "type": "image",
                "url": "https://www.gomaji.com/blog/wp-content/uploads/2020/11/%E7%91%9E%E6%A6%AE%E7%87%92%E8%87%98-1.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "燒臘飯"
                }
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://i0.wp.com/hoolee.tw/wp-content/uploads/20230718235630_16.jpg?resize=1000%2C667&quality=100&ssl=1",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "咖哩飯"
                }
              },
              {
                "type": "image",
                "url": "https://cc.tvbs.com.tw/img/program/upload/2022/08/19/20220819114323-ea211b16.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "丼飯"
                }
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://live.staticflickr.com/3569/3833478709_014bba9491_b.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "150:98",
            "gravity": "center",
            "action": {
              "type": "message",
              "text": "羹飯"
            }
          },
          {
            "type": "image",
            "url": "https://img.ltn.com.tw/Upload/food/page/2019/09/15/190915-9565-0-ksAe2.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "150:98",
            "gravity": "center",
            "action": {
              "type": "message",
              "text": "燉飯"
            }
          }
        ]
      }
    ],
    "paddingAll": "0px"
  }
}
    
    return contents

def noodle_class():
    contents = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://cdn-www.cw.com.tw/article/202101/article-5ff76e12dff12.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "拉麵"
                }
              },
              {
                "type": "image",
                "url": "https://cdn2.ettoday.net/images/5931/d5931680.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "乾麵"
                }
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://bussfood.com/Data/Images/20161006/13/c454419244ec6b0f5b79c61275a29884.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "湯麵"
                }
              },
              {
                "type": "image",
                "url": "https://img.ltn.com.tw/Upload/news/600/2018/07/28/2502439_1.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "羹麵"
                }
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://www.unileverfoodsolutions.tw/dam/global-ufs/mcos/na/taiwan/calcmenu/recipes/TW-recipes/general/%E9%87%91%E6%B2%99%E9%AE%AE%E8%9D%A6%E7%BE%A9%E5%A4%A7%E5%88%A9%E9%BA%B5/WR2023PhaseII008.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "150:70",
            "gravity": "center",
            "action": {
              "type": "message",
              "text": "義大利麵"
            }
          }
        ]
      }
    ],
    "paddingAll": "0px"
  }
}
    
    return contents

def dessert_class():
    contents = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://www.groyalhotel.com.tw/wp-content/uploads/2020/09/%E9%BB%9E%E5%BF%83%E5%9D%8A-6.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "港點"
                }
              },
              {
                "type": "image",
                "url": "https://media.gq.com.tw/photos/5dbc3ba9b0b8ce000860046d/master/pass/2018100946431169.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "麵包店"
                }
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://d9602aa1b5.cbaul-cdnwnd.com/487d5ddbb15c8956d05c8c45c33edd03/200000012-57edb58e66/3cac1cca-03cf-4da2-baff-7f38a9514eaa.jpg?ph=d9602aa1b5",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "下午茶"
                }
              },
              {
                "type": "image",
                "url": "https://img.shoplineapp.com/media/image_clips/66163ce060cc1b00110fcad4/original.png?1712733407",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "手搖飲"
                }
              }
            ]
          }
        ]
      }
    ],
    "paddingAll": "0px"
  }
}
    
    return contents

#需要改圖片
def hot_pot_class():
    contents = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://www.kkday.com/zh-tw/blog/wp-content/uploads/Fridays-1.jpeg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "美式餐廳"
                }
              },
              {
                "type": "image",
                "url": "https://cc.tvbs.com.tw/img/program/upload/2021/06/25/20210625173432-f8b66db2.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "西餐廳"
                }
              }
            ],
            "flex": 1
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": "https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2022/01/16/0/15343224.jpg&x=0&y=0&sw=0&sh=0&sl=W&fw=800&exp=3600&w=930",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "印度餐廳"
                }
              },
              {
                "type": "image",
                "url": "https://angelala.tw/wp-content/uploads/2021/01/ye1.jpg",
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "150:98",
                "gravity": "center",
                "action": {
                  "type": "message",
                  "text": "泰式餐廳"
                }
              }
            ]
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://www.kkday.com/zh-tw/blog/wp-content/uploads/%E8%B6%8A%E5%8D%97.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "150:98",
            "gravity": "center",
            "action": {
              "type": "message",
              "text": "越式餐廳"
            }
          },
          {
            "type": "image",
            "url": "https://media.vogue.com.tw/photos/5db7fbbf22a7000008dcb23d/3:2/w_1600%2Cc_limit/2019040682804897.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "150:98",
            "gravity": "center",
            "action": {
              "type": "message",
              "text": "港式餐廳"
            }
          }
        ]
      }
    ],
    "paddingAll": "0px"
  }
}
    
    return contents

def no_search():
    contents ={
  "type": "bubble",
  "size": "hecto",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "附近沒有您想搜尋的食物類型",
        "weight": "bold",
        "size": "md"
      }
    ]
  }
}
    return contents