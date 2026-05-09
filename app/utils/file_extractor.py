"""
File extraction utility - handles multiple file formats
"""

import io
import json
import csv
import PyPDF2
from docx import Document

try:
    import openpyxl
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False

try:
    from pptx import Presentation
    PPTX_SUPPORT = True
except ImportError:
    PPTX_SUPPORT = False


def extract_text_from_file(file_url: str, file_content_bytes: bytes, mime_type: str = None) -> str:
    """
    Extract text from various file formats.
    
    Supports: PDF, DOCX, XLSX, PPTX, CSV, TXT, JSON, Images
    
    Returns: Extracted FULL text content for evaluation
    """
    
    try:
        # Determine file type from URL or mime type
        file_ext = file_url.lower().split('.')[-1] if file_url else ""
        
        # PDF files
        if file_ext == "pdf" or (mime_type and "pdf" in mime_type):
            return extract_pdf(file_content_bytes)
        
        # Word documents (.docx)
        elif file_ext == "docx" or (mime_type and "word" in mime_type or "document" in mime_type):
            return extract_docx(file_content_bytes)
        
        # Excel files (.xlsx, .xls)
        elif file_ext in ["xlsx", "xls"] or (mime_type and "sheet" in mime_type):
            return extract_excel(file_content_bytes)
        
        # PowerPoint files (.pptx)
        elif file_ext == "pptx" or (mime_type and "presentation" in mime_type):
            return extract_pptx(file_content_bytes)
        
        # CSV files
        elif file_ext == "csv" or (mime_type and "csv" in mime_type):
            return extract_csv(file_content_bytes)
        
        # JSON files
        elif file_ext == "json" or (mime_type and "json" in mime_type):
            return extract_json(file_content_bytes)
        
        # Plain text and Code files
        elif file_ext in ["txt", "md", "py", "js", "html", "css", "sql"] or (mime_type and "text" in mime_type):
            raw_text = file_content_bytes.decode("utf-8", errors="ignore")
            
            # Inject line numbers for code files so agents can reference them
            if file_ext in ["py", "js", "html", "css", "sql"]:
                lines = raw_text.split('\n')
                numbered_lines = [f"[Line {i+1}] {line}" for i, line in enumerate(lines)]
                return "\n".join(numbered_lines)
                
            return raw_text
        
        # Default: try UTF-8 decode
        else:
            try:
                return file_content_bytes.decode("utf-8", errors="ignore")
            except:
                return "[Binary file - cannot extract text]"
    
    except Exception as e:
        return f"[Error extracting file: {str(e)}]"


def extract_pdf(file_bytes: bytes) -> str:
    """Extract full text from PDF"""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page_num, page in enumerate(reader.pages): 
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text() or "[No text found on page]"
        return text 
    except Exception as e:
        return f"[PDF extraction error: {str(e)}]"


def extract_docx(file_bytes: bytes) -> str:
    """Extract full text from Word document (.docx)"""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        
        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        
        # Extract tables
        for table in doc.tables:
            text += "\n[TABLE]\n"
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " | "
                text += "\n"
        
        return text
    except Exception as e:
        return f"[DOCX extraction error: {str(e)}]"


def extract_excel(file_bytes: bytes) -> str:
    """Extract full text from Excel file (.xlsx/.xls)"""
    if not EXCEL_SUPPORT:
        return "[Excel support not installed - install openpyxl]"
    
    try:
        workbook = openpyxl.load_workbook(io.BytesIO(file_bytes))
        text = ""
        
        for sheet_name in workbook.sheetnames: 
            worksheet = workbook[sheet_name]
            text += f"\n--- Sheet: {sheet_name} ---\n"
            
            for row in worksheet.iter_rows(values_only=True): 
                row_text = " | ".join(str(cell) if cell is not None else "" for cell in row)
                if row_text.strip():
                    text += row_text + "\n"
        
        return text
    except Exception as e:
        return f"[Excel extraction error: {str(e)}]"


def extract_pptx(file_bytes: bytes) -> str:
    """Extract full text from PowerPoint presentation (.pptx)"""
    if not PPTX_SUPPORT:
        return "[PowerPoint support not installed - install python-pptx]"
    
    try:
        prs = Presentation(io.BytesIO(file_bytes))
        text = ""
        
        for slide_num, slide in enumerate(prs.slides): 
            text += f"\n--- Slide {slide_num + 1} ---\n"
            
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text += shape.text + "\n"
        
        return text
    except Exception as e:
        return f"[PPTX extraction error: {str(e)}]"


def extract_csv(file_bytes: bytes) -> str:
    """Extract full text from CSV file"""
    try:
        text_content = file_bytes.decode("utf-8", errors="ignore")
        csv_reader = csv.reader(io.StringIO(text_content))
        text = ""
        
        for row in csv_reader:
            text += " | ".join(row) + "\n"
        
        return text
    except Exception as e:
        return f"[CSV extraction error: {str(e)}]"


def extract_json(file_bytes: bytes) -> str:
    """Extract full text from JSON file"""
    try:
        json_content = json.loads(file_bytes.decode("utf-8"))
        return json.dumps(json_content, indent=2)
    except Exception as e:
        return f"[JSON extraction error: {str(e)}]"