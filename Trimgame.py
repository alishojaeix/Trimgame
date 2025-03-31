import pygame
import sys
import requests
from io import BytesIO
from PIL import Image

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Trivia Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Fonts
question_font = pygame.font.SysFont('Arial', 24)
option_font = pygame.font.SysFont('Arial', 20)
score_font = pygame.font.SysFont('Arial', 30)

# Game variables
score = 0
current_question = 0
game_over = False

# Trivia questions with online image URLs
questions = [
    {
        "question": "What is this animal?",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
        "options": ["Dog", "Cat", "Elephant", "Lion"],
        "correct": 1
    },
    {
        "question": "Which country's flag is this?",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/1200px-Flag_of_the_United_States.svg.png",
        "options": ["Canada", "United Kingdom", "United States", "Australia"],
        "correct": 2
    },
    {
        "question": "What is this famous landmark?",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/NYC_Empire_State_Building.jpg/640px-NYC_Empire_State_Building.jpg",
        "options": ["Eiffel Tower", "Empire State Building", "Big Ben", "Sydney Opera House"],
        "correct": 1
    }
]

# Load images from URLs
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize((400, 300))
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    except:
        # Fallback if image fails to load
        surface = pygame.Surface((400, 300))
        surface.fill(GRAY)
        return surface

# Load all question images
for q in questions:
    q["image"] = load_image_from_url(q["image_url"])

def draw_question():
    if current_question >= len(questions):
        return
    
    question = questions[current_question]
    
    # Draw question text
    question_text = question_font.render(question["question"], True, BLACK)
    screen.blit(question_text, (50, 50))
    
    # Draw image
    screen.blit(question["image"], (SCREEN_WIDTH//2 - 200, 100))
    
    # Draw options
    for i, option in enumerate(question["options"]):
        y_pos = 450 + i * 50
        pygame.draw.rect(screen, BLUE, (100, y_pos, 600, 40))
        option_text = option_font.render(option, True, WHITE)
        screen.blit(option_text, (120, y_pos + 10)))

def draw_score():
    score_text = score_font.render(f"Score: {score}/{len(questions)}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

def draw_game_over():
    screen.fill(WHITE)
    game_over_text = score_font.render("Game Over!", True, BLACK)
    final_score_text = score_font.render(f"Final Score: {score}/{len(questions)}", True, BLACK)
    restart_text = option_font.render("Press R to restart", True, BLACK)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 50))

def check_answer(selected_option):
    global score, current_question
    
    if questions[current_question]["correct"] == selected_option:
        score += 1
    
    current_question += 1
    if current_question >= len(questions):
        global game_over
        game_over = True

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if an option was clicked
            for i in range(len(questions[current_question]["options"])):
                option_rect = pygame.Rect(100, 450 + i * 50, 600, 40)
                if option_rect.collidepoint(mouse_pos):
                    check_answer(i)
        
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Reset game
                score = 0
                current_question = 0
                game_over = False
    
    if not game_over:
        draw_question()
        draw_score()
    else:
        draw_game_over()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
