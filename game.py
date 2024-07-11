from engine import *
import pyxel
from math import copysign, sqrt

game = Game(Vector2(320, 180), "../celeste.pyxres", "CELESTE", 6, 60)

player_dir = 1
grounded = False
jump = 12
jump_buffer = 12
dash = 15
dashCD = 15
hasDash = False

idle_animation = Animation(Vector2(0, 0), "idle", 5, 5, Vector2(16, 32), Vector2(0, 0))
run_animation = Animation(Vector2(0, 0), "run", 20, 12, Vector2(16, 32), Vector2(0, 32))
jump_anim = Animation(Vector2(0, 0), "jump", 1, 1, Vector2(16, 32), Vector2(16, 64))
jump_anim_blue = Animation(Vector2(0, 0), "jump_blue", 1, 1, Vector2(16, 32), Vector2(16, 64), img=1)
jump_thin = Animation(Vector2(0, 0), "jump_thin", 1, 1, Vector2(16, 32), Vector2(0, 64))
fall_anim = Animation(Vector2(0, 0), "fall", 1, 1, Vector2(16, 32), Vector2(32, 64))
fall_anim_blue = Animation(Vector2(0, 0), "fall_blue", 1, 1, Vector2(16, 32), Vector2(32, 64), img=1)
fall_thin = Animation(Vector2(0, 0), "fall_thin", 1, 1, Vector2(16, 32), Vector2(48, 64))
fall_thin_blue = Animation(Vector2(0, 0), "fall_thin_blue", 1, 1, Vector2(16, 32), Vector2(48, 64), img=1)
dash_anim = Animation(Vector2(0, 0), "dash", 1, 1, Vector2(16, 32), Vector2(0, 96))
dash_anim_blue = Animation(Vector2(0, 0), "dash_blue", 1, 1, Vector2(16, 32), Vector2(0, 96), img=1)


def update_player(player: Character_body):
    global player_dir, grounded, idle_animation, run_animation, jump, jump_buffer, dash, hasDash, dashCD

    jump += 1
    jump_buffer += 1
    dash += 1
    dashCD += 1


    if pyxel.btnp(pyxel.KEY_J) and hasDash and dashCD >= 15:
        dash = 0
        dashCD = 0
        hasDash = False
        if hasDash:
            player.sprite.switch_to_animation("dash")
        else:
            player.sprite.switch_to_animation("dash_blue")
    
    if dash < 4:
        game.frozen = True
        if pyxel.btnp(pyxel.KEY_SPACE):
            jump_buffer = 0
    
    if dash < 15 and dash >= 4:
        
        if dash == 4:
            if (pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_S)) and (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_D)):
                if pyxel.btn(pyxel.KEY_W):
                    player.velocity.y = -240 / sqrt(2)
                else:
                    player.velocity.y = 240 / sqrt(2)
                
                if pyxel.btn(pyxel.KEY_A):
                    player.velocity.x = -240 / sqrt(2)
                else:
                    player.velocity.x = 240 / sqrt(2)
            
            elif (pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_S)) or (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_D)):
                player.velocity.y = -240 if pyxel.btn(pyxel.KEY_W) else (240 if pyxel.btn(pyxel.KEY_S) else 0)
                player.velocity.x = -240 if pyxel.btn(pyxel.KEY_A) else (240 if pyxel.btn(pyxel.KEY_D) else 0)
            else:
                player.velocity.x = player_dir * 240
                player.velocity.y = 0

        game.frozen = False

        if player.position.y == 120:
            grounded = True
        if pyxel.btnp(pyxel.KEY_SPACE):
                jump_buffer = 0
        if grounded:
            if dash >= 13:
                hasDash = True
            
            if jump_buffer < 5:
                dash = 15
                if abs(player.velocity.x) == 240:
                    jump = 0
                    if pyxel.btn(pyxel.KEY_D):
                        player.velocity.x = 240
                    elif pyxel.btn(pyxel.KEY_A):
                        player.velocity.x = -240

                elif abs(player.velocity.x) > 160:
                    if pyxel.btn(pyxel.KEY_D):
                        player.velocity.x = 325
                    elif pyxel.btn(pyxel.KEY_A):
                        player.velocity.x = -325
                    else:
                        player.velocity.x = copysign(325, player.velocity.x)
                    player.velocity.y = -52.5
                    jump = 0
                else:
                    jump = 0
                

        if dash == 14:
            if player.velocity.y > 0:
                player.velocity.x = copysign(160.0 * 0.75, player.velocity.x)
            elif player.velocity.y == 0:
                player.velocity.x = copysign(160.0, player.velocity.x)
            
                
            
    
    if dash >= 15:
        game.frozen = False
        if dash == 15 and grounded:
            player.sprite.switch_to_animation("run")
            if player.velocity.y < 0 and player.velocity.y != -52.5:
                jump = 0

        if pyxel.btn(pyxel.KEY_D):
            player_dir = 1
            if player.velocity.x == 0.0 and grounded:
                player.sprite.switch_to_animation("run")
            if player.velocity.x >= 90:
                player.velocity.x -= 6 + 2.0 / 3.0
                if player.velocity.x < 90:
                    player.velocity.x = 90
            else:
                player.velocity.x += 16 + 2.0 / 3.0

        elif pyxel.btn(pyxel.KEY_A):
            player_dir = -1
            if player.velocity.x == 0.0 and grounded:
                player.sprite.switch_to_animation("run")
            if player.velocity.x <= -90:
                player.velocity.x += 6 + 2.0 / 3.0
                if player.velocity.x > -90:
                    player.velocity.x = -90
            else:
                player.velocity.x -= 16 + 2.0 / 3.0

        else:
            if player.velocity.x == 0.0 and grounded == True:
                player.sprite.switch_to_animation("idle")

            if grounded:
                if abs(player.velocity.x) < 6 + 2.0 / 3.0:
                    player.velocity.x = 0.0
                else:
                    player.velocity.x -= copysign(6 + 2.0 / 3.0, player.velocity.x)
            else:
                if abs(player.velocity.x) < 10 + 5.0 / 6.0:
                    player.velocity.x = 0.0
                else:
                    player.velocity.x -= copysign(10 + 5.0 / 6.0, player.velocity.x)

        if not grounded:
            if player.velocity.y <= 0:
                if hasDash:
                    player.sprite.switch_to_animation("jump")
                else:
                    player.sprite.switch_to_animation("jump_blue")

            else:
                if player.velocity.y <= 160:
                    if hasDash:
                        player.sprite.switch_to_animation("fall")
                    else:
                        player.sprite.switch_to_animation("fall_blue")
                else:
                    if hasDash:
                        player.sprite.switch_to_animation("fall_thin")
                    else:
                        player.sprite.switch_to_animation("fall_thin_blue")
        
        if player.position.y < 120:
            grounded = False

            if not pyxel.btn(pyxel.KEY_S):
                player.velocity.y += 7.5 if (player.velocity.y <= 40 and player.velocity.y >= -40 and jump < 12) else 15

                if player.velocity.y > 160:
                    player.velocity.y = 160
            else:
                player.velocity.y += 7.5 if (player.velocity.y <= 40 and player.velocity.y >= -40 and jump < 12) else 15

                if player.velocity.y > 240:
                    player.velocity.y = 240
        else:
            if grounded == False:
                if player.velocity.x != 0.0:
                    player.sprite.switch_to_animation("run")
                else:
                    player.sprite.switch_to_animation("idle")
            grounded = True
            if dash > 10:
                hasDash = True
            if player.velocity.y != -52.5:
                player.velocity.y = 0
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            jump_buffer = 0

        if jump_buffer < 5 and pyxel.btn(pyxel.KEY_SPACE) and grounded:
            jump = 0
            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_A):
                player.velocity.x += 40.0 * player_dir
        
        if pyxel.btnr(pyxel.KEY_SPACE):
            jump = 12

        if jump < 12:
            if player.velocity.y == -52.5 or player.velocity.y == -37.5:
                player.velocity.y = -52.5
            else:
                player.velocity.y = -105.0

        if jump < 6:
            pass

    player.move_and_slide()

    if player.position.y > 120:
        player.position.y = 120

    if player_dir == 1:
        player.sprite.current_anim.flipped_x = False
    else:
        player.sprite.current_anim.flipped_x = True


Character = Character_body(Vector2(160, 90), Hitbox(Vector2(0, 0), Vector2(11, 8)), Animated_sprite(Vector2(0, 0), [idle_animation, run_animation, jump_anim, jump_thin, fall_anim, fall_thin, dash_anim, fall_anim_blue, fall_thin_blue, jump_anim_blue, dash_anim_blue]), update_player)

game.add_object(Character)
game.start()