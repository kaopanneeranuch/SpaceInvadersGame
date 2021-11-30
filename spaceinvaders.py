import turtle
import time
import math
import random

#Setup the screen
wn = turtle.Screen()
wn.title("Space Invaders Game")
wn.bgpic("space_invaders_bg.gif")
wn.setup(width=600, height=600)
wn.tracer(0)

wn.register_shape("invader.gif")
wn.register_shape("ship.gif")

#Create the player
player = turtle.Turtle()
player.speed(0)
player.shape("ship.gif")
player.penup()
player.goto(0,-250)

invaders = []

#Create the invaders
for _ in range(5):
    invader = turtle.Turtle()
    invader.speed(0)
    invader.shape("invader.gif")
    invader.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    invader.goto(x, y)
    invaders.append(invader)

invarderspeed = 2

#Create the bullet
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("triangle")
bullet.color("red")
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

score = 0
#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(-240, 270)
pen.write("Score: {}".format(score), align="center", font=("Courier", 14, "bold"))

#Bullet state
bulletstate = "ready"

#Functions
def go_left():
    x = player.xcor()
    x -= 15
    if x < -280:
        x = -280
    player.setx(x)

def go_right():
    x = player.xcor()
    x += 15
    if x > 280:
        x = 280
    player.setx(x)

def firebullet():
    #Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        #Move the bullet to above the player
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15 :
        return True
    else:
        return False


#keyboard binding
wn.listen()
wn.onkeypress(go_left, "Left") 
wn.onkeypress(go_right, "Right")
wn.onkeypress(firebullet, "space")

#Mainloop
while True:
    wn.update()
    time.sleep(1/110)

    for invader in invaders:
        #Move the invader
        x = invader.xcor()
        x += invarderspeed
        invader.setx(x)

        #Reverse&Move down the invaders
        if invader.xcor() > 280:
            for i in invaders:
                i.sety(i.ycor() - 40)
            invarderspeed *= -1


        if invader.xcor() < -280:
            for i in invaders:
                i.sety(i.ycor() - 40)
            invarderspeed *= -1

        #Check for the collision bullet&invader
        if isCollision(bullet, invader):
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.goto(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            invader.goto(x, y)

            #Increase the score
            score += 1

            pen.clear()
            pen.write("Score: {}".format(score), align="center", font=("Courier", 14, "bold"))

        #Check for the collision invader&player
        if isCollision(invader, player):
            time.sleep(1)
            player.goto(0,-250)

            #Hide the invaders
            for invader in invaders:
                invader.goto(1000, 1000) #Off the screen

            score = 0

            pen.clear()
            pen.goto(-110, 0)
            pen.write("GAME OVER!", font=("Courier", 30, "bold"))

    #Move the bullet
    if bulletstate == "fire":
        bullet.sety(bullet.ycor() + 20)

    #Check bullet to the top
    if bullet.ycor() > 280:
        bullet.hideturtle()
        bulletstate = "ready"


wn.mainloop()