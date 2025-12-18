import pygame


def create_main_surface():
    """
    Creates and returns the main application window (surface).
    """
    # Tuple representing width and height in pixels
    screen_size = (1024, 768)

    # Create window with given size and return it
    return pygame.display.set_mode(screen_size)


def main():
    """
    Entry point of the application.
    Initializes pygame, creates the window,
    and keeps the application alive.
    """
    # Initialize Pygame
    pygame.init()

    # Create the main window surface
    screen = create_main_surface()

    # Infinite loop to keep the application running
    while True:
        pass  # We'll handle events here later


# Manually call main since Python has no built-in main function
main()
