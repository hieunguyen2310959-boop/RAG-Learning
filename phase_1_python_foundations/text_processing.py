import os
import re
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_clean_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    cleaned_text = clean_text(text)
    return cleaned_text

def chunk_to_file(text, chunk_size=100, output_file="chunkFile"):
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    words = text.split()
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    for idx, chunk in enumerate(chunks):
        chunk_text = ' '.join(chunk)
        with open(os.path.join(output_file, f"chunk_{idx + 1}.txt"), 'w', encoding='utf-8') as f:
            f.write(chunk_text)



  
if __name__ == "__main__":
    file_path = 'p1.txt'
    try:
        cleaned_text = load_and_clean_text(file_path)
        chunk_to_file(cleaned_text, chunk_size=100, output_file="chunkFile")    
    except FileNotFoundError as e:
        print(e)

