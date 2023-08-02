import requests
import schedule
import threading
import time
import json
from plugins import register, Plugin, Event, logger
from channel.wechat import WeChatChannel
from utils.const import MessageType
from utils.gen import gen_id


@register
class Weather(Plugin):
    name = "weather"

    def __init__(self, config: dict):
        super().__init__(config)
        self.channel = WeChatChannel()
        scheduler_thread = threading.Thread(target=self.start_schedule)
        scheduler_thread.start()

    def did_receive_message(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        pass

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def help(self, **kwargs) -> str:
        return "每日天气预报"

    def start_schedule(self):
        schedule_time = self.config.get("schedule_time", "08:00")
        schedule.every().day.at(schedule_time).do(self.daily_push)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def daily_push(self):
        logger.info("Start daily push")
        single_chat_list = self.config.get("single_chat_list", [])
        group_chat_list = self.config.get("group_chat_list", [])
        content = self.get_weather()
        for single_chat in single_chat_list:
            reply_msg = self.serialize(content, None, single_chat)
            self.channel.ws.send(reply_msg)
        for group_chat in group_chat_list:
            reply_msg = self.serialize(content, group_chat, None)
            self.channel.ws.send(reply_msg)

    def serialize(
        self,
        content,
        room_id,
        sender_id,
    ) -> str:
        msg = {
            "id": gen_id(),
            "type": MessageType.TXT_MSG.value,
            "roomid": room_id or "null",
            "wxid": sender_id or "null",
            "content": content,
            "nickname": "null",
            "ext": "null",
        }
        return json.dumps(msg)

    def get_weather(self) -> str:
        city = self.config.get("city", "北京")
        app_id = self.config.get("app_id")
        app_secret = self.config.get("app_secret")
        try:
            response = requests.get(
                f"https://www.tianqiapi.com/free/day?appid={app_id}&appsecret={app_secret}&city={city}",
                timeout=5,
                verify=False,
            )
            if response.status_code == 200 and "errcode" not in response.text:
                data = response.json()
                text = (
                    f"今日{city}天气:\n"
                    f"日期:\t {data['date']}\n"
                    f"当前温度:\t {data['tem']}°C\n"
                    f"最高气温:\t {data['tem_day']}°C\n"
                    f"最低气温:\t {data['tem_night']}°C\n"
                    f"风向:\t {data['win']}\n"
                    f"风速:\t {data['win_meter']}\n"
                    f"天气:\t {data['wea']}\n"
                    f"湿度:\t {data['humidity']}\n"
                    f"\n更新时间:\t {data['update_time']}"
                )
            else:
                text = "查询天气失败, 请稍后再试"
        except Exception as e:
            logger.error(f"Get weather error: {e}")
            text = f"查询天气失败: {e}"
        return text
