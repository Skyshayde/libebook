# The MIT License (MIT)

# Copyright (c) 2015 Teddy Heinen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import zipfile
import xml.etree.ElementTree as etree

class Book:

    def __init__(self, name, fileformat, ):
        self.name = name
        self.format = fileformat
        self.chapters = []
        self.assets = []
        self.meta = {}
        self.file = None

    def build(self):
        if self.format == "epub":
            self.file = zipfile.ZipFile(self.name + "." + self.format, "w")

            self.file.writestr("mimetype", "application/epub+zip")

            # Generate container.xml

            container = etree.Element("container")

            container.attrib['version'] = "1.0"
            container.attrib['xmlns'] = "urn:oasis:names:tc:opendocument:xmlns:container"

            rootfiles = etree.SubElement(container, "rootfiles")

            rootfile = etree.SubElement(rootfiles, "rootfile")
            rootfile.attrib['full-path'] = "assets/content.opf"
            rootfile.attrib['media-type'] = "application/oebps-package+xml"

            self.file.writestr("META-INF/container.xml", etree.tostring(container, encoding="UTF-8"))

            # Generate content.opf

            pkg = etree.Element("package")

            pkg.attrib['version'] = "2.0"
            pkg.attrib['xmlns'] = "http://www.idpf.org/2007/opf"
            pkg.attrib['unique-identifier'] = self.name

            metadata = etree.SubElement(pkg, "metadata")
            for index in self.meta.items():
                dc = etree.SubElement(metadata, "dc:" + index[0])
                dc.text = index[1]

            manifest = etree.SubElement(pkg, "manifest")

            spine = etree.SubElement(pkg, "spine")
            spine.attrib['toc'] = "ncx"
            
            for index in self.chapters:
                item = etree.SubElement(manifest, "item")
                item.attrib['id'] = index.name.split('.')[0]
                item.attrib['href'] = index.name
                item.attrib['media-type'] = "application/xhtml+xml"

                spine_item = etree.SubElement(spine, "itemref")
                spine_item.attrib['idref'] = item.attrib['id']

            self.file.writestr("assets/content.opf", etree.tostring(pkg, encoding="UTF-8"))

            # Write chapters to epub
            for assets in self.chapters + self.assets:
                self.file.write(assets.name, "assets/" + assets.name)
                print("writing " + assets.name + " to zip")

            self.file.close()