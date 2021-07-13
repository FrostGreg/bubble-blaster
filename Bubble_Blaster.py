from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt
#####Creates the window and colours it#####
HEIGHT = 500
WIDTH = 800
window = Tk()
window.title('Bubble Blaster')
c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

#####Creates the submarine#####
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')
SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)

#####Creates the control scheme for the game#####
SHIP_SPD = 10
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
        
        
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
        
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)

    elif end < time() and event.keysym == 'Escape':
        exit()
c.bind_all('<Key>', move_ship)                    #Runs the move_ship function when any key is pressed

#####Creates the bubbles#####
bub_id = list()
bub_r = list()              #creates three empty lists for the attributes of each bubble
bub_speed = list()
MIN_BUB_R = 10
MAX_BUB_R = 30              #sets the range for the bubble radius
MAX_BUB_SPD = 10
GAP = 100

def create_bubble():
    x = WIDTH + GAP             #sets the position
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)         # generates a random size for bubble
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')           #creates the bubble shape
    bub_id.append(id1)
    bub_r.append(r)                             #adds the info to the empty lists
    bub_speed.append(randint(1, MAX_BUB_SPD))

#####Makes the bubbles move#####
def move_bubbles():
    for i in range(len(bub_id)):          #loops through all bubbles created
        c.move(bub_id[i], -bub_speed[i], 0)       #moves the bubble across the screen according to the speed

def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2       #works out the x coordinate of the middle bubble
    y = (pos[1] + pos[3])/2          #works out the y co-ordinate of the middle bubble
    return x, y

#####Making the bubbles pop#####

def del_bubble(i):  #deletes the bubble
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]

def clean_up_bubs():
    for i in range (len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)   #deletes any bubbles that are off the screen

def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2) #returns the distance

def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):  #checks for collision betwenn bub and sub
            points += (bub_r[bub] + bub_speed[bub])  #creates the num of points the bub is worth
            del_bubble(bub)
    return points

c.create_text(50, 30, text='TIME', fill='white')  #creates time and score labels
c.create_text(150, 30, text='SCORE', fill='white')
time_text = c.create_text(50, 50, fill='white')    #sets the time and score
score_text = c.create_text(150, 50, fill='white')

def show_score(score):
    c.itemconfig(score_text, text=str(score))      #displays the score
    
def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))     #displays the time remaining

BUB_CHANCE = 10
TIME_LIMIT = 30
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time() + TIME_LIMIT
#Main Game loop
while time() < end:
    if randint(1, BUB_CHANCE) == 1:     #generates num(1-10) if = 1 then it generates #this reduces the amount of bubbles created
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision()
    if (int(score / BONUS_SCORE)) > bonus:
        bonus += 1
        end += TIME_LIMIT
    show_score(score)
    show_time(int(end - time()))
    window.update()
    sleep(0.01)

#####creates the GAME OVER graphic#####
c.create_text(MID_X, MID_Y, \
    text = 'GAME OVER', fill='white', font=('Helvetica',30))
c.create_text(MID_X, MID_Y + 30, \
    text='Score: '+ str(score), fill='white')
c.create_text(MID_X, MID_Y + 45, \
    text='Bonus time: '+ str(bonus*TIME_LIMIT), fill='white')
c.create_text(MID_X, MID_Y + 60, \
    text='Press ESC to finish', fill='white')
