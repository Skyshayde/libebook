# lib-ebook.py
Module to create an ebook, designed for simplicity.  At the moment, all it supports is epub.  REALLY WIP.  

# Usage

```
import ebook

book = ebook.Book("{filename}", "epub")

book.meta['title'] = "Title goes here"
book.meta['language'] = "en"
book.meta['creator'] = "Skyshayde"
book.meta['identifier'] = "12345"

book.chapters = ["ch1.html", "ch2.html"]

book.build()
```
