import unittest
import os

import fitz
from pdfautotag import PDF

class TestPDFTOC(unittest.TestCase):
    """test for PDF class"""
    def __init__(self, *args, **kwargs):
        """create a test PDF file"""
        super(TestPDFTOC, self).__init__(*args, **kwargs)
        self.tmpdir = "/tmp"
        self.test_pdf_path = os.path.join(self.tmpdir, "test.pdf")

        doc = fitz.Document()
        doc.new_page(-1, width=595, height=842)
        doc.new_page(-1, width=595, height=842)
        doc.save(self.test_pdf_path)
        if not os.path.exists(self.test_pdf_path):
            raise Exception("Failed to create test PDF file.")
        doc.close()

    def __del__(self):
        """remove the test PDF file"""
        os.remove(self.test_pdf_path)
        if os.path.exists(self.test_pdf_path):
            raise Exception("Failed to remove test PDF file.")

    def test_pdf_toc(self):
        """test PDF class"""
        pdf = PDF(self.test_pdf_path)
        self.assertEqual(pdf.get_toc(), [])
        pdf.add_toc(1, "Chapter 1", 1)
        pdf.add_toc(2, "Chapter 1.1", 1)
        pdf.add_toc(2, "Chapter 1.2", 1)
        self.assertEqual(pdf.get_toc(), [
            [1, "Chapter 1", 1],
            [2, "Chapter 1.1", 1],
            [2, "Chapter 1.2", 1],
        ])
