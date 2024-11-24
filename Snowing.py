import time
import board
import neopixel
import random

# Matrix dimensions
NUM_ROWS = 10
NUM_COLS = 10
NUM_PIXELS = NUM_ROWS * NUM_COLS

# NeoPixel setup
pixel_pin = board.D21
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER
)

# Utility Functions
def get_pixel_index(x, y):
    """
    Converts 2D matrix coordinates (x, y) to the 1D NeoPixel index based on the zigzag layout:
    - Even rows (0-based index) go left-to-right.
    - Odd rows go right-to-left.
    """
    if x % 2 == 0:
        return x * NUM_COLS + y
    else:
        return x * NUM_COLS + (NUM_COLS - 1 - y)

def clear_pixels():
    """
    Clears all pixels in the matrix.
    """
    pixels.fill((0, 0, 0))
    pixels.show()

# Snow Effect
def snowing_effect():
    """
    Creates a snowing effect where lights fall from the top, stack at the bottom, and fill the matrix.
    Ensures no column is more than 2 higher than the shortest column.
    """
    # Initialize the snow stack matrix to track how full each column is
    snow_stack = [NUM_ROWS for _ in range(NUM_COLS)]  # Start with all rows open (highest row available)

    # Fill the bottom row with dim lights
    for y in range(NUM_COLS):
        pixels[get_pixel_index(NUM_ROWS - 1, y)] = (10, 10, 10)
    pixels.show()

    while True:
        # Check if the matrix is fully filled
        if all(snow_stack[y] == 0 for y in range(NUM_COLS)):
            print("Matrix is fully filled!")
            break

        # Find the current tallest and shortest columns
        max_height = NUM_ROWS - min(snow_stack)
        min_height = NUM_ROWS - max(snow_stack)

        # Limit column selection to those within the height constraint
        available_cols = [
            y for y in range(NUM_COLS)
            if snow_stack[y] > 0 and (NUM_ROWS - snow_stack[y]) <= min_height + 2
        ]
        if not available_cols:
            break

        # Choose a random column from the balanced available columns
        falling_col = random.choice(available_cols)

        # Simulate the falling snowflake from the top of the matrix
        for row in range(0, snow_stack[falling_col]):
            # Display the falling snowflake with a twinkling effect
            pixels[get_pixel_index(row, falling_col)] = (255, 255, 255)  # Bright white
            if row > 0:
                # Dim the previous position
                pixels[get_pixel_index(row - 1, falling_col)] = (0, 0, 0)
            pixels.show()
            time.sleep(0.2)  # Slower falling speed

        # Stop when the snowflake hits the stack
        row = snow_stack[falling_col] - 1
        snow_stack[falling_col] -= 1

        # Brighten the stacked snow
        brightness = min(255, 50 + (NUM_ROWS - snow_stack[falling_col]) * 20)
        for r in range(snow_stack[falling_col], NUM_ROWS):
            pixels[get_pixel_index(r, falling_col)] = (brightness, brightness, brightness)
        pixels.show()

# Main Function
def main():
    try:
        snowing_effect()
    finally:
        clear_pixels()

if __name__ == "__main__":
    main()
