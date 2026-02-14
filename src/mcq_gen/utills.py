import os 
import PyPDF2
import json
import traceback


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdffileReader(file)
            text=""
            for page in pdf_reader.pages:
                text =page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("error reading the pdf file")
        
    elif file.name.readswith(".txt"):
        return file.read().decode("utf.8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )
              
