import pygame


def create_main_surface():
    """
    Creates and returns the main application window (Surface).
    This surface acts as the back buffer we draw on.
    """
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)


def render_frame(surface):
    """
    Draws a single frame to the given surface and
    flips the back buffer to the front buffer.
    """
    # Define the circle properties
    color = (255, 0, 0)        # Red color (RGB)
    center = (512, 384)        # Center of the window
    radius = 50               # Radius in pixels

    # Draw a filled circle onto the surface
    pygame.draw.circle(surface, color, center, radius)

    # Copy the back buffer to the front buffer (double buffering)
    pygame.display.flip()


def main():
    """
    Entry point of the application.
    Initializes pygame, creates the window,
    renders a frame, and keeps the app alive.
    """
    # Initialize all pygame modules
    pygame.init()

    # Create the main window surface
    surface = create_main_surface()

    # Draw the circle once
    render_frame(surface)

    # Infinite loop to keep the application running
    while True:
        pass  # Event handling will be added later


# Manually start the program
main()
