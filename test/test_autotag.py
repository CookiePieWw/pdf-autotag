import unittest

from pdfautotag import AutoTag, OpenAIClient, PDF

class TestAutoTag(unittest.IsolatedAsyncioTestCase):
    """test for AutoTag class"""
    def __init__(self, *args, **kwargs):
        super(TestAutoTag, self).__init__(*args, **kwargs)
        self.page = 15
        self.pdf_path = "test/data/test.pdf"
        self.autotag = AutoTag(PDF(self.pdf_path), OpenAIClient())
    
    async def test_get_tags(self):
        tags = await self.autotag.tag([15])
        self.assertEqual(len(tags), 2)
        self.assertEqual(len(tags[0]), 2)
        self.assertEqual(len(tags[1]), 2)
        self.assertEqual(tags[0][0], 1)
        self.assertEqual(tags[1][0], 2)
        
        