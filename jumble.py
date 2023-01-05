import common
import config
import telebot
from telebot.types import Message
from telebot import types
import time
import datetime
import os,time
import threading
from dotenv import load_dotenv



load_dotenv()

# dataBase ___ import files
import schema
from DB_class import DynamoDB_con

DB = DynamoDB_con()

# print(DB.get_words())

r = 60
common.gameCounter = 1
common.game_creater = {}
common.participants = []
common.scour_Dict = {}
common.red_scour = {}

game_time = datetime.datetime.now()
common.nextEditButton = None
common.last_Right_ans = ''


def delete_message(chat_id, message_id, sec=0):
    # time.sleep(sec)
    bot.delete_message(chat_id, message_id)
    # return True


def alert(messageId, msg, show_alert=False):
    if show_alert:
        bot.answer_callback_query(messageId, msg, show_alert=True)
    else:
        bot.answer_callback_query(messageId, msg)


def create_game(game, message, t=60):
    print(message.from_user.id, message.from_user.first_name,
          'created jumble here ---')
    global editJoinMsg
    keyboard = telebot.types.InlineKeyboardMarkup()
    print(message.chat.id, message.message_id)
    chat_id = message.chat.id
    # return
    print(game)
    if (game == '/jumbleword' or game == '/jumbleword@botmorningbot_bot'):
        print('----> inside create game ')
        keyboard.row(
            telebot.types.InlineKeyboardButton(
                'Join Game 🎮', callback_data='join-jumble'),
        )
        first_name = message.from_user.first_name
        common.editJoinMsg = bot.send_message(
            chat_id, f'A Jumble word game is Starting... \nYou Have  *⌛{t}* _s_ to Join',
            reply_markup=keyboard,
            parse_mode='markdown'
        )
        if t == 60:
            bot.send_message(
                chat_id, f'{first_name} joined. \n There is now {common.total_players} players')
            common.scour_Dict[message.from_user.id] = {'points':0,"user_name":message.from_user.first_name }
            print(common.scour_Dict)
            # # creating thread for counter. students will get 60 seconds time to participate in jumble word game
            join_counter = threading.Thread(target=common.start_timer, args=(
                'join-wait', t, 'join-jumble', common.editJoinMsg))  # joining button thread
            join_counter.start()


def join_game(game, message, mode='auto', time=60):
    if mode == 'mannual':
        chat_id = message.json['message']['chat']['id']
    else:
        chat_id = message.json['chat']['id']
    global current_word_Message
    user_id = message.from_user.id

    if (game == 'join-jumble'):
        first_name = message.from_user.first_name
        if time == 0 and common.gameCounter <= 10:
            if mode == 'auto':
                bot.send_message(
                    chat_id, f'Here is the first word ⬇',
                    parse_mode='markdown'
                )

            if common.nextFlag:
                bot.edit_message_text(
                    chat_id=chat_id, message_id=common.nextEditButton.id, text=f'Congratulations {common.last_Right_ans} 🎉, \nYou guessed the word',
                    parse_mode='markdown'
                )
                common.gameCounter += 1
            data = {"Datatime":str(datetime.datetime.now()),'JumbledWord_InitiatedByUser_ID':str(common.game_creater['InitiatedBy']),"JumbledWord_Participation":len(common.participants)}
           

            DB.send_data(data,'TB_JumbledWord_Engagement')
            # time.sleep(2)
            current_word_Message = bot.send_message(
                chat_id, common.get_jumble(),
                parse_mode='markdown'
            )

        elif time > 0:
            print(60-common.wait60sec, 's time left')
            if user_id in common.participants:
                print(message.from_user.first_name, 'you already joined :)')
                alert(message.id, 'you already joined :)')

            else:
                common.total_players += 1
                common.participants.append(user_id)
                # print(message, 'yyyy')
                bot.send_message(
                    chat_id, f'{first_name} joined. \n There is now {common.total_players} players')
                common.scour_Dict[message.from_user.id] = {'points':0,"user_name":message.from_user.first_name }
                print(common.scour_Dict)
        elif common.gameCounter > 10:
            print(common.gameCounter, 'game left')
            common.time_breaker = False
            winner_announce = threading.Thread(
                target=common.start_timer, args=('ques-wait', 1, 'join-jumble', message))
            winner_announce.start()

def winner(message):
    print('game over',)
    chat_id = message.json['chat']['id']
    if common.gameCounter == 10:
        bot.send_message(
            message.chat.id, f'Congratulations *{message.from_user.first_name}*, \nYou guessed the word',
            parse_mode='markdown'
        )

    # print(common.scour_Dict, 'total score!! ')
    li = []
    name = []
    for ele in common.scour_Dict:
        li.append(common.scour_Dict[ele]['points'])
        name.append(common.scour_Dict[ele]['user_name'])

    li2 = li.copy()
    li.sort(reverse=True)
    print(li)
    firs = li2.index(li[0])
    li.pop(0)
    if len(common.scour_Dict) >= 2:
        sec = li2.index(li[0])
        li.pop(0)
        if len(common.scour_Dict) >= 3:
            thd = li2.index(li[0])
            li.pop(0)
            print(name[firs], name[sec], name[thd])
            # if (common.gameCounter >=3):

            bot.send_message(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

            🥇 {name[firs]} got {li2[firs]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️⭐️⭐️:

            🥈 {name[sec]} got {li2[sec]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️⭐️:

            🥉 {name[thd]} who got {li2[thd]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️:

            Congratulations {name[firs]} 👏🎊Keep it up and practice more. 📚📚📚''',
                             parse_mode='markdown'
                             )
        else:
            bot.send_message(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

            🥇 {name[firs]} got {li2[firs]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️⭐️⭐️:

            🥈 {name[sec]} got {li2[sec]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️⭐️:

            Congratulations {name[firs]} 👏🎊Keep it up and practice more. 📚📚📚''',
                             parse_mode='markdown'
                             )
    else:
        bot.send_message(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

            🥇 {name[firs]} got {li2[firs]//2}/{common.gameCounter} Questions correct ⭐️⭐️⭐️⭐️⭐️:

            Congratulations {name[firs]} 👏🎊Keep it up and practice more. 📚📚📚''',
                         parse_mode='markdown'
                         )
    
    for d in common.scour_Dict:
        t = time.time()
        t_ms = int(t * 1000)
        data = {"Id":str(t_ms),"Datetime":str(datetime.datetime.now()),"User_Id":str(d),"Points_Scored" :str(common.scour_Dict[d]['points'])}
        print('data: ',data)
        DB.send_data(data,'TB_Temp_JumbledWord_Session')
    # if common.day == 
    

    common.run = False
    # resetting all the valiables to default
    common.joinFlag = True  # to block joining patrticipants after 60 seconds
    # common.chat_type = None
    common.gameCounter = 0
    common.game_creater = {}
    common.participants = []
    common.nextButtonCount = False
    common.nextEditButton = None
    common.editJoinMsg = None
    common.last_Right_ans = ''
    common.nextFlag = False  # show or hide next button
    common.total_players = 0
    common.time_breaker = False
    common.wait60sec = 0  #
    common.wait40sec = 10
    common.word = ''
    common.used_words = []
    common.scour_Dict = {}
    common.red_scour = {}
    common.gameStarted = False  # to block creating new game if one is going on


print("Hi, Jumble here!")
bot = telebot.TeleBot(os.getenv('API_KEY'))

def main():
    @bot.message_handler(commands=['jumbleword'])
    def send_welcome(message):
        # common.chat_type = message.chat.type
        command = message.text
        print(message.chat.type, '-> chat type')
        if command.startswith('/jumbleword') and not common.gameStarted:
            # storing game creator information
            if common.joinFlag:
                print(common.joinFlag)
                common.total_players += 1
                common.game_creater = {
                    "date": game_time,
                    "InitiatedBy": message.from_user.id,
                    "total_common.participants": 0
                }
                common.participants.append(message.from_user.id)
                common.joinFlag = False
                common.gameStarted = True
                create_game(command, message)

    @bot.message_handler(content_types=['text'])
    def send_welcome(message):
        msg = message.text

        print(msg, common.word)

        keyboard = telebot.types.InlineKeyboardMarkup()
        if (msg.upper() == common.word):
            print(message.from_user.id, message.from_user.id)
            common.time_breaker = False
            if common.gameCounter <= 10:
                keyboard.row(
                    telebot.types.InlineKeyboardButton(
                        'Next Word', callback_data='next-jumble-word'),
                )
                common.nextEditButton = bot.send_message(
                    message.chat.id, f'Congratulations {message.from_user.first_name}, \nYou guessed the word',
                    reply_markup=keyboard,
                    parse_mode='markdown'
                )
                
                print( common.scour_Dict,'[[[[[[[[')
                common.scour_Dict[message.from_user.id]['points'] += 2
                print( common.scour_Dict[message.from_user.id],']]]]]]]]]]')


                if message.from_user.id in common.red_scour:
                    del common.red_scour[message.from_user.id]

                print(common.red_scour)
                for std in common.red_scour:
                    if std in common.scour_Dict:
                        common.scour_Dict[std]["points"] += 1

                common.last_Right_ans = message.from_user.first_name
                print(common.scour_Dict)
                common.nextButtonCount = False
                threads = threading.Thread(target=common.start_timer, args=(
                    'ques-wait', common.wait40sec, 'join-jumble', message))

            elif common.gameCounter > 10:
                threads = threading.Thread(target=common.start_timer, args=(
                    'ques-wait', 1, 'join-jumble', message))

            common.word = ''
            threads.start()
        elif (len(msg.upper()) == len(common.word)):
            dic, dic2, bool = {}, {}, True

            for i in range(len(msg.upper())):
                if common.word[i] not in dic2:
                    dic2[common.word[i]] = 1
                else:
                    dic2[common.word[i]] += 1

                if msg.upper()[i] not in dic:
                    dic[msg.upper()[i]] = 1
                else:
                    dic[msg.upper()[i]] += 1
            try:
                for k in dic:
                    if dic[k] != dic2[k]:
                        print('Wrong')
                        bool = False
                        break

                if (bool):

                    bot.send_message(
                        message.json['chat']['id'], f'You got this just missed, try again {message.from_user.first_name} 😱😱!', parse_mode='markdown')
                    
                    if message.from_user.id not in common.red_scour:
                        common.red_scour[message.from_user.id] = 1

            except:pass
                # bot.send_message(message.json['chat']['id'], f' Try again {message.from_user.first_name}🤔🤔',
                #                  parse_mode='markdown'
                #                  )

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(option):

        query = option.data
        common.run = True
        print(query, '000000000000')
        if query == 'join-jumble':
            join_game(query, option, 'mannual', 60)

        elif query == 'next-jumble-word':
            if not (common.nextButtonCount):
                print('uuuuuuuuu', common.wait60sec)
                common.nextButtonCount = True  # for limiting the next button click
                common.time_breaker = True
                common.nextFlag = True
                join_game('join-jumble', option, 'mannual', 0)

    bot.polling(none_stop=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('this is error!!!!!', e)
