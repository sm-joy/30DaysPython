import pygame

class Text:
    def __init__(self, 
                _text: str, 
                _font_size: int=36, 
                _font_path: str=None, 
                _color: tuple[int, int, int]=(255, 255, 255), 
                _bg_color: tuple[int, int, int] = None):

        self.text = _text
        self.color = _color
        self.bg_color = _bg_color
        self.font = pygame.font.Font(_font_path, _font_size) if _font_path else pygame.font.SysFont(None, _font_size)
        self.text_surface = self.font.render(self.text, True, self.color, self.bg_color)

    def set_text(self, _text: str) -> None:
        self.text = _text
        self.text_surface = self.font.render(self.text, True, self.color, self.bg_color)

    def set_color(self, _color: tuple[int, int]) -> None:
        self.color = _color
        self.text_surface = self.font.render(self.text, True, self.color, self.bg_color)

    def draw(self, _surface: pygame.Surface, _position: tuple[int, int]) -> None:
        text_rect = self.text_surface.get_rect(center=_position)
        _surface.blit(self.text_surface, text_rect)

class Button:
    def __init__(self, 
                _position: tuple[int, int], 
                _text: Text=None,
                _id: str=None,
                _image: pygame.Surface=None,
                _color: tuple[int, int, int] = None,
                _scale: float=1):

        self.position = _position
        self.id = _id
        if _text:
            self.text = _text
            self.rect = pygame.Rect(_position, _text.font.size(_text.text))
            self.image = None
            self.color = _color
        elif _image:
            self.image = pygame.transform.scale(_image, (int(_image.get_width() * _scale), int(_image.get_height() * _scale)))
            self.rect = self.image.get_rect(center=_position)
            self.text = None
            self.bg_color = None

    def draw(self, _surface: pygame.Surface) -> None:
        if self.image:
            _surface.blit(self.image, self.rect.topleft)
        elif self.text:
            pygame.draw.rect(_surface, self.color, self.rect)
            self.text.draw(_surface=_surface, _position=self.rect.center)

    def hover(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())
        
    def set_color(self, _color: tuple[int, int, int]):
        self.color = _color

    def is_pressed(self, _event: pygame.event) -> bool:
        return (_event.type == pygame.MOUSEBUTTONDOWN and self.hover())




        

        
