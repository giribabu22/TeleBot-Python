import random
import time
import jumble
import DB_class
from DB_class import DynamoDB_con

DB = DynamoDB_con()

data, l = DB.get_words()
words = []
for dic in data:
    words.append(dic['word'])
chat_id = None
gameStarted = False  # to block creating new game if one is going on
joinFlag = True  # to block joining patrticipants after 60 seconds
# chat_type = None
gameCounter = 0  # count the how many word appearead in a particular game
game_creater = {}  # storing data of who initiated the game
participants = []  # storing data of joined participants in a particular game
nextButtonCount = False  # decision for next word
nextEditButton = None  # storing current (Next Word) button data
editJoinMsg = None
last_Right_ans = ''  # storing name of user who guessed current word
nextFlag = False  # show or hide the next button
total_players = 0  # counting total participants
time_breaker = False  # decision on breaking timer
word = ''
runner = 0
used_words = []
day = 0
scour_Dict = {}
wait60sec = 0  # waiting time for particiants to join the game (60)
wait40sec = 20  # waiting time for particiants to join the game (60
guessTime = 20  # waiting time to guess the word

# var
sec60 = 7

another_var = True
DB = DB_class.DynamoDB_con()
# DB.read_read('TB_JumbleWord_Bank')

def get_jumble():
    try:
        global word, gameCounter, runner
        # words = ['furze', 'fuses', 'fusee', 'fused', 'fusel', 'fuser', 'fussy', 'gales', 'galls', 'gamba', 'gamer', 'gamin']
        word = random.choices(words)[0].upper()
        jumble = ' '.join(random.sample(word, len(word)))
        jumbled = ''
        random_number = random.randrange(1, len(word))
        jumbled += word[0]+' '
        for i in range(1, len(word)):
            if i == random_number and len(word) > 4:
                jumbled += word[i]+' '
            else:
                jumbled += '_ '
        gameCounter += 1
        runner = 1
        return f'🔤 {len(word)} letters: *{jumble}* \n 🤔 : *{" ".join(jumbled)}*'
    except Exception as e:
        jumble.ErrorHandler(e)
        print('error in get_jumble function :@@@@@@@@@@@@ ', e)
        
# # Join timer (60s) and word timer (40s)

def start_timer(name, sec, message):
    try:
        global wait60sec, runner
        for i in range(sec, -1, -1):
            # print('name: ',name,"sec: " ,sec,"game: ", game ,'running: ',runner)
            print(i,sec,'time_breaker: ',time_breaker)
            if time_breaker:
                print('i am the breaker ')
                break
            time.sleep(1)
            wait60sec = i
            if i == 30 or i == 15:
                if name == 'join-wait':
                    jumble.create_game('/jumbleword', message, i)
                    runner == 2

            elif i == 0:
                if name == 'guess-wait' and runner == 1:
                    jumble.auto_next_word(message)
                    runner == 2
                elif name == 'join-wait':
                    jumble.join_game(message, 'auto', i)
                    runner == 2
                elif name == 'ques-wait' and runner == 3:  # after 40 sec of 1 word
                    jumble.winner(message, False)
                elif  name == 'ques-wait' and runner == 0:
                    jumble.winner(message, False)
                # elif name == 'ques-wait'and (runner):
                #     jumble.winner(message, False)
                #     runner = False
                break
    except Exception as e:
        jumble.ErrorHandler(e)
        print('error in start_timer function @@@@@@@@@@@@@@', e)
