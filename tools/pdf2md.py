import sys
import os
import argparse
import shutil
import tempfile
import re

def convert_pdf_to_md(pdf_path):
    try:
        import pymupdf4llm
        import pymupdf
    except ImportError:
        print("Required package 'pymupdf4llm' not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf4llm", "pymupdf"])
        import pymupdf4llm
        import pymupdf

    pdf_path = os.path.abspath(pdf_path)
    if not os.path.exists(pdf_path):
        print(f"Error: File not found '{pdf_path}'")
        sys.exit(1)

    pdf_dir = os.path.dirname(pdf_path)
    target_images_dir = os.path.join(pdf_dir, "images")
    target_readme = os.path.join(pdf_dir, "README.md")
    
    print(f"Converting '{pdf_path}' to Markdown...")
    
    original_cwd = os.getcwd()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a safe filename for the PDF without spaces or special characters
        # so pymupdf4llm doesn't mangle paths incorrectly when saving images.
        original_basename = os.path.basename(pdf_path)
        safe_basename = re.sub(r'[^a-zA-Z0-9_.-]', '_', original_basename)
        if not safe_basename.endswith(".pdf"):
            safe_basename += ".pdf"
            
        temp_pdf = os.path.join(temp_dir, safe_basename)
        shutil.copy(pdf_path, temp_pdf)
        
        # Change to temp dir
        os.chdir(temp_dir)
        os.makedirs("images", exist_ok=True)
        
        # Convert
        doc = pymupdf.open(safe_basename)
        try:
            md_text = pymupdf4llm.to_markdown(
                doc,
                write_images=True,
                image_path="images"
            )
            
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(md_text)
        finally:
            doc.close()
            
        # Copy back to target directory
        os.chdir(original_cwd)
        
        shutil.copy(os.path.join(temp_dir, "README.md"), target_readme)
        
        temp_images = os.path.join(temp_dir, "images")
        if os.path.exists(target_images_dir):
            shutil.rmtree(target_images_dir)
        shutil.copytree(temp_images, target_images_dir)

    # --- Post-processing: Rename images based on context ---
    import unicodedata
    def sanitize_filename(text):
        text = text.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s-]+', '_', text).strip('_')
        words = text.split('_')
        short_text = ''
        for w in words:
            if len(short_text) + len(w) > 40:
                break
            short_text += w + '_'
        short_text = short_text.strip('_')
        return short_text if short_text else 'billede'

    try:
        with open(target_readme, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        used_names = set()
        
        for i, line in enumerate(lines):
            match = re.search(r'!\[.*?\]\((images/[^)]+)\)', line)
            if match:
                old_image_rel_path = match.group(1)
                old_image_filename = os.path.basename(old_image_rel_path)
                
                context_text = "billede"
                for j in range(i - 1, -1, -1):
                    prev_line = lines[j].strip()
                    if re.sub(r'[^a-zA-Z0-9]', '', prev_line):
                        context_text = sanitize_filename(prev_line)
                        break
                        
                base_name = context_text
                counter = 1
                new_name = f"{base_name}.png"
                while new_name in used_names:
                    new_name = f"{base_name}_{counter}.png"
                    counter += 1
                used_names.add(new_name)
                
                old_full_path = os.path.join(pdf_dir, "images", old_image_filename)
                new_full_path = os.path.join(pdf_dir, "images", new_name)
                
                if os.path.exists(old_full_path):
                    os.rename(old_full_path, new_full_path)
                    
                line = line.replace(old_image_rel_path, f"images/{new_name}")
                
            new_lines.append(line)
            
        with open(target_readme, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
    except Exception as e:
        print(f"Warning: Could not rename images based on context: {e}")
    # -------------------------------------------------------

    print(f"Success! Created '{target_readme}' and extracted images to '{target_images_dir}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown and extract images.")
    parser.add_argument("pdf_path", help="Path to the PDF file to convert")
    args = parser.parse_args()
    
    convert_pdf_to_md(args.pdf_path)
