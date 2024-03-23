import pygame
import Snake
from Settings import *
from sys import exit
import Food
import UI





class Core:
    def __init__(self, _event_manager=None):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.dt = 0
        self.snake_dir = "LEFT"
        pygame.display.set_caption(NAME)
 
        self.main_menu_init()
        self.game_loop_init()
        

    def update(self) -> None:
        pygame.display.flip()
        self.dt = self.clock.tick(FPS)/1000.0

    def destroy(self) -> None:
        pygame.quit()
        exit()
    
    def set_window_title(_title: str) -> None:
        pygame.display.set_caption(_title)

    def main_menu_init(self) -> None:
        self.menu_title_text = UI.Text(_text="Snake", _font_path=FONT_PATH, _font_size=170)
        
        self.menu_options_btn_text = UI.Text(_text="Options", _font_path=FONT_PATH, _color=(0,0,0), _font_size=60)
        self.menu_options_btn = UI.Button(_id="options", _position=(int((WINDOW_SIZE[0] - self.menu_options_btn_text.text_surface.get_width())/2), 330), _text=self.menu_options_btn_text, _color=(255,255,255))

        self.menu_quit_btn_text = UI.Text(_text="Quit", _font_path=FONT_PATH, _color=(0,0,0), _font_size=60)
        self.menu_quit_btn = UI.Button(_id="quit", _position=(int((WINDOW_SIZE[0] - self.menu_quit_btn_text.text_surface.get_width())/2), 430), _text=self.menu_quit_btn_text, _color=(255,255,255))
        
        self.menu_start_btn_text = UI.Text(_text="Start", _font_path=FONT_PATH, _color=(0,0,0), _font_size=60)
        self.menu_start_btn = UI.Button(_id="start", _position=(int((WINDOW_SIZE[0] - self.menu_start_btn_text.text_surface.get_width())/2), 230), _text=self.menu_start_btn_text, _color=(255,255,255))

        self.menu_btns = [self.menu_options_btn, self.menu_quit_btn, self.menu_start_btn]
        self.menu_btns_text = [self.menu_options_btn_text, self.menu_quit_btn_text,  self.menu_start_btn_text]

    def main_menu(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.destroy()
        
            for btn in self.menu_btns:
                if btn.is_pressed(_event=event):
                    if btn.id == "quit":
                        self.quit()
                    elif btn.id == "start":
                        return "Game"
                    elif btn.id == "options":
                        return "Options"

        self.window.fill((80, 80, 80))
        self.menu_title_text.draw(self.window, (int(WINDOW_SIZE[0] / 2), 100))
        
        for i, btn in enumerate(self.menu_btns):
            self.menu_btns_text[i].set_color((80, 80, 80) if btn.hover() else (0, 0, 0))
            btn.draw(self.window)

        return "Menu"

    
    def game_loop_init(self) -> None:
        #maye slower
            # self.keys = {
            #     "UP": (pygame.K_UP, pygame.K_w),
            #     "DOWN": (pygame.K_DOWN, pygame.K_a),
            #     "LEFT": (pygame.K_LEFT, pygame.K_s),
            #     "RIGHT": (pygame.K_RIGHT, pygame.K_d)
            # }
        self.snake = Snake.Snake()
        self.snake.add_seg()
        self.food= Food.Food_Manager()


    def game_loop(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.destroy()
            elif event.type == pygame.KEYDOWN:
                if CONTROL == "Arrow":
                    #maybe slower
                        # for key in self.keys:
                        #     if event.key == self.keys[key][0]:
                        #         self.snake_dir = key
                    if event.key == pygame.K_UP:
                        self.snake_dir = "UP"
                    elif event.key == pygame.K_DOWN:
                        self.snake_dir = "DOWN"
                    elif event.key == pygame.K_LEFT:
                        self.snake_dir = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        self.snake_dir = "RIGHT"
                elif CONTROL == "WSAD":
                    if event.key == pygame.K_w:
                        self.snake_dir = "UP"
                    elif event.key == pygame.K_s:
                        self.snake_dir = "DOWN"
                    elif event.key == pygame.K_a:
                        self.snake_dir = "LEFT"
                    elif event.key == pygame.K_d:
                        self.snake_dir = "RIGHT"
        
        self.snake.move(_dir=self.snake_dir, _dt=self.dt)
        self.food.spawn()
        food_id = self.food.check_collision(_snake_rect=self.snake.seggs[0].rect)
        if food_id: # is collision successfull
            self.food.despawn(_id=food_id)
            self.snake.add_seg()
        self.window.fill((0, 0, 0))
        self.food.draw(_surface=self.window)
        self.snake.draw(_surface=self.window)

        return "Game"

    def options_menu(self)-> str:
        return "Options"





