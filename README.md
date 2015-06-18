# lib-ebook.py
Module to create an ebook, designed for simplicity.  At the moment, all it supports is epub.  REALLY WIP.  

# Usage

```
from libebook import Book

book = Book("{filename}", "epub")

book.meta['title'] = "Title goes here"
book.meta['language'] = "en"
book.meta['creator'] = "Skyshayde"
book.meta['identifier'] = "12345"

book.chapters = [open("ch1.html"), open("ch2.html")]
book.assets = [open("cover.png"), open("ch1_pic.png")]

book.build()
```
