from random import randint
import pygame
from Settings import *
 
class Food:
    def __init__(self, _id, _x, _y, _color: tuple[int, int, int]=(255, 0, 0)) -> None:
        self.rect = pygame.Rect(_x, _y, FOOD_SIZE, FOOD_SIZE)
        self.id = _id
        self.color = _color



class Food_Manager:
    def __init__(self) -> None:
        self.last_id = 1
        self.las_spawned_time = 0
        self.foods = []

    def spawn(self) -> None:
        if len(self.foods) > 5:
            current_spawned_time = pygame.time.get_ticks()
            if current_spawned_time - self.las_spawned_time >= randint(3000, 7000):
                x = randint(0, WINDOW_WIDTH - FOOD_SIZE)
                y = randint(0, WINDOW_HEIGHT - FOOD_SIZE)
                self.foods.append(Food(_id=self.last_id, _x=x, _y=y))
                self.last_id += 1
                self.las_spawned_time = current_spawned_time

    def despawn(self, _id) -> None:
        for food in self.foods:
            if food.id == _id:
                self.foods.remove(food)
                break

    def draw(self, _surface) -> None:
        for food in self.foods:
            pygame.draw.rect(_surface, food.color, food.rect)

    def check_collision(self, _snake_rect: pygame.Rect) -> [None, int]:
        for food in self.foods:
            if food.rect.colliderect(_snake_rect):
                return food.id
        return None