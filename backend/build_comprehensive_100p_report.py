"""
Master Report Generator: Hệ thống Quản lý Thư viện có Tích hợp AI
Tạo file Word Báo cáo Đồ án Toàn diện 80 - 100+ Trang đạt chuẩn Điểm 10 Tuyệt Đối.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DIAGRAMS_DIR = os.path.join(DOCS_DIR, "diagrams")
SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx")

# Theme Colors
COLOR_PRIMARY = RGBColor(30, 27, 75)      # Deep Indigo #1E1B4B
COLOR_SECONDARY = RGBColor(49, 46, 129)   # Indigo #312E81
COLOR_ACCENT = RGBColor(79, 70, 229)      # Indigo #4F46E5
COLOR_DARK = RGBColor(15, 23, 42)         # Slate 900 #0F172A
COLOR_MUTED = RGBColor(71, 85, 105)       # Slate 600 #475569

HEX_PRIMARY = "1E1B4B"
HEX_SECONDARY = "312E81"
HEX_ACCENT = "4F46E5"
HEX_BG_LIGHT = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_CALLOUT_BG = "EEF2FF"
HEX_CODE_BG = "F1F5F9"

def set_cell_background(cell, hex_color):
    """Đặt màu nền cho cell trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Đặt padding cho ô trong bảng (đơn vị dxa: 20 dxa = 1 pt)"""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, hex_color=HEX_BORDER):
    """Đặt viền thanh mảnh cho toàn bộ bảng"""
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

class ReportBuilder:
    def __init__(self):
        self.doc = Document()
        self.setup_page_layout()
        self.fig_counter = {}
        self.tbl_counter = {}
        self.current_chapter = 0

    def setup_page_layout(self):
        """Thiết lập khổ giấy A4 và lề chuẩn học thuật"""
        for section in self.doc.sections:
            section.page_width = Cm(21.0)
            section.page_height = Cm(29.7)
            section.top_margin = Cm(2.0)
            section.bottom_margin = Cm(2.0)
            section.left_margin = Cm(3.0)
            section.right_margin = Cm(2.0)
            
            # Setup Header & Footer
            header = section.header
            hp = header.paragraphs[0]
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            hrun = hp.add_run("BÁO CÁO ĐỒ ÁN: HỆ THỐNG QUẢN LÝ THƯ VIỆN CÓ TÍCH HỢP AI")
            hrun.font.name = "Times New Roman"
            hrun.font.size = Pt(8.5)
            hrun.font.italic = True
            hrun.font.color.rgb = COLOR_MUTED

            footer = section.footer
            fp = footer.paragraphs[0]
            fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            frun = fp.add_run("Học phần: Ứng dụng Trí tuệ Nhân tạo | Trang ")
            frun.font.name = "Times New Roman"
            frun.font.size = Pt(9)
            frun.font.color.rgb = COLOR_MUTED
            
            # Add Page number field via XML
            fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
            fp._element.append(fld)

    def add_title_page(self):
        """Tạo trang bìa chuẩn học thuật"""
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN & AN TOÀN THÔNG TIN")
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY

        p_line = self.doc.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_line.paragraph_format.space_before = Pt(2)
        p_line.paragraph_format.space_after = Pt(40)
        r_line = p_line.add_run("━━━━━━━━━━━━━━━━━━━━━")
        r_line.font.bold = True
        r_line.font.color.rgb = COLOR_ACCENT

        p_logo_text = self.doc.add_paragraph()
        p_logo_text.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo_text.paragraph_format.space_before = Pt(20)
        p_logo_text.paragraph_format.space_after = Pt(20)
        r_sub = p_logo_text.add_run("BÁO CÁO TỔNG KẾT ĐỒ ÁN HỌC PHẦN\nỨNG DỤNG TRÍ TUỆ NHÂN TẠO TRONG PHÁT TRIỂN PHẦN MỀM")
        r_sub.font.name = "Times New Roman"
        r_sub.font.size = Pt(14)
        r_sub.font.bold = True
        r_sub.font.color.rgb = COLOR_MUTED

        p_title = self.doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.space_before = Pt(30)
        p_title.paragraph_format.space_after = Pt(40)
        r_title = p_title.add_run("ĐỀ TÀI:\nHỆ THỐNG QUẢN LÝ THƯ VIỆN CÓ TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI)\n(SMART LIBRARY MANAGEMENT SYSTEM)")
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(20)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_PRIMARY

        p_info = self.doc.add_paragraph()
        p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_info.paragraph_format.left_indent = Inches(1.2)
        p_info.paragraph_format.space_before = Pt(60)
        p_info.paragraph_format.space_after = Pt(4)
        p_info.paragraph_format.line_spacing = 1.3

        info_runs = [
            ("Giảng viên hướng dẫn: ", True), ("TS. Nguyễn Văn A\n", False),
            ("Lớp học phần: ", True), ("Ứng dụng trí tuệ nhân tạo (K23.K1.ATTT K23A)\n", False),
            ("Sinh viên thực hiện: ", True), ("Nhóm Sinh Viên Xuất Sắc\n", False),
            ("Mã sinh viên: ", True), ("23010001, 23010002, 23010003\n", False),
            ("Chuyên ngành: ", True), ("An toàn Thông tin & Công nghệ Phần mềm\n", False),
            ("Thời gian thực hiện: ", True), ("Học kỳ 1 - Năm học 2026 - 2027\n", False),
        ]
        for text, bold in info_runs:
            r = p_info.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.bold = bold
            r.font.color.rgb = COLOR_DARK

        p_foot = self.doc.add_paragraph()
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_foot.paragraph_format.space_before = Pt(80)
        p_foot.paragraph_format.space_after = Pt(0)
        r_foot = p_foot.add_run("HÀ NỘI, NĂM 2026")
        r_foot.font.name = "Times New Roman"
        r_foot.font.size = Pt(12)
        r_foot.font.bold = True
        r_foot.font.color.rgb = COLOR_PRIMARY

        self.doc.add_page_break()

    def add_heading_1(self, text, chapter_num=None):
        """Thêm tiêu đề cấp 1 (Chương)"""
        if chapter_num:
            self.current_chapter = chapter_num
            self.fig_counter[chapter_num] = 0
            self.tbl_counter[chapter_num] = 0
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading_2(self, text):
        """Thêm tiêu đề cấp 2 (1.1, 1.2)"""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        return p

    def add_heading_3(self, text):
        """Thêm tiêu đề cấp 3 (1.1.1, 1.1.2)"""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = COLOR_ACCENT
        return p

    def add_heading_4(self, text):
        """Thêm tiêu đề cấp 4"""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = COLOR_DARK
        return p

    def add_paragraph(self, text="", style=None, bold_prefix=None, space_after=6):
        """Thêm đoạn văn bản chuẩn học thuật (Justified, 13pt, line spacing 1.3)"""
        p = self.doc.add_paragraph(style=style)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.3

        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Times New Roman"
            r_bold.font.size = Pt(13)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_DARK

        if text:
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.color.rgb = COLOR_DARK

        return p

    def add_bullet(self, bold_text, normal_text):
        """Thêm mục gạch đầu dòng chuyên nghiệp"""
        p = self.doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.25

        r_bold = p.add_run(bold_text)
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(13)
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_DARK

        r_normal = p.add_run(normal_text)
        r_normal.font.name = "Times New Roman"
        r_normal.font.size = Pt(13)
        r_normal.font.color.rgb = COLOR_DARK

    def add_callout(self, title, text):
        """Thêm hộp chú thích (Callout box) với viền tím nổi bật"""
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_CALLOUT_BG)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        # Thick left border
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_ACCENT}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.2

        r_title = p.add_run(f"💡 {title}\n")
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(12)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_ACCENT

        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(12)
        r_text.font.italic = True
        r_text.font.color.rgb = COLOR_DARK

        # Space after table
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)

    def add_code_block(self, code_text, language="Python"):
        """Thêm khối hiển thị mã nguồn hoặc Prompt"""
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_CODE_BG)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15

        r_code = p.add_run(code_text.strip())
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(10)
        r_code.font.color.rgb = RGBColor(30, 41, 59)

        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)

    def add_image_with_caption(self, image_path, caption_text, width_inch=6.0):
        """Chèn hình ảnh / sơ đồ kèm Caption tự động đánh số"""
        ch = self.current_chapter if self.current_chapter > 0 else 1
        if ch not in self.fig_counter:
            self.fig_counter[ch] = 0
        self.fig_counter[ch] += 1
        fig_label = f"Hình {ch}.{self.fig_counter[ch]}"

        p_img = self.doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)

        if os.path.exists(image_path):
            p_img.add_run().add_picture(image_path, width=Inches(width_inch))
        else:
            r_err = p_img.add_run(f"[{fig_label}: {caption_text} - File ảnh không tồn tại]")
            r_err.font.italic = True
            r_err.font.color.rgb = RGBColor(220, 38, 38)

        p_cap = self.doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        p_cap.paragraph_format.keep_with_next = True

        r_lbl = p_cap.add_run(f"{fig_label}: ")
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(11)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_DARK

        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

    def add_styled_table(self, title, headers, rows, col_widths=None):
        """Thêm bảng biểu định dạng Header Indigo, sọc xen kẽ và viền thanh mảnh"""
        ch = self.current_chapter if self.current_chapter > 0 else 1
        if ch not in self.tbl_counter:
            self.tbl_counter[ch] = 0
        self.tbl_counter[ch] += 1
        tbl_label = f"Bảng {ch}.{self.tbl_counter[ch]}"

        p_title = self.doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_title.paragraph_format.space_before = Pt(10)
        p_title.paragraph_format.space_after = Pt(3)
        p_title.paragraph_format.keep_with_next = True

        r_lbl = p_title.add_run(f"{tbl_label}: ")
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(11)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = COLOR_DARK

        r_t = p_title.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_SECONDARY

        table = self.doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            set_cell_background(cell, HEX_SECONDARY)
            set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(header_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, row_data in enumerate(rows):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = HEX_BG_LIGHT if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 1 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                r = p.add_run(str(val))
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                r.font.color.rgb = COLOR_DARK

        # Set Column widths if provided
        if col_widths and len(col_widths) == len(headers):
            for row in table.rows:
                for i, w in enumerate(col_widths):
                    row.cells[i].width = Inches(w)

        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(6)

print("ReportBuilder Core Initialized.")
