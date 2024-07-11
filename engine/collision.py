from engine.positioning import Vector2
from math import copysign

class Hitbox:
    """General hitbox class for collisions. Only rectangular hitboxes are allowed"""
    def __init__(self, position: Vector2, hitbox_size: Vector2):
        """
        position is position of hitbox\n
        hitbox_size is the size of the hitbox (for rectangular) in format Vector2(length, height)\n
        """
        self.position = position
        self.local_position = position
        self.size = hitbox_size.round()


    def __repr__(self):
        return f"Hitbox: size = {self.size} | position = {self.position}"

    def is_colliding_with_hitbox(self, other: "Hitbox") -> bool:
        """
        Checks if the two hitboxes are colliding.
        """

        self.position.round(True)
        other.position.round(True)

        return True if 2 * abs(self.position.x - other.position.x) < self.size.x + other.size.x and 2 * abs(self.position.y - other.position.y) < self.size.y + other.size.y else False

    def is_colliding_with_point(self, other: Vector2) -> bool:
        """
        Checks if the two point is contained in self.
        """

        return True if 2 * abs(self.position.x - other.x) < self.size.x and 2 * abs(self.position.y - other.y) < self.size.y else False

class MultiHitbox(Hitbox):
    """For when you want multiple hitboxes for one object to make more complex hitboxes"""
    def __init__(self, position: Vector2, hitboxes: list[Hitbox]):
        self.position = position
        self.local_position = position
        self.hitboxes = hitboxes
        self.size = Vector2(0, 0)
    
    def __repr__(self):
        return f"MultiHitboxes: {[repr(i) for i in self.hitboxes]}"

    def is_colliding_with_hitbox(self, other: Hitbox) -> bool:
        return (True in [i.is_colliding_with_hitbox(other) for i in self.hitboxes])
    
    def is_colliding_with_point(self, other: Vector2) -> bool:
        return (True in [i.is_colliding_with_point(other) for i in self.hitboxes])
