#!/usr/bin/env python3
import curses
import random
import time

def init_colors():
    """Initialize color pairs for the game"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score

def is_valid_move(key, current_direction):
    """Prevent snake from reversing direction"""
    if (key == curses.KEY_DOWN and current_direction == curses.KEY_UP) or \
       (key == curses.KEY_UP and current_direction == curses.KEY_DOWN) or \
       (key == curses.KEY_LEFT and current_direction == curses.KEY_RIGHT) or \
       (key == curses.KEY_RIGHT and current_direction == curses.KEY_LEFT):
        return False
    return True

def main(stdscr):
    # Setup initial game state
    curses.curs_set(0)      # Hide cursor
    stdscr.timeout(100)     # Refresh rate
    sh, sw = stdscr.getmaxyx()  # Screen height and width
    
    # Initialize colors
    init_colors()
    
    # Create border
    stdscr.border()
    
    # Create initial snake position (middle of screen)
    snake_y = sh // 2
    snake_x = sw // 4
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Create initial food position
    food = [sh // 2, sw // 2]
    stdscr.addch(food[0], food[1], 'O', curses.color_pair(2))
    
    # Initial direction (right)
    direction = curses.KEY_RIGHT
    
    # Initial score and level
    score = 0
    level = 1
    speed = 100
    
    # Display score and level
    score_text = f"Score: {score} | Level: {level}"
    stdscr.addstr(0, sw - len(score_text) - 1, score_text, curses.color_pair(3))
    
    # Draw initial snake
    for y, x in snake:
        stdscr.addch(y, x, '■', curses.color_pair(1))
    
    # Game loop
    # Game loop
    while True:
        # Get next key input (if available)
        next_key = stdscr.getch()
        
        # Update direction only if it's a valid move
        if next_key != -1 and is_valid_move(next_key, direction):
            direction = next_key
        
        # Randomly change snake direction occasionally (1% chance)
        if random.random() < 0.01:
            possible_directions = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
            # Filter out invalid moves (can't reverse direction)
            valid_directions = [d for d in possible_directions if is_valid_move(d, direction)]
            if valid_directions:
                direction = random.choice(valid_directions)
        # Calculate next position based on direction
        head_y, head_x = snake[0]
        if direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1
        
        # Check for exit key (q or Q)
        if next_key in [ord('q'), ord('Q')]:
            break
        
        # Insert new head
        snake.insert(0, [head_y, head_x])
        
        # Check if snake hit the border
        if (
            head_y >= sh - 1 or head_y <= 0 or 
            head_x >= sw - 1 or head_x <= 0
        ):
            if game_over(stdscr, sh, sw, score):
                # Restart the game
                stdscr.clear()
                return main(stdscr)
            break
        
        # Check if snake hit itself
        if snake[0] in snake[1:]:
            if game_over(stdscr, sh, sw, score):
                # Restart the game
                stdscr.clear()
                return main(stdscr)
            break
        
        # Check if snake ate the food
        if snake[0] == food:
            # Create new food
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake else None
            stdscr.addch(food[0], food[1], 'O', curses.color_pair(2))
            
            # Increase score and update level
            score += 10
            level = (score // 50) + 1
            speed = max(50, 100 - (level * 5))
            stdscr.timeout(speed)
            
            # Update score display
            score_text = f"Score: {score} | Level: {level}"
            stdscr.addstr(0, sw - len(score_text) - 1, ' ' * len(score_text))
            stdscr.addstr(0, sw - len(score_text) - 1, score_text, curses.color_pair(3))
        else:
            # Remove tail
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        stdscr.addch(snake[0][0], snake[0][1], '■', curses.color_pair(1))
        
        # Refresh the screen
        stdscr.refresh()

def game_over(stdscr, sh, sw, score):
    """Display game over screen"""
    stdscr.clear()
    game_over_text = "GAME OVER!"
    score_text = f"Final Score: {score}"
    quit_text = "Press Q to quit or SPACE to restart"
    
    stdscr.addstr(sh // 2, sw // 2 - len(game_over_text) // 2, game_over_text, curses.A_BOLD)
    stdscr.addstr(sh // 2 + 1, sw // 2 - len(score_text) // 2, score_text)
    stdscr.addstr(sh // 2 + 3, sw // 2 - len(quit_text) // 2, quit_text)
    stdscr.refresh()
    
    # Wait for user to press Q to quit or SPACE to restart
    stdscr.nodelay(False)  # Make getch() wait for input
    while True:
        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            return False  # Don't restart
        elif key == ord(' '):  # Spacebar
            return True   # Restart the game

def restart_game(stdscr):
    """Clear the screen and start a new game"""
    stdscr.clear()
    stdscr.refresh()
    main(stdscr)

if __name__ == "__main__":
    try:
        # Initialize curses and start the game
        curses.wrapper(main)
    except curses.error:
        print("Error: Terminal window too small. Please resize and try again.")
    finally:
        print("Thanks for playing Snake!")

