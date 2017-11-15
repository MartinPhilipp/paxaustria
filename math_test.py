
import math
import turtle

ws = turtle.Screen()
ws.bgcolor("lightblue")
fred = turtle.Turtle()
for angle in range(120):
    y = math.sin(math.radians(angle*250))
    fred.goto(5*angle-300, y * 100)

ws.exitonclick()


