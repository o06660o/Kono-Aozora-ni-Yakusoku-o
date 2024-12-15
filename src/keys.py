from typing import Self
import pygame

from settings import BASE


class Keys:
    _instance = None
    key_press_time: dict[int, int] = {}
    key_release_time: dict[int, int] = {}

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def update(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.key_press_time[event.key] = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP:
            assert (
                event.key in self.key_press_time
            ), f"Class `Keys` does not receive KEYDOWN event for key {event.key} but received KEYUP event."
            del self.key_press_time[event.key]
            self.key_release_time[event.key] = pygame.time.get_ticks()

    def query(self, key: int) -> int:
        """
        Return the status of `key`.

        Parameters:
            key (int): The key to query.

        Returns:
            0: if the key is not pressed.
            1: if the key is clicked (pressed for less than `LONG_PRESS_TIME` milliseconds).
            2: if the key is held (pressed for more than or equal to `LONG_PRESS_TIME` milliseconds).
        """
        if key not in self.key_press_time:
            return 0
        else:
            if pygame.time.get_ticks() - self.key_press_time[key] < BASE.LONG_PRESS_TIME:
                return 1
            else:
                return 2
