import re
from deep_translator import GoogleTranslator

def split_text_and_tags(line):
    """Hàm tách riêng câu văn và các tag điểm số (O,C,E,A,N)"""
    parts = line.split()
    text_parts = []
    tags = []
    for p in parts:
        # Nhận diện các cụm như E:1, A:-1, C:2...
        if re.match(r'^[OCEAN]:-?\d+$', p):
            tags.append(p)
        else:
            text_parts.append(p)
    return " ".join(text_parts), " ".join(tags)

def translate_file():
    print("🚀 Bắt đầu quá trình tự động dịch...")
    
    # Khởi tạo 2 cỗ máy dịch
    translator_vi = GoogleTranslator(source='en', target='vi')
    translator_de = GoogleTranslator(source='en', target='de')
    
    with open('questions_en.txt', 'r', encoding='utf-8') as f_en, \
         open('questions_vi.txt', 'w', encoding='utf-8') as f_vi, \
         open('questions_de.txt', 'w', encoding='utf-8') as f_de:
        
        lines = f_en.readlines()
        total = len(lines)
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line: continue
            
            # Loại bỏ mấy cái tag linh tinh như nếu có
            line = re.sub(r'\\s*', '', line)
            
            text_en, tags = split_text_and_tags(line)
            
            try:
                # Dịch câu văn
                text_vi = translator_vi.translate(text_en)
                text_de = translator_de.translate(text_en)
                
                # Ghép tag vào lại và ghi ra file
                f_vi.write(f"{text_vi} {tags}\n")
                f_de.write(f"{text_de} {tags}\n")
                
                print(f"✅ Đã dịch [{i+1}/{total}]: {text_en[:30]}...")
                
            except Exception as e:
                print(f"❌ Lỗi ở câu {i+1}: {e}")
                
    print("🎉 Hoàn tất! Đã tạo xong questions_vi.txt và questions_de.txt")

if __name__ == "__main__":
    translate_file()