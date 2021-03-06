"""2d vector game in pure python3 / pygame, no external files necessary.
   create beautiful patterns by steering your spaceships with keyboard or
   joysticks (joysticks recommended. 4 players maximum"""

import pygame
import random

# patterns for player spaceship

def create_picture(color=(0, 0, 255), size=35):
    # create 1 pictures of a spaceship, pointing to right
    pic = pygame.Surface((size, size))
    pygame.draw.polygon(pic, color, [(0, 0), (size, size // 2), (0, size), (size // 3, size // 2)])
    pic.set_colorkey((0, 0, 0))
    pic.convert_alpha()
    return pic

def validcolor(colorvalue):
    """makes sure a value remains between 0 and 255"""
    return 0 if colorvalue < 0 else 255 if colorvalue > 255 else colorvalue

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
        try:
            mytext = pygame.transform.scale(mytext, grid_size)
        except:
            raise ValueError("grid size must be tuple of positive integers")
        mytext = mytext.convert_alpha()  # pygame surface, use for blitting
        return mytext, (grid_size[0], grid_size[1])

    return mytext, (size_x, size_y)


def write(background, text, x=50, y=150, color=(0, 0, 0),
          font_size=None, font_name="mono", bold=True, origin="topleft"):
    """blit text on a given pygame surface (given as 'background')
       the origin is the alignment of the text surface
       origin can be 'center', 'centercenter', 'topleft', 'topcenter', 'topright', 'centerleft', 'centerright',
       'bottomleft', 'bottomcenter', 'bottomright'
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


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    #numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
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
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
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


        if "stop_on_edge" not in kwargs:
            self.stop_on_edge = False
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False
        if "age" not in kwargs:
            self.age = 0  # age in seconds. A negative age means waiting time until sprite appears
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


    def kill(self):
        # check if this is a boss and kill all his underlings as well
        tokill = []
        for s in Viewer.allgroup:
            if "boss" in s.__dict__:
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
        self.age += seconds
        if self.age < 0:
            return
        self.distance_traveled += self.move.length() * seconds
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
             self.wallcheck()
        self.rect.center = ( round(self.pos.x, 0), round(self.pos.y, 0) )

    def wallcheck(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.stop_on_edge:
                self.pos.x = 0
            if self.kill_on_edge:
                self.kill()
            if self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            if self.warp_on_edge:
                self.pos.x = Viewer.width
        # -------- upper edge -----
        # hud on top screen edge = 20 pixel = Viewer.hud_height
        if self.pos.y  < Viewer.hud_height:
            if self.stop_on_edge:
                self.pos.y = Viewer.hud_height
            if self.kill_on_edge:
                self.kill()
            if self.bounce_on_edge:
                self.pos.y = Viewer.hud_height
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


class Flytext(VectorSprite):
    """a text flying for a short time around, like hitpoints lost message"""
    def __init__(self, pos=pygame.math.Vector2(50,50), move=pygame.math.Vector2(0,-50),
                  text="hallo", color=(255, 0, 0), max_age=2, age=0,
                 acceleration_factor = 1.0,  fontsize=22,):
        """a text flying upward and for a short time and disappearing"""
        VectorSprite.__init__(self, pos=pos, move=move, text=text, color=color,
                              max_age=max_age, age=age, acceleration_factor=acceleration_factor,
                              fontsize=fontsize)
        self._layer = 7  # order of sprite layers (before / behind other sprites)

        #acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.

    def create_image(self):
        self.image = make_text(self.text, (self.color), self.fontsize)[0]  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (-400,-400) # if you leave this out the Flytext is stuck in the left upper corner at 0,0


        #self.rect.center = (self.pos.x, self.pos.y)

    def update(self, seconds):
        self.move *= self.acceleration_factor
        VectorSprite.update(self, seconds)

class Bubble(VectorSprite):
    """a round fragment or bubble particle"""


    def _overwrite_parameters(self):
        self.speed = random.randint(10,50)
        self.max_age = 2+random.random()*2.4
        self.kill_on_edge = True
        self.kill_with_boss = False # VERY IMPORTANT!!!
        if self.boss and self.move == pygame.math.Vector2(0,0):
            self.move = pygame.math.Vector2(self.boss.move.x, self.boss.move.y)
            self.move.normalize_ip()
            self.move *= self.speed
            a, b = 160, 200
        else:
            a, b = 0, 360
            self.move = pygame.math.Vector2(self.speed, 0)
        self.move.rotate_ip(random.randint(a,b))
        print("ich bin da", self.pos, self.move)


    def create_image(self):
        self.radius = random.randint(1,5)
        self.image = pygame.Surface((2*self.radius, 2*self.radius))
        r,g,b = self.color
        r+= random.randint(-30,30)
        g+= random.randint(-30,30)
        b+= random.randint(-30,30)
        r = validcolor(r)
        g = validcolor(g)
        b = validcolor(b)
        self.color = (r,g,b)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius )
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()



class Beam(VectorSprite):
    """laser-beam, need color, pos, move and angle """

    def _overwrite_parameters(self):
        self.kill_on_edge = True
        self._layer = 7
        self.max_age = 5
        self.max_distance = 400
        self.damage = 1
        self.radius = 5
        self.hitpoints = 1


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

    aimings = ["free", "forward", "fixed", "locked"]

    def _overwrite_parameters(self):
        self.hitpoints = 100
        self.hitpointsfull = 100
        self.stop_on_edge = True
        self.turnspeed = 90 # degrees per second
        self.movespeed = 100 # pixel per second
        self.friction = 0.999
        self.cannon_angle = 0
        self.firespeed = 150
        self.radius = 17
        #if self.number == 0:
        #    self.aiming = "locked"
        #    self.victim_number = 1
        #else:
        #self.victim = None
        #self.valid_targets()
        self.aiming = "free"  #
        self.target = "nearest"
        self.reload_time = 0.15 # minimal time between 2 shots
        #self.last_button1 = 0
        #self.button1_wait = 0.35
        self.last_shot = 0 # time of last shot
        self.cannon_turn_speed = 150 # degrees per second

        Crosshair(boss=self)

    def switch_target(self):
        if self.hitpoints <= 0:
            return
        """select the next target out of the self.targets list
        that looks like ['nearest', 'green', 'red', 'yellow']"""

        if self.target not in self.targets:
            self.target = self.targets[0]
            return
        i = self.targets.index(self.target)
        if i == len(self.targets)-1:
            self.target = self.targets[0]
        else:
            self.target = self.targets[i+1]
        #print("target is now:", self.target)


    def switch_aiming(self):
        if self.hitpoints <= 0:
            return
        """change the aimingmode to the next string in self.aimings
           aimings = ["free", "forward", "fixed", "locked"] """
        i = self.aimings.index(self.aiming)
        if i == len(self.aimings) -1:
            self.aiming = self.aimings[0]
        else:
            self.aiming = self.aimings[i+1]

        # instantly re-aim when set to 'forward', don't wait for turn:
        if self.aiming == "forward":
            self.cannon_angle = self.angle


    def fire(self):
        if self.hitpoints <= 0:
            return
        if self.age < (self.last_shot + self.reload_time):
            return # gun is too hot now, wait for cooldown
        self.last_shot = self.age
        m = pygame.math.Vector2(self.firespeed, 0)
        m.rotate_ip(self.cannon_angle)
        #m += self.move
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        a = self.cannon_angle
        Beam(boss=self, pos=p, move=m, color=self.color, angle=a)

    def aim(self, seconds, factor):
        """turn the cannon/crosshair, depending on aiming mode"""
        if self.hitpoints <= 0:
            return
        if self.aiming == "free" or self.aiming == "fixed":
            self.cannon_angle += self.cannon_turn_speed * factor * seconds

    def turn_left(self, seconds, factor=1):
        self.turn(seconds, factor, -1)


    def turn_right(self, seconds, factor=1):
        self.turn(seconds, factor, 1)

    def turn(self, seconds, factor, clockwise=1 ):
        """clockwise can be 1 or -1 (=counter-clockwise)"""
        if self.hitpoints <= 0:
            return
        degrees = self.turnspeed * factor * seconds * clockwise
        self.rotate(degrees)
        # rotate the crosshair as well?
        if self.aiming == "free":
            return
        elif self.aiming == "forward":
            self.cannon_angle = self.angle
        elif self.aiming == "fixed":
            self.cannon_angle += degrees

    def move_forward(self, factor=1):
        if self.hitpoints <= 0:
            return
        m = pygame.math.Vector2(self.movespeed * factor, 0)
        m.rotate_ip(self.angle)
        #self.move += m
        self.move = m

    def move_backward(self, factor=1):
        if self.hitpoints <= 0:
            return
        """backward goes only half as fast as forward"""
        m = pygame.math.Vector2(-self.movespeed/2 * factor, 0)
        m.rotate_ip(self.angle)
        #self.move += m
        self.move = m

    def aim_at_player(self, colorstring=None):
        """aims at player whose name matches the colorstring,
           or 'nearest'
           like: 'blue', 'yellow', 'red', 'green'"""
        if self.hitpoints <= 0:
            return
        if colorstring is None:
            return
        if colorstring == "nearest":
            best = self.get_closest_player()
        else:
            best = [p for p in Viewer.playergroup if p.name == colorstring][0]
        v = best.pos - self.pos
        a = -v.angle_to(pygame.math.Vector2(1, 0))
        self.cannon_angle = a

    def get_closest_player(self):
        best_distance = None
        # best = None
        for p in Viewer.playergroup:
            if p == self:
                continue
            dist = (p.pos - self.pos).length()
            if best_distance is None or best_distance > dist:
                best_distance = dist
                best = p
        return best

    def valid_targets(self):
        """list of valid target names. """
        self.targets = ["nearest"]
        for p in Viewer.playergroup:
            if p.hitpoints > 0 and p != self:
                self.targets.append(p.name)
        #print("targets aquired for {}: {}".format(self.name, self.targets))


    def kill(self):
        # remove own name from Player.targets and update all players
        for p in Viewer.playergroup:
            p.valid_targets()
        Flytext(pos=pygame.math.Vector2(self.pos.x, self.pos.y), text="Game over for {} player ".format(self.name),
                color=self.color, max_age=1  )
        ## don't kill because this would mess up joystick control.
        ## instead, just move the dead player out of the screen
        self.stop_on_edge = False
        self.pos = pygame.math.Vector2(-200,-200)
        self.move = pygame.math.Vector2(0,0)
        #self.rect.center = (round(self.pos.x, 0), round(self.pos.y, 0))
        ##VectorSprite.kill(self)
        survivors = [p for p in Viewer.playergroup if p.hitpoints > 0]
        if len(survivors) == 1:
            Flytext(pos=pygame.math.Vector2(Viewer.width//2, Viewer.height -50), color=survivors[0].color,
                    max_age=10, fontsize=33, text="Victory for {} player!".format(survivors[0].name))
            Flytext(pos=pygame.math.Vector2(Viewer.width, 100), text="press r to restart the game",
                    move=pygame.math.Vector2(-5,0), max_age=30)

    # DONE : aiming update when one player is killed
    # DONE: aimingmode reducing when less then 4 players alive
    def update(self, seconds):
        #if self.hitpoints <= 0:
        #    return
        self.move *= self.friction
        if self.aiming == "locked":
            self.aim_at_player(self.target)

        VectorSprite.update(self, seconds)
        #print(self.move, self.angle)

class Crosshair(VectorSprite):

    def _overwrite_parameters(self):
        self.move = pygame.math.Vector2(0,0)
        self.boss_distance = pygame.math.Vector2(85,0)

    def create_image(self):
        self.image = pygame.Surface((30,30))
        pygame.draw.line(self.image, self.boss.color, (0,0), (30,30),1)
        pygame.draw.line(self.image, self.boss.color, (30, 0), (0, 30), 1)
        pygame.draw.circle(self.image, (10,10,10), (15,15), 15, 1)
        pygame.draw.circle(self.image, self.boss.color, (15, 15), 10, 1)
        pygame.draw.circle(self.image, (10, 10, 10), (15, 15), 5, 1)
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 2, 0)  # black -> transparent. makes a hole
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
    hud_height = 20 # height of hud on top of screen, for displaying hitpoints etc
    allgroup = None # pygame sprite Group for all sprites
    playergroup = None # pygame sprite Group only for players
    players = []

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
        #Viewer.players = []
        # --- create 4 player sprites. They will automatically be members of Viewer.playergroup ---
        self.corners = [(100,100), (Viewer.width-100,100), (100, Viewer.height-100), (Viewer.width-100, Viewer.height-100)]
        colors =  [(128,128,255), (0,255,0),              (255,0,0),                (255,255,0)]
        names =   ["blue",    "green",                "red",                    "yellow"]
        for nr in range(4):
              pic = create_picture(color=colors[nr])
              startpos = pygame.math.Vector2(self.corners[nr][0], self.corners[nr][1])
              Player(playernumber = nr, pos= startpos, picture=pic, color=colors[nr], name=names[nr])

        for p in Viewer.playergroup:
            p.valid_targets()
        self.run()


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
        Viewer.allgroup = pygame.sprite.LayeredUpdates()  # for drawing with layers
        Viewer.playergroup  = pygame.sprite.OrderedUpdates() # a group maintaining order in list
        self.bulletgroup = pygame.sprite.Group() # simple group for collision testing only
        #self.tracergroup = pygame.sprite.Group()
        #self.mousegroup = pygame.sprite.Group()
        self.explosiongroup = pygame.sprite.Group()

        #Mouse.groups = self.allgroup, self.mousegroup
        Player.groups = self.allgroup, self.playergroup
        Beam.groups = self.allgroup, self.bulletgroup
        VectorSprite.groups = self.allgroup
        Bubble.groups = self.allgroup
        #Flytext.groups = self.allgroup
        #Explosion.groups = self.allgroup, self.explosiongroup


        # ------ player1,2,3: mouse, keyboard, joystick ---

    def hud(self):
        """make a Head Up Display on the top of the screen with bars for player hitpoints"""
        y = Viewer.hud_height
        for nr, p in enumerate(self.playergroup):
            percent = p.hitpoints / p.hitpointsfull
            length = Viewer.width // 4
            pygame.draw.rect(self.screen, p.color, (nr * length +1 , 1 , int(length * percent)-2, y-1), 0) # fill
            pygame.draw.rect(self.screen, (0, 0, 0), (nr * length, 0, length, y), 1)  # black border
            if p.hitpoints <= 0:
                t = "Game Over"
            else:
                t = p.aiming + ("  (" if p.aiming != "locked" else " --> ") + p.target + (")" if p.aiming != "locked" else "")
            write(background=self.screen, text=t, x= nr*length + 50, y=5,
                  color=(0,0,0), bold=True, font_size=10)

    def run(self):
        """The mainloop"""
        running = True
        #pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright = False, False, False
        pygame.display.set_caption("use 4 joysticks for 4 players.Change aimingmode and target with buttons")
        Flytext(pos=pygame.math.Vector2(Viewer.width//2,Viewer.height//2), text="player 1 keys: cursor, home/end, pgup/pgdown")
        while running:
            #print(self.playergroup[0].pos, self.playergroup[0].cannon_angle)
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
                    #if event.key == pygame.K_SPACE:
                    #  self.playergroup[0].fire()
                    # ---- for player1 ---
                    if event.key == pygame.K_HOME:
                        self.playergroup.sprites()[0].switch_aiming()
                    if event.key == pygame.K_END:
                        self.playergroup.sprites()[0].switch_target()
                    #--test
                    if event.key == pygame.K_x:
                        Bubble(pos=pygame.math.Vector2(400,200))
                    # ---- restart and reset all players -----
                    if event.key == pygame.K_r:
                        #for nr, p in enumerate(Viewer.playergroup.sprites()):
                        for nr, p in enumerate(Viewer.playergroup):
                            p.hitpoints = p.hitpointsfull
                            p.set_angle(0)
                            p.cannon_angle = 0
                            p.aiming = "free"
                            p.target = "nearest"
                            p.move = pygame.math.Vector2(0,0)
                            p.stop_on_edge = True
                            p.pos = pygame.math.Vector2(self.corners[nr][0],self.corners[nr][1])

                # --- joy button up --
                elif event.type == pygame.JOYBUTTONUP:
                    #print(event) <Event(11-JoyButtonUp {'joy': 0, 'button': 0})>
                    #switch aiming mode of player of that joystick if first button was released
                    if event.button == 0 or event.button == 6:
                        self.playergroup.sprites()[event.joy].switch_aiming()
                    if event.button == 1 or event.button == 7:
                        self.playergroup.sprites()[event.joy].switch_target()

                #elif event.type == pygame.JOYBUTTONDOWN:

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_RIGHT]:
                self.playergroup.sprites()[0].turn_right(seconds)
                # self.playergroup.sprites()[0] is player1
            if pressed_keys[pygame.K_LEFT]:
                self.playergroup.sprites()[0].turn_left(seconds)
            if pressed_keys[pygame.K_UP]:
                self.playergroup.sprites()[0].move_forward()
            if pressed_keys[pygame.K_DOWN]:
                self.playergroup.sprites()[0].move_backward()
            if pressed_keys[pygame.K_PAGEUP]:
                self.playergroup.sprites()[0].cannon_angle += self.playergroup.sprites()[0].cannon_turn_speed * seconds
            if pressed_keys[pygame.K_PAGEDOWN]:
                self.playergroup.sprites()[0].cannon_angle -= self.playergroup.sprites()[0].cannon_turn_speed * seconds


            # ------ mouse handler ------
            left, middle, right = pygame.mouse.get_pressed()
            # if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
            oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                #if number == 0:
                    x1 = j.get_axis(0)
                    #y1 = j.get_axis(1)
                    #x2 = j.get_axis(2)
                    y2 = j.get_axis(3)
                    #x3, y3 = j.get_hat(0) # get  hat movement

                    buttons = j.get_numbuttons()
                    for b in range(buttons):
                        pushed = j.get_button(b)
                        # rotate cannon/crosshair while buttons are pressed down
                        # (for single button press (and relase), use events
                        if pushed and (b == 4 or b == 3):
                            self.playergroup.sprites()[number].aim(seconds, -1)
                        if pushed and (b == 5 or b== 2):
                            self.playergroup.sprites()[number].aim(seconds, 1)
                        #    self.playergroup[number].switch_aiming()

                    # ----- control 4 players with 4 joysticks
                    if x1 < 0:
                        self.playergroup.sprites()[number].turn_left(seconds, abs(x1))
                    if x1 > 0:
                        self.playergroup.sprites()[number].turn_right(seconds, abs(x1))
                    if y2 < 0:
                        self.playergroup.sprites()[number].move_forward(abs(y2))
                    if y2 > 0:
                        self.playergroup.sprites()[number].move_backward(abs(y2))
                    # -- control aiming with second stick of joystick

            # permanent fire for all players
            for p in self.playergroup:
                p.fire()

            # -------------------------delete everything on screen--------------------------------------
            self.screen.blit(self.background, (0, 0))

            # ---- update -----------------
            self.allgroup.update(seconds)

            # --------- collision detection between Player and Beam -----
            for player  in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(player, self.bulletgroup,
                             False, pygame.sprite.collide_circle) # need 'radius' attribute for both sprites
                for beam in crashgroup:
                    if beam.boss == player:
                        continue
                    player.hitpoints -= beam.damage
                    # explosion with bubbels
                    if random.random() < 0.85:
                        v = pygame.math.Vector2(beam.move.x, beam.move.y)
                        v.normalize_ip()
                        v *= random.randint(60,160) # speed
                        v.rotate_ip(beam.angle + 180 + random.randint(-20,20))
                        Bubble(pos=pygame.math.Vector2(beam.pos.x, beam.pos.y), color=beam.color,
                               move=v)
                    beam.kill()
                    #beam.hitpoints = 0 # kill later
            # ----------- draw  -----------------
            self.allgroup.draw(self.screen)
            # write text below sprites
            fps_text = "FPS: {:8.3}".format(self.clock.get_fps())
            write(self.screen, text=fps_text, origin="bottomright", x=Viewer.width - 5, y=Viewer.height - 5,
                  font_size=18, color=(200, 40, 40))
            # ----- hud ----
            self.hud()
            # -------- next frame -------------
            pygame.display.flip()
        # -----------------------------------------------------
        pygame.mouse.set_visible(True)
        pygame.quit()


if __name__ == '__main__':
    Viewer(width=1024, height=800)
