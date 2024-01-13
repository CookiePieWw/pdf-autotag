from PIL import Image
import base64
from io import BytesIO

from typing import List

from .gptclient import OpenAIClient
from .pdf import PDF

class AutoTag:
    def __init__(self, pdf: PDF, openai_client: OpenAIClient) -> None:
        self.pdf = pdf
        self.openai_client = openai_client
        self.model = "gpt-4-vision-preview"

    def display(self) -> None:
        pass

    async def tag(self, pages: List[int]):
        tags = []
        for i in pages:
            message = self._prompt(i)
            response = await self.openai_client.sendMessage(message, self.model)
            tags.append(eval(response))

        for tag, page in zip(tags, pages):
            try:
                self.pdf.add_toc(tag[0], tag[1], page)
            except Exception as e:
                print(f"Warning: failed to explain returning toc {tag}\n")
                print(str(e))

        return tags

    def _prompt(self, page: int):
        img_b64encoding = self._img_to_b64(self.pdf.get_img(page))
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You're a reader reading a pdf without the table of contents. You'd like to tag the pdf with the table of contents. Here's the image of the page you're reading:\n",
                    },
                    {
                        "type": "image",
                        "image": img_b64encoding,
                    },
                    {
                        "type": "text",
                        "text": "Does this image means a new section or a new subsection, or both?\n",
                    },
                    {
                        "type": "text",
                        "text": "You should answer as follows:\n",
                    },
                    {
                        "type": "text",
                        "text": "If the image means a new section or a new subsection, answer the section with python lists including [level, name of the content you recognized]\n",
                    },
                    {
                        "type": "text",
                        "text": "example: if the title of the section is \"Chapter 1 ABCDE\"\n",
                    },
                    {
                        "type": "text",
                        "text": "answer: [1, \"Chapter 1 ABCDE\"]\n",
                    },
                    {
                        "type": "text",
                        "text": "if a sub section, answer [2, \"Chapter 1 ABCDE\"]\n",
                    },
                    {
                        "type": "text",
                        "text": "if there's no section or subsection, answer None\n",
                    },
                    {
                        "type": "text",
                        "text": "Now, give me the python lists of the image I give you, following the rules above\n",
                    }
                ],
            },
        ]
        return message

    def _img_to_b64(self, img: Image.Image) -> str:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
