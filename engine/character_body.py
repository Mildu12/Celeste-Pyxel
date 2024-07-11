from engine.collision import Hitbox, MultiHitbox
from engine.positioning import Vector2
from engine.sprites import Sprite, Animated_sprite
from typing import Callable

class Character_body:
    def __init__(self, position: Vector2, hitbox: Hitbox | MultiHitbox, sprite: Sprite | Animated_sprite, update: Callable, velocity: Vector2 = Vector2(0, 0), move_type: str = "D"):
        self.position = position
        self.hitbox = hitbox
        self.velocity = velocity
        self.sprite = sprite
        self.updateCustom = update
        self.game_fps = 60
        self.frozen = False
    
    def move_and_slide(self):
        if not self.frozen:
            self.position += self.velocity * (1.0 / float(self.game_fps))
    
    def update(self, frozen: bool):
        self.frozen = frozen
        self.sprite.position = self.position + self.sprite.local_position
        self.hitbox.position = self.position + self.hitbox.local_position
        self.updateCustom(self)