import os
from dotenv import load_dotenv
from PIL import Image
from pptx import Presentation
from pptx.util import Inches

# 加载环境变量
load_dotenv()

def crop_image(original_image_path, cropped_image_path, top_left, bottom_right):
    """裁剪图片并保存。"""
    image = Image.open(original_image_path)
    crop_area = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
    cropped_image = image.crop(crop_area)
    
    # 在保存之前删除已存在的文件
    if os.path.exists(cropped_image_path):
        os.remove(cropped_image_path)
    
    cropped_image.save(cropped_image_path)

def get_sorted_png_files(folder):
    """获取指定文件夹中的PNG文件，并按最后修改时间排序。"""
    png_files = [f for f in os.listdir(folder) if f.lower().endswith('.png')]

    print(f"找到 {len(png_files)} 个PNG文件。")
    print("排序前的文件名：")
    for png_file in png_files:
        print(png_file)

    # 获取图像最后修改时间并排序
    png_files.sort(key=lambda x: os.stat(os.path.join(folder, x)).st_mtime)

    # 打印排序后的文件结果
    print("排序后的文件名：")
    for png_file in png_files:
        print(png_file)
    
    return png_files

def create_ppt_from_png_files(png_files, output_pptx_path):
    """将PNG文件列表生成PPTX文件。"""
    presentation = Presentation()

    # 设置幻灯片大小为16:9
    presentation.slide_width = Inches(16)
    presentation.slide_height = Inches(9)

    for png_file in png_files:
        slide = presentation.slides.add_slide(presentation.slide_layouts[5])  # 使用空白幻灯片布局
        img_path = png_file  # 假设png_file是完整路径
        
        # 添加图片并使其填满幻灯片
        slide.shapes.add_picture(img_path, 0, 0, width=presentation.slide_width, height=presentation.slide_height)

    # 保存PPTX文件
    presentation.save(output_pptx_path)

def crop_images_in_folder(input_folder, output_folder, top_left, bottom_right):
    """遍历文件夹中的PNG图片，按最后修改时间裁剪并保存。"""
    png_files = get_sorted_png_files(input_folder)
    os.makedirs(output_folder, exist_ok=True)

    for png_file in png_files:
        original_image_path = os.path.join(input_folder, png_file)
        cropped_image_name = f"{os.path.splitext(png_file)[0]}_cropped.png"
        cropped_image_path = os.path.join(output_folder, cropped_image_name)
        print(f"裁剪 {original_image_path} -> {cropped_image_path}")

        crop_image(original_image_path, cropped_image_path, top_left, bottom_right)

    sorted_cropped_files = get_sorted_png_files(output_folder)
    return sorted_cropped_files

# 从环境变量读取参数
input_folder = os.getenv('INPUT_FOLDER')
output_folder = os.getenv('OUTPUT_FOLDER')
top_left = (int(os.getenv('TOP_LEFT_X')), int(os.getenv('TOP_LEFT_Y')))
bottom_right = (int(os.getenv('BOTTOM_RIGHT_X')), int(os.getenv('BOTTOM_RIGHT_Y')))

# 示例调用
cropped_images = crop_images_in_folder(input_folder, output_folder, top_left, bottom_right)

# 生成PPTX文件
output_pptx_path = os.path.join(input_folder, 'output_presentation.pptx')
create_ppt_from_png_files([os.path.join(output_folder, img) for img in cropped_images], output_pptx_path)

print(f"PPTX文件已保存为 {output_pptx_path}")
