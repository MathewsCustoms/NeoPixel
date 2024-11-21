def tunnel_drip_rainbow(fade_steps, max_distance, ring_interval, swirl_speed):
    """
    Forward tunnel drip with rainbow colors that swirl outward.
    
    Parameters:
    - fade_steps: Number of steps to fade out each ring.
    - max_distance: The maximum distance a drip can propagate.
    - ring_interval: Number of rings before starting a new drip.
    - swirl_speed: Phase offset to create a swirling effect.
    """
    active_drips = []
    current_frame = 0
    start_time = time.time()

    while True:
        # Add a new drip if enough rings have passed
        if current_frame % ring_interval == 0:
            active_drips.append(0)  # Start at the center (distance = 0)

        # Clear the matrix for the current frame
        pixels.fill((0, 0, 0))

        # Update and render each active drip
        for distance in active_drips:
            for x in range(NUM_ROWS):
                for y in range(NUM_COLS):
                    # Manhattan distance from the center
                    min_dist = min(abs(x - cx) + abs(y - cy) for cx, cy in CENTER)
                    if min_dist == distance:
                        # Generate a rainbow color based on the distance and frame
                        hue = (distance * 256 // max_distance + current_frame * swirl_speed) % 256
                        color = wheel(hue)

                        # Apply fading based on distance
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
