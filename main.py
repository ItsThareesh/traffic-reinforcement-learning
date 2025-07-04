import pygame
import sys
from ui.draw import draw_edge_green_boxes, draw_lanes, draw_stop_lines, draw_traffic_lights, show_fps, show_cars
from ui import ui_constants
from game.traffic_light import TrafficLight
from game.cars_spawner import CarsSpawner
from game.cars_controller import CarsController
from utils.logger import logger

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((ui_constants.WIDTH, ui_constants.HEIGHT))
pygame.display.set_caption("Traffic Intersection Simulation")
clock = pygame.time.Clock()


def main():
    running = True
    paused = False

    logger.info("Started App!")

    # Create Instances
    traffic_lights = [TrafficLight(d) for d in ['N', 'S', 'W', 'E']]
    spawner = CarsSpawner(max_cars=30)
    controller = CarsController(spawner.cars, traffic_lights)

    while running:
        screen.fill(ui_constants.UI_COLORS['BLACK'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    logger.info("Paused" if paused else "Resumed")

        # Draw UI elements
        draw_edge_green_boxes(screen)
        draw_lanes(screen)
        draw_stop_lines(screen)
        draw_traffic_lights(screen, traffic_lights)
        show_cars(screen, spawner.get_total_cars())

        if not paused:
            spawner.maybe_spawn_car(controller.lane_queues)

            # Switch Lights
            for tl in traffic_lights:
                tl.update()

            controller.update_cars(screen)

            # Show FPS
            show_fps(screen, clock)

            # Update the display
            pygame.display.flip()
            clock.tick(ui_constants.FPS)


    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
