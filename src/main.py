# src/main.py

import pygame
import sys
import os

# --- Constants ---
# Screen dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
SKY_BLUE = (135, 206, 235)

# Tile properties
TILESIZE = 32

# Player properties
PLAYER_ACC = 0.6
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.7
PLAYER_JUMP = 18

# --- Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 40))
        # BUG FIX: Corrected "LUE" to "BLUE"
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # Your chosen starting position
        self.pos = pygame.math.Vector2(5 * TILESIZE, 8 * TILESIZE)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

    def jump(self):
        # Jump only if standing on a platform
        self.rect.y += 1
        # BUG FIX: Corrected "spritecollide" to "spritecollide"
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        
        # Get key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game:
    def __init__(self):
        # Initialize pygame and create window
        pygame.init()
        pygame.mixer.init() # For sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # Start a new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        # --- PROFESSIONAL FIX FOR FILE PATH ---
        game_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(game_dir, '..', 'assets')
        map_path = os.path.join(assets_dir, 'level1.map')

        # Load the map from the file
        with open(map_path, 'r') as f:
            lines = f.readlines()
        
        # PERFORMANCE FIX: Calculate level dimensions ONCE and store them
        self.level_width = len(lines[0].strip()) * TILESIZE
        self.level_height = len(lines) * TILESIZE
        
        # Create platforms based on the map
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '1':
                    p = Platform(self, x, y)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
        
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        
        # Check for collision with platforms only when falling
        if self.player.vel.y > 0:
            # BUG FIX: Corrected "spritecollide" to "spritecollide"
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # This prevents the player from "sticking" to the side of a platform
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(SKY_BLUE)

        # --- SCROLLING CAMERA LOGIC (your excellent addition) ---
        # Calculate camera offset to keep the player centered
        camera_offset_x = self.player.rect.centerx - WIDTH // 2
        camera_offset_y = self.player.rect.centery - HEIGHT // 2
        
        # Stop the camera from scrolling past the edges of the level
        if camera_offset_x < 0:
            camera_offset_x = 0
        if camera_offset_x > self.level_width - WIDTH:
            camera_offset_x = self.level_width - WIDTH
            
        if camera_offset_y < 0:
            camera_offset_y = 0
        if camera_offset_y > self.level_height - HEIGHT:
            camera_offset_y = self.level_height - HEIGHT

        # Draw all sprites, adjusting their position based on the camera offset
        for sprite in self.all_sprites:
            # Create a temporary rectangle for drawing
            draw_rect = sprite.rect.copy()
            # Adjust the x and y position
            draw_rect.x -= camera_offset_x
            draw_rect.y -= camera_offset_y
            # Draw the sprite at the new position
            self.screen.blit(sprite.image, draw_rect)

        pygame.display.flip()

g = Game()
while g.running:
    g.new()

pygame.quit()
sys.exit()