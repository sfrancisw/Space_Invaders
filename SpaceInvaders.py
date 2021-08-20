import os, turtle, math, random

#initialize screen
wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Space Invaders')
wn.bgpic('Space_Invaders_Background.gif')

#draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#draw player score
score = 0

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290, 270)
scorestring = 'Score: %s' % score
score_pen.write(scorestring, False, align='left', font=('Arial', 14, "normal"))
score_pen.hideturtle()

#create player
playerspeed = 20

player = turtle.Turtle()
player.color('blue')
player.shape('triangle')
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

#create enemies
multiplier = 1
number_of_enemies = 5
enemyspeed = 10
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color('red')
    enemy.shape('circle')
    enemy.penup()
    enemy.speed(0)
    enemy.setheading(90)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

#create bullet
bulletspeed = 30
bulletstate = 'ready'

bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

#create movement system
def left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)


def right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

#create shooting system
def fire():
    global bulletstate
    if bulletstate == 'ready':
        bulletstate = 'fire'
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

#looks for collisions
def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 20:
        return True
    else:
        return False

#set controls
turtle.listen()
turtle.onkey(left, 'Left')
turtle.onkey(right, 'Right')
turtle.onkey(fire, 'space')

#gameloop
while True:
    for enemy in enemies:
        #enemy movement system
        x = enemy.xcor()

        if enemy.heading() == 90:
            x += enemyspeed * multiplier

        else:
            x -= enemyspeed * multiplier
 
        enemy.setx(x)

        #enemy turns at game border
        if enemy.xcor() > 280:
            y = enemy.ycor()
            y -= 40
            enemy.sety(y)
            enemy.setheading(270)

        if enemy.xcor() < -280:
            y = enemy.ycor()
            y -= 40
            enemy.sety(y)
            enemy.setheading(90)

        #check for collision with bullet and enemy -> destroy enemy
        if isCollision(bullet, enemy):
            multiplier += 0.1
            bullet.hideturtle()
            bulletstate = 'ready'
            bullet.setposition(0, -400)
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            score += 10
            scorestring = 'Score: %s' % score
            score_pen.clear()
            score_pen.write(scorestring, False, align='left', font=('Arial', 14, "normal"))
            score_pen.hideturtle()

        #check for collision between player and enemy -> game over
        if isCollision(player, enemy):
            player.hideturtle()
            for enemy in enemies:
                enemy.hideturtle()
            print('Game Over')
            break

    #bullet fire and reload system
    if bulletstate == 'fire':
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = 'ready'

turtle.mainloop()
