import pygame
import sys
from board import Board
import sudoku_generator

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 149, 237)
TEXT_COLOR = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")


def create_button(screen, text, x, y, width, height, color, font):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return button_rect


def game_start_screen():
    screen.fill(BACKGROUND_COLOR)
    title_text = FONT.render("Welcome to Sudoku!", True, TEXT_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

    easy_button = create_button(screen, "Easy", 200, 200, 200, 50, BUTTON_COLOR, FONT)
    medium_button = create_button(screen, "Medium", 200, 300, 200, 50, BUTTON_COLOR, FONT)
    hard_button = create_button(screen, "Hard", 200, 400, 200, 50, BUTTON_COLOR, FONT)

    pygame.display.flip()

    return easy_button, medium_button, hard_button


def game_over_screen(win):
    screen.fill(BACKGROUND_COLOR)
    if win:
        message = "Game Won!"
    else:
        message = "Game Over"
    message_text = FONT.render(message, True, TEXT_COLOR)
    screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 300))

    if win:
        exit_button = create_button(screen, "Exit", 200, 400, 200, 50, BUTTON_COLOR, FONT)
        pygame.display.flip()
        return exit_button, None
    else:
        restart_button = create_button(screen, "Restart", 200, 400, 200, 50, BUTTON_COLOR, FONT)
        exit_button = create_button(screen, "Exit", 200, 500, 200, 50, BUTTON_COLOR, FONT)
        pygame.display.flip()
        return restart_button, exit_button


def main():
    running = True
    difficulty = None
    game_board = None
    opening_board = None
    selected_cell = None

    while running:
        if not game_board:
            easy_button, medium_button, hard_button = game_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        difficulty = "Easy"
                        solution_board, board_data = sudoku_generator.generate_sudoku(9, 30)
                        game_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, screen, "Easy")
                    elif medium_button.collidepoint(event.pos):
                        difficulty = "Medium"
                        solution_board, board_data = sudoku_generator.generate_sudoku(9, 40)
                        game_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, screen, "Medium")
                    elif hard_button.collidepoint(event.pos):
                        difficulty = "Hard"
                        solution_board, board_data = sudoku_generator.generate_sudoku(9, 50)
                        game_board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, screen, "Hard")

        elif game_board and game_board.is_full():
            if game_board.check_board():  # Game win
                exit_button, _ = game_over_screen(win=True)
            else:
                restart_button, exit_button = game_over_screen(win=False)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if exit_button and exit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        elif restart_button and restart_button.collidepoint(event.pos):
                            game_board = None
                            break
                else:
                    continue
                break

        else:
            screen.fill(BACKGROUND_COLOR)
            game_board.draw()

            reset_button = create_button(screen, "Reset", 50, 650, 100, 50, BUTTON_COLOR, FONT)
            restart_button = create_button(screen, "Restart", 250, 650, 100, 50, BUTTON_COLOR, FONT)
            exit_button = create_button(screen, "Exit", 450, 650, 100, 50, BUTTON_COLOR, FONT)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.collidepoint(event.pos):
                        game_board.reset_to_original()
                    elif restart_button.collidepoint(event.pos):
                        game_board = None
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    else:
                        clicked_cell = game_board.click(*event.pos)
                        if clicked_cell:
                            row, col = clicked_cell
                            selected_cell = (row, col)
                            game_board.select(row, col)
                elif event.type == pygame.KEYDOWN:
                    if selected_cell:
                        if event.key in range(pygame.K_1, pygame.K_9 + 1):
                            game_board.sketch(event.key - pygame.K_0)
                        elif event.key == pygame.K_RETURN:
                            game_board.finalize_number()

if __name__ == "__main__":
    main()