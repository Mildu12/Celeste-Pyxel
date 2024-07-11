from engine.positioning import Vector2
import pyxel
from math import floor

class Sprite:
    """General sprite class"""
    def __init__(self, position: Vector2, start: Vector2, size: Vector2, z_position: float = 0, img: int = 0, colkey: int = 7, flipped_x: bool = False, flipped_y: bool = False):
        self.start = start
        self.size = size
        self.local_position = position
        self.position = position
        self.img = img
        self.colkey = colkey
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
    
    def draw(self):
        pyxel.blt(self.position.x - (self.size.x / 2), self.position.y - (self.size.y / 2), self.img, self.start.x, self.start.y, -self.size.x if self.flipped_x else self.size.x, -self.size.y if self.flipped_y else self.size.y, self.colkey)

class Animation(Sprite):
    """To be used by an Animated_sprite"""
    def __init__(self, offset: Vector2, name: str, fps: float, frame_count: int, size: Vector2, start: Vector2, colkey: int = 7, img: int = 0, flipped_x: bool = False, flipped_y: bool = False):
        super().__init__(offset, start, size, 0, img, colkey, flipped_x, flipped_y)
        self.fps = fps
        self.frame_count = frame_count
        self.name = name
        self.frame = 0.0
        self.timer = 0.0
        self.game_fps = 60
    
    def update(self):
        self.timer += 1.0 / float(self.game_fps)
        self.frame = floor(self.timer * self.fps)
        if self.frame > self.frame_count - 1:
            self.frame = 0
            self.timer -= float(self.frame_count) / float(self.fps)
    
    def reset(self):
        self.timer = 0.0
        self.frame = 0.0
    
    def draw(self):
        pyxel.blt(self.position.x - (self.size.x / 2), self.position.y - (self.size.y / 2), self.img, self.start.x + (self.size.x * self.frame), self.start.y, -self.size.x if self.flipped_x else self.size.x, -self.size.y if self.flipped_y else self.size.y, self.colkey)

class Animated_sprite():
    """For frame-by-frame animations"""
    def __init__(self, position: Vector2, animations = Animation, z_position: int = 0):
        self.animations: list[Animation] = animations
        self.current_anim: Animation = (self.animations)[0]
        self.position = position
        self.local_position = position
        self.z_position = z_position
        self.game_fps = 60
    
    def update(self):
        self.current_anim.position = self.position + self.current_anim.local_position
        self.current_anim.update()
    
    def draw(self):
        self.current_anim.draw()
    
    def switch_to_animation(self, animation_name: str):

        if self.current_anim.name != animation_name:
            for i in self.animations:
                if i.name == animation_name:
                    self.current_anim = i
                    self.current_anim.reset()
                    self.current_anim.position = self.position + self.current_anim.local_position
                    return 
            assert False, f"Animation \"{animation_name}\" not in animations list"
