import docx
import os

docx_path = r"c:\Users\bahun\Downloads\Đồ án 2\Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx"
doc = docx.Document(docx_path)

rels = doc.part.rels
img_map = {}
for rel_id, rel in rels.items():
    if "image" in rel.target_ref:
        img_map[rel_id] = rel.target_ref

print(f"Total image rels: {len(img_map)}")

for i, p in enumerate(doc.paragraphs):
    blips = p._element.xpath(".//a:blip")
    if blips:
        r_ids = [b.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed") for b in blips]
        target_imgs = [img_map.get(rid) for rid in r_ids]
        caption = p.text.strip()
        next_text = doc.paragraphs[i+1].text.strip() if i + 1 < len(doc.paragraphs) else ""
        prev_text = doc.paragraphs[i-1].text.strip() if i > 0 else ""
        print(f"Para {i:3d} | imgs={target_imgs} | prev: '{prev_text[:50]}' | cur: '{caption[:40]}' | next: '{next_text[:60]}'")
