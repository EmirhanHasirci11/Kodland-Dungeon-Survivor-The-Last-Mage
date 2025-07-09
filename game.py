# -*- coding: utf-8 -*-
# type: ignore

import math
import random
from pygame import Rect
from pgzero import music

WIDTH = 1920
HEIGHT = 1080
TITLE = "Dungeon Survivor: The Last Mage"

game_state = "menu"
sound_on = True
is_music_playing = False

score = 0
frame_count = 0
ghost_last_spawn_frame = 0
cyclops_last_spawn_frame = 0
fireball_last_frame = -100
ghost_spawn_interval = random.randint(60, 120)
cyclops_spawn_interval = random.randint(60, 180)

buttons = {
    "start": Rect(WIDTH // 2 - 100, 250, 200, 50),
    "sound": Rect(WIDTH // 2 - 100, 320, 200, 50),
    "quit": Rect(WIDTH // 2 - 100, 390, 200, 50),
    "menu": Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50)
}

class Mage:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 5
        self.facing = "right"
        self.image_index = 0
        self.frame = 0
        self.actor = Actor("mage_idle_0", (self.x, self.y))

        self.idle_images = {
            "right": ["mage_idle_0", "mage_idle_1"],
            "left": ["mage_idle_left_0", "mage_idle_left_1"]
        }
        self.walk_images = {
            "right": ["mage_walk_0", "mage_walk_1", "mage_walk_2"],
            "left": ["mage_walk_left_0", "mage_walk_left_1", "mage_walk_left_2"]
        }

    def draw(self):
        self.actor.draw()

    def update(self):
        moved = False
        if keyboard.left or keyboard.a:
            self.x -= self.speed
            self.facing = "left"
            moved = True
        if keyboard.right or keyboard.d:
            self.x += self.speed
            self.facing = "right"
            moved = True
        if keyboard.up or keyboard.w:
            self.y -= self.speed
            moved = True
        if keyboard.down or keyboard.s:
            self.y += self.speed
            moved = True

        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))
        self.actor.pos = (self.x, self.y)

        self.frame += 1
        if self.frame % 10 == 0:
            images = self.walk_images[self.facing] if moved else self.idle_images[self.facing]
            self.image_index = (self.image_index + 1) % len(images)
            self.actor.image = images[self.image_index]

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)

class Fireball:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y
        self.speed = 15
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy)
        self.vel_x = dx / distance * self.speed
        self.vel_y = dy / distance * self.speed
        self.actor = Actor("fireball", (self.x, self.y))

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.actor.pos = (self.x, self.y)

    def draw(self):
        self.actor.draw()

    def get_rect(self):
        return Rect(self.x - 8, self.y - 8, 16, 16)

class Cyclops:
    def __init__(self, x, y):
        self.health = 2
        self.x = x
        self.y = y
        self.speed = 1.5
        self.facing = "left"
        self.image_index = 0
        self.frame = 0
        self.actor = Actor("cyclops_idle_left_0", (self.x, self.y))
        self.idle_images = {
            "right": ["cyclops_idle_0", "cyclops_idle_1"],
            "left": ["cyclops_idle_left_0", "cyclops_idle_left_1"]
        }
        self.walk_images = {
            "right": ["cyclops_walk_0", "cyclops_walk_1", "cyclops_walk_2", "cyclops_walk_3"],
            "left": ["cyclops_walk_left_0", "cyclops_walk_left_1", "cyclops_walk_left_2", "cyclops_walk_left_3"]
        }

    def draw(self):
        self.actor.draw()

    def update(self):
        moved = False
        if mage.x > self.x:
            self.x += self.speed
            self.facing = "right"
            moved = True
        else:
            self.x -= self.speed
            self.facing = "left"
            moved = True
        if mage.y > self.y:
            self.y += self.speed
        else:
            self.y -= self.speed

        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))
        self.actor.pos = (self.x, self.y)
        self.frame += 1
        if self.frame % 10 == 0:
            images = self.walk_images[self.facing] if moved else self.idle_images[self.facing]
            self.image_index = (self.image_index + 1) % len(images)
            self.actor.image = images[self.image_index]

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)

class Ghost:
    def __init__(self, x, y):
        self.health = 1
        self.x = x
        self.y = y
        self.speed = 2.8
        self.facing = "left"
        self.image_index = 0
        self.frame = 0
        self.actor = Actor("ghost_idle_left_0", (self.x, self.y))
        self.idle_images = {
            "right": ["ghost_idle_0", "ghost_idle_1"],
            "left": ["ghost_idle_left_0", "ghost_idle_left_1"]
        }
        self.fly_images = {
            "right": ["ghost_fly_0", "ghost_fly_1"],
            "left": ["ghost_fly_left_0", "ghost_fly_left_1"]
        }

    def draw(self):
        self.actor.draw()

    def update(self):
        if mage.x > self.x:
            self.x += self.speed
            self.facing = "right"
        else:
            self.x -= self.speed
            self.facing = "left"
        if mage.y > self.y:
            self.y += self.speed
        else:
            self.y -= self.speed

        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))
        self.actor.pos = (self.x, self.y)
        self.frame += 1
        if self.frame % 10 == 0:
            images = self.fly_images[self.facing]
            self.image_index = (self.image_index + 1) % len(images)
            self.actor.image = images[self.image_index]

    def get_rect(self):
        return Rect(self.x - 16, self.y - 16, 32, 32)

mage = Mage(300, 300)
fireballs = []
enemies = []

def reset_game():
    global mage, fireballs, enemies, score
    global ghost_last_spawn_frame, cyclops_last_spawn_frame, fireball_last_frame
    global ghost_spawn_interval, cyclops_spawn_interval
    mage = Mage(300, 300)
    fireballs = []
    enemies = []
    score = 0
    ghost_last_spawn_frame = 0
    cyclops_last_spawn_frame = 0
    fireball_last_frame = -100
    ghost_spawn_interval = random.randint(60, 120)
    cyclops_spawn_interval = random.randint(60, 180)

def draw():
    screen.clear()
    screen.blit("background", (0, 0))
    if game_state == "menu":
        screen.draw.text("Dungeon Survivor", center=(WIDTH / 2, 150), fontsize=64, color="orange")
        for key, rect in buttons.items():
            if key == "menu": continue
            screen.draw.filled_rect(rect, "blue")
            label = {
                "start": "Start Game",
                "sound": "Sound: ON" if sound_on else "Sound: OFF",
                "quit": "Quit"
            }[key]
            screen.draw.text(label, center=rect.center, fontsize=32, color="white")
    elif game_state == "playing":
        mage.draw()
        for enemy in enemies:
            enemy.draw()
        for fb in fireballs:
            fb.draw()
        screen.draw.text(f"Health: {mage.health}", (30, 30), fontsize=40, color="white")
        screen.draw.text(f"Score: {score}", (30, 80), fontsize=40, color="yellow")
    elif game_state == "gameover":
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color="red")
        screen.draw.text(f"Final Score: {score}", center=(WIDTH / 2, HEIGHT / 2 + 80), fontsize=50, color="white")
        screen.draw.filled_rect(buttons["menu"], "darkgray")
        screen.draw.text("Main Menu", center=buttons["menu"].center, fontsize=32, color="white")

def update():
    global frame_count, ghost_last_spawn_frame, cyclops_last_spawn_frame
    global ghost_spawn_interval, cyclops_spawn_interval
    global game_state, score

    frame_count += 1

    if game_state == "playing":
        mage.update()

        if frame_count - ghost_last_spawn_frame >= ghost_spawn_interval:
            enemies.append(Ghost(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            ghost_last_spawn_frame = frame_count
            ghost_spawn_interval = random.randint(60, 120)

        if frame_count - cyclops_last_spawn_frame >= cyclops_spawn_interval:
            enemies.append(Cyclops(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            cyclops_last_spawn_frame = frame_count
            cyclops_spawn_interval = random.randint(60, 180)

        for enemy in enemies[:]:
            enemy.update()
            if mage.get_rect().colliderect(enemy.get_rect()):
                if isinstance(enemy, Ghost):
                    mage.health -= 1
                elif isinstance(enemy, Cyclops):
                    mage.health -= 2
                if sound_on:
                    sounds.enemy_death_voice.play()
                enemies.remove(enemy)
                if mage.health <= 0:
                    if sound_on:
                        music.stop()
                        sounds.game_over.play()
                    game_state = "gameover"

        for fb in fireballs[:]:
            fb.update()
            for enemy in enemies[:]:
                if fb.get_rect().colliderect(enemy.get_rect()):
                    fireballs.remove(fb)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        score += 10 if isinstance(enemy, Ghost) else 20
                        if sound_on:
                            sounds.enemy_death_voice.play()
                        enemies.remove(enemy)
                    break
            if fb.x < 0 or fb.x > WIDTH or fb.y < 0 or fb.y > HEIGHT:
                fireballs.remove(fb)

def on_mouse_down(pos):
    global game_state, sound_on, fireball_last_frame
    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            reset_game()
            game_state = "playing"
            if sound_on:
                music.stop()
                music.play("game_level_music")
                music.set_volume(0.4)
        elif buttons["sound"].collidepoint(pos):
            sound_on = not sound_on
            if not sound_on:
                music.set_volume(0)
            else:
                music.set_volume(0.4)
        elif buttons["quit"].collidepoint(pos):
            exit()
    elif game_state == "playing":
        if frame_count - fireball_last_frame >= 60:
            fireballs.append(Fireball(mage.x, mage.y, pos))
            fireball_last_frame = frame_count
            if sound_on:
                sounds.mage_fire_sound.play()
    elif game_state == "gameover":
        if buttons["menu"].collidepoint(pos):
            game_state = "menu"
            music.stop()
            reset_game()
