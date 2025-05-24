import pygame

class Input:
    mouse_pos: tuple[int] = (0, 0)
    pressed_keys: list[str] = []

    _events: list[pygame.event.Event] = []
    _lmb_d: bool = False
    _mmb_d: bool = False
    _rmb_d: bool = False
    _sumb_d: bool = False
    _sdmb_d: bool = False
    _lmb_u: bool = False
    _mmb_u: bool = False
    _rmb_u: bool = False
    _sumb_u: bool = False
    _sdmb_u: bool = False
    _lmb_c: bool = False
    _mmb_c: bool = False
    _rmb_c: bool = False
    _sumb_c: bool = False
    _sdmb_c: bool = False
    _lmb_h: bool = False
    _mmb_h: bool = False
    _rmb_h: bool = False
    _sumb_h: bool = False
    _sdmb_h: bool = False
    _lmb_d_h: bool = False
    _mmb_d_h: bool = False
    _rmb_d_h: bool = False
    _sumb_d_h: bool = False
    _sdmb_d_h: bool = False
    _key_downs: list = []
    _key_ups: list = []
    _key_downs_h: list = []
    _key_clicks: list = []
    _key_down_unicode: list = []
    
    @classmethod
    def is_left_mouse_button_down(cls) -> bool:
        """
        Returns True if left mouse button is down during game loop cycle.

        Returns:
            bool: True if left mouse button is down.
        """

        return cls._lmb_d
    
    @classmethod
    def is_left_mouse_button_up(cls) -> bool:
        """
        Returns True if left mouse button is up during game loop cycle.

        Returns:
            bool: True if left mouse button is up.
        """

        return cls._lmb_u
    
    @classmethod
    def is_left_mouse_button_click(cls) -> bool:
        """
        Returns True if left mouse button is clicked during game loop cycle.

        Returns:
            bool: True if left mouse button is clicked.
        """

        return cls._lmb_c
    
    @classmethod
    def is_left_mouse_button_held(cls) -> bool:
        """
        Returns True if left mouse button is held during game loop cycle.

        Returns:
            bool: True if left mouse button is held.
        """

        return cls._lmb_h

    @classmethod
    def is_middle_mouse_button_down(cls) -> bool:
        """
        Returns True if middle mouse button is down during game loop cycle.

        Returns:
            bool: True if middle mouse button is down.
        """

        return cls._mmb_d
    
    @classmethod
    def is_middle_mouse_button_up(cls) -> bool:
        """
        Returns True if middle mouse button is up during game loop cycle.

        Returns:
            bool: True if middle mouse button is up.
        """

        return cls._mmb_u
    
    @classmethod
    def is_middle_mouse_button_click(cls) -> bool:
        """
        Returns True if middle mouse button is clicked during game loop cycle.

        Returns:
            bool: True if middle mouse button is clicked.
        """

        return cls._mmb_c
    
    @classmethod
    def is_middle_mouse_button_held(cls) -> bool:
        """
        Returns True if middle mouse button is held during game loop cycle.

        Returns:
            bool: True if middle mouse button is held.
        """

        return cls._mmb_h
    
    @classmethod
    def is_right_mouse_button_down(cls) -> bool:
        """
        Returns True if right mouse button is down during game loop cycle.

        Returns:
            bool: True if right mouse button is down.
        """

        return cls._rmb_d
    
    @classmethod
    def is_right_mouse_button_up(cls) -> bool:
        """
        Returns True if right mouse button is up during game loop cycle.

        Returns:
            bool: True if right mouse button is up.
        """

        return cls._rmb_u
    
    @classmethod
    def is_right_mouse_button_click(cls) -> bool:
        """
        Returns True if right mouse button is clicked during game loop cycle.

        Returns:
            bool: True if right mouse button is clicked.
        """

        return cls._rmb_c

    @classmethod
    def is_right_mouse_button_held(cls) -> bool:
        """
        Returns True if right mouse button is held during game loop cycle.

        Returns:
            bool: True if right mouse button is held.
        """

        return cls._rmb_h
    
    @classmethod
    def is_scroll_up_down(cls) -> bool:
        """
        Returns True if scroll up is down during game loop cycle.

        Returns:
            bool: True if scroll up is down.
        """

        return cls._sumb_d
    
    @classmethod
    def is_scroll_up_up(cls) -> bool:
        """
        Returns True if scroll up is up during game loop cycle.

        Returns:
            bool: True if scroll up is up.
        """

        return cls._sumb_u
    
    @classmethod
    def is_scroll_up_click(cls) -> bool:
        """
        Returns True if scroll up is clicked during game loop cycle.

        Returns:
            bool: True if scroll up is clicked.
        """

        return cls._sumb_c
    
    @classmethod
    def is_scroll_up_held(cls) -> bool:
        """
        Returns True if scroll up is held during game loop cycle.

        Returns:
            bool: True if scroll up is held.
        """

        return cls._sumb_h

    @classmethod
    def is_scroll_down_down(cls) -> bool:
        """
        Returns True if scroll down is down during game loop cycle.

        Returns:
            bool: True if scroll down is down.
        """

        return cls._sdmb_d
    
    @classmethod
    def is_scroll_down_up(cls) -> bool:
        """
        Returns True if scroll down is up during game loop cycle.

        Returns:
            bool: True if scroll down is up.
        """

        return cls._sdmb_u
    
    @classmethod
    def is_scroll_down_click(cls) -> bool:
        """
        Returns True if scroll down is clicked during game loop cycle.

        Returns:
            bool: True if scroll down is clicked.
        """

        return cls._sdmb_c

    @classmethod
    def is_scroll_down_held(cls) -> bool:
        """
        Returns True if scroll down is held during game loop cycle.

        Returns:
            bool: True if scroll down is held.
        """

        return cls._sdmb_h
    
    @classmethod
    def is_key_down(cls, key_string) -> bool:
        """
        Returns True if key is down during game loop cycle.

        Returns:
            bool: True if key is down.
        """

        key_ord: int = ord(key_string)
        is_down: bool = key_ord in cls._key_downs

        return is_down

    @classmethod
    def is_key_up(cls, key_string) -> bool:
        """
        Returns True if key is up during game loop cycle.

        Returns:
            bool: True if key is up.
        """

        key_ord: int = ord(key_string)
        is_up: bool = key_ord in cls._key_ups

        return is_up
    
    @classmethod
    def is_key_held(cls, key_string) -> bool:
        """
        Returns True if key is held during game loop cycle.

        Returns:
            bool: True if key is held.
        """

        key_ord: int = ord(key_string)
        is_held: bool = cls.pressed_keys[key_ord]

        return is_held

    @classmethod
    def is_key_click(cls, key_string) -> bool:
        """
        Returns True if key is clicked during game loop cycle.

        Returns:
            bool: True if key is clicked.
        """

        key_ord: int = ord(key_string)
        is_clicked: bool = key_ord in cls._key_clicks

        return is_clicked

    @classmethod
    def _update_input(cls, events: list[pygame.event.Event], pressed_keys: list[str]) -> None:
        cls.mouse_pos = pygame.mouse.get_pos()
        cls.pressed_keys = pressed_keys
        cls._events = events

        cls._mmb_d = False
        cls._lmb_d = False
        cls._rmb_d = False
        cls._sumb_d = False
        cls._sdmb_d = False
        cls._lmb_u = False
        cls._mmb_u = False
        cls._rmb_u = False
        cls._sumb_u = False
        cls._sdmb_u = False
        cls._lmb_c = False
        cls._mmb_c = False
        cls._rmb_c = False
        cls._sumb_c = False
        cls._sdmb_c = False
        cls._key_downs = []
        cls._key_ups = []
        cls._key_clicks = []
        cls._key_down_unicode = []

        for event in cls._events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cls._lmb_d = True
                    cls._lmb_h = True
                    cls._lmb_d_h = True
                elif event.button == 2:
                    cls._mmb_d = True
                    cls._mmb_h = True
                    cls._mmb_d_h = True
                elif event.button == 3:
                    cls._rmb_d = True
                    cls._rmb_h = True
                    cls._rmb_d_h = True
                elif event.button == 4:
                    cls._sumb_d = True
                    cls._sumb_h = True
                    cls._sumb_d_h = True
                elif event.button == 5:
                    cls._sdmb_d = True
                    cls._sdmb_h = True
                    cls._sdmb_d_h = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    cls._lmb_h = False
                    cls._lmb_u = True

                    if cls._lmb_d_h:
                        cls._lmb_c = True
                    
                    cls._lmb_d_h = False
                elif event.button == 2:
                    cls._mmb_h = False
                    cls._mmb_u = True

                    if cls._mmb_d_h:
                        cls._mmb_c = True
                    
                    cls._mmb_d_h = False
                elif event.button == 3:
                    cls._rmb_h = False
                    cls._rmb_u = True

                    if cls._rmb_d_h:
                        cls._rmb_c = True
                    
                    cls._rmb_d_h = False
                elif event.button == 4:
                    cls._sumb_h = False
                    cls._sumb_u = True

                    if cls._sumb_d_h:
                        cls._sumb_c = True
                    
                    cls._sumb_d_h = False
                elif event.button == 5:
                    cls._sdmb_h = False
                    cls._sdmb_u = True

                    if cls._sdmb_d_h:
                        cls._sdmb_c = True
                    
                    cls._sdmb_d_h = False
            elif event.type == pygame.KEYDOWN:
                cls._key_downs.append(event.key)
                cls._key_downs_h.append(event.key)
                cls._key_down_unicode.append(event.unicode)
            elif event.type == pygame.KEYUP:
                cls._key_ups.append(event.key)
                
                if event.key in cls._key_downs_h:
                    cls._key_clicks.append(event.key)
                    cls._key_downs_h.remove(event.key)