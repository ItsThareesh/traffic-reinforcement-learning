import pygame

import ui.ui_constants
from utils.logger import logger
import random
from ui import ui_constants
from . import game_constants


class Car:
    def __init__(self, direction: str):
        self.ID = 0
        self.direction = direction
        self.color = random.choice(list(ui_constants.CAR_COLORS.values()))
        self.spawned = True
        # Assume left side driving... Then the right most lane is 0th index and 1st index is left to it
        self.lane = random.choice([0, 1])

        self._decide_direction()

    def _decide_direction(self):
        height = ui_constants.HEIGHT
        width = ui_constants.WIDTH
        center = ui_constants.CENTER

        lane_width_offset = ui_constants.LANE_WIDTH // 8
        grass_bos_size = ui_constants.GRASS_BOX_SIZE

        if self.direction == 'N':
            if self.lane == 0:
                self.x = grass_bos_size + lane_width_offset
                self.vy = game_constants.CAR_SPEED
            else:
                self.x = center - lane_width_offset
                self.vy = game_constants.CAR_SPEED * 1.25

            self.y = 0
            self.vx = 0

        elif self.direction == 'S':
            if self.lane == 0:
                self.x = width - grass_bos_size - lane_width_offset
                self.vy = -game_constants.CAR_SPEED
            else:
                self.x = center + lane_width_offset
                self.vy = -game_constants.CAR_SPEED * 1.25

            self.y = ui_constants.HEIGHT

            self.vx = 0

        elif self.direction == 'W':
            self.x = 0

            if self.lane == 0:
                self.y = height - grass_bos_size - lane_width_offset
                self.vx = game_constants.CAR_SPEED
            else:
                self.y = center + lane_width_offset
                self.vx = game_constants.CAR_SPEED * 1.25

            self.vy = 0

        elif self.direction == 'E':
            self.x = ui_constants.WIDTH

            if self.lane == 0:
                self.y = grass_bos_size + lane_width_offset
                self.vx = -game_constants.CAR_SPEED
            else:
                self.y = center - lane_width_offset
                self.vx = -game_constants.CAR_SPEED * 1.25

            self.vy = 0

        else:
            logger.fatal(f"Invalid direction: {self.direction}")
            raise

    def is_out_of_bounds(self):
        left_bound = 0 - game_constants.CAR_SIZE
        right_bound = ui_constants.WIDTH + game_constants.CAR_SIZE
        top_bound = 0 - game_constants.CAR_SIZE
        bottom_bound = ui_constants.HEIGHT + game_constants.CAR_SIZE

        if self.x < left_bound or self.x > right_bound or self.y < top_bound or self.y > bottom_bound:
            return True
        else:
            return False

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        car_offset = game_constants.CAR_SIZE // 2

        rect = pygame.Rect(self.x - car_offset, self.y - car_offset, game_constants.CAR_SIZE, game_constants.CAR_SIZE)
        pygame.draw.rect(screen, self.color, rect)
