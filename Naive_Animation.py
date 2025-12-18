import pygame


def create_main_surface():
    """
    Creates and returns the main application window (Surface).
    """
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)


def render_frame(surface, x):
    """
    Draws a single frame.
    The x-parameter determines the horizontal position of the circle.
    """
    # Circle properties
    color = (255, 0, 0)      # Red
    y = 384                  # Fixed vertical position (middle of the screen)
    radius = 50

    # Draw the circle at the given x-coordinate
    pygame.draw.circle(surface, color, (x, y), radius)

    # Show the back buffer on screen
    pygame.display.flip()


def main():
    """
    Entry point of the application.
    Animates a circle moving to the right.
    """
    pygame.init()

    # Create the window surface
    surface = create_main_surface()

    # Starting x-position of the circle
    x = 0

    # Main loop: runs forever
    while True:
        # Draw the current frame
        render_frame(surface, x)

        # Move the circle one pixel to the right
        x += 1


# Start the program
main()
