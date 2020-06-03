from colorsys import rgb_to_hls
from dataclasses import dataclass
from typing import Dict, Union


@dataclass
class Colour:
    hex: str
    rgb: Dict[Union[str, int], int]
    hsl: Dict[Union[str, int], int]

    def __str__(self) -> str:
        return self.hex

    @staticmethod
    def hex_value_to_rgb_value(value: str) -> int:
        return int(Colour.bound_hex_value(value[0:2]), 16)

    @staticmethod
    def bound_hex_value(value: str) -> str:
        bound_value = ""
        for letter in value:
            if letter not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"}:
                bound_value += "f"
            else:
                bound_value += letter

        return bound_value

    @staticmethod
    def hex_to_rgb(hex_code: str) -> Dict[Union[str, int], int]:
        r = Colour.hex_value_to_rgb_value(value=hex_code[0:2])
        g = Colour.hex_value_to_rgb_value(value=hex_code[2:4])
        b = Colour.hex_value_to_rgb_value(value=hex_code[4:6])

        return {0: r, 1: g, 2: b, "red": r, "green": g, "blue": b}

    @staticmethod
    def hex_to_hsl(hex_code: str) -> Dict[Union[str, int], int]:
        rgb = Colour.hex_to_rgb(hex_code=hex_code)
        h, s, l = rgb_to_hls(r=rgb[0], g=rgb[1], b=rgb[2])

        return {0: h, 1: s, 2: l, "hue": h, "saturation": s, "luminance": l}

    @staticmethod
    def from_hex(hex_code: str) -> "Colour":
        hex_code = hex_code.strip("#").lstrip("0x")
        return Colour(
            hex=hex_code.lower(),
            rgb=Colour.hex_to_rgb(hex_code=hex_code),
            hsl=Colour.hex_to_hsl(hex_code=hex_code),
        )

    @staticmethod
    def bound_rgb_value(value: int) -> int:
        return max(0, min(255, value))

    @staticmethod
    def rgb_value_to_hex_value(value: int) -> str:
        hex_value = hex(Colour.bound_rgb_value(value=value)).replace('0x', '')
        return f"0{hex_value}" if len(hex_value) == 1 else hex_value

    @staticmethod
    def rgb_to_hex(red: int, green: int, blue: int) -> str:
        return (
            f"{hex(Colour.bound_rgb_value(value=red)).replace('0x', '')}"
            f"{hex(Colour.bound_rgb_value(value=green)).replace('0x', '')}"
            f"{hex(Colour.bound_rgb_value(value=blue)).replace('0x', '')}"
        )

    @staticmethod
    def rgb_to_hsl(red: int, green: int, blue: int) -> Dict[Union[str, int], int]:
        h, s, l = rgb_to_hls(
            r=Colour.bound_rgb_value(value=red),
            g=Colour.bound_rgb_value(value=green),
            b=Colour.bound_rgb_value(value=blue),
        )

        return {0: h, 1: s, 2: l, "hue": h, "saturation": s, "luminance": l}

    @staticmethod
    def from_rgb(red: int, green: int, blue: int) -> "Colour":
        return Colour(
            hex=Colour.rgb_to_hex(red=red, green=green, blue=blue),
            rgb={
                0: Colour.bound_rgb_value(value=red),
                1: Colour.bound_rgb_value(value=green),
                2: Colour.bound_rgb_value(value=blue),
                "red": Colour.bound_rgb_value(value=red),
                "green": Colour.bound_rgb_value(value=green),
                "blue": Colour.bound_rgb_value(value=blue),
            },
            hsl=Colour.rgb_to_hsl(red=red, green=green, blue=blue),
        )
