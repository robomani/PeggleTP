# Peggle

from livewires import games
from livewires import color
import random
import math

games.init(screen_width = 800, screen_height = 800, fps = 50)

ToDestroy = []
points = 0
multiplyer = 0
lives = 5
ballImage = games.load_image("Chakram.gif")
dotImage = games.load_image("Dot.gif")
ballInPlay = False
Score = games.Text("Score : ", 30, color.red, x = 70, y = 50)
multy = games.Text("Multiplyer : ", 30, color.red, x = 70, y = 100)
balls = games.Text("Chakrams : 5", 30, color.blue, x = 700, y = 50)

class FollowMouse(games.Sprite):
    cooldown = 10
    timer = 0
    """ An image controlled by the mouse"""
    def update(self):
        """ Move to mouse position """
        self.x = games.screen.width / 2
        self.y = 50
        self.angle = math.degrees(math.atan2((self.y - games.mouse.y),(self.x - games.mouse.x))) +270
        self.timer += 1
        global ballInPlay
        if self.timer >= self.cooldown and ballInPlay == False:
            self.timer = 0
            dot = Dot(image = dotImage, x = games.screen.width / 2, y = 100, dy = 1, dx = (games.mouse.x - self.x)/50)
            games.screen.add(dot)
        if games.mouse.is_pressed(0) and not ballInPlay:
            ball = Ball(image = ballImage, x = games.screen.width / 2, y = 100, dy = 1, dx = (games.mouse.x - self.x)/50)
            games.screen.add(ball)
            global lives
            balls.value = "Chakrams : " + str(lives)
            global ballInPlay
            ballInPlay = True
            

class Peggle(games.Sprite):
    marked = False
    def start(self):
        self.marked = False
        
    def update(self):
        self.handle_collide()
    """ Peggle to destroy """
    def handle_collide(self):
        """ Place in array to destroy at the end of the round """
        global ballInPlay
        for ball in self.overlapping_sprites:
            if self.marked == False and ballInPlay == True:
                self.marked = True
                ToDestroy.append(self)
                global multiplyer
                multiplyer += 1
                multy.value = "Multyplier : " + str(multiplyer)
            ball.dx = -ball.dx * 0.8
            ball.dy = -(ball.dy * 0.8)
            
    def destroy_self(self):
        global points
        global multiplyer
        points += 100 * multiplyer
        multiplyer -= 1
        Score.value = "Score : " + str(points)
        self.destroy()
        
class Dot(games.Sprite):
    lifetime = 75
    def update(self):
        self.lifetime -= 1
        global ballInPlay
        if self.lifetime <= 0 or ballInPlay == True:
            self.destroy()
        self.dy += 0.1
        """ Reverse a velocity component if lateral edge of screen reached. """
        if self.right > games.screen.width or self.left < 0:
            self.dx = -(self.dx * 0.8)
        """ Add impultion if stuck """
        if self.dy == 0:
            self.dy = 1.8
        if self.dx == 0:
            self.dx = 2.5
    def handle_collide(self):
        """ Check collision with ball """
        


class Ball(games.Sprite): 
    """ Technically a chakram """
    def update(self):
        self.dy += 0.1
        """ Reverse a velocity component if lateral edge of screen reached. """
        if self.right > games.screen.width or self.left < 0:
            self.dx = -(self.dx * 0.8)
        """ Add impultion if stuck """
        if self.dy == 0:
            self.dy = 1.8
        if self.dx == 0:
            self.dx = 2.5

        """ End turn if the ball reach the bottom of the screen """
        if self.bottom > games.screen.height or self.top < 0:
            self.end_turn(False)
    def check_collider(self):
        """ Check collision with things """
        for objects in self.overlapping_sprites:
            objects.handle_collide()
    def end_turn(self, gotCatched):
        """ End current turn """
        global ballInPlay
        ballInPlay = False
        global ToDestroy
        for peggle in ToDestroy:
            peggle.destroy_self()
        del ToDestroy[:]
        """ If the ball has not been cached the player lose a life """
        if gotCatched != True:
            global lives
            lives = lives - 1
        """ If there is no life left the game is dead (has ended) """
        #if lives < 1:
            #games.quit()
        self.destroy()
            
class Catcher(games.Sprite):
    """ The thing that catch the ball to prevent
        the loss of a life when the turn end"""
    def update(self):
        self.handle_collide()
        """ Reverse a velocity component if edge of screen reached. """
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
        
    def handle_collide(self):
        """ Check collision with ball """
        for ball in self.overlapping_sprites:
            ball.end_turn(True)

def main():
    

    Score.value = "Score : " + str(points)
    games.screen.add(Score)

    multy.value = "Multyplier : " + str(multiplyer)
    games.screen.add(multy)

    balls.value = "Chakrams : " + str(lives)
    games.screen.add(balls)
    
    peggleImage = games.load_image("head.jpg")

    ballImage = games.load_image("Chakram.gif")
    
    xenaImage = games.load_image("xena.jpg")
    xenaPosX = games.screen.width / 2
    xenaPosY = 50
    xena =  games.Sprite(image = xenaImage, x = xenaPosX, y = xenaPosY)
    games.screen.add(xena)

    catcherImage = games.load_image("Catch.jpg")
    catchPosX = games.screen.width / 2
    catchPosY = games.screen.height - 100
    catcher = Catcher(image = catcherImage, x = catchPosX, y = catchPosY, dx = 1)
    games.screen.add(catcher)

    luncherImage = games.load_image("Arm.jpg")
    luncher = FollowMouse(image = luncherImage)
    games.screen.add(luncher)



    peggle1 = Peggle(image = peggleImage, x = 308, y = 505)
    games.screen.add(peggle1)

    peggle2 = Peggle(image = peggleImage, x = 142, y = 456)
    games.screen.add(peggle2)

    peggle3 = Peggle(image = peggleImage, x = 683, y = 472)
    games.screen.add(peggle3)

    peggle4 = Peggle(image = peggleImage, x = 495, y = 314)
    games.screen.add(peggle4)

    peggle5 = Peggle(image = peggleImage, x = 319, y = 268)
    games.screen.add(peggle5)

    peggle6 = Peggle(image = peggleImage, x = 176, y = 394)
    games.screen.add(peggle6)

    peggle7 = Peggle(image = peggleImage, x = 83, y = 593)
    games.screen.add(peggle7)

    peggle8 = Peggle(image = peggleImage, x = 598, y = 462)
    games.screen.add(peggle8)

    peggle9 = Peggle(image = peggleImage, x = 668, y = 355)
    games.screen.add(peggle9)

    peggle10 = Peggle(image = peggleImage, x = 228, y = 260)
    games.screen.add(peggle10)
    
    games.mouse.is_visible = False
    #games.screen.event_grab = True

    games.screen.mainloop()

    

# Start the game
main()
