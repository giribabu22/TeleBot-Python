import threading
from DB_class import DynamoDB_con
import schema
import common
import time
import datetime
import os
import time
import telebot
from dotenv import load_dotenv
from classes.pizza import FunctionFlow

game_time = datetime.datetime.now()
load_dotenv()


# ___creating the object for the classes
print("Hi, Jumble here!")
bot = telebot.TeleBot(os.getenv('API_KEY'))
DB = DynamoDB_con()
classObj = FunctionFlow(bot)

def main():
    @bot.message_handler(commands=['jumbleword'])
    def send_welcome(message):
        command = message.text
        print(message.chat.type, '-> chat type', command)
        if command.startswith('/jumbleword') and not classObj.gameStarted:
            # storing game creator information
            if classObj.joinFlag:
                classObj.total_players += 1
                classObj.game_creater = {
                    "date": game_time,
                    "InitiatedBy": message.from_user.id,
                    "total_common.participants": 0
                }
                classObj.participants.append(message.from_user.id)
                classObj.joinFlag = False
                classObj.gameStarted = True
                classObj.create_game(command, message)

    @bot.message_handler(content_types=['text'])
    def send_welcome(message):
        msg = message.text
        print(msg, classObj.word)

        keyboard = telebot.types.InlineKeyboardMarkup()
        try:
            if message.from_user.id not in classObj.scour_Dict.keys():
                classObj.alert(message.id, 'You are not a part of this game!')
        except:
            pass
        else:
            if classObj.wait60sec > 1:
                if (msg.upper() == classObj.word):
                    classObj.time_breaker = True
                    # threads = threading.Thread(target=classObj.start_timer, args=(
                    #     'guess-wait', 1, 'join-jumble', message))
                    # print('classObj.time_breaker: ', classObj.time_breaker)

                    classObj.controleNextBtn(message, True)

                elif (len(msg.upper()) == len(classObj.word)):
                    dic, dic2, bool = {}, {}, True

                    for i in range(len(msg.upper())):
                        if classObj.word[i] not in dic2:
                            dic2[classObj.word[i]] = 1
                        else:
                            dic2[classObj.word[i]] += 1

                        if msg.upper()[i] not in dic:
                            dic[msg.upper()[i]] = 1
                        else:
                            dic[msg.upper()[i]] += 1
                    try:
                        for k in dic:
                            if dic[k] != dic2[k]:
                                bool = False
                                break
                        if (bool):
                            bot.send_message(
                                message.json['chat']['id'], f'You got this just missed, try again {message.from_user.first_name} 😱😱!', parse_mode='markdown')

                            if message.from_user.id not in classObj.red_scour:
                                classObj.red_scour[message.from_user.id] = 1

                    except:
                        pass

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(option):
        query = option.data
        if query == 'join-jumble':
            classObj.join_game(query, option, 'mannual', classObj.sec60)

        elif query == 'next-jumble-word' and option.from_user.id not in classObj.scour_Dict.keys():
            classObj.alert(option.id, 'You are not a part of this game!')

        elif query == 'next-jumble-word' or query == '1next-jumble-word':
            if not (classObj.nextButtonCount):
                classObj.nextButtonCount = True  # for limiting the next button click
                classObj.time_breaker = True
                classObj.nextFlag = True
                classObj.join_game('join-jumble', option, 'mannual', 0)

    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
