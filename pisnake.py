# forked from https://repl.it/@LorenzoCampos
from os import system, name as OSname
from getkey import getkey, keys
from threading import Thread
from random import randint
from cursor import hide
from sys import stdout
from time import sleep

#--------------configs-------------#
# color codes
green = '\033[92m'
red = '\033[91m'
normal = '\033[0m'
speed = .2
food_index = 0
IMG_body = f'{green}π{normal}'
IMG_border = "⬜"
IMG_empty = " "
length = 20
width = 16
snakeBody = [5, 3]  # start position
foodPos = [5, 7]  # food start position
#----------------------------------#

# get pi digits
# decimal input
with open('pi_dec_1m.txt', 'r') as f:
    dec_pi = f.read()

# initialize
hide()
border = 0
points = 1
running = True
order, old = "null", "null"
world = [[IMG_empty]*length for _ in range(width)]
x, y = snakeBody[0], snakeBody[1]
world[x][y] = IMG_body
world[foodPos[0]][foodPos[1]] = red + dec_pi[food_index] + normal

# setup border
for _ in world:
  world[border][0] = IMG_border
  world[border][-1] = IMG_border
  border += 1
world[0] = IMG_border*len(world[0])
world[-1] = IMG_border*len(world[-1])

# clear screen
def clear(t = 0):
  sleep(t)
  system('cls' if OSname == 'nt' else 'clear')

# special print
def printt(string, delay = 0.005):
  for character in string:
    stdout.write(character)
    stdout.flush()
    sleep(delay)
  print("")

# display map
def display():
  print("\033[H",end="")
  for row in world:
    print(" ".join(map(str,row)))

# generate food at random position
def foodgen():
  pos1 = randint(1, width-2)
  pos2 = randint(1, length-2)

  if world[pos1][pos2] == IMG_empty:
    global food_index
    food_index += 1
    world[pos1][pos2] = red + dec_pi[food_index] + normal
  else: foodgen()

# update board
def update(nx = 0, ny = 0):
  global x, y, points, running
  x += nx
  y += ny
  snakeBody.append(x)
  snakeBody.append(y)
  
  if world[x][y] == IMG_empty:
    world[snakeBody[0]][snakeBody[1]] = IMG_empty
    del snakeBody[1]
    del snakeBody[0]
  if red in world[x][y]:
    points += 1
    foodgen()
  if world[x][y] == IMG_border or world[x][y] == IMG_body:
    running = False
  else:
    try: world[x][y] = IMG_body
    except: running = False

# determine movement
def move():
  global old
  if order == "up":
    update(-1, 0) 
    old = "up"
  if order == "down":
    update(1, 0)
    old = "down"
  if order == "left":
    update(0, -1)
    old = "left"
  if order == "right":
    update(0, 1)
    old = "right"
  display()

# detect keypress
def keypress(key):
  global order
  if key == keys.UP and old != "down" or key == "w" and old != "down": order = "up"
  if key == keys.DOWN and old != "up" or key == "s" and old != "up": order = "down"
  if key == keys.LEFT and old != "right" or key == "a" and old != "right": order = "left"
  if key == keys.RIGHT and old != "left" or key == "d" and old != "left": order = "right"

# keyboard jazz
class KeyboardThread(Thread):
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while running:
            self.input_cbk(getkey())


# main program
printt("Use WASD or ←↕→ to move", 0.05)
clear(1)
kthread = KeyboardThread(keypress)
while running:
  move()
  sleep(speed)
print("You died... Got to: ")
print(''.join(dec_pi[:food_index+1]))
