import os

import fitz
from PIL import Image

class PDF:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist")
        self.path = path
        self.pdf = fitz.open(path)

    def get_img(self, page_num: int) -> Image.Image:
        """Returns a PIL Image object of the page at page_num"""
        if page_num < 0 or page_num >= self.pdf.page_count:
            raise ValueError(f"Page number {page_num} is out of range")
        pixmap = self.pdf.load_page(page_num).get_pixmap()
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        return img

    def get_toc(self):
        """Returns the table of contents of the PDF"""
        return self.pdf.get_toc()

    def add_toc(self, lvl: int, title: str, page: int) -> None:
        """Add a new entry to the tail of the table of contents"""
        if lvl < 1 or lvl > 6:
            raise ValueError(f"Level {lvl} is out of range")
        if page < 0 or page >= self.pdf.page_count:
            raise ValueError(f"Page number {page} is out of range")

        cur_toc = self.pdf.get_toc()
        self.pdf.set_toc((cur_toc + [lvl, title, page]))

    def save(self, path: str) -> None:
        """Save the PDF to the given path"""
        if not os.path.exists(os.path.dirname(path)):
            raise FileNotFoundError(f"Directory {os.path.dirname(path)} does not exist")

        self.pdf.save(path)