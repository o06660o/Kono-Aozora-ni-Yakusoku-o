from openai import OpenAI
import pygame

from settings import ENV
from settings import NPC as NPC_SETTINGS
from utils import create_rect_hitbox_image


class NPC(pygame.sprite.Sprite):
    def __init__(
        self,
        scale: float,
        pos: tuple[int, int],
        groups,
        npc_type: str,
        sprite_type: str = "npc",
    ) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.image = create_rect_hitbox_image(
            scale,
            (
                NPC_SETTINGS.WIDTH * ENV.TILE_SIZE * scale,
                NPC_SETTINGS.HEIGHT * ENV.TILE_SIZE * scale,
            ),
        )

        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect
        try:
            self.client = OpenAI(
                base_url="http://10.15.88.73:5020/v1",
                api_key="ollama",  # required but ignored
            )
        except Exception as e:
            raise Exception(f"ERROR: OPENAI CLIENT FAILED TO INITIALIZE: {e}")
        self.displaying_message = "test message"
        self.init_message = NPC_SETTINGS.INIT_MESSAGE[npc_type]
        self.messages: list[dict] = self.init_message

    def fetch_message(self, new_message: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": new_message,
            }
        )
        try:
            response = self.client.chat.completions.create(
                model="llama3.2",
                messages=self.messages,  # pyright: ignore
            )
        except Exception as e:
            raise Exception(f"ERROR: OPENAI CLIENT FAILED TO INITIALIZE: {e}")
        assistant_reply = response.choices[0].message.content
        self.messages.append(
            {
                "role": "assistant",
                "content": assistant_reply,
            }
        )
        self.displaying_message = assistant_reply

    def clear_messages(self) -> None:
        self.messages = self.init_message
