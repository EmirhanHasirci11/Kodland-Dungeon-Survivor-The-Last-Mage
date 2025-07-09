# Dungeon Survivor: The Last Mage 🧙‍♂️🔥

**Dungeon Survivor: The Last Mage** is a 2D roguelike game built entirely with **Pygame Zero**, following strict development constraints. The player controls a mage who must survive waves of monsters while casting fireballs, avoiding damage, and managing health and score.

## 🎮 Gameplay Overview

- Move the mage using **WASD** or **Arrow Keys**
- Click to shoot fireballs at incoming enemies
- Face off against two enemy types: **Ghosts** and **Cyclops**
- Ghosts have 1 HP / Cyclops have 2 HP
- Lose health when touched by enemies
- Earn points by eliminating them
- If your health drops to 0 → Game Over
- Return to **Main Menu** and restart at any time

---

## 📋 Features

✅ Main Menu with:
- Start Game  
- Sound ON/OFF Toggle  
- Quit Button  

✅ In-Game:
- OOP-based character and enemy logic  
- Sprite animation for all entities (idle and walk/fly)  
- Click-to-fire projectile system  
- Health and Score tracking  
- Background music and sound effects  
- Frame-based spawn and fire rate mechanics (no time module)  
- Game Over screen with "Return to Menu" button  
- **Screen boundaries enforced**: Characters cannot go outside the screen  

---

## 📷 Sprites

| Character        | Preview                  |
|------------------|---------------------------|
| **Mage (Player)**| ![Mage](https://github.com/user-attachments/assets/bc567b46-e39a-4200-8284-e7dd6d6c0630) |
| **Ghost**        | ![Ghost](https://github.com/user-attachments/assets/db7f8abc-349e-4f57-89af-2c5fb03a0d29) |
| **Cyclops**      | ![Cyclops](https://github.com/user-attachments/assets/a4564330-58b9-46f2-9c0b-e50599494ad9) |

_Replace the placeholder links above with your actual image URLs._

All sprites are animated using 2–4 frame sequences for idle and movement states. You can extend this further with additional visual effects.

---

## 🔊 Sound & Music

- `mage_fire_sound.wav`: Plays when casting a fireball  
- `enemy_death_voice.wav`: Plays when an enemy is defeated  
- `game_over.wav`: Plays when the player loses  
- `game_level_music.wav`: Background music during gameplay

All sound files are stored under the `/sounds` directory and are in `.wav` format.
