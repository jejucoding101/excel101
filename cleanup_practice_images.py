# -*- coding: utf-8 -*-
import os
import re

base_dir = r"c:\GENERAL_LLM\EXCEL_101"

# "완성 결과 미리보기"와 관련된 마크다운 및 이미지 줄을 찾아서 삭제하는 정규식
# 주로 형태:
# **📋 완성 결과 미리보기**:
# 
# ![실습 완성 결과 — ...](images/practice_result.png)
# 이런 패턴들을 지웁니다.
# 
# 보다 안전하게 한 줄씩 읽으면서 처리하겠습니다.

deleted_images_count = 0
modified_readmes_count = 0

for item in os.listdir(base_dir):
    if item.startswith("L") and os.path.isdir(os.path.join(base_dir, item)):
        lecture_dir = os.path.join(base_dir, item)
        readme_path = os.path.join(lecture_dir, "README.md")
        images_dir = os.path.join(lecture_dir, "images")
        
        # 1. README.md에서 실습 이미지 링크 및 미리보기 텍스트 제거
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            skip_next_empty = False
            modified = False
            
            for line in lines:
                # 미리보기 텍스트 줄 제거
                if "**📋 완성 결과 미리보기**" in line:
                    modified = True
                    skip_next_empty = True
                    continue
                
                # 이미지 링크 줄 제거
                if "![실습 완성 결과" in line or "practice_result" in line:
                    modified = True
                    skip_next_empty = True
                    continue
                
                # 삭제된 줄 바로 밑에 있는 빈 줄 1개 지우기
                if skip_next_empty and line.strip() == "":
                    skip_next_empty = False
                    continue
                
                skip_next_empty = False
                new_lines.append(line)
            
            if modified:
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                modified_readmes_count += 1
                
        # 2. images 폴더 내의 practice_*.png 파일 삭제
        if os.path.exists(images_dir):
            for img_file in os.listdir(images_dir):
                if img_file.startswith("practice_") and img_file.endswith(".png"):
                    try:
                        os.remove(os.path.join(images_dir, img_file))
                        deleted_images_count += 1
                    except Exception as e:
                        print(f"Error deleting {img_file}: {e}")

print(f"작업 완료: README.md {modified_readmes_count}개 수정, 실습 이미지 {deleted_images_count}개 삭제.")
