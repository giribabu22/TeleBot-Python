from dotenv import load_dotenv
import time
import datetime
import os
import time
import telebot
import threading
import common
from DB_class import DynamoDB_con
load_dotenv()


class FunctionFlow():
    def __init__(self,bot):
        self.bot_username = '@jumble_word_bot'
        self.bot = bot
        self.joinFlag = True  # to block joining patrticipants after 60 seconds
        self.gameCounter = 0
        self.game_creater = {}
        self.participants = []
        self.nextButtonCount = False
        self.nextEditButton = None
        self.editJoinMsg = None
        self.last_Right_ans = ''
        self.nextFlag = False  # show or hide next button
        self.total_players = 0
        self.time_breaker = False
        # waiting time for particiants to join the game (60)
        self.wait60sec = 0
        # waiting time for particiants to join the game (60
        self.wait40sec = 10
        self.guessTime = 10  # waiting time to guess the word

        # variiiii
        self.sec60 = 7
        self.word = ''
        self.used_words = []
        self.scour_Dict = {}
        self.runner = 0
        self.red_scour = {}
        self.gameStarted = False  # to block creating new game if one is going on

    def restartGame(self):
        self.joinFlag = True  # to block joining patrticipants after 60 seconds
        self.gameCounter = 0
        self.game_creater = {}
        self.participants = []
        self.nextButtonCount = False
        self.nextEditButton = None
        self.editJoinMsg = None
        self.last_Right_ans = ''
        self.nextFlag = False  # show or hide next button
        self.total_players = 0
        self.time_breaker = False
        # waiting time for particiants to join the game (60)
        self.wait60sec = 0
        # waiting time for particiants to join the game (60
        self.wait40sec = 40
        self.guessTime = 40  # waiting time to guess the word

        # variiiii
        self.sec60 = 60
        self.word = ''
        self.used_words = []
        self.scour_Dict = {}
        self.runner = 0
        self.red_scour = {}
        self.gameStarted = False  # to block creating new game if one is going on

    def ErrorHandler(self, er):
        self.restartGame()
        self.botsendingMassage(
            self.chat_id, f'''Server is down try again start the game /jumbleword@lazydynamo_bot \n  {er}''')

    def delete_message(self, chat_id, message_id, sec=0):
        self.bot.delete_message(chat_id, message_id)
        # return True

    def controleNextBtn(self, message, bool):
        if self.gameCounter < 10:
            try:
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton(
                        'Next Word', callback_data='next-jumble-word'),
                )
                self.time_breaker = True
                if (bool):
                    self.nextEditButton = self.botsendingMassage(
                        message.chat.id, f'Congratulations {message.from_user.first_name}, \nYou guessed the word',
                        reply_markup=keyboard)
                    self.runner = 3
                    self.scour_Dict[message.from_user.id]['points'] += 2
                    if message.from_user.id in self.red_scour:
                        del self.red_scour[message.from_user.id]

                    for std in self.red_scour:
                        if std in self.scour_Dict:
                            self.scour_Dict[std]["points"] += 1

                    self.last_Right_ans = message.from_user.first_name
                else:
                    self.nextEditButton = self.botsendingMassage(
                        self.chat_id, f"Word : {self.word}\n Guy's you missed it 👎🏻👎🏻👎🏻 \n !! Time up ⏱⏱⏱....",
                        reply_markup=keyboard)
                    self.runner = 3
                self.nextButtonCount = False
                self.time_breaker = False
                threads = threading.Thread(target=common.start_timer, args=(
                    'ques-wait', self.wait40sec, message)).start()

            except Exception as e:
                self.ErrorHandler(e)

        elif self.gameCounter > 10:
            self.runner = 3
            self.time_breaker = False
            threads = threading.Thread(target=common.start_timer, args=(
                'ques-wait', 1, message))

            self.word = ''
            try:
                threads.start()
            except Exception as e:
                self.ErrorHandler(e)

    def alert(self, messageId, msg, show_alert=False):
        if show_alert:
            self.bot.answer_callback_query(messageId, msg, show_alert=True)
        else:
            self.bot.answer_callback_query(messageId, msg)

    def create_game(self, game, message, t = 7):
        # global editJoinMsg
        keyboard = telebot.types.InlineKeyboardMarkup()
        chat_id = message.chat.id
        self.chat_id = chat_id
        if (game == '/jumbleword' or game == '/jumbleword'+self.bot_username):
            print('----> inside create game ')
            keyboard.row(
                telebot.types.InlineKeyboardButton(
                    'Join Game 🎮', ccallback_data='join-jumble'),
            )
            first_name = message.from_user.first_name
            self.editJoinMsg = self.botsendingMassage(
                chat_id, f'A Jumble word game is Start... \nYou Have  *⌛{t}* _s_ to Join',
                reply_markup=keyboard)
            if t == self.sec60:
                self.bot.send_message(
                    chat_id, f'{first_name} joined. \n There is now {self.total_players} players')
                self.scour_Dict[message.from_user.id] = {
                    'points': 0, "user_name": message.from_user.first_name}
                # # creating thread for counter. students will get 60 seconds time to participate in jumble word game
                join_counter = threading.Thread(target=common.start_timer, args=(
                    'join-wait', t, self.editJoinMsg))  # joining button thread
                try:
                    join_counter.start()
                except Exception as e:
                    self.ErrorHandler(e)
            if t == self.guessTime:
                if self.nextFlag:
                    self.botsendingMassage(chat_id=chat_id, message_id=self.nextEditButton.id,
                                           text=f'Congratulations {self.last_Right_ans} 🎉, \nthe You guessed the word')
                data = {"Datatime": str(datetime.datetime.now()), 'JumbledWord_InitiatedByUser_ID': str(
                    self.game_creater['InitiatedBy']), "JumbledWord_Participation": len(self.participants)}

    def auto_next_word(self, message):
        self.nextButtonCount = True  # for limiting the next button click
        self.time_breaker = True
        self.nextFlag = True
        self.join_game("option", 'skip', 0)

    def join_game(self, message, mode='auto', time=7):

        skip = False
        if mode == 'skip':
            skip = True
        elif mode == 'mannual':
            chat_id = message.json['message']['chat']['id']
        else:
            chat_id = message.json['chat']['id']

        if not (skip):
            global current_word_Message
            user_id = message.from_user.id

            first_name = message.from_user.first_name

            # if len(self.scour_Dict) == 1:
            #     bot.send_message(
            #         chat_id, f'You need atleast 2 players to play this game !! \n \n \t Happy learning⬇',
            #         parse_mode='markdown'
            #     )
            #     # resetting all the valiables to default
            #     restartGame()
            if time == 0 and self.gameCounter < 10:
                self.time_breaker = True
                if mode == 'auto':
                    self.botsendingMassage(
                        chat_id, f'Here is the first word ⬇')
                data = {"Datatime": str(datetime.datetime.now()), 'JumbledWord_InitiatedByUser_ID': str(
                    self.game_creater['InitiatedBy']), "JumbledWord_Participation": len(self.participants)}

                # DB.send_data(data, 'TB_JumbledWord_Engagement')

                if self.runner == 0 or self.runner == 3:

                    current_word_Message = self.botsendingMassage(
                        chat_id, common.get_jumble())
                    self.time_breaker = False
                    guessWait = threading.Thread(
                        target=common.start_timer, args=('guess-wait', self.guessTime, message))
                    try:
                        guessWait.start()
                    except Exception as e:
                        self.ErrorHandler(e)
            elif time > 0:
                if self.wait60sec <= 0:
                    self.alert(
                        message.id, "Game is already started! Try joining next game ")

                elif user_id in self.participants:
                    self.alert(message.id, 'you already joined :)')
                else:
                    self.total_players += 1
                    self.participants.append(user_id)
                    self.botsendingMassage(
                        chat_id, f'{first_name} joined. \n There are now {self.total_players} players')
                    self.scour_Dict[message.from_user.id] = {
                        'points': 0, "user_name": message.from_user.first_name}
            elif self.gameCounter >= 10:
                self.time_breaker = False
                winner_announce = threading.Thread(
                    target=common.start_timer, args=(
                        'ques-wait', self.wait40sec, message))
                try:
                    winner_announce.start()
                except Exception as e:
                    self.ErrorHandler(e)
        else:
            self.controleNextBtn(message, False)

    def winner(self, message, r=True):
        self.time_breaker = True
        threads = threading.Thread(target=common.start_timer, args=(
            'ques-wait', 1, message))
        if r:
            chat_id = message.json['chat']['id']
        else:
            chat_id = self.chat_id
        if self.gameCounter == 10:
            self.botsendingMassage(
                message.chat.id, f'Congratulations *{message.from_user.first_name}*, \n the You guessed the word')

        print('total score!! : ', self.scour_Dict)
        self.lastCngmessage(chat_id)  # calling the last message show function

    def lastCngmessage(self, chat_id):
        li = []
        name = []
        for ele in self.scour_Dict:
            li.append(self.scour_Dict[ele]['points'])
            name.append(self.scour_Dict[ele]['user_name'])

        li2 = li.copy()
        li.sort(reverse=True)
        firs = li2.index(li[0])

        li.pop(0)
        first_name = name.pop(0)
        self.runner = 2
        if li2[firs] != 0:
            if len(self.scour_Dict) >= 2:

                sec = li2.index(li[0])
                li.pop(0)
                sec_name = name.pop(0)
                if len(self.scour_Dict) >= 3:
                    thd = li2.index(li[0])
                    li.pop(0)
                    thd_name = name.pop(0)

                    self.botsendingMassage(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

                    🥇 {first_name} got {li2[firs]//2}/{self.gameCounter} Questions correct ⭐️⭐️⭐️:

                    🥈 {sec_name} got {li2[sec]//2}/{self.gameCounter} Questions correct ⭐️⭐️:

                    🥉 {thd_name} got {li2[thd]//2}/{self.gameCounter} Questions correct ⭐️:

                    Congratulations {first_name} 👏🎊Keep it up and practice more. 📚📚📚''')
                else:
                    self.botsendingMassage(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

                    🥇 {first_name} got {li2[firs]//2}/{self.gameCounter} Questions correct ⭐️⭐️⭐️:

                    🥈 {sec_name} got {li2[sec]//2}/{self.gameCounter} Questions correct ⭐️⭐️:

                    Congratulations {first_name} 👏🎊Keep it up and practice more. 📚📚📚''')
            else:
                self.botsendingMassage(chat_id, f''' Thank you for participating in today's  Jumble word Game! 🥳🎉🎉🎉

                    🥇 {first_name} got {li2[firs]//2}/{self.gameCounter} Questions correct ⭐️⭐️⭐️:

                    Congratulations {first_name} 👏🎊Keep it up and practice more. 📚📚📚''')
        else:
            self.botsendingMassage(chat_id, f''' Thank you for participating in today's  Jumble word Game!
                    👎🏻👎🏻👎🏻Oops there is no Winner! 👎🏻👎🏻👎🏻 
                Try to answer it and practice more. 📚📚📚''')

        for d in self.scour_Dict:
            t = time.time()
            t_ms = int(t * 1000)
            data = {"Id": str(t_ms), "Datetime": str(datetime.datetime.now()), "User_Id": str(
                d), "Points_Scored": str(self.scour_Dict[d]['points'])}
            # DB.send_data(data, 'TB_Temp_JumbledWord_Session')

        # resetting all the valiables to default
        self.restartGame()

    def botsendingMassage(self, id, msg):
        return self.bot.send_message(id, msg, parse_mode='markdown')

    def threadRun(self, msgData, name):
        self.time_breaker = True
        threads = threading.Thread(target=common.start_timer, args=(
            name, 1, msgData))
