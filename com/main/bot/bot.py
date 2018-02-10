from time import sleep

import telebot
import vk_api
from com.main.files import config

bot = telebot.TeleBot(config.ACCESS_TG_TOKEN)
vk_session = vk_api.VkApi(token=config.ACCESS_VK_TOKEN)
vk = vk_session.get_api()


def get_post(owner):
    return vk.wall.get(owner_id=owner, count=2)


def error_message(msg):
    bot.send_message(config.ADMIN_ID, msg)


@bot.message_handler(commands=["start"])
def start(msg):
    print(str(msg))
    bot.send_message(msg.chat.id, config.LIST_TEXT["start"], parse_mode='Markdown')
    last_post_JustStory = get_post(config.LIST_ID_GROUPS["JustStory"])["items"][0]
    last_post_Whore = get_post(config.LIST_ID_GROUPS["HackWhore"])["items"][0]

    try:
        while True:
            post_JustStory = get_post(config.LIST_ID_GROUPS["JustStory"])["items"][1]
            post_HackWhore = get_post(config.LIST_ID_GROUPS["HackWhore"])["items"][1]
            if post_JustStory["id"] != last_post_JustStory["id"]:
                print("post=" + str(post_JustStory))
                last_post_JustStory = post_JustStory
                post_text = post_JustStory["text"]

                if post_text != "":
                    if len(post_text) > 2000:
                        while len(post_text) > 2000:
                            bot.send_message(msg.chat.id, post_text[0:1999])
                            sleep(0.2)
                            post_text = post_text[1999:]
                    else:
                        bot.send_message(msg.chat.id, post_text)

            if post_HackWhore["id"] != last_post_Whore["id"]:
                print("post=" + str(post_HackWhore))
                post_image = post_HackWhore["attachments"][0]["photo"]["photo_1280"]
                bot.send_photo(msg.chat.id, post_image, "HackWhore")
                last_post_Whore = post_HackWhore
            else:
                print("Нет новых постов")
            sleep(15)
    except Exception:
        print('Unknown error')


@bot.message_handler(content_types=["text"])
def send_msg(msg):
    print("msg?")
    if msg.from_user.id == 149168806:
        bot.send_message(418184119, "Любимый: " + msg.text)
        print("send::msg yes to me")
    else:
        bot.send_message(149168806, "Горошек: " + msg.text)
        print("send::msg yes to goroh")


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=60000)
