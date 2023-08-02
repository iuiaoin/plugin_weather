## 🚀 Getting Start

Add the following config in your wechat-gptbot's config.json:

```bash
 "plugins": [
  {
    "name": "weather",
    "city": "北京",                                 # The city of the weather report
    "schedule_time": "08:00",                      # The scheduled time
    "single_chat_list": ["wxid_dierxe23232kye67"], # Single chat id aka sender_id, send a message then you can get it from console
    "group_chat_list": ["8393042746@chatroom"],    # Group chat id aka room_id, send a message in chat group then you can get it from console
    "app_id": "84759372",                          # app id for weather api
    "app_secret": "049uhKIL"                       # app secret for weather api
  }
]
```

> `app_id` and `app_secret` can be obtained from https://www.tianqiapi.com/index/doc?version=day for free.

Then the weather report will be sent to the group chat and private chat in the configuration every day~
