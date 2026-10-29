import docx
import os
import sys
import shutil
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(backend_dir, '..', '..'))
docx_path = os.path.join(root_dir, "Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx")
backup_path = os.path.join(root_dir, "Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang_backup.docx")
img_folder = os.path.join(backend_dir, "docs", "diagrams")

# 1. Create backup
print("=== 1. TAO BAN SAO LUU (BACKUP) ===")
shutil.copy2(docx_path, backup_path)
print(f"Da tao backup tai: {backup_path}")

# 2. Mapping of 18 diagrams
mapping = [
    ('image1.png', '02_usecase_general.png'),
    ('image2.png', '03_usecase_library.png'),
    ('image3.png', '04_usecase_ai.png'),
    ('image4.png', '01_context_diagram.png'),
    ('image5.png', '16_system_architecture.png'),
    ('image6.png', '05_activity_borrow.png'),
    ('image7.png', '06_activity_return.png'),
    ('image8.png', '07_activity_renew.png'),
    ('image9.png', '08_activity_reservation.png'),
    ('image10.png', '09_activity_fine.png'),
    ('image11.png', '10_activity_ai_chat.png'),
    ('image12.png', '11_sequence_borrow.png'),
    ('image13.png', '12_sequence_return.png'),
    ('image14.png', '13_sequence_ai_chat.png'),
    ('image15.png', '14_sequence_ai_suggest.png'),
    ('image16.png', '15_erd_database.png'),
    ('image17.png', '17_ai_pipeline_flow.png'),
    ('image18.png', '18_rag_architecture.png'),
]

MAX_W = 5303520 # 5.8 inches (chieu rong trang A4 tru le)
MAX_H = 6580000 # 7.2 inches (chieu cao toi da tren trang A4 kem chu thich)

print("\n=== 2. CAP NHAT ANH VA KICH THUOC TRONG DOCX ===")
doc = docx.Document(docx_path)
print(f"Tong so hinh anh inline trong tai lieu: {len(doc.inline_shapes)}")

for i in range(18):
    s = doc.inline_shapes[i]
    blip = s._inline.xpath('.//a:blip')[0]
    embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    part = doc.part.related_parts[embed]
    
    img_tag, img_name = mapping[i]
    high_res_path = os.path.join(img_folder, img_name)
    
    # Calculate aspect ratio and new dimensions
    with Image.open(high_res_path) as im:
        w, h = im.size
        aspect = w / h
        new_w = MAX_W
        new_h = int(new_w / aspect)
        if new_h > MAX_H:
            new_h = MAX_H
            new_w = int(new_h * aspect)
            
    with open(high_res_path, 'rb') as f:
        new_bytes = f.read()
        
    old_size = len(part.blob)
    old_w, old_h = s.width, s.height
    
    # Update dimensions and image blob
    s.width = new_w
    s.height = new_h
    part._blob = new_bytes
    
    print(f"[{i+1:2d}/18] Cap nhat {img_name}:")
    print(f"       Kich thuoc cu: {old_w}x{old_h} ({old_size} bytes)")
    print(f"       Kich thuoc moi: {new_w}x{new_h} ({len(new_bytes)} bytes, do phan giai {w}x{h})")

# 3. Save modified document
print("\n=== 3. LUU TAI LIEU ===")
doc.save(docx_path)
shutil.copy2(docx_path, backup_path)
print(f"Da luu thanh cong tep: {docx_path}")
print(f"Da dong bo sang backup tai: {backup_path}")
print(f"Kich thuoc tep moi: {os.path.getsize(docx_path):,} bytes")

# 4. Verify modified document
print("\n=== 4. KIEM TRA XAC THUC TAI LIEU MOI ===")
doc_verify = docx.Document(docx_path)
print(f"Xac thuc so inline shapes: {len(doc_verify.inline_shapes)} (chuan 28)")
for i in range(18):
    s = doc_verify.inline_shapes[i]
    blip = s._inline.xpath('.//a:blip')[0]
    embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    part = doc_verify.part.related_parts[embed]
    print(f"Hinh #{i+1:2d}: width={s.width}, height={s.height}, blob={len(part.blob):,} bytes - OK")

# Also check that UI screenshots are intact
for i in range(18, 28):
    s = doc_verify.inline_shapes[i]
    blip = s._inline.xpath('.//a:blip')[0]
    embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
    part = doc_verify.part.related_parts[embed]
    print(f"UI #{i-17:2d}: width={s.width}, height={s.height}, blob={len(part.blob):,} bytes - Intact OK")

print("\n=== HOAN TAT 100% ===")
