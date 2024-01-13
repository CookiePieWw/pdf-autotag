# PDF Auto-tagger

:warning: The repo is completely useless. Do not use it anyway.

Since I've been tired of creating table of contents (TOC) manually for *Real Analysis*, I tried to automatically create TOC for books with the help of the GPT4's vision model: gpt4-vision-preview. It's actually an OCR task but we need to recognize the TOC part like 'Chapter 1.1 ...' after OCR, so I think it will be much simpler if GPT4 can directly create TOC.

But it seems the model cannot recognize the TOC and yield "Please note that the actual name of the chapter is not provided due to the image's quality." or something else, complaining about the poor quality of the image. It's as expected since I'm not convinced that AI can do such a delicate job.

There are still something I learned: a successful client to connect to OpenAI and some unit tests. I tried to use pyproject.toml to organize the repo but after STFW I think the toml file is used for packaging instead of organizing the project.

## Useful Codes

1. A very simple wrapper for TOC of pdfs using fitz: [pdf.py](./pdfautotag/pdf.py)
2. Client to connect to OpenAI: [gptclient.py](./pdfautotag/gptclient.py)
3. Unittests: [Test](./test)

## Some other problems

1. I cannot connect to OpenAI api using the python lib provided by OpenAI, but it works
2. What the heck is pyproject.toml
3. Asyncio and SSE
