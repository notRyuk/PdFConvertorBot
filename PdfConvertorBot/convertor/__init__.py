from os import PathLike
import fitz, codecs
from pathlib import Path
from typing import AnyStr, Optional
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from re import sub
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# with open("./pdfconvertorbot/convertor/files/V17_Novel_Reincarnated_as_a_Slime.pdf", "rb") as file:
#     print(PDF(file))


# import json

# input1 = PdfFileReader(open("./pdfconvertorbot/convertor/files/V17_Novel_Reincarnated_as_a_Slime.pdf", "rb"))
# print(input1.getDocumentInfo())

# doc = fitz.open("./pdfconvertorbot/convertor/files/V17_Novel_Reincarnated_as_a_Slime.pdf")
# img_path_list = []
# for i in range(len(doc)):
#     for img in doc.get_page_images(i):
#         xref = img[0]
#         pix = fitz.Pixmap(doc, xref)
#         if pix.n < 5:
#             pix.save("./pdfconvertorbot/convertor/files/images/V17_Novel_Reincarnated_as_a_Slime(%s-%s).png" % (i+1, xref))
#             img_path_list.append(
#                 "./pdfconvertorbot/convertor/files/images/V17_Novel_Reincarnated_as_a_Slime(%s-%s).png" % (i+1, xref)
#             )
#         else:
#             pix1 = fitz.Pixmap(fitz.csRGB, pix)
#             pix1.save("./pdfconvertorbot/convertor/files/images/V17_Novel_Reincarnated_as_a_Slime(%s-%s).png" % (i+1, xref))
#             img_path_list.append(
#                 "./pdfconvertorbot/convertor/files/images/V17_Novel_Reincarnated_as_a_Slime(%s-%s).png" % (i+1, xref)
#             )
#             pix1 = None
#         pix = None

RETURN_HTML = """
<html>
<style>
html, body {
    height: 100%;
}

html {
    display: table;
    margin: auto;
}

body {
    display: table-cell;
    vertical-align: middle;
}
</style>
<body>
"""

class PdfDoc:
    """
        :param:
        file_name: Name of the pdf file with or without the extension
        password: Password of the pdf if any
    """
    def __init__(self, file_name: str, password: Optional[str] = "") -> None:
        base_path = "./PdfConvertorBot/convertor/files/"
        if file_name.endswith(".pdf"):
            self.pdf_path = base_path+file_name
            self.pdf_name = file_name[:-4]
            is_file = Path(base_path+file_name).is_file()
        if not file_name.endswith(".pdf"):
            self.pdf_path = base_path+file_name +".pdf"
            self.pdf_name = file_name
            is_file = Path(base_path+file_name +".pdf").is_file()
        if is_file:
            self.pdf_pass = password
            self.is_file = is_file
        if not is_file:
            raise FileNotFoundError("The mentioned file is not existing.")
        self.codec = "utf-8"
    
    async def get_page_text_list(self) -> Optional[list[str]]:
        if not self.is_file:
            return None
        resource_manager = PDFResourceManager()
        la_params = LAParams()
        pages = PDFPage.get_pages(
            open(self.pdf_path, "rb"),
            password = self.pdf_pass,
            caching = True, 
            pagenos = set(),
            maxpages = 0,
            check_extractable = True
        )
        page_text = []
        for page in pages:
            io = BytesIO()
            device = TextConverter(resource_manager, io, self.codec, laparams = la_params)
            interpreter = PDFPageInterpreter(resource_manager, device)
            interpreter.process_page(page)
            page_text.append(sub(r'[\x0b-\x0c]', "", io.getvalue().decode(self.codec)))
            device.close()
            io.close()
        return page_text
    
    @property
    def num_pages(cls) -> int:
        if not cls.is_file:
            return -1
        pages = PDFPage.get_pages(
            open(cls.pdf_path, "rb"), 
            password = cls.pdf_pass,
            caching = True, 
            pagenos = set(),
            maxpages = 0,
            check_extractable = True
        )
        count = 0
        for _ in pages:
            count += 1
        return count

    async def get_page_text(self, page_number: int) -> Optional[str]:
        "Page number starts from 1"
        if not self.is_file:
            return None
        if page_number < 1 or page_number > self.num_pages: return None
        resource_manager = PDFResourceManager()
        la_params = LAParams()
        _io = BytesIO()
        device = TextConverter(resource_manager, _io, self.codec, laparams = la_params)
        interpreter = PDFPageInterpreter(resource_manager, device)
        pages = PDFPage.get_pages(
            open(self.pdf_path, "rb"),
            password = self.pdf_pass,
            caching = True, 
            pagenos = set(),
            maxpages = 0,
            check_extractable = True
        )
        for i, page in enumerate(pages):
            if i+1 < page_number or i+1 > page_number:
                continue
            interpreter.process_page(page)
        device.close()
        return_str = sub(r'[\x0b-\x0c]', "", _io.getvalue().decode(self.codec))
        _io.close()
        return return_str

    async def get_details(self):
        parser = PDFParser(open(self.pdf_path, "rb"))
        pdf_doc = PDFDocument(parser, self.pdf_pass, caching = True)
        codec = codecs.BOM_UTF16_BE
        info = {}
        for key in pdf_doc.info[0].keys():
            if key.lower() not in ("creationdate", "moddate"):
                info[key] = pdf_doc.info[0][key][len(codec):].decode("utf-16be")
            if key.lower() in ("creationdate", "moddate"):
                info[key] = pdf_doc.info[0][key].decode(self.codec)
        return info
    
    @property
    def table_of_contents(cls):
        doc = fitz.open(cls.pdf_path)
        return doc.get_toc()
    
    async def convert_to_html(self) -> Optional[str]:
        doc = fitz.open(self.pdf_path)
        return_html = RETURN_HTML
        for i in range(len(doc)):
            return_html += doc.get_page_text(i, option = "html")
        return_html += "</body></html>"
        try:
            open(self.pdf_path[:-3]+"html", "w").write(return_html)
            return self.pdf_path[:-3]+"html"
        except Exception as e:
            print(e)
            return None
        


# images = []
# for i in range(input1.numPages):
#     images.append(input1.getPage(i).getContents())

# print(images)

# print(len(images))