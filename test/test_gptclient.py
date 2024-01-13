import unittest
import os

from pdfautotag import OpenAIClient

class TestOpenAIClient(unittest.IsolatedAsyncioTestCase):
    """test for OpenAIClient class"""
    def __init__(self, *args, **kwargs):
        super(TestOpenAIClient, self).__init__(*args, **kwargs)
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.assertFalse(self.api_key is None, "No API key available, please set the OPENAI_API_KEY environment variable")
        self.client = OpenAIClient()
        self.message = [
            {
                "role": "user",
                "content": "say 'hello' to me",
            },
        ]

    async def test_openai(self):
        """test connection to OpenAI API"""
        response = await self.client.sendMessage(self.message)
        print('\n\tResponse from openai client: ', response, '\n')
        self.assertTrue(response is not None, "OpenAI API connection failed")