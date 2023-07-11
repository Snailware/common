import pyautogui as pag
from time import sleep
from pathlib import Path

from pyperclip import paste

import PIL


class Autoclicker:
    def __init__(self, failsafe: bool = True, pause: float = 0.08) -> None:
        pag.FAILSAFE = failsafe
        pag.PAUSE = pause

    def find_and_click(
        self,
        image_path: Path,
        x_offset: int = 0,
        y_offset: int = 0,
        confidence: float = 0.9,
    ) -> None:
        failed_attempts = 0
        x, y = None, None
        while x == None or y == None:
            try:
                x, y = pag.locateCenterOnScreen(image_path, confidence=confidence)
            except:
                failed_attempts += 1
                sleep(0.1)
            if failed_attempts > 50:
                raise Exception("could not locate image on screen.")
        pag.moveRel(x_offset, y_offset)
        pag.click(x, y)

    def find_field_and_enter_string(
        self,
        input: str,
        image_path: Path,
        overwrite: bool = True,
        x_offset: int = 0,
        y_offset: int = 0,
        confidence: float = 0.9,
    ) -> None:
        self.find_and_click(
            image_path=image_path,
            x_offset=x_offset,
            y_offset=y_offset,
            confidence=confidence,
        )
        self.enter_string(input=input, overwrite=overwrite)

    def find_field_and_extract_string(
        self,
        image_path: Path,
        x_offset: int = 0,
        y_offset: int = 0,
        confidence: float = 0.9,
    ) -> str:
        self.find_and_click(
            image_path=image_path,
            x_offset=x_offset,
            y_offset=y_offset,
            confidence=confidence,
        )
        return self.extract_string()

    def enter_string(self, input: str, overwrite: bool = True) -> None:
        if overwrite:
            pag.hotkey("ctrl", "a")
            pag.press("backspace")
        pag.write(input)
        pag.press("enter")

    def extract_string(self) -> str:
        pag.hotkey("ctrl", "a")
        pag.hotkey("ctrl", "c")
        return paste()


if __name__ == "__main__":
    print("this file should not be run directly. it contains code used by other files.")
