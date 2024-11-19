import time
import board
import neopixel
import math

# Matrix dimensions
NUM_ROWS = 10
NUM_COLS = 10
NUM_PIXELS = NUM_ROWS * NUM_COLS
CENTER = [(4, 4), (4, 5), (5, 4), (5, 5)]  # 4-center LEDs for a 10x10 grid

# NeoPixel setup
pixel_pin = board.D21
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER
)

def get_pixel_index(x, y):
    """
    Converts 2D matrix coordinates (x, y) to the 1D NeoPixel index based on the zigzag layout:
    - Even rows (0-based index) go left-to-right.
    - Odd rows go right-to-left.
    """
    if x % 2 == 0:
        # Even rows go left to right
        return x * NUM_COLS + y
    else:
        # Odd rows go right to left
        return x * NUM_COLS + (NUM_COLS - 1 - y)

def drip(color, wait):
    """
    Symmetric drip effect starting from the center and expanding evenly outward.
    """
    # Max Manhattan distance from the center to any edge
    max_distance = NUM_ROWS + NUM_COLS

    # Step 1: Light up the 4 center LEDs
    for x, y in CENTER:
        pixels[get_pixel_index(x, y)] = color
    pixels.show()
    time.sleep(wait)

    # Fade out the 4 center LEDs
    for fade_step in range(10, -1, -1):  # Gradually decrease brightness
        fade_color = tuple(int(c * fade_step / 10) for c in color)
        for x, y in CENTER:
            pixels[get_pixel_index(x, y)] = fade_color
        pixels.show()
        time.sleep(wait / 5)

    # Step 2: Expand outward in concentric rings
    for distance in range(1, max_distance):
        # Step 2.1: Light up LEDs at the current ring
        for x in range(NUM_ROWS):
            for y in range(NUM_COLS):
                # Manhattan distance from the center region
                min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                if min_dist == distance:
                    pixels[get_pixel_index(x, y)] = color
        pixels.show()
        time.sleep(wait)

        # Step 2.2: Fade out the current ring
        for fade_step in range(10, -1, -1):  # Gradually decrease brightness
            fade_color = tuple(int(c * fade_step / 10) for c in color)
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        pixels[get_pixel_index(x, y)] = fade_color
            pixels.show()
            time.sleep(wait / 5)

    # Clear all pixels after the effect
    pixels.fill((0, 0, 0))
    pixels.show()

# Clear All Pixels
def clear_pixels():
    """
    Clears all pixels in the matrix.
    """
    pixels.fill((0, 0, 0))
    pixels.show()

# Main function to display the drip effect
def main():
    try:
        while True:
            print("Running drip effect...")
            drip((0, 0, 255), 0.1)  # Blue drip effect
            time.sleep(1)  # Pause before repeating
    finally:
        clear_pixels()

if __name__ == "__main__":
    main()
