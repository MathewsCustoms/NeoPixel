import time
import board
import neopixel
import math
import random

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

# Utility Functions
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

def clear_pixels():
    """
    Clears all pixels in the matrix.
    """
    pixels.fill((0, 0, 0))
    pixels.show()

def random_color():
    """
    Generates a random RGB color.
    """
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Effects
def drip(color, wait):
    """
    Symmetric drip effect starting from the center and expanding evenly outward.
    """
    max_distance = NUM_ROWS + NUM_COLS
    for distance in range(max_distance):
        for x in range(NUM_ROWS):
            for y in range(NUM_COLS):
                min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                if min_dist == distance:
                    pixels[get_pixel_index(x, y)] = color
        pixels.show()
        time.sleep(wait)

        # Fade out the current ring
        for fade_step in range(10, -1, -1):
            fade_color = tuple(int(c * fade_step / 10) for c in color)
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        pixels[get_pixel_index(x, y)] = fade_color
            pixels.show()
            time.sleep(wait / 5)
    clear_pixels()

def wave(color, wave_length, wait):
    """
    Creates a wave effect that moves down the strip and then back.
    """
    center_brightness = 1.0  # Brightness of the center LED

    # Forward direction
    for position in range(NUM_PIXELS + wave_length):
        for i in range(NUM_PIXELS):
            x, y = divmod(i, NUM_COLS)
            distance = abs(i - position)
            if distance < wave_length // 2 + 1:
                brightness = max(0, center_brightness - (distance / (wave_length // 2 + 1)))
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels[get_pixel_index(x, y)] = scaled_color
            else:
                pixels[get_pixel_index(x, y)] = (0, 0, 0)
        pixels.show()
        time.sleep(wait)

    # Backward direction
    for position in range(NUM_PIXELS + wave_length, -wave_length, -1):
        for i in range(NUM_PIXELS):
            x, y = divmod(i, NUM_COLS)
            distance = abs(i - position)
            if distance < wave_length // 2 + 1:
                brightness = max(0, center_brightness - (distance / (wave_length // 2 + 1)))
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels[get_pixel_index(x, y)] = scaled_color
            else:
                pixels[get_pixel_index(x, y)] = (0, 0, 0)
        pixels.show()
        time.sleep(wait)

def tunnel_drip(color, fade_steps, max_distance, ring_interval):
    """
    Continuous tunnel drip effect with overlapping drips.
    """
    active_drips = []
    current_frame = 0

    start_time = time.time()
    while time.time() - start_time < 30:  # Run for 30 seconds
        # Add a new drip if enough rings have passed
        if current_frame % ring_interval == 0:
            active_drips.append(0)

        # Clear the matrix for the current frame
        pixels.fill((0, 0, 0))

        # Update and render each active drip
        for distance in active_drips:
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        brightness = max(0, 1 - (distance / max_distance))
                        fade_color = tuple(int(c * brightness) for c in color)
                        pixels[get_pixel_index(x, y)] = fade_color

        # Show the updated frame
        pixels.show()

        # Increment the distance of each drip
        active_drips = [distance + 1 for distance in active_drips if distance < max_distance]

        # Increment the frame counter
        current_frame += 1
        time.sleep(0.05)

    clear_pixels()

# Main function to cycle through effects
def main():
    effects = [
        lambda color: drip(color, 0.1),
        lambda color: wave(color, 5, 0.05),
        lambda color: tunnel_drip(color, fade_steps=10, max_distance=NUM_ROWS + NUM_COLS, ring_interval=4),
    ]

    while True:
        for effect in effects:
            color = random_color()
            print(f"Running effect: {effect.__name__} with color {color}")
            effect(color)

if __name__ == "__main__":
    main()
