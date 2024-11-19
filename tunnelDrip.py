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

def tunnel_drip(color, fade_steps, max_distance, ring_interval):
    """
    Continuous tunnel drip effect with overlapping drips.

    Parameters:
    - color: Tuple (R, G, B), the color of the drips.
    - fade_steps: Number of steps to fade out each ring.
    - max_distance: The maximum distance a drip can propagate.
    - ring_interval: Number of rings before starting a new drip.
    """
    active_drips = []  # List to track each drip's current ring
    current_frame = 0  # Frame counter for timing

    while True:
        # Add a new drip if enough rings have passed
        if current_frame % ring_interval == 0:
            active_drips.append(0)  # Start a new drip at ring 0

        # Clear the matrix for the current frame
        pixels.fill((0, 0, 0))

        # Update and render each active drip
        for drip_index, distance in enumerate(active_drips):
            # Step 1: Light up the current ring
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        # Calculate fade color for the ring
                        brightness = max(0, 1 - (distance / max_distance))
                        fade_color = tuple(int(c * brightness) for c in color)
                        pixels[get_pixel_index(x, y)] = fade_color

        # Show the updated frame
        pixels.show()

        # Step 2: Increment the distance of each drip
        active_drips = [distance + 1 for distance in active_drips if distance < max_distance]

        # Step 3: Increment the frame counter
        current_frame += 1

        # Add a small delay for smooth animation
        time.sleep(0.05)

# Main function to start the tunnel drip effect
def main():
    try:
        print("Running continuous tunnel drip effect...")
        tunnel_drip(color=(0, 0, 255), fade_steps=10, max_distance=NUM_ROWS + NUM_COLS, ring_interval=4)
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()

if __name__ == "__main__":
    main()
