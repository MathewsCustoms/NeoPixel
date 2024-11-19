import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Color Wheel Function
def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

# Rainbow Cycle
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

# Blink Effect
def blink(color, wait, times):
    for _ in range(times):
        pixels.fill(color)
        pixels.show()
        time.sleep(wait)
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(wait)

# Breathing Effect (fixed)
def breathe(color, steps, pause):
    for b in range(steps):
        scale = b / steps
        scaled_color = tuple(int(c * scale) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(pause)
    for b in range(steps, -1, -1):
        scale = b / steps
        scaled_color = tuple(int(c * scale) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(pause)

# Color Chase
def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)

# Theater Chase
def theater_chase(color, wait):
    for j in range(10):
        for q in range(3):
            for i in range(0, num_pixels, 3):
                if (i + q) < num_pixels:
                    pixels[i + q] = color
            pixels.show()
            time.sleep(wait)
            for i in range(0, num_pixels, 3):
                if (i + q) < num_pixels:
                    pixels[i + q] = (0, 0, 0)

# Color Wipe
def color_wipe(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)

# Clear All Pixels
def clear_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()

# Main Function
def main():
    while True:
        print("Running rainbow cycle...")
        rainbow_cycle(0.001)
        clear_pixels()

        print("Blinking red...")
        blink((255, 0, 0), 0.5, 5)
        clear_pixels()

        print("Breathing blue...")
        breathe((0, 0, 255), 50, 0.02)
        clear_pixels()

        print("Chasing green...")
        color_chase((0, 255, 0), 0.05)
        clear_pixels()

        print("Theater chase white...")
        theater_chase((255, 255, 255), 0.1)
        clear_pixels()

        print("Wiping yellow...")
        color_wipe((255, 255, 0), 0.02)
        clear_pixels()

if __name__ == "__main__":
    main()
