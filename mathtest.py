

import math
import turtle

ws = turtle.Screen()
ws.bgcolor("lightblue")
fred = turtle.Turtle()
for angle in range(120):
    y = math.sin(math.radians(angle*8))
    fred.goto(3*angle-200, y * 90)

ws.exitonclick()


