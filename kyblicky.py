import pygame
import serial
import os

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
IMAGE_WIDTH = 50
IMAGE_HEIGHT = 50
LINE_HEIGHT = WINDOW_HEIGHT - IMAGE_HEIGHT * 2
TEAMS_COUNT = 4
GROUPS_COUNT = 4
LINE_POINTS = 100
POINTS_ADDED = [0.3, 0.3, 0.3, 0.3]
POINTS_SUBTRACTED = [2, 2, 2, 2]

SEGMENT_WIDTH = WINDOW_WIDTH / TEAMS_COUNT / GROUPS_COUNT

POINTS = [[LINE_POINTS for _ in range(GROUPS_COUNT)] for _ in range(TEAMS_COUNT)]

ser = serial.Serial("/dev/ttyUSB0", 9600)

# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

# Initialize Pygame
pygame.init()

# Set up the display window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), display=1)

pygame.display.set_caption("Kyblicky")

# Load the images (You need to replace the paths with your image files)
image_paths = [
    "bucket-green.png",
    "bucket-red.png",
    "bucket-blue.png",
    "bucket-yellow.png",
]

images = [pygame.image.load(image_path) for image_path in image_paths]
images = [pygame.transform.scale(image, (SEGMENT_WIDTH, SEGMENT_WIDTH)) for image in images]


def draw_buckets():
    window.fill((255, 255, 255))
    for t in range(TEAMS_COUNT):
        x_start = (WINDOW_WIDTH / TEAMS_COUNT) * t
        for b in range(GROUPS_COUNT):
            x = x_start + SEGMENT_WIDTH * b
            if POINTS[t][b] > 0:
                y = LINE_HEIGHT - (LINE_HEIGHT / LINE_POINTS) * POINTS[t][b]
                window.blit(images[t], (x, y))
            pygame.draw.line(window, (0, 0, 0), (x + SEGMENT_WIDTH / 2, 0),
                             (x + SEGMENT_WIDTH / 2, LINE_HEIGHT), 2)


def count_points():
    while ser.inWaiting() > 0:
        rec = ser.readline()
        # print(rec)
        # return
        team = int(rec.decode('utf-8').strip())
        group = POINTS[team].count(0)
        if group >= GROUPS_COUNT:
            continue
        for t in range(TEAMS_COUNT):
            if t == team:
                continue
            if POINTS[t][group] == 0:
                continue
            POINTS[t][group] += POINTS_ADDED[group]
            if POINTS[t][group] > LINE_POINTS:
                POINTS[t][group] = LINE_POINTS
        POINTS[team][group] -= POINTS_SUBTRACTED[group]
        if POINTS[team][group] <= 0:
            POINTS[team][group] = 0
            print(f"Team {team} {image_paths[team]} finished group {group}")
        print(POINTS)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # print(POINTS)
    try:
        count_points()
    except Exception as e:
        print(e)
    # count_points()
    draw_buckets()
    # Update the display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
