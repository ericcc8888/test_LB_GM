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

#選擇圖卡的flexmassage
def store_message(store_name , open_status, rate_star):
   contents =  {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": "https://developers-resource.landpress.line.me/fx/clip/clip10.jpg",
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
            "text": store_name,
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "size": "xs",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "xs",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "xs",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "xs",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "xs",
                "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
              },
              {
                "type": "text",
                "text": rate_star,
                "size": "xs",
                "color": "#8c8c8c",
                "margin": "md",
                "flex": 0
              }
            ]
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
                    "text": open_status,
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    }
  ]
}
   return contents

    