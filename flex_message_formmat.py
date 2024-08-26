#選擇地區的flexmessage
def locations_flexmessage():
    contents = {
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
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "地區選擇",
            "weight": "bold",
            "size": "xl"
        }
        ]
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
            "text": "台北hello"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "台中",
            "text": "台中hello"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "台南",
            "text": "台南hello"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "高雄",
            "text": "高雄hello"
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

def exotic_cuisine_class():
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