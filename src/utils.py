import csv
import os

import pygame


def read_csv(path: str) -> list[list[str]]:
    """
    Parameters:
        path : str
            The relative path to the CSV file.
    """
    ret: list[list[str]] = []
    with open(path) as csv_file:
        for row in csv.reader(csv_file, delimiter=","):
            ret.append(list(row))
    assert ret, f"CSV file {path} is empty."
    return ret


SPPORTED = ("png",)


def read_images_as_list(scale: float, path: str) -> list[pygame.Surface]:
    """
    Read images from a folder and return them as a list.
    Supported image formats: PNG.
    Others formats will be ignored.

    Parameters:
        scale : float
            The global scale value of the game.
        path : str
            The relative path to the folder of images.
    """
    ret: list[pygame.Surface] = []
    for _, _, filenames in os.walk(path):
        for filename in sorted(filenames):
            _, extension_name = filename.rsplit(".", 1)
            if extension_name not in SPPORTED:
                continue
            image = pygame.image.load(os.path.join(path, filename)).convert_alpha()
            ret.append(
                pygame.transform.scale(
                    image, (int(image.get_width() * scale), int(image.get_height() * scale))
                )
            )
    assert ret, f"Folder {path} is empty."
    return ret


def read_images(scale: float, path: str) -> dict[str, pygame.Surface]:
    """
    Read images from a folder and return them as a dictionary.
    Supported image formats: PNG.
    Others formats will be ignored.

    Parameters:
        scale : float
            The global scale value of the game.
        path : str
            The relative path to the folder of images.
    """
    ret: dict[str, pygame.Surface] = {}
    for _, _, filenames in os.walk(path):
        for filename in sorted(filenames):
            basename, extension_name = filename.rsplit(".", 1)
            if extension_name not in SPPORTED:
                continue
            image = pygame.image.load(os.path.join(path, filename))
            image = pygame.transform.scale(
                image, (int(image.get_width() * scale), int(image.get_height() * scale))
            )
            ret[basename] = image
    assert ret, f"Folder {path} is empty."
    return ret


def create_rect_hitbox_image(
    scale: float,
    size: tuple[int | float, int | float],
    border_width: int = 8,
    color: tuple[int, int, int] | tuple[int, int, int, int] | int | str = (255, 255, 255),
) -> pygame.Surface:
    """
    Create a rectanglar hitbox image with a transparent center and colored border.

    Parameters:
        scale : float
            The global scale value of the game.
        size: tuple[int | float, int | float]
            The width `size[0]`, and height `size[1]` of the hitbox.
        border_width: int
            The width of the border.
            Default value is 8.
        color: tuple[int, int, int] | tuple[int, int, int, int] | int | str
            The color in RGB, RGBA format, or simply a string.
            Default value is (255, 255, 255).
    """
    image = pygame.Surface((size[0] * scale, size[1] * scale), pygame.SRCALPHA)
    image.fill((0, 0, 0, 0))  # a fully transparent background
    border_rect = pygame.Rect(
        0,
        0,
        image.get_width(),
        image.get_height(),
    )
    pygame.draw.rect(image, color, border_rect, border_width)
    return image


# TODO
def create_half_ellipse_hitbox_image(
    scale: float,
    A: float,
    B: float,
    precision: int = 5,
    border_width: int = 8,
    color: tuple[int, int, int] | tuple[int, int, int, int] | str = (255, 255, 255),
) -> list[pygame.Surface]:
    """
    Create a ellipse hitbox image with a transparent center and colored border, then return the right half of the ellipse.

    Parameters:
        scale : float
            The global scale value of the game.
        A: float
            The horizontal radius of the ellipse.
        B: float
            The vertical radius of the ellipse.
        precision: int
            The number of rectangles to approximate the ellipse.
            Default value is 5.
        border_width: int
            The width of the border.
            Default value is 8.
        color: tuple[int, int, int] | tuple[int, int, int, int] | str
            The color in RGB, RGBA format, or simply a string.
            Default value is (255, 255, 255).
    """
    pass
