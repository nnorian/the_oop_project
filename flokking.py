import simplegui
import random
import math

CANVAS_RES = (840, 460)
C_WIDTH = CANVAS_RES[0]
C_HEIGHT = CANVAS_RES[1]
DIMENSIONS = 2
BOID_SHAPE = [(0, -5), (-5, 0), (5, 0)]
BOID_RADIUS = 5
SHIP_SHAPE = [(0, -10), (-10, 0), (0, 10), (10, 0)]
SHIP_RADIUS = 10
BOID_PERCEPTION = 65
BOID_COHESION_PERCEPTION = 10
BOID_SEPARATION_PERCEPTION = 40
BOID_MAX_FORCE = 0.8
BOID_MAX_SPEED = 1
BOID_RAGE = 2.5 # magnitude of the boid launging at the ship
BOID_NUMBER = 25
SHIP_PRESENCE_FACTOR = 5



const_friction = .04
const_thrust   = .1
const_rotation = .1
const_missile  = 5

playing = False
lives = 2

# Setting volume

class SpaceObject:
    def __init__(self):
        self.position = Vector(0, 0)
        
    def draw(self, canvas):
        pass
    
    def update(self):
        pass
    
    def get_pos(self):
        return self.position
    
    def collided(self, other_object):
        """
        Method that takes as imput a sprite and another object (e.g. the ship, a sprite)
        and returns True if they collide, else False
        """
        distance = self.position.distance(other_object.position)
        sum_radii = self.radius + other_object.radius
        
        if distance < sum_radii:
            return True
        else:
            return False

class Boid(SpaceObject):
    def __init__(self):
        # Add random spawn
        self.position = Vector(
            random.randint(0, C_WIDTH), 
            random.randint(0, C_HEIGHT)
        )
        self.radius = BOID_RADIUS
        # Add initial random velocity
        self.velocity = Vector.random_2Dvector(-4, 4)
        self.acceleration = Vector(0, 0)
        self.is_aggressive = random.randint(1, 10) == 1
        self.color = "White"
        if self.is_aggressive:
            self.color = "Red"
    
    def draw(self, canvas):
        # Use of the vector function 
        # to sculpt a boid in it's shape
        canvas.draw_polygon([
            (self.position + BOID_SHAPE[0]),
            (self.position + BOID_SHAPE[1]),
            (self.position + BOID_SHAPE[2])       
        ], 1, self.color)
        
        OFFSET = 8
        angle = math.atan2(self.velocity[0], self.velocity[1])
        x_rot = self.position[0] + OFFSET*math.cos(angle)
        y_rot = self.position[1] + OFFSET*math.sin(angle)
        
        canvas.draw_circle(
            [x_rot, y_rot],
            1,
            1,
            self.color
        )
        
    def update(self):
        self.velocity.limit(BOID_MAX_SPEED)
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.bound()
    
    def flocking(self, boids):
        self.acceleration = Vector(0, 0)
        self.acceleration = self.acceleration + self.calculate_steering(boids)
    
    def calculate_steering(self, boids):
        separation = Vector(0, 0)
        alignment = Vector(0, 0)
        cohesion = Vector(0, 0)
        separation_total = 0
        alignment_total = 0
        cohesion_total = 0
        
        ship_proximity_sep = Vector(0, 0)
       
        for boid in boids:
            
            distance = self.position.distance(boid.position)
            if distance < BOID_SEPARATION_PERCEPTION and boid != self:
                if not(self.is_aggressive and type(boid) is Ship):
                    difference = self.position - boid.position
                    difference = difference / distance
                    separation = separation + difference
                    separation_total = separation_total + 1
            
            if type(boid) is Ship and distance < BOID_SEPARATION_PERCEPTION:
                if not(self.is_aggressive and type(boid) is Ship):
                    difference = self.position - boid.position
                    difference = difference / distance
                    ship_proximity_sep = (separation + difference) * SHIP_PRESENCE_FACTOR

            if distance < BOID_COHESION_PERCEPTION and boid != self and type(boid) is not Ship:
                cohesion = cohesion + boid.position
                cohesion_total = cohesion_total + 1

            if distance < BOID_PERCEPTION and boid != self and type(boid) is not Ship:
                alignment = alignment + boid.velocity
                alignment_total = alignment_total + 1

        if separation_total > 0:
            separation = separation / separation_total
            separation.set_magnitude(BOID_MAX_SPEED)
            separation = separation - self.velocity
            separation.limit(BOID_MAX_FORCE)

        if alignment_total > 0:
            alignment = alignment / alignment_total
            alignment.set_magnitude(BOID_MAX_SPEED)
            alignment = alignment - self.velocity
            alignment.limit(BOID_MAX_FORCE)

        if cohesion_total > 0:
            cohesion = cohesion / cohesion_total
            cohesion = cohesion - self.position
            cohesion.set_magnitude(BOID_MAX_SPEED)
            cohesion = cohesion - self.velocity
            cohesion.limit(BOID_MAX_FORCE)


        return separation + alignment + cohesion + ship_proximity_sep
        
    def cohesion(self, boids):
        steering = Vector(0, 0)
        total = 0
        
        for boid in boids:
            distance = self.position.distance(boid.position)
            if distance < BOID_COHESION_PERCEPTION and boid != self:
                steering = steering + boid.position
                total = total + 1
        
        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.set_magnitude(BOID_MAX_SPEED)
            steering = steering - self.velocity
            steering.limit(BOID_MAX_FORCE)
        
        return steering
    
    def align(self, boids):
        steering = Vector(0, 0)
        total = 0
        
        for boid in boids:
            distance = self.position.distance(boid.position)
            if distance < BOID_PERCEPTION and boid != self:
                steering = steering + boid.velocity
                total = total + 1
        
        if total > 0:
            steering = steering / total
            steering.set_magnitude(BOID_MAX_SPEED)
            steering = steering - self.velocity
            steering.limit(BOID_MAX_FORCE)
        
        return steering
    
    def separation(self, boids):
        steering = Vector(0, 0)
        total = 0
        
        for boid in boids:
            distance = self.position.distance(boid.position)
            if (distance < BOID_SEPARATION_PERCEPTION and boid != self):
                difference = self.position - boid.position
                difference = difference / distance
                steering = steering + difference
                total = total + 1
        
        if(total > 0):
            steering = steering / total
            steering.set_magnitude(BOID_MAX_SPEED)
            steering = steering - self.velocity
            steering.limit(BOID_MAX_FORCE)
        
        return steering
        
    def bound(self):
        if (self.position[0] > C_WIDTH):
            self.position = Vector(0, self.position[1])
        elif (self.position[0] < 0):
            self.position = Vector(C_WIDTH, self.position[1])
        elif (self.position[1] > C_HEIGHT):
            self.position = Vector(self.position[0], 0)
        elif (self.position[1] < 0):
            self.position = Vector(self.position[0], C_HEIGHT)

class Ship(SpaceObject):
    def __init__(self):
        self.position = Vector(C_WIDTH/2, C_HEIGHT/2)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.color = "Purple"
        
        self.thrust = False
        self.angle = -math.pi/2
        self.angle_vel = 0
        self.radius = SHIP_RADIUS
        
        self.x_rot_turret = 0
        self.y_rot_turret = 0
        
    def draw(self, canvas):
        canvas.draw_polygon([
            (self.position + SHIP_SHAPE[0]),
            (self.position + SHIP_SHAPE[1]),
            (self.position + SHIP_SHAPE[2]),
            (self.position + SHIP_SHAPE[3])            
        ], 1, self.color)
        
        OFFSET = 15
        self.x_rot_turret = self.position[0] + OFFSET*math.cos(self.angle)
        self.y_rot_turret = self.position[1] + OFFSET*math.sin(self.angle)
        
        canvas.draw_circle(
            [self.x_rot_turret, self.y_rot_turret],
            2,
            1,
            self.color
        )
        
    def update(self):
        forward_vector = Vector.angle_to_vector(self.angle)
        self.bound()
        self.position = self.position + self.velocity
        self.velocity = self.velocity * (1 - const_friction)
        
        if(self.thrust and self.velocity.norm() < 6):
            self.velocity = self.velocity + forward_vector
        
        self.angle += self.angle_vel
    
    def turn(self, turn):
        self.angle_vel = const_rotation * turn
        
    def accelerate(self, thrust_on):
        if (thrust_on > 0):
            self.thrust = True
            #ship_thrust_sound.rewind()
            #ship_thrust_sound.play()
        else:
            self.thrust = False
            #ship_thrust_sound.pause()
 
    def fire(self, shoot):
        newvel = Vector(0, 0)
        
        if (shoot > 0 and len(missile_group) < 3):
            forward_vector = Vector.angle_to_vector(self.angle)
            newvel = self.velocity + forward_vector * const_missile
            missl = Missle(
                Vector(self.x_rot_turret, self.y_rot_turret), # position
                newvel)
        
            missile_group.add(missl)
            
    def bound(self):
        if (self.position[0] > C_WIDTH):
            self.position = Vector(0, self.position[1])
        elif (self.position[0] < 0):
            self.position = Vector(C_WIDTH, self.position[1])
        elif (self.position[1] > C_HEIGHT):
            self.position = Vector(self.position[0], 0)
        elif (self.position[1] < 0):
            self.position = Vector(self.position[0], C_HEIGHT)

class Missle(SpaceObject):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.color = "Purple"
        self.radius = 3
        
    def draw(self, canvas):
        canvas.draw_circle(
            [self.position[0], self.position[1]],
            1,
            1,
            self.color
        )  
    
    def update(self):
        if self.exited():
            dead_missiles.add(self)
        self.position = self.position + self.velocity
        
    def exited(self):
        return (self.position[0] > C_WIDTH) or (self.position[0] < 0) or (self.position[1] > C_HEIGHT) or (self.position[1] < 0)
 
class Vector:
    def __init__(self, *components):
        self.components = components

    def __repr__(self):
        return "Vector{}".format(self.components)

    def __len__(self):
        return len(self.components)

    def __getitem__(self, index):
        return self.components[index]
    
    def norm(self):
        return math.sqrt(sum([component**2 for component in self.components]))

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors should have the same length")
        return Vector(*[self[i] + other[i] for i in range(len(self))])

    def __sub__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors should have the same lengthd")
        return Vector(*[self[i] - other[i] for i in range(len(self))])

    def __mul__(self, scalar):
        return Vector(*[component * scalar for component in self.components])

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("division by zero")
        return Vector(*[component / scalar for component in self.components])
    
    def dot_product(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors should have the same length")
        return sum([self[i] * other[i] for i in range(len(self))])

    def cross_product(self, other):
        if len(self) != 3 or len(other) != 3:
            raise ValueError("cross product is possible only for 3D Vector")
        return Vector(self[1] * other[2] - self[2] * other[1],
                      self[2] * other[0] - self[0] * other[2],
                      self[0] * other[1] - self[1] * other[0])
    
    # Vector class
    def random_2Dvector(lower_bound, upper_bound):
        return Vector(
            random.uniform(lower_bound, upper_bound), 
            random.uniform(lower_bound, upper_bound)
        )
    
    def distance(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors should have same length")
        
        return math.sqrt(sum([(self[i] - other[i])**2 for i in range(len(self))]))
    
    def set_magnitude(self, magnitude):
        norm = self.norm()
        if norm == 0:
            self.components = [magnitude] * len(self.components)
        else:
            self.components = [component * magnitude / norm for component in self.components]
    
    def limit(self, mag_limit):
        magnitude = self.norm()
        if magnitude > mag_limit:
            self = (self / magnitude) * mag_limit

    def angle_to_vector(ang):
        return Vector(math.cos(ang), math.sin(ang))
    
    def rotate(line, angle):
        degree = angle * 180/math.pi
        return Vector(
            math.cos(degree) - math.sin(degree),
            math.sin(degree) + math.cos(degree)
        )

def keydown(key):
    for i in inputs: # sugested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](inputs[i][1])
            
def keyup(key): 
    for i in inputs: # sugested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](0)

def group_collide(sprite_group, other_object):
    global lives, boids_destroyed, aggressive_boids, score
    """
    Function takes a group of sprites and another object (e.g. the ship, a sprite) 
    and if these two collided makes an explosion, returning True; else False
    """
    remove_sprites = set([])
    
    if(type(other_object) is Ship):
        for sprite in sprite_group:
            if sprite.collided(other_object) and sprite.is_aggressive:
                remove_sprites.add(sprite)
                lives -= 1
                score += .5
                aggressive_boids -= 1
                
    elif(type(other_object) is Missle):
        for sprite in sprite_group:
            if sprite.collided(other_object):
                remove_sprites.add(sprite)
                if sprite.is_aggressive:
                    aggressive_boids -= 1
                    print(score)
                    score += 1
                else:
                    boids_destroyed += 1
    
    if len(remove_sprites): # if something collided..
        sprite_group.difference_update(remove_sprites)
        return True
    
    else: # if not..
        return False

def process_sprite_group(sprite_group, canvas):
    """Function to draw sprites on canvas, update them and delete those who became old"""
    remove_sprites = set([])
    
    for sprite in sprite_group:
        sprite.draw(canvas)
        
        if sprite.update(): # update returns True if the sprite became old, else False
            remove_sprites.add(sprite)
            
    if len(remove_sprites): # if something needs to be deleted..
        sprite_group.difference_update(remove_sprites)


# Handler to draw on canvas
def draw(canvas):
    global aggressive_boids
    if playing:
        if aggressive_boids == 0:
            canvas.draw_text("WON", [C_WIDTH/2 - 200, C_HEIGHT/2], 15, "Blue", "monospace")
            win_text = "Bad boids: " + str(score) + " Good boids: " + str(boids_destroyed)
            canvas.draw_text(win_text, [C_WIDTH/2 - 200, C_HEIGHT/2 + 20], 15, "Blue", "monospace")
        elif lives > 0:
            # Drawing boids
            space_objects = {ship} | flock 
            for boid in flock:
                boid.flocking(space_objects)
                boid.update()
                boid.draw(canvas)

            if group_collide(flock, ship):
                print("ouch")

            ship.update()
            ship.draw(canvas)

            for missl in missile_group:
                missl.draw(canvas)
                missl.update()
                if group_collide(flock, missl):
                    print("Boid destroyed")

            missile_group.difference_update(dead_missiles)

            canvas.draw_text("Bad boids:", [12, 36], 15, "White", "monospace")
            canvas.draw_text(str(aggressive_boids), [100, 36], 15, "White", "monospace")
            canvas.draw_text("Lives    :", [12, 36+20], 15, "White", "monospace")
            canvas.draw_text(str(lives), [100, 36+20], 15, "White", "monospace")
        elif lives == 0:
            canvas.draw_text("CRASHED", [C_WIDTH/2 - 200, C_HEIGHT/2], 15, "Red", "monospace")
    else:
        canvas.draw_text("Welcome!", [50, C_HEIGHT/2 - 50], 15, "Blue", "monospace")
        canvas.draw_text("This is a flocking simulator mimicking the behavior of Solanum tuberosum with boids", [50, C_HEIGHT/2 - 20], 15, "Blue", "monospace")
        canvas.draw_text("Red Boid - aggressive, won't steer away, does damage", [50, C_HEIGHT/2], 15, "Blue", "monospace")
        canvas.draw_text("White Boid - non-agressive, will steer away, does no damage", [50, C_HEIGHT/2 + 20], 15, "Blue", "monospace")
        canvas.draw_text("Your mission: destroy all red boids, minimal casualties to white boids, prefferably non at all", [50, C_HEIGHT/2 + 40], 15, "Blue", "monospace")
        canvas.draw_text("Good luck!", [50, C_HEIGHT/2 + 70], 15, "Blue", "monospace")
        
        canvas.draw_text("Red boid: 1 point", [50, C_HEIGHT/2 + 120], 12, "Blue", "monospace")
        canvas.draw_text("White boid: 0 point", [50, C_HEIGHT/2 + 135], 12, "Blue", "monospace")
        canvas.draw_text("Collide Red boid: .5 point", [50, C_HEIGHT/2 + 150], 12, "Blue", "monospace")
    canvas


def click(pos):
    global playing
    playing = True

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Flokk", CANVAS_RES[0], CANVAS_RES[1])
frame.set_draw_handler(draw)
# Gray better for the eyes
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_canvas_background("Gray")
frame.set_mouseclick_handler(click)

    
# Instantiate flock
flock = set([])
missile_group = set([])
dead_missiles = set([])
aggressive_boids = 0;
score = 0;
boids_destroyed = 0;
for x in range(BOID_NUMBER):
    boid = Boid()
    if boid.is_aggressive:
        aggressive_boids += 1
    flock.add(boid)

ship = Ship()
    
inputs = {"left":  (ship.turn,      -1),
          "right": (ship.turn,       1),
          "up":    (ship.accelerate, 1),
          "space": (ship.fire,       1)} 

# Start the frame animation
frame.start()
