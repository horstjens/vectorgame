"""2d vector game in pure python3 / pygame, no external files necessary.
   create beautiul patterns by steering your spaceships with keyboard or
   joysticks (joysticks recommended. 4 players maximum"""

import pygame
import random


# patterns for player spaceship


# generic pygame functions



def make_text(text="@", font_color=(255, 0, 255), font_size=48, font_name = "mono", bold=True, grid_size=None):
    """returns pygame surface with text and x, y dimensions in pixel
       grid_size must be None or a tuple with positive integers.
       Use grid_size to scale the text to your desired dimension or None to just render it
       You still need to blit the surface.
       Example: text with one char for font_size 48 returns the dimensions 29,49
    """
    myfont = pygame.font.SysFont(font_name, font_size, bold)
    size_x, size_y = myfont.size(text)
    mytext = myfont.render(text, True, font_color)
    mytext = mytext.convert_alpha() # pygame surface, use for blitting
    if grid_size is not None:
        # TODO error handler if grid_size is not a tuple of positive integers
        mytext = pygame.transform.scale(mytext, grid_size)
        mytext = mytext.convert_alpha()  # pygame surface, use for blitting
        return mytext, (grid_size[0], grid_size[1])

    return mytext, (size_x, size_y)


def write(background, text, x=50, y=150, color=(0, 0, 0),
          font_size=None, font_name="mono", bold=True, origin="topleft"):
    """blit text on a given pygame surface (given as 'background')
       the origin is the alignement of the text surface
    """
    if font_size is None:
        font_size = 24
    font = pygame.font.SysFont(font_name, font_size, bold)
    width, height = font.size(text)
    surface = font.render(text, True, color)

    if origin == "center" or origin == "centercenter":
        background.blit(surface, (x - width // 2, y - height // 2))
    elif origin == "topleft":
        background.blit(surface, (x, y))
    elif origin == "topcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "topright":
        background.blit(surface, (x - width , y))
    elif origin == "centerleft":
        background.blit(surface, (x, y - height // 2))
    elif origin == "centerright":
        background.blit(surface, (x - width , y - height // 2))
    elif origin == "bottomleft":
        background.blit(surface, (x , y - height ))
    elif origin == "bottomcenter":
        background.blit(surface, (x - width // 2, y ))
    elif origin == "bottomright":
        background.blit(surface, (x - width, y - height))

class Flytext(pygame.sprite.Sprite):
    """a text flying for a short time around, like hitpoints lost message"""
    def __init__(self, x, y, text="hallo", color=(255, 0, 0),
                 dx=0, dy=-50, duration=2, acceleration_factor = 1.0, delay = 0, fontsize=22):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        self.text = text
        self.r, self.g, self.b = color[0], color[1], color[2]
        self.dx = dx
        self.dy = dy
        self.x, self.y = x, y
        self.duration = duration  # duration of flight in seconds
        self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        self.image = make_text(self.text, (self.r, self.g, self.b), fontsize)  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0 - delay

    def update(self, seconds):
        self.time += seconds
        if self.time < 0:
            self.rect.center = (-100,-100)
        else:
            self.y += self.dy * seconds
            self.x += self.dx * seconds
            self.dy *= self.acc  # slower and slower
            self.dx *= self.acc
            self.rect.center = (self.x, self.y)
            if self.time > self.duration:
                self.kill()      # remove Sprite from screen and from groups



class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    #number = 0
    #numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        #self.number = VectorSprite.number # unique number for each sprite
        #VectorSprite.number += 1
        #VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        #self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called"""
        pass

    def _default_parameters(self, **kwargs):
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self.layer = 0
        else:
            self.layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "stop_on_edge" not in kwargs:
            self.stop_on_edge = False
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "boss" not in kwargs:
            self.boss = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "move_with_boss" not in kwargs:
            self.move_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False

    def kill(self):
        # check if this is a boss and kill all his underlings as well
        tokill = []
        for s in Viewer.allgroup:
            if s.boss == self:
                tokill.append(s)
        for s in tokill:
            s.kill()
        #if self.number in self.numbers:
        #   del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height


    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        self.angle = self.angle % 360
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, -self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        self.angle = self.angle % 360
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, -self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.boss and self.move_with_boss:
                self.pos = self.boss.pos
                self.move = self.boss.move
        else:
             # move independent of boss
             self.pos += self.move * seconds
             self.distance_traveled += self.move.length() * seconds
             self.age += seconds
             self.wallcheck()
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )

    def wallcheck(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.stop_on_edge:
                self.x = 0
            if self.kill_on_edge:
                self.kill()
            if self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            if self.warp_on_edge:
                self.pos.x = Viewer.width
        # -------- upper edge -----
        if self.pos.y  < 0:
            if self.stop_on_edge:
                self.y = 0
            if self.kill_on_edge:
                self.kill()
            if self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            if self.warp_on_edge:
                self.pos.y = Viewer.height
        # -------- right edge -----
        if self.pos.x  > Viewer.width:
            if self.stop_on_edge:
                self.pos.x = Viewer.width
            if self.kill_on_edge:
                self.kill()
            if self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            if self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   > Viewer.height:
            if self.stop_on_edge:
                self.pos.y = Viewer.height
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            if self.bounce_on_edge:
                self.pos.y = PygView.height
                self.move.y *= -1
            if self.warp_on_edge:
                self.pos.y = 0

class Beam(VectorSprite):
    """laser-beam, need color, pos, move and angle """

    def _overwrite_parameters(self):
        self.kill_on_edge = True
        self._layer = 7
        self.max_age = 5 


    def create_image(self):
        self.image = pygame.Surface((20, 20))
        pygame.draw.line(self.image, self.color, (0, 10), (20, 10), 3)
        #pygame.draw.line(self.image, (255,255,255), (2, 10), (18, 10), 1)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.set_angle(self.angle)







class Player(VectorSprite):

    def _overwrite_parameters(self):
        self.stop_on_edge = True
        self.turnspeed = 90 # degrees per second
        self.movespeed = 150 # pixel per second
        self.friction = 0.99
        self.cannon_angle = 0
        self.firespeed = 150
        self.cannon_turn_speed = 90 # degrees per second
        Crosshair(boss=self)

    def turn_left(self, seconds, factor=1):
        degrees = self.turnspeed * factor * seconds
        self.rotate(-degrees)

    def turn_right(self, seconds, factor=1):
        degrees = self.turnspeed * factor * seconds
        self.rotate(degrees)

    def move_forward(self, factor=1):
        self.move = pygame.math.Vector2(self.movespeed * factor, 0)
        self.move.rotate_ip(self.angle)

    def move_backward(self, factor=1):
        """backward goes only half as fast as forward"""
        self.move = pygame.math.Vector2(-self.movespeed/2 * factor, 0)
        self.move.rotate_ip(self.angle)

    def update(self, seconds):
        self.move *= self.friction
        VectorSprite.update(self, seconds)
        #print(self.move, self.angle)

class Crosshair(VectorSprite):

    def _overwrite_parameters(self):
        self.move = pygame.math.Vector2(0,0)
        self.boss_distance = pygame.math.Vector2(85,0)

    def create_image(self):
        self.image = pygame.Surface((30,30))
        pygame.draw.line(self.image, (200,0,0), (0,0), (30,30),1)
        pygame.draw.line(self.image, (200, 0, 0), (30, 0), (0, 30), 1)
        pygame.draw.circle(self.image, (150,0,0), (15,15), 15, 1)
        pygame.draw.circle(self.image, (150, 0, 0), (15, 15), 10, 1)
        pygame.draw.circle(self.image, (150, 0, 0), (15, 15), 5, 1)
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 2, 0)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height


    def update(self, seconds):
        self.boss_distance = pygame.math.Vector2(85, 0)
        self.boss_distance.rotate_ip(self.boss.cannon_angle)
        self.pos = self.boss.pos + self.boss_distance
        VectorSprite.update(self,seconds)






class Viewer():
    width = 0
    height = 0
    allgroup = None # pygame sprite Group for all sprites

    def __init__(self,width=800, height=600 ):
        Viewer.width = width
        Viewer.height = height
        # ---- pygame init
        pygame.init()
        # ------ joysticks init ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.playtime = 0.0
        # ------ background images ------
        self.backgroundfilenames = []  # every .jpg or .jpeg file in the folder 'data'
        self.make_background()
        self.prepare_sprites()
        self.players = []
        # --- create 4 player sprites ---
        corners = [(100,100), (Viewer.width-100,100), (100, Viewer.height-100), (Viewer.width-100, Viewer.height-100)]
        colors = [(0,0,222), (0,222,0), (222,0,0), (222,222,0)]
        for nr in range(4):
              pic = self.create_picture(color=colors[nr])
              startpos = pygame.math.Vector2(corners[nr][0], corners[nr][1])
              self.players.append( Player(pos= startpos, picture=pic, color=colors[nr]))

        self.run()

    def create_picture(self, color=(0,0,255)):
        # create 1 pictures of a spaceship, pointing to right
        pic = pygame.Surface((100,100))
        pygame.draw.polygon(pic, color, [(0,20), (100,50), (0, 80), (30,50)])
        pic.set_colorkey((0,0,0))
        pic.convert_alpha()
        return pic


    def make_background(self):
        """scans the subfolder 'data' for .jpg files, randomly selects
        one of those as background image. If no files are found, makes a
        white screen"""
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:].lower() == ".jpg" or file[-5:].lower() == ".jpeg":
                        self.backgroundfilenames.append(os.path.join(root, file))
            random.shuffle(self.backgroundfilenames)  # remix sort order
            self.background = pygame.image.load(self.backgroundfilenames[0])

        except:
            print("no folder 'data' or no jpg files in it")
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255, 255, 255))  # fill background white

        self.background = pygame.transform.scale(self.background,
                                                 (Viewer.width, Viewer.height))
        self.background.convert()

    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        Viewer.allgroup = pygame.sprite.LayeredUpdates()  # for drawing
        self.playergroup  = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()
        #self.tracergroup = pygame.sprite.Group()
        #self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()

        #Mouse.groups = self.allgroup, self.mousegroup
        Player.groups = self.allgroup, self.playergroup
        Beam.groups = self.allgroup, self.bulletgroup
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup
        #Explosion.groups = self.allgroup, self.explosiongroup


        # ------ player1,2,3: mouse, keyboard, joystick ---


    def run(self):
        """The mainloop"""
        running = True
        #pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright = False, False, False
        pygame.display.set_caption("use joysticks or cursor/pgup/pdwn/space")
        # exittime = 0
        while running:
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.playtime += seconds
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        m = pygame.math.Vector2(self.players[0].firespeed, 0)
                        m.rotate_ip(self.players[0].cannon_angle)
                        m += self.players[0].move
                        p = pygame.math.Vector2(self.players[0].pos.x, self.players[0].pos.y)
                        a = self.players[0].cannon_angle
                        Beam(boss=self.players[0], pos=p, move=m, color=self.players[0].color, angle=a )

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            # if pressed_keys[pygame.K_SPACE]:
            #    pass
            if pressed_keys[pygame.K_RIGHT]:
                self.players[0].turn_right(seconds)
            if pressed_keys[pygame.K_LEFT]:
                self.players[0].turn_left(seconds)
            if pressed_keys[pygame.K_UP]:
                self.players[0].move_forward()
            if pressed_keys[pygame.K_DOWN]:
                self.players[0].move_backward()
            if pressed_keys[pygame.K_PAGEUP]:
                self.players[0].cannon_angle += self.players[0].cannon_turn_speed * seconds
            if pressed_keys[pygame.K_PAGEDOWN]:
                self.players[0].cannon_angle -= self.players[0].cannon_turn_speed * seconds

            # ------ mouse handler ------
            left, middle, right = pygame.mouse.get_pressed()
            # if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
            oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                #if number == 0:
                    x = j.get_axis(0)
                    y = j.get_axis(1)
                    x2 = j.get_axis(2)
                    y2 = j.get_axis(3)
                    buttons = j.get_numbuttons()
                    for b in range(buttons):
                        pushed = j.get_button(b)
                    # ----- control 4 players with 4 joysticks
                    if x < 0:
                        self.players[number].turn_left(seconds, abs(x))
                    if x > 0:
                        self.players[number].turn_right(seconds, abs(x))
                    if y < 0:
                        self.players[number].move_forward(abs(y))
                    if y > 0:
                        self.players[number].move_backward(abs(y))
                    # -- control aiming with second stick of joystick
                    self.players[number].cannon_angle += self.players[number].cannon_turn_speed * seconds * x2



            # permanent fire for all players
            for nr, player in enumerate(self.players):
                m = pygame.math.Vector2(player.firespeed, 0)
                m.rotate_ip(player.cannon_angle)
                m += player.move
                p = pygame.math.Vector2(player.pos.x, player.pos.y)
                a = player.cannon_angle
                Beam(boss=player, pos=p, move=m, color=player.color, angle=a)




            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            # --- order of drawing (back to front) ---

            # write text below sprites
            fps_text = "FPS: {:8.3}".format(self.clock.get_fps())
            write(self.screen, text=fps_text, origin="bottomright", x=Viewer.width - 5, y=Viewer.height - 5,
                  font_size=18, color=(200, 40, 40))

            self.allgroup.update(seconds)

            # --------- collision detection between target and Explosion -----
            # for e in self.explosiongroup:
            #    crashgroup = pygame.sprite.spritecollide(e, self.targetgroup,
            #                 False, pygame.sprite.collide_circle)
            #    for t in crashgroup:
            #        t.hitpoints -= e.damage
            #        if random.random() < 0.5:
            #            Fire(pos = t.pos, max_age=3, bossnumber=t.number)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # -------- next frame -------------
            pygame.display.flip()
        # -----------------------------------------------------
        pygame.mouse.set_visible(True)
        pygame.quit()


if __name__ == '__main__':
    Viewer(width=1024, height=800)
