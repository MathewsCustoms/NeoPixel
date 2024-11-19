def wave(color, wave_length, wait):
    """
    Creates a wave effect that moves down the strip and then back.
    
    Parameters:
    - color: Tuple, RGB color of the wave.
    - wave_length: Number of LEDs in the wave (odd number, 5 in this case).
    - wait: Delay between each frame.
    """
    center_brightness = 1.0  # Brightness of the center LED

    # Forward direction
    for position in range(num_pixels + wave_length):
        for i in range(num_pixels):
            # Calculate brightness based on distance from the wave's center
            distance = abs(i - position)
            if distance < wave_length // 2 + 1:
                brightness = max(0, center_brightness - (distance / (wave_length // 2 + 1)))
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels[i] = scaled_color
            else:
                pixels[i] = (0, 0, 0)  # Turn off LEDs outside the wave range
        pixels.show()
        time.sleep(wait)

    # Backward direction
    for position in range(num_pixels + wave_length, -wave_length, -1):
        for i in range(num_pixels):
            # Calculate brightness based on distance from the wave's center
            distance = abs(i - position)
            if distance < wave_length // 2 + 1:
                brightness = max(0, center_brightness - (distance / (wave_length // 2 + 1)))
                scaled_color = tuple(int(c * brightness) for c in color)
                pixels[i] = scaled_color
            else:
                pixels[i] = (0, 0, 0)  # Turn off LEDs outside the wave range
        pixels.show()
        time.sleep(wait)
