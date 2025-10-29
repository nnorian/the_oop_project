import simplegui
import random
import math

# Canvas and game world settings
CANVAS_RES = (840, 460)
C_WIDTH = CANVAS_RES[0]
C_HEIGHT = CANVAS_RES[1]

# Visual shapes for entities
BOID_SHAPE = [(0, -5), (-5, 0), (5, 0)]
BOID_RADIUS = 5
SHIP_SHAPE = [(0, -10), (-10, 0), (0, 10), (10, 0)]
SHIP_RADIUS = 10

# Boid flocking behavior parameters
BOID_PERCEPTION = 65
BOID_COHESION_PERCEPTION = 10
BOID_SEPARATION_PERCEPTION = 40
BOID_MAX_FORCE = 0.8
BOID_MAX_SPEED = 1
BOID_NUMBER = 25
SHIP_PRESENCE_FACTOR = 5

# Ship movement parameters
SHIP_FRICTION = 0.04
SHIP_ROTATION = 0.1
SHIP_MAX_SPEED = 6
MISSILE_SPEED = 5
MAX_MISSILES = 3

# Game configuration
STARTING_LIVES = 2
AGGRESSIVE_SPAWN_CHANCE = 0.1


class Vector:
    # Basic vector class for handling 2D math operations
    
    def __init__(self, *components):
        # Store vector components as a tuple so they can't be accidentally modified
        self.components = tuple(components)

    def __repr__(self):
        # Return a string representation for debugging
        return "Vector{}".format(self.components)

    def __len__(self):
        # Return how many dimensions this vector has
        return len(self.components)

    def __getitem__(self, index):
        # Allow indexing like vector[0] to get x coordinate
        return self.components[index]
    
    def norm(self):
        # Calculate the length or magnitude of the vector
        return math.sqrt(sum(c**2 for c in self.components))

    def __add__(self, other):
        # Add two vectors together component by component
        self._check_length(other)
        return Vector(*(self[i] + other[i] for i in range(len(self))))

    def __sub__(self, other):
        # Subtract one vector from another
        self._check_length(other)
        return Vector(*(self[i] - other[i] for i in range(len(self))))

    def __mul__(self, scalar):
        # Multiply vector by a number to scale it
        return Vector(*(c * scalar for c in self.components))

    def __truediv__(self, scalar):
        # Divide vector by a number
        if scalar == 0:
            raise ValueError("Division by zero")
        return Vector(*(c / scalar for c in self.components))
    
    def _check_length(self, other):
        # Make sure we're not trying to add vectors of different dimensions
        if len(self) != len(other):
            raise ValueError("Vectors must have same length")
    
    def distance(self, other):
        # Calculate distance between two points represented as vectors
        self._check_length(other)
        return math.sqrt(sum((self[i] - other[i])**2 for i in range(len(self))))
    
    def normalized(self):
        # Return a unit vector pointing in the same direction
        norm = self.norm()
        return self / norm if norm > 0 else self
    
    def with_magnitude(self, magnitude):
        # Return a new vector with a specific length but same direction
        return self.normalized() * magnitude
    
    def limited(self, max_magnitude):
        # Return a new vector that won't exceed the given length
        magnitude = self.norm()
        if magnitude > max_magnitude:
            return self.with_magnitude(max_magnitude)
        return self
    
    @staticmethod
    def random_2d(lower_bound, upper_bound):
        # Create a random 2D vector within the given bounds
        return Vector(
            random.uniform(lower_bound, upper_bound), 
            random.uniform(lower_bound, upper_bound)
        )
    
    @staticmethod
    def from_angle(angle):
        # Convert an angle in radians to a unit vector
        return Vector(math.cos(angle), math.sin(angle))


class GameEvent:
    # Just a container for event type names
    BOID_DESTROYED = "boid_destroyed"
    SHIP_HIT = "ship_hit"
    GAME_WON = "game_won"
    GAME_LOST = "game_lost"


class EventData:
    # Wrapper for event information that gets passed around
    def __init__(self, event_type, **kwargs):
        self.event_type = event_type
        self.data = kwargs


class Observer:
    # Interface for objects that want to be notified of game events
    def on_event(self, event_data):
        # Subclasses need to implement this to react to events
        raise NotImplementedError("Subclass must implement on_event()")


class Observable:
    # Manages a list of observers and notifies them when something happens
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        # Add a new observer to the list if it's not already there
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        # Remove an observer from the notification list
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_data):
        # Tell all observers that something happened
        for observer in self._observers:
            observer.on_event(event_data)


class BoidBehavior:
    # Base class for different boid AI strategies
    
    def calculate_steering(self, boid, nearby_objects):
        # Figure out which direction the boid should move
        raise NotImplementedError("Subclass must implement calculate_steering()")
    
    def get_color(self):
        # Return what color this type of boid should be
        raise NotImplementedError("Subclass must implement get_color()")
    
    def is_aggressive(self):
        # Return whether this boid attacks the ship
        raise NotImplementedError("Subclass must implement is_aggressive()")


class PassiveBehavior(BoidBehavior):
    # Normal flocking behavior that avoids the ship
    
    def get_color(self):
        return "White"
    
    def is_aggressive(self):
        return False
    
    def calculate_steering(self, boid, nearby_objects):
        # Calculate all the flocking forces for this frame
        separation = Vector(0, 0)
        alignment = Vector(0, 0)
        cohesion = Vector(0, 0)
        sep_count = 0
        align_count = 0
        coh_count = 0
        
        ship_avoidance = Vector(0, 0)
       
        for obj in nearby_objects:
            if obj == boid:
                continue
                
            distance = boid.position.distance(obj.position)
            
            # Keep some space from nearby objects
            if distance < BOID_SEPARATION_PERCEPTION:
                difference = (boid.position - obj.position) / distance
                separation = separation + difference
                sep_count += 1
            
            # Really try to stay away from the ship
            if isinstance(obj, Ship) and distance < BOID_SEPARATION_PERCEPTION:
                difference = (boid.position - obj.position) / distance
                ship_avoidance = ship_avoidance + (difference * SHIP_PRESENCE_FACTOR)
            
            # Stick with the group but not with ships or missiles
            if not isinstance(obj, (Ship, Missile)):
                if distance < BOID_COHESION_PERCEPTION:
                    cohesion = cohesion + obj.position
                    coh_count += 1
                
                # Try to match velocity with nearby boids
                if distance < BOID_PERCEPTION:
                    alignment = alignment + obj.velocity
                    align_count += 1
        
        # Convert the accumulated forces into actual steering
        separation = self._apply_force(separation, sep_count, boid.velocity)
        alignment = self._apply_force(alignment, align_count, boid.velocity)
        
        if coh_count > 0:
            cohesion = cohesion / coh_count
            cohesion = cohesion - boid.position
            cohesion = self._apply_force_direct(cohesion, boid.velocity)
        
        return separation + alignment + cohesion + ship_avoidance
    
    def _apply_force(self, force, count, velocity):
        # Helper to average and apply a force if we found any neighbors
        if count > 0:
            force = force / count
            return self._apply_force_direct(force, velocity)
        return Vector(0, 0)
    
    def _apply_force_direct(self, force, velocity):
        # Apply speed and force limits to keep movement realistic
        desired = force.with_magnitude(BOID_MAX_SPEED)
        steering = desired - velocity
        return steering.limited(BOID_MAX_FORCE)


class AggressiveBehavior(BoidBehavior):
    # Attack behavior that chases the ship
    
    def get_color(self):
        return "Red"
    
    def is_aggressive(self):
        return True
    
    def calculate_steering(self, boid, nearby_objects):
        # Look for the ship and go after it
        ship = None
        for obj in nearby_objects:
            if isinstance(obj, Ship):
                ship = obj
                break
        
        if ship:
            # Head straight for the ship
            desired = ship.position - boid.position
            attack_force = desired.with_magnitude(BOID_MAX_SPEED * 2)
            
            # Still avoid crashing into other boids though
            separation = Vector(0, 0)
            sep_count = 0
            
            for obj in nearby_objects:
                if obj != boid and not isinstance(obj, Ship):
                    distance = boid.position.distance(obj.position)
                    if distance < BOID_SEPARATION_PERCEPTION / 2:
                        difference = (boid.position - obj.position) / distance
                        separation = separation + difference
                        sep_count += 1
            
            if sep_count > 0:
                separation = separation / sep_count
                separation = separation.with_magnitude(BOID_MAX_SPEED)
                separation = (separation - boid.velocity).limited(BOID_MAX_FORCE)
            
            return attack_force.limited(BOID_MAX_FORCE * 1.5) + separation
        
        # If no ship around just flock normally
        passive = PassiveBehavior()
        return passive.calculate_steering(boid, nearby_objects)


class EntityFactory:
    # Handles creating new game objects so we don't have to remember all the details
    
    @staticmethod
    def create_boid():
        # Make a new boid at a random position with random velocity
        position = Vector(
            random.randint(0, C_WIDTH),
            random.randint(0, C_HEIGHT)
        )
        velocity = Vector.random_2d(-4, 4)
        
        # Randomly decide if this boid will be aggressive
        if random.random() < AGGRESSIVE_SPAWN_CHANCE:
            behavior = AggressiveBehavior()
        else:
            behavior = PassiveBehavior()
        
        return Boid(position, velocity, behavior)
    
    @staticmethod
    def create_ship():
        # Put the ship in the center of the screen
        position = Vector(C_WIDTH / 2, C_HEIGHT / 2)
        return Ship(position)
    
    @staticmethod
    def create_missile(position, velocity):
        # Create a missile with the given starting position and velocity
        return Missile(position, velocity)


class GameObject:
    # Base class for everything that appears in the game world
    
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.velocity = Vector(0, 0)
    
    def update(self):
        # Update the object's state each frame
        raise NotImplementedError("Subclass must implement update()")
    
    def draw(self, canvas):
        # Draw the object on the screen
        raise NotImplementedError("Subclass must implement draw()")
    
    def collides_with(self, other):
        # Simple circle collision check
        distance = self.position.distance(other.position)
        return distance < (self.radius + other.radius)
    
    def wrap_around_screen(self):
        # Make objects appear on the opposite side when they go off screen
        x, y = self.position[0], self.position[1]
        
        if x > C_WIDTH:
            x = 0
        elif x < 0:
            x = C_WIDTH
        
        if y > C_HEIGHT:
            y = 0
        elif y < 0:
            y = C_HEIGHT
        
        self.position = Vector(x, y)


class Boid(GameObject):
    # A flocking creature with AI behavior
    
    def __init__(self, position, velocity, behavior):
        GameObject.__init__(self, position, BOID_RADIUS)
        self.velocity = velocity
        self.behavior = behavior
        self.acceleration = Vector(0, 0)
    
    def update(self):
        # Apply forces and update position
        self.velocity = (self.velocity + self.acceleration).limited(BOID_MAX_SPEED)
        self.position = self.position + self.velocity
        self.wrap_around_screen()
        self.acceleration = Vector(0, 0)
    
    def draw(self, canvas):
        # Draw the triangular boid shape
        canvas.draw_polygon([
            (self.position + BOID_SHAPE[0]),
            (self.position + BOID_SHAPE[1]),
            (self.position + BOID_SHAPE[2])
        ], 1, self.behavior.get_color())
        
        # Add a small dot to show which way it's facing
        angle = math.atan2(self.velocity[0], self.velocity[1])
        offset_pos = self.position + Vector.from_angle(angle) * 8
        canvas.draw_circle([offset_pos[0], offset_pos[1]], 1, 1, self.behavior.get_color())
    
    def apply_flocking(self, nearby_objects):
        # Let the behavior strategy figure out where to go
        self.acceleration = self.behavior.calculate_steering(self, nearby_objects)
    
    def is_aggressive(self):
        return self.behavior.is_aggressive()


class Ship(GameObject):
    # The player controlled spaceship
    
    def __init__(self, position):
        GameObject.__init__(self, position, SHIP_RADIUS)
        self.angle = -math.pi / 2
        self.angle_vel = 0
        self.thrust = False
        self.color = "Purple"
    
    def update(self):
        # Calculate movement based on current angle and thrust
        forward = Vector.from_angle(self.angle)
        
        self.position = self.position + self.velocity
        self.velocity = self.velocity * (1 - SHIP_FRICTION)
        
        if self.thrust and self.velocity.norm() < SHIP_MAX_SPEED:
            self.velocity = self.velocity + forward
        
        self.angle += self.angle_vel
        self.wrap_around_screen()
    
    def draw(self, canvas):
        # Draw the diamond shaped ship
        canvas.draw_polygon([
            (self.position + SHIP_SHAPE[0]),
            (self.position + SHIP_SHAPE[1]),
            (self.position + SHIP_SHAPE[2]),
            (self.position + SHIP_SHAPE[3])
        ], 1, self.color)
        
        # Draw the turret point where missiles come from
        turret_pos = self.position + Vector.from_angle(self.angle) * 15
        canvas.draw_circle([turret_pos[0], turret_pos[1]], 2, 1, self.color)
        self.turret_pos = turret_pos
    
    def turn(self, direction):
        # Start rotating the ship
        self.angle_vel = SHIP_ROTATION * direction
    
    def set_thrust(self, active):
        # Turn thrust on or off
        self.thrust = active
    
    def get_firing_position(self):
        # Return where missiles should spawn from
        return self.turret_pos if hasattr(self, 'turret_pos') else self.position
    
    def get_firing_velocity(self):
        # Calculate missile velocity based on ship's current velocity and direction
        forward = Vector.from_angle(self.angle)
        return self.velocity + forward * MISSILE_SPEED


class Missile(GameObject):
    # A projectile fired by the ship
    
    def __init__(self, position, velocity):
        GameObject.__init__(self, position, 3)
        self.velocity = velocity
        self.color = "Purple"
        self.alive = True
    
    def update(self):
        # Move the missile and check if it left the screen
        self.position = self.position + self.velocity
        
        x, y = self.position[0], self.position[1]
        if x < 0 or x > C_WIDTH or y < 0 or y > C_HEIGHT:
            self.alive = False
    
    def draw(self, canvas):
        # Draw a small dot for the missile
        canvas.draw_circle([self.position[0], self.position[1]], 1, 1, self.color)
    
    def is_alive(self):
        return self.alive


class GameState:
    # Base class for different game states like menu, playing, game over
    
    def update(self, game):
        # Update logic for this state
        raise NotImplementedError("Subclass must implement update()")
    
    def draw(self, game, canvas):
        # Draw this state to the screen
        raise NotImplementedError("Subclass must implement draw()")
    
    def handle_click(self, game):
        # React to mouse clicks in this state
        raise NotImplementedError("Subclass must implement handle_click()")


class MenuState(GameState):
    # The initial menu screen before the game starts
    
    def update(self, game):
        # Nothing to update on the menu
        pass
    
    def draw(self, game, canvas):
        # Show instructions and welcome message
        canvas.draw_text("Welcome!", [50, C_HEIGHT/2 - 50], 15, "Blue", "monospace")
        canvas.draw_text("Flocking simulator with aggressive (Red) and passive (White) boids", 
                        [50, C_HEIGHT/2 - 20], 15, "Blue", "monospace")
        canvas.draw_text("Destroy all red boids, minimize white casualties", 
                        [50, C_HEIGHT/2 + 10], 15, "Blue", "monospace")
        canvas.draw_text("Controls: Arrow keys to move, Space to fire", 
                        [50, C_HEIGHT/2 + 40], 15, "Blue", "monospace")
        canvas.draw_text("Click to start!", [50, C_HEIGHT/2 + 70], 15, "Blue", "monospace")
    
    def handle_click(self, game):
        # Start the game when clicked
        game.set_state(PlayingState())


class PlayingState(GameState):
    # The main gameplay state where everything happens
    
    def update(self, game):
        # Update all the game entities
        all_objects = game.get_all_objects()
        for boid in game.flock:
            boid.apply_flocking(all_objects)
            boid.update()
        
        game.ship.update()
        
        # Clean up dead missiles
        for missile in list(game.missiles):
            missile.update()
            if not missile.is_alive():
                game.missiles.remove(missile)
        
        # Check if anything collided
        game.check_collisions()
        
        # See if the game should end
        if game.aggressive_count == 0:
            game.set_state(VictoryState())
        elif game.lives <= 0:
            game.set_state(GameOverState())
    
    def draw(self, game, canvas):
        # Draw everything on screen
        for boid in game.flock:
            boid.draw(canvas)
        
        game.ship.draw(canvas)
        
        for missile in game.missiles:
            missile.draw(canvas)
        
        # Show the player's stats
        canvas.draw_text("Red boids:", [12, 36], 15, "White", "monospace")
        canvas.draw_text(str(game.aggressive_count), [100, 36], 15, "White", "monospace")
        canvas.draw_text("Lives    :", [12, 56], 15, "White", "monospace")
        canvas.draw_text(str(game.lives), [100, 56], 15, "White", "monospace")
        canvas.draw_text("Score    :", [12, 76], 15, "White", "monospace")
        canvas.draw_text(str(game.score), [100, 76], 15, "White", "monospace")
    
    def handle_click(self, game):
        # Ignore clicks during gameplay
        pass


class VictoryState(GameState):
    # Victory screen when player destroys all red boids
    
    def update(self, game):
        pass
    
    def draw(self, game, canvas):
        # Show victory message and stats
        canvas.draw_text("VICTORY!", [C_WIDTH/2 - 100, C_HEIGHT/2 - 20], 20, "Green", "monospace")
        canvas.draw_text("Score: " + str(game.score), [C_WIDTH/2 - 100, C_HEIGHT/2 + 20], 15, "Green", "monospace")
        canvas.draw_text("Casualties: " + str(game.casualties), [C_WIDTH/2 - 100, C_HEIGHT/2 + 40], 15, "Green", "monospace")
        canvas.draw_text("Click to play again!", [C_WIDTH/2 - 100, C_HEIGHT/2 + 80], 15, "Yellow", "monospace")
    
    def handle_click(self, game):
        # Restart when player clicks
        game.restart()


class GameOverState(GameState):
    # Game over screen when player loses all lives
    
    def update(self, game):
        pass
    
    def draw(self, game, canvas):
        # Show game over message
        canvas.draw_text("GAME OVER", [C_WIDTH/2 - 100, C_HEIGHT/2 - 20], 20, "Red", "monospace")
        canvas.draw_text("Score: " + str(game.score), [C_WIDTH/2 - 100, C_HEIGHT/2 + 20], 15, "Red", "monospace")
        canvas.draw_text("Click to try again!", [C_WIDTH/2 - 100, C_HEIGHT/2 + 60], 15, "Yellow", "monospace")
    
    def handle_click(self, game):
        # Restart when player clicks
        game.restart()


class Game(Observable, Observer):
    # Main controller for the entire game
    
    def __init__(self):
        Observable.__init__(self)
        self.factory = EntityFactory()
        
        # Set up the initial game state
        self._initialize_game()
        
        # Listen to our own events
        self.attach(self)
    
    def _initialize_game(self):
        # Set up or reset everything for a new game
        self.state = MenuState()
        self.lives = STARTING_LIVES
        self.score = 0
        self.casualties = 0
        self.aggressive_count = 0
        
        # Create the ship and boids
        self.ship = self.factory.create_ship()
        self.flock = set()
        self.missiles = set()
        
        # Spawn the initial flock
        for _ in range(BOID_NUMBER):
            boid = self.factory.create_boid()
            self.flock.add(boid)
            if boid.is_aggressive():
                self.aggressive_count += 1
    
    def restart(self):
        # Start a fresh game
        self._initialize_game()
        self.set_state(PlayingState())
    
    def set_state(self, new_state):
        # Switch to a different game state
        self.state = new_state
    
    def get_all_objects(self):
        # Get every object that boids need to be aware of
        return {self.ship} | self.flock
    
    def update(self):
        # Let the current state handle the update
        self.state.update(self)
    
    def draw(self, canvas):
        # Let the current state handle drawing
        self.state.draw(self, canvas)
    
    def handle_click(self):
        # Pass click events to the current state
        self.state.handle_click(self)
    
    def fire_missile(self):
        # Create a new missile if we haven't hit the limit
        if len(self.missiles) < MAX_MISSILES:
            position = self.ship.get_firing_position()
            velocity = self.ship.get_firing_velocity()
            missile = self.factory.create_missile(position, velocity)
            self.missiles.add(missile)
    
    def check_collisions(self):
        # Check if any objects hit each other
        for boid in list(self.flock):
            if boid.collides_with(self.ship) and boid.is_aggressive():
                self._handle_ship_hit(boid)
        
        for missile in list(self.missiles):
            for boid in list(self.flock):
                if missile.is_alive() and boid.collides_with(missile):
                    self._handle_boid_destroyed(boid, missile)
    
    def _handle_ship_hit(self, boid):
        # Deal with the ship getting hit by an aggressive boid
        self.flock.remove(boid)
        self.aggressive_count -= 1
        self.lives -= 1
        self.score += 0.5
        
        event = EventData(GameEvent.SHIP_HIT, boid=boid)
        self.notify(event)
    
    def _handle_boid_destroyed(self, boid, missile):
        # Handle a boid getting shot
        self.flock.remove(boid)
        missile.alive = False
        
        if boid.is_aggressive():
            self.aggressive_count -= 1
            self.score += 1
        else:
            self.casualties += 1
        
        event = EventData(GameEvent.BOID_DESTROYED, boid=boid, missile=missile)
        self.notify(event)
    
    def on_event(self, event_data):
        # React to game events by printing messages
        if event_data.event_type == GameEvent.BOID_DESTROYED:
            print("Boid destroyed! Score: " + str(self.score))
        elif event_data.event_type == GameEvent.SHIP_HIT:
            print("Ship hit! Lives: " + str(self.lives))


class InputController:
    # Maps keyboard input to game actions
    
    def __init__(self, game):
        self.game = game
        
        # What to do when each key is pressed
        self.key_actions = {
            "left": lambda: game.ship.turn(-1),
            "right": lambda: game.ship.turn(1),
            "up": lambda: game.ship.set_thrust(True),
            "space": lambda: game.fire_missile()
        }
        
        # What to do when each key is released
        self.key_releases = {
            "left": lambda: game.ship.turn(0),
            "right": lambda: game.ship.turn(0),
            "up": lambda: game.ship.set_thrust(False),
            "space": lambda: None
        }
    
    def handle_keydown(self, key):
        # Check if this key does anything when pressed
        for key_name in self.key_actions:
            if key == simplegui.KEY_MAP[key_name]:
                self.key_actions[key_name]()
    
    def handle_keyup(self, key):
        # Check if this key does anything when released
        for key_name in self.key_releases:
            if key == simplegui.KEY_MAP[key_name]:
                self.key_releases[key_name]()


# Create the game and input handler
game = Game()
input_controller = InputController(game)

# These functions connect the game to the simplegui framework
def draw(canvas):
    game.update()
    game.draw(canvas)

def keydown(key):
    input_controller.handle_keydown(key)

def keyup(key):
    input_controller.handle_keyup(key)

def click(pos):
    game.handle_click()

# Set up the game window
frame = simplegui.create_frame("Flokk - Enterprise Edition", C_WIDTH, C_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_canvas_background("Gray")
frame.set_mouseclick_handler(click)

frame.start()