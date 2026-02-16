import pygame
import random
import math

# --- 1. SET UP VARIABLES ---
pygame.init()

# Dimensions (w, h)
w, h = 1000, 600
canvas = pygame.display.set_mode((w, h))
pygame.display.set_caption("Coin Toss Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)  # Grass/Table color

# Game Variables
clock = pygame.time.Clock()
gravity = 0.9
bounce_factor = 0.5

# Load Images (Replace these with actual file paths if needed)
# For this example, we create placeholder circles if images aren't found
try:
    head_img = pygame.image.load("head_img.png")
    tail_img = pygame.image.load("tail_img.png")
    # Resize for consistency
    head_img = pygame.transform.scale(head_img, (100, 100))
    tail_img = pygame.transform.scale(tail_img, (100, 100))
except FileNotFoundError:
    print("Images not found. Using colored circles instead.")
    head_img = None
    tail_img = None

def draw_coin(surface, x, y, face):
    """Draws the coin image or a placeholder circle."""
    if face == "Heads":
        if head_img:
            surface.blit(head_img, (x - 50, y - 50))
        else:
            pygame.draw.circle(surface, (255, 215, 0), (int(x), int(y)), 50) # Gold
            font = pygame.font.Font(None, 36)
            text = font.render("H", True, BLACK)
            surface.blit(text, (x-10, y-10))
    else:
        if tail_img:
            surface.blit(tail_img, (x - 50, y - 50))
        else:
            pygame.draw.circle(surface, (192, 192, 192), (int(x), int(y)), 50) # Silver
            font = pygame.font.Font(None, 36)
            text = font.render("T", True, BLACK)
            surface.blit(text, (x-10, y-10))

# --- 2. CREATE ANIMATION LOOP ---
def toss_coin():
    running = True
    
    # Initial Coin State
    x, y = w // 2, h - 100
    y_velocity = -25  # Initial upward force (toss)
    x_velocity = random.choice([-2, 2]) # Slight drift left or right
    
    # Result (0 or 1)
    result = random.randint(0, 1) # 0 = Heads, 1 = Tails
    final_face = "Heads" if result == 0 else "Tails"
    
    # Animation State
    current_face = "Heads"
    flip_timer = 0
    bounces = 0
    max_bounces = 3
    is_tossing = True

    while running:
        canvas.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset / Re-toss
                    x, y = w // 2, h - 100
                    y_velocity = -25
                    x_velocity = random.choice([-2, 2])
                    result = random.randint(0, 1)
                    final_face = "Heads" if result == 0 else "Tails"
                    bounces = 0
                    is_tossing = True

        if is_tossing:
            # Physics: Apply Gravity
            y_velocity += gravity
            y += y_velocity
            x += x_velocity
            
            # Visual: Rapid flipping effect while in air
            flip_timer += 1
            if flip_timer % 5 == 0 and bounces < 2:
                current_face = "Tails" if current_face == "Heads" else "Heads"

            # Physics: Bounce logic
            if y >= h - 100: # Floor level
                y = h - 100
                if bounces < max_bounces:
                    y_velocity = -y_velocity * bounce_factor
                    bounces += 1
                else:
                    # Stop Animation
                    y_velocity = 0
                    x_velocity = 0
                    is_tossing = False
                    current_face = final_face # Reveal result

        # Draw Floor
        pygame.draw.rect(canvas, GREEN, (0, h-50, w, 50))
        
        # --- 3. DISPLAY RESULT ---
        draw_coin(canvas, x, y, current_face)
        
        # UI Text
        font = pygame.font.Font(None, 36)
        if not is_tossing:
            res_text = font.render(f"Result: {final_face}! Press SPACE to toss again.", True, BLACK)
            canvas.blit(res_text, (w//2 - 200, 50))
        else:
            hint_text = font.render("Tossing...", True, BLACK)
            canvas.blit(hint_text, (w//2 - 50, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    toss_coin()