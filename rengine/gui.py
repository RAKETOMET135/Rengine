import pygame
from .input import Input
from typing import Callable

class GuiElement:
    def __init__(self, x: int = 0, y: int = 0):
        """
        Creates instance of GuiElement with basic gui settings.

        Args:
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
        """

        self.x = x
        self.y = y
        self.hidden = False
        self.z_index = 0
        self._main_rect = None
        self._hover_cursor = None
    
    def adjust_draw_order(self, draw_order: int) -> None:
        """
        Adjusts the draw order for this GuiElement.

        Elements with higher order are rendered on top of elements with lower order.

        Args:
            draw_order (int): The draw order for this GuiElement.
        """

        self.z_index = draw_order
    
    def add_to_gui(self, gui) -> None:
        """
        Adds this GuiElement into gui.

        Args:
            gui (Gui): Gui to add GuiElement to.
        """

        gui.add_gui_element(self)

class TextLabel(GuiElement):
    def __init__(self, text: str, text_size: int, text_color: tuple[int] = (255, 255, 255), font: str = None, x = 0, y = 0):
        """
        Creates instance of TextLabel with text.

        Args:
            text (str): Text to display.
            text_size (str): Size of the displayed text.
            text_color (tuple[int]): Color of the displayed text.
            font (str): Optional path to font file.
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
        """

        super().__init__(x, y)
        
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font_path = font
        self.font = pygame.font.Font(font, text_size)
        self.surface = self.font.render(text, False, text_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)

        self._main_rect = self.rect
    
    def render(self, screen: pygame.display, is_mouse_on: bool) -> None:
        """
        Renders the TextLabel onto screen.
        """

        screen.blit(self.surface, self.rect)

class TextButton(GuiElement):
    def __init__(self, text: str, text_size: int, text_color: tuple[int] = (255, 255, 255), background_color: tuple[int] = (100, 100, 100), 
                background_hover_color: tuple[int] = (150, 150, 150), hover_scale: float = 1, text_hover_scale: float = 1, border_radius: int = 0,
                border_width: int = 0, border_color: tuple[int] = (0, 0, 0), background_transparency: float = 0, background_hover_transparency: float = 0,
                on_left_click: Callable = None, on_right_click: Callable = None, on_middle_click: Callable = None, 
                font: str = None, x = 0, y = 0):
        """
        Creates instance of TextButton with text and a background.

        Args:
            text (str): Text to display.
            text_size (str): Size of the displayed text.
            text_color (tuple[int]): Color of the displayed text.
            background_color (tuple[int]): Color of TextButton's background.
            background_hover_color (tuple[int]): Color of TextButton's background on hover.
            hover_scale (float): The scale of the button on hover.
            text_hover_scale (float): The scale of the button's text on hover.
            border_radius (int): The border radius of the TextButton.
            border_width (int): The width of the TextButton's border.
            border_color (int): The color of the TextButton's border.
            background_transparency (float): The transparency of TextButton's background. (0 - 1)
            background_hover_transparency (float): The transparency of TextButton's background on hover. (0 - 1)
            on_left_click (Callable): Function that is called when left clicked.
            on_right_click (Callable): Function that is called when right clicked.
            on_middle_click (Callable): Function that is called when middle clicked.
            font (str): Optional path to font file.
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
        """

        super().__init__(x, y)

        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.on_middle_click = on_middle_click

        self.background_transparency = int(255 - background_transparency * 255)
        self.background_hover_transparency = int(255 - background_hover_transparency * 255)
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font_path = font
        self.font = pygame.font.Font(font, text_size)
        self.surface = self.font.render(text, False, text_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)
        self.background_color = background_color
        self.background_hover_color = background_hover_color
        self.background_rect = pygame.rect.Rect(int(x - text_size/4), int(y - text_size/8), self.rect.width + int(text_size/2), self.rect.height + int(text_size/4))
        self.background_surface = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(self.background_surface, 
                            (self.background_color[0], self.background_color[1], self.background_color[2], self.background_transparency), 
                            (0, 0, self.background_rect.width, self.background_rect.height), 
                            border_radius=self.border_radius)

        self._background_hover_rect = pygame.rect.Rect(int(x - (text_size/4) * hover_scale), 
                                                       int(y - (text_size/8) * hover_scale), 
                                                       self.rect.width + int((text_size/2) * hover_scale), 
                                                       self.rect.height + int((text_size/4) * hover_scale))
        self._background_hover_surface = pygame.Surface(self._background_hover_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(self._background_hover_surface,
                         (self.background_hover_color[0], self.background_hover_color[1], self.background_hover_color[2], self.background_hover_transparency),
                         (0, 0, self._background_hover_rect.width, self._background_hover_rect.height),
                         border_radius=self.border_radius
                         )
        
        self._font = pygame.font.Font(font, int(text_size * text_hover_scale))
        self._surface = self._font.render(text, False, text_color)
        self._hover_rect = self._surface.get_rect()
        self._hover_rect.center = self._background_hover_rect.center

        self._border_rect = pygame.rect.Rect(self.background_rect.x - int(border_width/2),
                                             self.background_rect.y - int(border_width/2),
                                             self.background_rect.width + border_width,
                                             self.background_rect.height + border_width
                                             )
        
        self._border_hover_rect = pygame.rect.Rect(self._background_hover_rect.x - int(border_width/2),
                                                self._background_hover_rect.y - int(border_width/2),
                                                self._background_hover_rect.width + border_width,
                                                self._background_hover_rect.height + border_width
                                                )

        self._main_rect = self.background_rect
        self._hover_cursor = pygame.SYSTEM_CURSOR_HAND

    def left_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with LMB.
        """

        if self.on_left_click:
            self.on_left_click()
    
    def right_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with RMB.
        """

        if self.on_right_click:
            self.on_right_click()
    
    def middle_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with MMB.
        """

        if self.on_middle_click:
            self.on_middle_click()

    def render(self, screen: pygame.display, is_mouse_on: bool) -> None:
        """
        Renders the TextLabel onto screen.
        """

        if is_mouse_on:
            pygame.draw.rect(screen, self.border_color, self._border_hover_rect, border_radius=self.border_radius, width=self.border_width)
            screen.blit(self._background_hover_surface, self._background_hover_rect)
            screen.blit(self._surface, self._hover_rect)
        else:
            pygame.draw.rect(screen, self.border_color, self._border_rect, border_radius=self.border_radius, width=self.border_width)
            screen.blit(self.background_surface, self.background_rect)
            screen.blit(self.surface, self.rect)

class Gui:
    def __init__(self, scene):
        """
        Creates instance of Gui for scene. Scene can only have one Gui handler.

        Args:
            scene (Scene): Scene to append Gui to.
        """

        scene.gui = self

        self.__elements = []
    
    def add_gui_element(self, gui_element) -> None:
        """
        Adds GuiElement to Gui.

        Args:
            gui_element (GuiElement): GuiElement to add.
        """

        self.__elements.append(gui_element)
    
    def render(self, screen: pygame.display, delta_time: float, window_size: tuple[int], pressed_keys: pygame.key.ScancodeWrapper) -> None:
        """
        Called by Scene's render method. This method renders the Gui on screen.

        Args:
            screen (display): Pygame screen.
            delta_time (float): The time from last frame.
            window_size (tuple[int]): Size of Pygame window.
            pressed_keys (ScancodeWrapper): Currently pressed keys.
        """

        self.__elements.sort(key=lambda gui_element: gui_element.z_index)

        to_display_cursor: int = pygame.SYSTEM_CURSOR_ARROW
        z_index_cursor_request: int = -999999999

        left_click: bool = Input.is_left_mouse_button_click()
        right_click: bool = Input.is_right_mouse_button_click()
        middle_click: bool = Input.is_middle_mouse_button_click()

        for element in self.__elements:
            if element.hidden:
                continue
            
            is_mouse_on: bool = False

            if element._main_rect.collidepoint(Input.mouse_pos):
                if element._hover_cursor and element.z_index >= z_index_cursor_request:
                    z_index_cursor_request = element.z_index
                    to_display_cursor = element._hover_cursor
                
                if left_click:
                    if hasattr(element, "left_click") and callable(getattr(element, "left_click")):
                        element.left_click()
                
                if right_click:
                    if hasattr(element, "right_click") and callable(getattr(element, "right_click")):
                        element.right_click()
                
                if middle_click:
                    if hasattr(element, "middle_click") and callable(getattr(element, "middle_click")):
                        element.middle_click()
                
                is_mouse_on = True

            element.render(screen, is_mouse_on)
        
        pygame.mouse.set_cursor(to_display_cursor)
        