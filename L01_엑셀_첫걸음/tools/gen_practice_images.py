# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

SRC = r"c:\GENERAL_LLM\EXCEL_101\.screenshot\excel_source.png"
DIR = r"c:\GENERAL_LLM\EXCEL_101\L01_엑셀_첫걸음\images"

FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_REG  = r"C:\Windows\Fonts\malgun.ttf"

def create_practice_image(output_name, title=None, active_cell=None, data=None, name_box=None):
    img = Image.open(SRC).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    font_cell = ImageFont.truetype(FONT_REG, 14)
    font_bold = ImageFont.truetype(FONT_BOLD, 14)
    font_title = ImageFont.truetype(FONT_REG, 13)
    font_namebox = ImageFont.truetype(FONT_REG, 14)

    # Title Box
    if title:
        draw.rectangle([340, 5, 560, 25], fill=(255,255,255))
        draw.text((380, 5), title, fill=(0,0,0), font=font_title)

    # Name Box
    if name_box:
        draw.rectangle([10, 180, 60, 200], fill=(255,255,255))
        draw.text((10, 182), name_box, fill=(0,0,0), font=font_namebox)

    col_x = {'A': 25, 'B': 108, 'C': 171, 'D': 234}
    col_w = {'A': 83, 'B': 63, 'C': 63, 'D': 63}
    # y coordinates of the *top* of each row
    row_y = {1: 215, 2: 235, 3: 255, 4: 275, 5: 295}
    row_h = 20

    # 데이터가 있으면 해당 영역을 다 흰색으로 지우고 격자를 다시 그림
    if data:
        max_r = len(data)
        max_c = max(len(row) for row in data)
        # 영역 계산 (A1부터)
        area_x1 = 25
        area_y1 = 215
        area_x2 = col_x[chr(ord('A') + max_c - 1)] + col_w[chr(ord('A') + max_c - 1)]
        area_y2 = row_y[max_r] + row_h
        
        draw.rectangle([area_x1, area_y1, area_x2, area_y2], fill=(255,255,255))
        
        # 가로선
        for r in range(1, max_r + 2):
            y = 215 + (r-1)*row_h
            draw.line([(area_x1, y), (area_x2, y)], fill=(212,212,212), width=1)
        # 세로선
        for c in range(max_c + 1):
            c_char = chr(ord('A') + c)
            x = col_x[c_char] if c_char in col_x else (area_x2)
            draw.line([(x, area_y1), (x, area_y2)], fill=(212,212,212), width=1)

        # 텍스트 그리기
        for r, row_data in enumerate(data):
            r_idx = r + 1
            for c, cell_val in enumerate(row_data):
                c_chr = chr(ord('A') + c)
                x = col_x.get(c_chr, 0)
                y = row_y.get(r_idx, 0)
                f = font_bold if r_idx == 1 else font_cell
                # 셀 안에서 글자 정렬 (약간 패딩)
                draw.text((x + 6, y + 2), str(cell_val), fill=(0,0,0), font=f)
    elif active_cell == "D5":   # 실습 1을 위해 기존 초록 박스만 임시로 제거
        draw.rectangle([25, 215, 108, 235], fill=(255,255,255))
        draw.line([(25, 215), (108, 215)], fill=(212,212,212), width=1)
        draw.line([(25, 235), (108, 235)], fill=(212,212,212), width=1)
        draw.line([(25, 215), (25, 235)], fill=(212,212,212), width=1)
        draw.line([(108, 215), (108, 235)], fill=(212,212,212), width=1)

    # 활성 셀 테두리 그리기
    if active_cell:
        col_c = active_cell[0]
        row_n = int(active_cell[1:])
        ax = col_x.get(col_c, 25)
        ay = row_y.get(row_n, 215)
        aw = col_w.get(col_c, 63)
        ah = row_h
        
        # Green border
        draw.rectangle([ax, ay, ax+aw, ay+ah], outline=(33, 115, 70), width=2)
        # small square bottom right
        draw.rectangle([ax+aw-3, ay+ah-3, ax+aw+2, ay+ah+2], fill=(33, 115, 70))

    out_path = os.path.join(DIR, output_name)
    img.save(out_path)
    print(f"Saved: {out_path}")

create_practice_image("practice_1_result.png", name_box="D5", active_cell="D5")

data_2 = [
    ["이름", "나이", "취미"],
    ["홍길동", 25, "독서"],
    ["김철수", 28, "운동"],
    ["이영희", 24, "요리"]
]
create_practice_image("practice_2_result.png", name_box="A1", active_cell="A1", data=data_2)

create_practice_image("practice_3_result.png", title="내_첫_엑셀파일.xlsx - Excel", name_box="A1", active_cell="A1", data=data_2)
