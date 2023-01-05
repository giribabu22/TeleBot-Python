import random
import time
import jumble
import DB_class
from DB_class import DynamoDB_con

DB = DynamoDB_con()

data,l = DB.get_words()
words =[]
for dic in data:
    words.append(dic['word'])
gameStarted = False #  to block creating new game if one is going on
joinFlag = True ## to block joining patrticipants after 60 seconds
# chat_type = None
gameCounter = 1
game_creater = {}
participants = []
nextButtonCount = False
nextEditButton = None
editJoinMsg = None
last_Right_ans = ''
nextFlag = False # show or hide next button
total_players = 0
time_breaker = False
wait60sec = 0  # 
wait40sec = 40 # 
word = ''
used_words = []
day = 0
scour_Dict = {}
# red_scour =   {}
run        = False
DB = DB_class.DynamoDB_con()
# DB.read_read('TB_JumbleWord_Bank')
def get_jumble():
    global word
    # words =  DB.get_words()
    # words = ['furze', 'fuses', 'fusee', 'fused', 'fusel', 'fuser', 'fussy', 'gales', 'galls', 'gamba', 'gamer', 'gamin']
    word = random.choices(words)[0].upper()
    # if len(words) > 0 and len(used_words) == 0:
    #     words.remove(word)
    #     used_words.append(word) 
    # else:
    #     word = random.choices(used_words)[0].upper()
    #     used_words.remove(word)
    #     words.append(word)
    
    jumble = ' '.join(random.sample(word, len(word)))    
    jumbled = ''
    random_number = random.randrange(1, len(word))
    jumbled += word[0]+' '
    for i in range(1, len(word)):
        if i == random_number and len(word) > 4:
            jumbled += word[i]+' '
        else:
            jumbled += '_ '
    return f'🔤 {len(word)} letters: *{jumble}* \n 🤔 : *{" ".join(jumbled)}*'

# # Join timer (60s) and word timer (40s)
def start_timer(name, sec, game, message):
    global wait60sec
    for i in range(sec, -1, -1):
        if time_breaker:
            break
        # else:
        time.sleep(1)
        wait60sec = i
        print(i, sec)
        if i == 30 or i == 15:
            if name == 'join-wait':
                jumble.create_game('/jumbleword', message, i)
                
        elif i == 0:
            if name == 'join-wait':
                jumble.join_game(game, message, 'auto', i)
                
            if name == 'ques-wait': # after 40 sec of 1 word 
                # jumble.join_game(game, message, 'auto', i)
                jumble.winner(message)
                
            break
            
        
        
        
    
