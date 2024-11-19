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
        return x * NUM_COLS + y
    else:
        return x * NUM_COLS + (NUM_COLS - 1 - y)

def clear_pixels():
    """
    Clears all pixels in the matrix.
    """
    pixels.fill((0, 0, 0))
    pixels.show()

def random_color():
    """
    Generates a random RGB color ensuring at least one component is 0.
    """
    components = [0, random.randint(100, 255), random.randint(100, 255)]
    random.shuffle(components)  # Shuffle to randomly place the 0
    return tuple(components)

# Effects
def drip(color, wait):
    max_distance = NUM_ROWS + NUM_COLS
    for distance in range(max_distance):
        for x in range(NUM_ROWS):
            for y in range(NUM_COLS):
                min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                if min_dist == distance:
                    pixels[get_pixel_index(x, y)] = color
        pixels.show()
        time.sleep(wait)
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
    center_brightness = 1.0
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
    clear_pixels()

def breathe(color, steps, pause):
    for b in range(steps):
        brightness = b / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(pause)
    for b in range(steps, -1, -1):
        brightness = b / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(pause)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def color_chase(color, wait):
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)
    clear_pixels()

def color_wipe(color, wait):
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    clear_pixels()

def blink(color, wait, times):
    for _ in range(times):
        pixels.fill(color)
        pixels.show()
        time.sleep(wait)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(wait)

def theater_chase(color, wait):
    """
    Theater chase effect where every third LED is lit, creating a marquee effect.
    """
    for cycle in range(10):  # Run for 10 cycles
        for offset in range(3):  # Offset for every third LED
            for i in range(NUM_PIXELS):
                if (i + offset) % 3 == 0:
                    pixels[i] = color
                else:
                    pixels[i] = (0, 0, 0)
            pixels.show()
            time.sleep(wait)

def tunnel_drip(color, fade_steps, max_distance, ring_interval):
    active_drips = []
    current_frame = 0
    start_time = time.time()
    while time.time() - start_time < 30:
        if current_frame % ring_interval == 0:
            active_drips.append(0)
        pixels.fill((0, 0, 0))
        for distance in active_drips:
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        brightness = max(0, 1 - (distance / max_distance))
                        fade_color = tuple(int(c * brightness) for c in color)
                        pixels[get_pixel_index(x, y)] = fade_color
        pixels.show()
        active_drips = [distance + 1 for distance in active_drips if distance < max_distance]
        current_frame += 1
        time.sleep(0.05)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Main Function
def main():
    effects = [
        lambda color: drip(color, 0.1),
        lambda color: wave(color, 5, 0.05),
        lambda color: breathe(color, 50, 0.02),
        lambda _: rainbow_cycle(0.001),
        lambda color: color_chase(color, 0.05),
        lambda color: color_wipe(color, 0.02),
        lambda color: blink(color, 0.5, 5),
        lambda color: theater_chase(color, 0.1),
        lambda color: tunnel_drip(color, fade_steps=10, max_distance=NUM_ROWS + NUM_COLS, ring_interval=4),
    ]

    while True:
        for effect in effects:
            color = random_color()
            print(f"Running effect: {effect.__name__ if hasattr(effect, '__name__') else 'Anonymous'} with color {color}")
            effect(color)

if __name__ == "__main__":
    main()
