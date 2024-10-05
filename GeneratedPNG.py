from PIL import Image, ImageDraw, ImageFont, ImageFilter, PngImagePlugin
import os

# narratorc stílus hozzáadva
#tpng feature hozzáadva
#kihagyja a létező fileokat, META adatok alpján
#[NLA] & [NRA] felismerése DOCTYPE5-től OK
#simple
#[i] és [b]
def create_image(text, output_path):
    img = Image.new('RGB', (512, 448), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    fonts = {
        "regular": ImageFont.truetype("arial.ttf", 14, encoding="unic"),
        "italic": ImageFont.truetype("ariali.ttf", 14, encoding="unic"),
        "title": ImageFont.truetype("arial.ttf", 24, encoding="unic"),
        "centered": ImageFont.truetype("arial.ttf", 14, encoding="unic"),
        "white_bg": ImageFont.truetype("arial.ttf", 26, encoding="unic"),
        "blue_center": ImageFont.truetype("arial.ttf", 24, encoding="unic")
    }
    
    styles = {
        "title": {"font": fonts["title"], "fill": (245, 245, 245)},
        "narrator": {"font": fonts["italic"], "fill": (80, 131, 213)},
        "dialogue": {"font": fonts["regular"], "fill": (171, 171, 171)},
        "centered": {"font": fonts["centered"], "fill": (255, 255, 255)},
        "narratorc": {"font": fonts["italic"], "fill": (80, 131, 213)},
        "white_bg": {"font": fonts["white_bg"], "fill": (255, 255, 255)},
        "blue_center": {"font": fonts["blue_center"], "fill": (5, 20, 220)}
    }
    
    line_spacing = {
        "title": 15,
        "narrator": 4,
        "dialogue": 4,
        "centered": 4,
        "narratorc": 4
    }
    
    y_position = 20
    max_width = img.width - 40
    show_prev = True
    show_next = True
    
    for line in text.split('\n'):
        if "[NLA]" in line:
            show_prev = False
        if "[NRA]" in line:
            show_next = False
        
        if line.startswith("[title]"):
            style = styles["title"]
            line = line.replace("[title]", "")
            position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
            draw.text((position[0], position[1]), line, font=styles["white_bg"]["font"], fill=styles["white_bg"]["fill"])
            img_blur_white = img.filter(ImageFilter.GaussianBlur(radius=15))
            img.paste(img_blur_white)
            draw.text((position[0], position[1]), line, font=styles["blue_center"]["font"], fill=styles["blue_center"]["fill"])
            img_blur_blue = img.filter(ImageFilter.GaussianBlur(radius=5))
            img.paste(img_blur_blue)
            draw.text(position, line, font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing["title"]
        
        elif line.startswith("[narrator]") or line.startswith("[narratorc]"):
            style = styles["narrator"] if line.startswith("[narrator]") else styles["narratorc"]
            line = line.replace("[narrator]", "").replace("[narratorc]", "")
            words = line.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if draw.textbbox((0, 0), test_line, font=style["font"])[2] <= max_width - 40:
                    current_line = test_line
                else:
                    draw.text((50, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
                    y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["narrator"]
                    current_line = word + " "
            draw.text((50, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["narrator"]
        
        elif line.startswith("[dialogue]"):
            style = styles["dialogue"]
            line = line.replace("[dialogue]", "")
            words = line.split(' ')
            current_line = ""
            for word in words:
                if word == "+":
                    y_position += line_spacing["dialogue"]
                elif word == "/":
                    draw.text((70, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
                    y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["dialogue"]
                    current_line = ""
                else:
                    test_line = current_line + word + " "
                    if draw.textbbox((0, 0), test_line, font=style["font"])[2] <= max_width - 40:
                        current_line = test_line
                    else:
                        draw.text((70, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
                        y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["dialogue"]
                        current_line = word + " "
            draw.text((70, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["dialogue"]
        
        elif line.startswith("[centered]"):
            style = styles["centered"]
            line = line.replace("[centered]", "")
            position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
            draw.text(position, line, font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing["centered"]
    
    if show_next:
        next_text = "következő"
        next_position_text = (img.width - draw.textbbox((0, 0), next_text, font=styles["dialogue"]["font"])[2] - 70, img.height - 36)
        next_position_arrow = (next_position_text[0] + draw.textbbox((0, 0), next_text, font=styles["dialogue"]["font"])[2] + 10, img.height - 40)
        draw.text(next_position_text, next_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))
        if os.path.exists("right_arrow.png"):
            right_arrow_img = Image.open("right_arrow.png")
            img.paste(right_arrow_img, next_position_arrow)
        else:
            print("right_arrow.png nem található, kihagyva.")
    
    if show_prev:
        prev_text = "előző"
        prev_position_text = (70, img.height - 36)
        prev_position_arrow = (prev_position_text[0] - 40, img.height - 40)
        draw.text(prev_position_text, prev_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))
        if os.path.exists("left_arrow.png"):
            left_arrow_img = Image.open("left_arrow.png")
            img.paste(left_arrow_img, prev_position_arrow)
        else:
            print("left_arrow.png nem található, kihagyva.")
    
    page_number_text = "1"
    for line in text.split('\n'):
        if line.startswith("[pn]"):
            page_number_text = line.replace("[pn]", "").strip()
            break
    page_number_position = (img.width // 2 - draw.textbbox((0, 0), page_number_text, font=styles["dialogue"]["font"])[2] // 2, img.height - 40)
    draw.text(page_number_position, page_number_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))
    
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Description", text)
    img.save(output_path, pnginfo=meta)

def verify_image_text(image_path, original_text):
    img = Image.open(image_path)
    meta = img.info
    embedded_text = meta.get("Description", "")
    return embedded_text == original_text

def process_all_tpng_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".tpng"):
            text_file_path = os.path.join(directory, filename)
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            output_path = os.path.join(directory, filename.replace(".tpng", ".png"))
            if os.path.exists(output_path):
                if verify_image_text(output_path, text):
                    print(f"{output_path} már létezik és a szöveg egyezik, kihagyva.")
                    continue
                else:
                    print(f"{output_path} már létezik, de a szöveg eltér, újragenerálás.")
            create_image(text, output_path)

# A könyvtár megadása, ahol a .tpng fájlok találhatók
directory = "tpng/"

# .tpng fájlok feldolgozása a megadott könyvtárban
process_all_tpng_files(directory)
