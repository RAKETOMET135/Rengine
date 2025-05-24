import pygame
from .input import Input
from typing import Callable
from enum import Enum

class HorizontalAlign(Enum):
    LEFT = 1,
    RIGHT = 2,
    CENTER = 3

class VerticalAlign(Enum):
    TOP = 1,
    BOTTOM = 2,
    CENTER = 3

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
        self._hover = False
    
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
    def __init__(self, text: str, text_size: int, text_color: tuple[int] = (255, 255, 255), font: str = None, x = 0, y = 0, 
                 horizontal_align: HorizontalAlign = None, vertical_align: VerticalAlign = None,
                 translation_x: int = 0, translation_y: int = 0):
        """
        Creates instance of TextLabel with text.

        Args:
            text (str): Text to display.
            text_size (str): Size of the displayed text.
            text_color (tuple[int]): Color of the displayed text.
            font (str): Optional path to font file.
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
            horizontal_align (HorizontalAlign): The horizontal alignment of TextLabel.
            vertical_align (VerticalAlign): The vertical alignment of TextLabel.
            translation_x (int): The distance on x axis that this element will move from origin.
            translation_y (int): The distance on y axis that this element will move from origin.
        """

        super().__init__(x, y)
        
        self.translation_x = translation_x
        self.translation_y = translation_y
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font_path = font
        self.font = pygame.font.Font(font, text_size)
        self.surface = self.font.render(text, False, text_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)

        self._main_rect = self.rect
        self.frame = None
        self.__align_applied = False

    def change_text(self, text: str = "", text_size: int = None) -> None:
        """
        Changes the TextLabel's text.

        Text can not be changed using text attribute.

        Args:
            text (str): Text to set as the new text.
            text_size (int): The new size of the text.
        """

        if text_size:
            self.text_size = text_size

        prev_rect_position: tuple[int] = self.rect.topleft

        self.text = text
        self.font = pygame.font.Font(self.font_path, self.text_size)
        self.surface = self.font.render(text, False, self.text_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = prev_rect_position

        self._main_rect = self.rect
        self.__align_applied = False
    
    def apply_alignment(self, parent_coords: tuple[int]) -> None:
        """
        Applies the horizontal alignment to the GuiElement. Called on first render.
        """

        match self.horizontal_align:
            case HorizontalAlign.LEFT:
                self._main_rect.x = parent_coords[0]
            case HorizontalAlign.RIGHT:
                self._main_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width
            case HorizontalAlign.CENTER:
                self._main_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2)
            case _:
                pass
        
        match self.vertical_align:
            case VerticalAlign.TOP:
                self._main_rect.y = parent_coords[1]
            case VerticalAlign.BOTTOM:
                self._main_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height
            case VerticalAlign.CENTER:
                self._main_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2)
            case _:
                pass

    def render(self, screen: pygame.display, is_mouse_on: bool, parent_coords: tuple[int]) -> None:
        """
        Renders the TextLabel onto screen.
        """

        if not self.__align_applied:
            self.__align_applied = True

            if self.horizontal_align or self.vertical_align:
                self.apply_alignment(parent_coords)

        screen.blit(self.surface, (self.rect.x + self.translation_x, self.rect.y + self.translation_y, self.rect.width, self.rect.height))

class TextInput(GuiElement):
    def __init__(self, text: str = "", placeholder_text: int = "", text_color: tuple[int] = (255, 255, 255), placeholder_text_color: tuple[int] = (200, 200, 200),
                 background_color: tuple[int] = (100, 100, 100), border_radius: int = 0, font: str = None, border_width: int = 0, border_color: tuple[int] = (0, 0, 0),
                 background_transparency: int = 0, text_size: int = 25, input_width: int = 150, input_height: int = 30,
                 horizontal_align: HorizontalAlign = None, vertical_align: VerticalAlign = None, translation_x: int = 0, translation_y: int = 0,
                x: int = 0, y: int = 0):
        """
        Creates instance of TextInput with placeholder text and a background.

        Args:
            text (str): Text that is already typed in the input.
            placeholder_text (str): Text to display when input is empty.
            text_color (tuple[int]): Color of the displayed text.
            placeholder_text_color (tuple[int]): Color of placeholder text.
            background_color (tuple[int]): Color of the background.
            border_radius (int): The border radius of TextInput.
            font (str): Optional path to font file.
            border_width (int): The width of the border.
            border_color (tuple[int]): The color of the border.
            background_transparency (int): The transparency of the background. (0 - 1)
            text_size (int): The size of the text.
            input_width (int): The width of the TextInput. This GuiElement is not sizing based on text.
            input_height (int): The height of TextInput. This GuiElement is not sizing based on text.
            horizontal_align (HorizontalAlign): The horizontal alignment of TextInput.
            vertical_align (VerticalAlign): The vertical alignment of TextInput.
            translation_x (int): The distance on x axis that this element will move from origin.
            translation_y (int): The distance on y axis that this element will move from origin.
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
        """

        super().__init__(x, y)

        self.x = x
        self.y = y

        self.translation_x = translation_x
        self.translation_y = translation_y
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

        self.background_transparency = int(255 - background_transparency * 255)
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.text = text
        self.placeholder_text = placeholder_text
        self.text_size = text_size
        self.text_color = text_color
        self.placeholder_text_color = placeholder_text_color
        self.font_path = font
        self.font = pygame.font.Font(self.font_path, self.text_size)
        self.background_color = background_color
        self.width = input_width
        self.height = input_height
        self.background_rect = pygame.rect.Rect(x, y, input_width, input_height)
        self.background_surface = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(self.background_surface, 
                        (self.background_color[0], self.background_color[1], self.background_color[2], self.background_transparency), 
                        (0, 0, self.background_rect.width, self.background_rect.height), 
                        border_radius=self.border_radius)
        self.border_rect = pygame.rect.Rect(self.background_rect.x - int(border_width/2),
                                            self.background_rect.y - int(border_width/2),
                                            self.background_rect.width + border_width,
                                            self.background_rect.height + border_width
                                            )

        self._main_rect = self.background_rect
        self._hover_cursor = pygame.SYSTEM_CURSOR_IBEAM
        self.frame = None
        self._input = text
        self.input_surface = None
        self.input_rect = None
        self.line_rect = pygame.rect.Rect(0, 0, 2, self.font.get_height())
        self.line_pos = -1
        self._update_text()
        self.placeholder_surface = self.font.render(self.placeholder_text, False, self.placeholder_text_color)
        self.placeholder_rect = self.placeholder_surface.get_rect()
        self.placeholder_rect.x = int(self.background_rect.x + self.background_rect.width/2 - self.placeholder_rect.width/2)
        self.placeholder_rect.y = int(self.background_rect.y + self.background_rect.height/2 - self.placeholder_rect.height/2)
        self.focused = False
        self.remove_delay = 0
        self.move_delay = 0
        self.line_blink_delay = 0

        self.__align_applied = False

    def _get_line_position(self) -> int:
        """
        Returns a position on x axis for line to position in string.

        Returns:
            int: X axis position in string based on line position.
        """

        move: int = 0

        for i in range(self.line_pos):
            if i > len(self.input) - 1:
                return move
            
            letter: str = self.input[i]
            size: tuple[int] = self.font.size(letter)

            move += size[0]

        return move

    def _change_line_pos_based_on_click(self, mouse_pos: tuple[int]) -> None:
        """
        Changes the line position index to mouse position letter.

        Args:
            mouse_pos (tuple[int]): The position of the mouse.
        """

        move: int = self.input_rect.x

        if mouse_pos[0] <= move:
            self.line_pos = 0

            return

        for i in range(len(self.input)):
            letter: str = self.input[i]
            size: tuple[int] = self.font.size(letter)

            if i < len(self.input) -1:
                next_letter: str = self.input[i + 1]
                next_size: tuple[int] = self.font.size(next_letter)

                if mouse_pos[0] > next_size[0] + move:
                    move += size[0]

                    continue
                else:
                    distance_1: int = abs(size[0] + move - mouse_pos[0])
                    distance_2: int = abs(next_size[0] + move - mouse_pos[0])

                    if distance_1 < distance_2:
                        self.line_pos = i + 1
                    else:
                        self.line_pos = i + 1
                    
                    break
            else:
                self.line_pos = -1

    def _update_text(self) -> None:
        """
        Changes the displayed text in TextInput and centers it.
        """

        self.input_surface = self.font.render(self.input, False, self.text_color)
        self.input_rect = self.input_surface.get_rect()
        self.input_rect.x = int(self.background_rect.x + self.background_rect.width/2 - self.input_rect.width/2)
        self.input_rect.y = int(self.background_rect.y + self.background_rect.height/2 - self.input_rect.height/2)

        if self.line_pos == -1:
            self.line_rect.x = self.input_rect.x + self.input_rect.width
        else:
            self.line_rect.x = self.input_rect.x + self._get_line_position()

        self.line_rect.y = self.input_rect.y

    def _update_placeholder(self) -> None:
        """
        Changes the displayd placeholder text in TextInput and centers it.
        """

        self.placeholder_surface = self.font.render(self.placeholder_text, False, self.placeholder_text_color)
        self.placeholder_rect = self.placeholder_surface.get_rect()
        self.placeholder_rect.x = int(self.background_rect.x + self.background_rect.width/2 - self.placeholder_rect.width/2)
        self.placeholder_rect.y = int(self.background_rect.y + self.background_rect.height/2 - self.placeholder_rect.height/2)
    
    def apply_alignment(self, parent_coords: tuple[int]) -> None:
        """
        Applies the horizontal alignment to the GuiElement. Called on first render.
        """

        if self.horizontal_align == HorizontalAlign.LEFT:
            parent_coords = (
                parent_coords[0] + int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.horizontal_align == HorizontalAlign.RIGHT:
            parent_coords = (
                parent_coords[0] - int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )
        
        match self.horizontal_align:
            case HorizontalAlign.LEFT:
                self._main_rect.x = parent_coords[0]
                self.border_rect.x = parent_coords[0] - int(self.border_width/2)
            case HorizontalAlign.RIGHT:
                self._main_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width
                self.border_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width - int(self.border_width/2)
            case HorizontalAlign.CENTER:
                self._main_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2)
                self.border_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2 - self.border_width/2)
            case _:
                pass
        
        if self.vertical_align == VerticalAlign.BOTTOM:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] - int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.vertical_align == VerticalAlign.TOP:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] + int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        match self.vertical_align:
            case VerticalAlign.TOP:
                self._main_rect.y = parent_coords[1]
                self.border_rect.y = parent_coords[1] - int(self.border_width/2)
            case VerticalAlign.BOTTOM:
                self._main_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height
                self.border_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height - int(self.border_width/2)
            case VerticalAlign.CENTER:
                self._main_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2)
                self.border_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2 - self.border_width/2)
        
        self._update_text()
        self._update_placeholder()

    def left_click(self) -> None:
        """
        Called by Gui on left click.
        """

        self.focused = True

    def render(self, screen: pygame.display, is_mouse_on: bool, parent_coords: tuple[int]) -> None:
        """
        Renders TextInput onto screen.
        """

        if not self.__align_applied:
            self.__align_applied = True

            if self.horizontal_align or self.vertical_align:
                self.apply_alignment(parent_coords)

        if Input.is_left_mouse_button_click() and not is_mouse_on:
            self.focused = False

        if self.focused:
            for char in Input._key_down_unicode:
                if char == "":
                    continue

                if self.line_pos == -1:
                    self._input += char
                else:
                    self._input = self._input[:self.line_pos] + char + self._input[self.line_pos:]
                    self.line_pos += 1
                    self.move_delay = 3
            
            if pygame.K_BACKSPACE in Input._key_downs_h and self.remove_delay <= 0:
                self.remove_delay = 3

                if self.line_pos == -1:
                    self._input = self._input[:-1]
                else:
                    self._input = self._input[:self.line_pos - 1] + self._input[self.line_pos:]
                    self.line_pos -= 1
                    self.move_delay = 3

            self._update_text()

            if Input.is_left_mouse_button_click():
                mouse_pos: tuple[int] = Input.mouse_pos

                self._change_line_pos_based_on_click(mouse_pos)

            if pygame.K_LEFT in Input._key_downs and self.move_delay <= 0:
                self.move_delay = 3
                
                if self.line_pos == -1:
                    self.line_pos = len(self.input) - 1
                else:
                    self.line_pos -= 1
            
            if pygame.K_RIGHT in Input._key_downs and self.move_delay <= 0:
                self.move_delay = 3

                if self.line_pos == -1:
                    self.line_pos = 0
                elif self.line_pos == len(self.input) - 1:
                    self.line_pos = -1
                else:
                    self.line_pos += 1
        
        self.remove_delay -= 1
        self.move_delay -= 1

        pygame.draw.rect(screen, self.border_color, (self.border_rect.x + self.translation_x, self.border_rect.y + self.translation_y, self.border_rect.width, self.border_rect.height), border_radius=self.border_radius, width=int(self.border_width))
        screen.blit(self.background_surface, (self.background_rect.x + self.translation_x, self.background_rect.y + self.translation_y, self.background_rect.width, self.background_rect.height))

        if self.input_surface and self.input_rect and self.input:
            screen.blit(self.input_surface, (self.input_rect.x + self.translation_x, self.input_rect.y + self.translation_y, self.input_rect.width, self.input_rect.height))

            if self.focused:
                if self.line_blink_delay <= 24:
                    pygame.draw.rect(screen, (255, 255, 255), self.line_rect)

                    if self.line_blink_delay <= 0:
                        self.line_blink_delay = 48
                
                self.line_blink_delay -= 1
        else:
            screen.blit(self.placeholder_surface, (self.placeholder_rect.x + self.translation_x, self.placeholder_rect.y + self.translation_y, self.placeholder_rect.width, self.placeholder_rect.height))

    @property
    def input(self) -> str:
        return self._input
    
    @input.setter
    def input(self, new_input: str) -> None:
        """
        Use this property to change input text.

        Args:
            new_input (str): The new input text to change to.
        """

        self._input = new_input
        self._update_text()

class TextButton(GuiElement):
    def __init__(self, text: str, text_size: int, text_color: tuple[int] = (255, 255, 255), background_color: tuple[int] = (100, 100, 100), 
                background_hover_color: tuple[int] = (150, 150, 150), hover_scale: float = 1, border_radius: int = 0,
                border_width: int = 0, border_color: tuple[int] = (0, 0, 0), background_transparency: float = 0, background_hover_transparency: float = 0,
                on_left_click: Callable = None, on_right_click: Callable = None, on_middle_click: Callable = None, on_hover_enter: Callable = None,
                on_hover_exit: Callable = None, horizontal_align: HorizontalAlign = None, vertical_align: VerticalAlign = None,
                translation_x: int = 0, translation_y: int = 0,
                font: str = None, x: int = 0, y: int = 0):
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
            on_hover_enter (Callable): Function that is called when TextButton is hovered.
            on_hover_exit (Callable): Function that is called when TextButton is unhovered.
            horizontal_align (HorizontalAlign): The horizontal alignment of TextLabel.
            vertical_align (VerticalAlign): The vertical alignment of TextLabel.
            translation_x (int): The distance on x axis that this element will move from origin.
            translation_y (int): The distance on y axis that this element will move from origin.
            font (str): Optional path to font file.
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
        """

        x += int(text_size/4)
        y += int(text_size/8)

        super().__init__(x, y)
        
        self.translation_x = translation_x
        self.translation_y = translation_y
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.on_middle_click = on_middle_click
        self.on_hover_enter = on_hover_enter
        self.on_hover_exit = on_hover_exit

        self.hover_scale = hover_scale
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
        
        self._font = pygame.font.Font(font, int(text_size))
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
        self.frame = None

        self.__align_applied = False

    def change_text(self, text: str = "", text_size: int = None) -> None:
        """
        Changes the TextButtons's text.

        Text can not be changed using text attribute.

        Args:
            text (str): Text to set as the new text.
            text_size (int): The new size of the text.
        """

        if text_size:
            self.text_size = text_size

        prev_rect_position: tuple[int] = self.rect.topleft

        self.text = text
        self.font = pygame.font.Font(self.font_path, self.text_size)
        self.surface = self.font.render(text, False, self.text_color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = prev_rect_position

        x = self.rect.left
        y = self.rect.top

        self.background_rect = pygame.rect.Rect(int(x - self.text_size/4), int(y - self.text_size/8), self.rect.width + int(self.text_size/2), self.rect.height + int(self.text_size/4))
        self.background_surface = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(self.background_surface, 
                            (self.background_color[0], self.background_color[1], self.background_color[2], self.background_transparency), 
                            (0, 0, self.background_rect.width, self.background_rect.height), 
                            border_radius=self.border_radius)

        self._background_hover_rect = pygame.rect.Rect(int(x - (self.text_size/4) * self.hover_scale), 
                                                       int(y - (self.text_size/8) * self.hover_scale), 
                                                       self.rect.width + int((self.text_size/2) * self.hover_scale), 
                                                       self.rect.height + int((self.text_size/4) * self.hover_scale))
        self._background_hover_surface = pygame.Surface(self._background_hover_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(self._background_hover_surface,
                         (self.background_hover_color[0], self.background_hover_color[1], self.background_hover_color[2], self.background_hover_transparency),
                         (0, 0, self._background_hover_rect.width, self._background_hover_rect.height),
                         border_radius=self.border_radius
                         )
        
        self._font = pygame.font.Font(self.font_path, int(self.text_size))
        self._surface = self._font.render(text, False, self.text_color)
        self._hover_rect = self._surface.get_rect()
        self._hover_rect.center = self._background_hover_rect.center

        self._border_rect = pygame.rect.Rect(self.background_rect.x - int(self.border_width/2),
                                             self.background_rect.y - int(self.border_width/2),
                                             self.background_rect.width + self.border_width,
                                             self.background_rect.height + self.border_width
                                             )
        
        self._border_hover_rect = pygame.rect.Rect(self._background_hover_rect.x - int(self.border_width/2),
                                                self._background_hover_rect.y - int(self.border_width/2),
                                                self._background_hover_rect.width + self.border_width,
                                                self._background_hover_rect.height + self.border_width
                                                )

        self._main_rect = self.background_rect
        self.__align_applied = False

    def left_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with LMB.
        """

        if self.on_left_click:
            self.on_left_click(self)
    
    def right_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with RMB.
        """

        if self.on_right_click:
            self.on_right_click(self)
    
    def middle_click(self) -> None:
        """
        This method is called by Gui handling when element clicked with MMB.
        """

        if self.on_middle_click:
            self.on_middle_click(self)

    def apply_alignment(self, parent_coords: tuple[int]) -> None:
        """
        Applies the horizontal alignment to the GuiElement. Called on first render.
        """

        if self.horizontal_align == HorizontalAlign.LEFT:
            parent_coords = (
                parent_coords[0] + int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.horizontal_align == HorizontalAlign.RIGHT:
            parent_coords = (
                parent_coords[0] - int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )

        match self.horizontal_align:
            case HorizontalAlign.LEFT:
                self._main_rect.x = parent_coords[0]
                self.rect.x = parent_coords[0] + int(self.text_size / 4)
                self._border_rect.x = parent_coords[0] - int(self.border_width / 2)
                self._background_hover_rect.x = parent_coords[0]
                self._hover_rect.x = parent_coords[0] + int(self.text_size / 4 + (self._background_hover_rect.width - self.background_rect.width) / 2)
                self._border_hover_rect.x = parent_coords[0] - int(self.border_width / 2)
            case HorizontalAlign.RIGHT:
                self._main_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width
                self.rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width + int(self.text_size / 4)
                self._border_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width - int(self.border_width / 2)
                self._background_hover_rect.x = parent_coords[0] + parent_coords[2] - self._background_hover_rect.width
                self._hover_rect.x = parent_coords[0] + parent_coords[2] - self._background_hover_rect.width + int(self.text_size / 4 + (self._background_hover_rect.width - self.background_rect.width) / 2)
                self._border_hover_rect.x = parent_coords[0] + parent_coords[2] - self._background_hover_rect.width - int(self.border_width / 2)
            case HorizontalAlign.CENTER:
                self._main_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2)
                self.rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2 + self.text_size / 4)
                self._border_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2 - self.border_width / 2)
                self._background_hover_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._background_hover_rect.width / 2)
                self._hover_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self.background_rect.width / 2 + self.text_size / 4)
                self._border_hover_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._background_hover_rect.width / 2 - self.border_width / 2)
            case _:
                pass
        
        if self.vertical_align == VerticalAlign.BOTTOM:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] - int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.vertical_align == VerticalAlign.TOP:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] + int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        match self.vertical_align:
            case VerticalAlign.TOP:
                self._main_rect.y = parent_coords[1]
                self.rect.y = parent_coords[1] + int(self.text_size / 8)
                self._border_rect.y = parent_coords[1] - int(self.border_width / 2)
                self._background_hover_rect.y = parent_coords[1]
                self._hover_rect.y = parent_coords[1] + int(self.text_size / 8 + (self._background_hover_rect.height - self.background_rect.height) / 2)
                self._border_hover_rect.y = parent_coords[1] - int(self.border_width / 2)
            case VerticalAlign.BOTTOM:
                self._main_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height
                self.rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height + int(self.text_size / 8)
                self._border_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height - int(self.border_width / 2)
                self._background_hover_rect.y = parent_coords[1] + parent_coords[3] - self._background_hover_rect.height
                self._hover_rect.y = parent_coords[1] + parent_coords[3] - self._background_hover_rect.height + int(self.text_size / 8 + (self._background_hover_rect.height - self.background_rect.height) / 2)
                self._border_hover_rect.y = parent_coords[1] + parent_coords[3] - self._background_hover_rect.height - int(self.border_width / 2)
            case VerticalAlign.CENTER:
                self._main_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2)
                self.rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2 + self.text_size / 8)
                self._border_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2 - self.border_width / 2)
                self._background_hover_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._background_hover_rect.height / 2)
                self._hover_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2 + self.text_size / 8)
                self._border_hover_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._border_hover_rect.height / 2)
            case _:
                pass

    def render(self, screen: pygame.display, is_mouse_on: bool, parent_coords: tuple[int]) -> None:
        """
        Renders the TextLabel onto screen.
        """

        if not self.__align_applied:
            self.__align_applied = True

            if self.horizontal_align or self.vertical_align:
                self.apply_alignment(parent_coords)

        if is_mouse_on:
            pygame.draw.rect(screen, self.border_color, (self._border_hover_rect.x + self.translation_x, self._border_hover_rect.y + self.translation_y, self._border_hover_rect.width, self._border_hover_rect.height), border_radius=self.border_radius, width=int(self.border_width))
            screen.blit(self._background_hover_surface, (self._background_hover_rect.x + self.translation_x, self._background_hover_rect.y + self.translation_y, self._background_hover_rect.width, self._background_hover_rect.height))
            screen.blit(self._surface, (self._hover_rect.x + self.translation_x, self._hover_rect.y + self.translation_y, self._hover_rect.width, self._hover_rect.height))

            if not self._hover:
                self._hover = True

                if self.on_hover_enter:
                    self.on_hover_enter(self)
        else:
            pygame.draw.rect(screen, self.border_color, (self._border_rect.x + self.translation_x, self._border_rect.y + self.translation_y, self._border_rect.width, self._border_rect.height), border_radius=self.border_radius, width=int(self.border_width))
            screen.blit(self.background_surface, (self.background_rect.x + self.translation_x, self.background_rect.y + self.translation_y, self.background_rect.width, self.background_rect.height))
            screen.blit(self.surface, (self.rect.x + self.translation_x, self.rect.y + self.translation_y, self.rect.width, self.rect.height))

            if self._hover:
                self._hover = False

                if self.on_hover_exit:
                    self.on_hover_exit(self)

class Frame(GuiElement):
    def __init__(self, x = 0, y = 0, width: int = 100, height: int = 100, background_color: tuple[int] = (255, 255, 255), background_transparency: float = 0,
                 border_radius: int = 0, border_width: int = 0, border_color: tuple[int] = (255, 255, 255),
                 horizontal_align: HorizontalAlign = None, vertical_align: VerticalAlign = None, translation_x: int = 0, translation_y: int = 0):
        """
        Creates instance of Frame class with background.

        Add GuiElements into frame for better workflow.

        Args:
            x (int): Position of GuiElement on x axis.
            y (int): Position of GuiElement on y axis.
            width (int): Frames's width.
            height (int): Frame's height.
            background_color (tuple[int]): Frame's background color.
            background_transparency (float): Frame's background transparency. (0 - 1)
            border_radius (int): Frame's border radius.
            border_width (int): Frame's border width.
            border_color (tuple[int]): Frame's border color.
            horizontal_align (HorizontalAlign): The horizontal alignment of TextLabel.
            vertical_align (VerticalAlign): The vertical alignment of TextLabel.
            translation_x (int): The distance on x axis that this element will move from origin.
            translation_y (int): The distance on y axis that this element will move from origin.
        """

        super().__init__(x, y)

        self.translation_x = translation_x
        self.translation_y = translation_y
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

        self.x = x + translation_x
        self.y = y + translation_y

        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.border_width = border_width
        self.border_color = border_color
        self.background_color = background_color
        self.background_transparency = int(255 - (background_transparency * 255))
        self.rect = pygame.rect.Rect(x + self.translation_x, y + self.translation_y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.rect(self.surface,
                         (self.background_color[0], self.background_color[1], self.background_color[2], self.background_transparency),
                         (0, 0, self.rect.width, self.rect.height),
                         border_radius=self.border_radius
                         )

        self._border_rect = pygame.rect.Rect(self.rect.x - int(border_width/2),
                                             self.rect.y - int(border_width/2),
                                             self.rect.width + border_width,
                                             self.rect.height + border_width
                                             )
        
        self._main_rect = self.rect
        self.__elements = []
        self.__align_applied = False
        self.frame = None
    
    def add_gui_element(self, gui_element) -> None:
        """
        Adds GuiElement into Frame. GuiElement will have (0, 0) on Frame's topleft corner.

        Args:
            gui_element (GuiElement): GuiElement to add to Frame.
        """

        self.__elements.append(gui_element)

        gui_element.frame = self
        
        gui_element._main_rect.topleft = (self.x + gui_element._main_rect.x, self.y + gui_element._main_rect.y)

        if hasattr(gui_element, "_background_hover_rect"):
            gui_element._background_hover_rect.topleft = (self.x + gui_element._background_hover_rect.x, self.y + gui_element._background_hover_rect.y)
        
        if hasattr(gui_element, "rect") and not type(gui_element) == TextLabel and not type(gui_element) == Frame:
            gui_element.rect.topleft = (self.x + gui_element.rect.x, self.y + gui_element.rect.y)
        
        if hasattr(gui_element, "_hover_rect"):
            gui_element._hover_rect.topleft = (self.x + gui_element._hover_rect.x, self.y + gui_element._hover_rect.y)
        
        if hasattr(gui_element, "_border_rect"):
            gui_element._border_rect.topleft = (self.x + gui_element._border_rect.x, self.y + gui_element._border_rect.y)
        
        if hasattr(gui_element, "border_rect"):
            gui_element.border_rect.topleft = (self.x + gui_element.border_rect.x, self.y + gui_element.border_rect.y)

        if hasattr(gui_element, "_border_hover_rect"):
            gui_element._border_hover_rect.topleft = (self.x + gui_element._border_hover_rect.x, self.y + gui_element._border_hover_rect.y)
        
        if hasattr(gui_element, "render_content"):
            gui_element.x = gui_element._main_rect.x
            gui_element.y = gui_element._main_rect.y
        
        if hasattr(gui_element, "input_surface"):
            gui_element._update_text()
            gui_element._update_placeholder()
    
    def _align_gui_element_to_frame(self, gui_element, move: tuple[int]) -> None:
        """
        Aligns thu GuiElement to frame and calls align on it.

        Args:
            gui_element (GuiElement): The GuiElement to align.
        """

        gui_element._main_rect.topleft = (gui_element._main_rect.x + move[0], gui_element._main_rect.y + move[1])

        if hasattr(gui_element, "_background_hover_rect"):
            gui_element._background_hover_rect.topleft = (gui_element._background_hover_rect.x + move[0], gui_element._background_hover_rect.y + move[1])
        
        if hasattr(gui_element, "rect") and not type(gui_element) == TextLabel and not type(gui_element) == Frame:
            gui_element.rect.topleft = (gui_element.rect.x + move[0], gui_element.rect.y + move[1])
        
        if hasattr(gui_element, "_hover_rect"):
            gui_element._hover_rect.topleft = (gui_element._hover_rect.x + move[0], gui_element._hover_rect.y + move[1])
        
        if hasattr(gui_element, "_border_rect"):
            gui_element._border_rect.topleft = (gui_element._border_rect.x + move[0], gui_element._border_rect.y + move[1])
        
        if hasattr(gui_element, "border_rect"):
            gui_element.border_rect.topleft = (gui_element.border_rect.x + move[0], gui_element.border_rect.y + move[1])
        
        if hasattr(gui_element, "_border_hover_rect"):
            gui_element._border_hover_rect.topleft = (gui_element._border_hover_rect.x + move[0], gui_element._border_hover_rect.y + move[1])
        
        if hasattr(gui_element, "render_content"):
            gui_element.x = gui_element._main_rect.x
            gui_element.y = gui_element._main_rect.y

            elements = gui_element.get_elements()

            for element in elements:
                gui_element._align_gui_element_to_frame(element, move)
        
        gui_element.apply_alignment((self.x, self.y, self.width, self.height))

    def get_elements(self) -> list:
        """
        Returns a list of all GuiElements in this Frame.

        Returns:
            list[GuiElement]: List of all Frame's GuiElements.
        """

        return self.__elements

    def remove_gui_element(self, gui_element) -> None:
        """
        Removes GuiElement from Frame if it was added.

        Args:
            gui_element (GuiElement): GuiElement to remove from Frame.
        """

        if gui_element in self.__elements:
            self.__elements.remove(gui_element)

            gui_element.frame = None
    
    def apply_alignment(self, parent_coords: tuple[int]) -> None:
        """
        Applies the horizontal alignment to the GuiElement. Called on first render.
        """

        move: tuple[int] = (self.x, self.y)

        if self.horizontal_align == HorizontalAlign.LEFT:
            parent_coords = (
                parent_coords[0] + int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.horizontal_align == HorizontalAlign.RIGHT:
            parent_coords = (
                parent_coords[0] - int(self.border_width / 2),
                parent_coords[1],
                parent_coords[2],
                parent_coords[3]
            )

        match self.horizontal_align:
            case HorizontalAlign.LEFT:
                self._main_rect.x = parent_coords[0] + self.translation_x
                self._border_rect.x = parent_coords[0] - int(self.border_width / 2) + self.translation_x
                self.x = parent_coords[0] + self.translation_x
            case HorizontalAlign.RIGHT:
                self._main_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width + self.translation_x
                self._border_rect.x = parent_coords[0] + parent_coords[2] - self._main_rect.width - int(self.border_width / 2) + self.translation_x
                self.x = parent_coords[0] + parent_coords[2] - self._main_rect.width + self.translation_x
            case HorizontalAlign.CENTER:
                self._main_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2) + self.translation_x
                self._border_rect.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2 - self.border_width / 2) + self.translation_x
                self.x = parent_coords[0] + int(parent_coords[2] / 2 - self._main_rect.width / 2) + self.translation_x
            case _:
                pass

        if self.vertical_align == VerticalAlign.BOTTOM:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] - int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        if self.vertical_align == VerticalAlign.TOP:
            parent_coords = (
                parent_coords[0],
                parent_coords[1] + int(self.border_width / 2),
                parent_coords[2],
                parent_coords[3]
            )
        
        match self.vertical_align:
            case VerticalAlign.TOP:
                self._main_rect.y = parent_coords[1] + self.translation_y
                self._border_rect.y = parent_coords[1] - int(self.border_width / 2) + self.translation_y
                self.y = parent_coords[1] + self.translation_y
            case VerticalAlign.BOTTOM:
                self._main_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height + self.translation_y
                self._border_rect.y = parent_coords[1] + parent_coords[3] - self._main_rect.height - int(self.border_width / 2) + self.translation_y
                self.y = parent_coords[1] + parent_coords[3] - self._main_rect.height + self.translation_y
            case VerticalAlign.CENTER:
                self._main_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2) + self.translation_y
                self._border_rect.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2 - self.border_width / 2) + self.translation_y
                self.y = parent_coords[1] + int(parent_coords[3] / 2 - self._main_rect.height / 2) + self.translation_y
            case _:
                pass
        
        move = (self.x - move[0], self.y - move[1])

        for element in self.__elements:
            self._align_gui_element_to_frame(element, move)
    
    def render(self, screen: pygame.display, is_mouse_on: bool, parent_coords: tuple[int]) -> None:
        """
        Renders the Frame onto screen.
        """

        if not self.__align_applied:
            self.__align_applied = True

            if self.horizontal_align or self.vertical_align:
                self.apply_alignment(parent_coords)

        pygame.draw.rect(screen, self.border_color, self._border_rect, border_radius=self.border_radius, width=int(self.border_width/2))
        screen.blit(self.surface, self.rect)
    
    def render_content(self, screen: pygame.display, left_click: bool, right_click: bool, middle_click: bool) -> None:
        """
        Renders the Frame's content onto screen.
        """

        self.__elements.sort(key=lambda gui_element: gui_element.z_index)

        to_display_cursor: int = pygame.SYSTEM_CURSOR_ARROW
        z_index_cursor_request: int = -999999999

        for element in self.__elements:
            if element.hidden:
                continue

            is_mouse_on: bool = False

            if pygame.rect.Rect(element._main_rect.x + element.translation_x, element._main_rect.y + element.translation_y, element._main_rect.width, element._main_rect.height).collidepoint(Input.mouse_pos):
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
            
            element.render(screen, is_mouse_on, (self.x, self.y, self.width, self.height))

            if hasattr(element, "render_content") and callable(getattr(element, "render_content")):
                cursor = element.render_content(screen, left_click, right_click, middle_click)

                if element.z_index >= z_index_cursor_request and not cursor == 0:
                    z_index_cursor_request = element.z_index
                    to_display_cursor = cursor
        
        return to_display_cursor

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

            if pygame.rect.Rect(element._main_rect.x + element.translation_x, element._main_rect.y + element.translation_y, element._main_rect.width, element._main_rect.height).collidepoint(Input.mouse_pos):
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
            
            element.render(screen, is_mouse_on, (0, 0, window_size[0], window_size[1]))

            if hasattr(element, "render_content") and callable(getattr(element, "render_content")):
                cursor = element.render_content(screen, left_click, right_click, middle_click)

                if element.z_index >= z_index_cursor_request and not cursor == 0:
                    z_index_cursor_request = element.z_index
                    to_display_cursor = cursor
        
        pygame.mouse.set_cursor(to_display_cursor)
        