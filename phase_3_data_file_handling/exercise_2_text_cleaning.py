"""
Phase 3 - Exercise 2 (Self-practice)
Text cleaning and preprocessing.
"""

import re


def normalize_whitespace(text: str) -> str:
    # TODO:
    # 1. normalize newline ve \n
    # 2. gom nhieu space/tab ve 1 space
    # 3. tranh qua nhieu dong trong lien tiep
    # Hint nho: re.sub(...)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    result = text.strip()
    return result


def remove_page_number_lines(text: str) -> str:
    # TODO:
    # 1. bo cac dong chi chua so trang
    # 2. bo mau "Page 1", "page 2", ...
    # Hint nho: re.fullmatch(r"\\d+", line.strip())
    lines = text.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\d+", stripped) or re.fullmatch(r"[Pp]age\s+\d+", stripped):
            continue
        result.append(line)
    return "\n".join(result)

def remove_repeated_header_footer(text: str, top_n: int = 1, bottom_n: int = 1) -> str:
    # TODO:
    # 1. tach text thanh "pages"
    # 2. tim header/footer lap lai giua cac page
    # 3. remove cac dong do
    # Hint nho: dung phep giao set de tim dong chung
    pages = text.split("\n\n")
    result = []
    cleaned_pages = []
    
    for page in pages:
        lines = page.split("\n")
        header = "\n".join(lines[:top_n])
        footer = "\n".join(lines[-bottom_n:])
        
        if header in result:
            page = page.replace(header, "")
        else:
            result.append(header)
            
        if footer in result:
            page = page.replace(footer, "")
        else:
            result.append(footer)
        
        cleaned_pages.append(page)
    
    return "\n\n".join(cleaned_pages)



def clean_text(text: str) -> str:
    # TODO: goi 3 buoc cleaning theo thu tu hop ly
    text = normalize_whitespace(text)
    text = remove_page_number_lines(text)
    text = remove_repeated_header_footer(text)
    return text



def exercise_3_2():
    print("=" * 60)
    print("PHASE 3 - EXERCISE 2: TEXT CLEANING")
    print("=" * 60)

    sample_text = """
My Report Header
Page 1

This   is   page one.  
It has    extra spaces.

My Report Header
Page 2

This is page two.
It also has noise.

Confidential Footer
""".strip()

    print("Original:\n", sample_text)
    print("\n" + "-" * 60)

    # TODO: goi clean_text(sample_text) va in ket qua
    # Hint nho: cleaned = clean_text(sample_text)
    cleaned = clean_text(sample_text)
    print("Cleaned:\n", cleaned)
    print("\n" + "-" * 60)
    print(f"Original length: {len(sample_text)}, Cleaned length: {len(cleaned)}")

    # TODO:
    # 1. Replace sample_text with text extracted from your real document
    # 2. Improve regex rules for your document style
    # 3. Add extra normalization rules if needed


if __name__ == "__main__":
    exercise_3_2()
