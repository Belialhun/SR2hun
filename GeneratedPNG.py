from PIL import Image, ImageDraw, ImageFont, ImageFilter, PngImagePlugin
import os

def create_image(text, output_path):
    img = Image.new('RGB', (512, 448), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define fonts
    fonts = {
        "regular": ImageFont.truetype("arial.ttf", 14, encoding="unic"),
        "italic": ImageFont.truetype("ariali.ttf", 14, encoding="unic"),
        "bold": ImageFont.truetype("arialbd.ttf", 14, encoding="unic"),
        "title": ImageFont.truetype("arial.ttf", 24, encoding="unic"),
        "centered": ImageFont.truetype("arial.ttf", 14, encoding="unic"),
        "white_bg": ImageFont.truetype("arial.ttf", 26, encoding="unic"),
        "blue_center": ImageFont.truetype("arial.ttf", 24, encoding="unic")
    }
    
    # Define styles
    styles = {
        "title": {"font": fonts["title"], "fill": (245, 245, 245)},
        "narrator": {"font": fonts["italic"], "fill": (80, 131, 213)},
        "dialogue": {"font": fonts["regular"], "fill": (171, 171, 171)},
        "centered": {"font": fonts["centered"], "fill": (255, 255, 255)},
        "narratorc": {"font": fonts["italic"], "fill": (80, 131, 213)},
        "white_bg": {"font": fonts["white_bg"], "fill": (255, 255, 255)},
        "blue_center": {"font": fonts["blue_center"], "fill": (5, 20, 220)}
    }
    

# Define line spacing for different styles
line_spacing = {
    "title": 15,
    "narrator": 4,
    "dialogue": 4,
    "centered": 4,
    "narratorc": 4
}

# Check if the text reaches the top of the left_arrow.png
left_arrow_top = img.height - 40  # Assuming the arrow is 40 pixels from the bottom
if y_position >= left_arrow_top:
    # Calculate the reduction factor
    reduction_amount = y_position - left_arrow_top
    reduction_factor = reduction_amount / y_position
    print(f"Warning: Text exceeds the limit by {reduction_amount} pixels. Reducing line spacing by a factor of {reduction_factor:.2f}.")

    for key in line_spacing:
        line_spacing[key] = max(1, line_spacing[key] - reduction_factor * line_spacing[key])

    # Redraw the text with the reduced line spacing
    y_position = 20
    previous_style_key = None
    for line in text.split('\n'):
        original_line = line
        if "[NLA]" in line:
            show_prev = False
        if "[NRA]" in line:
            show_next = False

        style_key = None
        if line.startswith("[title]"):
            style_key = "title"
            line = line.replace("[title]", "")
        elif line.startswith("[narrator]"):
            style_key = "narrator"
            line = line.replace("[narrator]", "")
        elif line.startswith("[narratorc]"):
            style_key = "narratorc"
            line = line.replace("[narratorc]", "")
        elif line.startswith("[dialogue]"):
            style_key = "dialogue"
            line = line.replace("[dialogue]", "").replace("+", "")
        elif line.startswith("[centered]"):
            style_key = "centered"
            line = line.replace("[centered]", "")

        if style_key:
            style = styles[style_key]
            if previous_style_key and previous_style_key != style_key:
                y_position += 8 if previous_style_key == "title" or style_key == "title" else 4
            
            if style_key == "narratorc" or style_key == "centered":
                position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
                draw.text(position, line, font=style["font"], fill=style["fill"])
                y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing.get(style_key, 6)
            else:
                y_position = draw_text_with_formatting(draw, (50 if style_key == "narrator" else 70, y_position), line, style["font"], style["fill"], line_spacing.get(style_key, 6))
                if style_key == "narrator":
                    next_line_index = text.split('\n').index(original_line) + 1
                    if next_line_index < len(text.split('\n')) and not text.split('\n')[next_line_index].startswith("[dialogue]+"):
                        y_position += 4
                if style_key == "dialogue" and "[dialogue]+" not in original_line:
                    y_position += 4
            
            previous_style_key = style_key

    if show_next:
        next_text = "következő"
        next_position_text = (img.width - draw.textbbox((0, 0), next_text, font=styles["dialogue"]["font"])[2] - 70, img.height - 36)
        next_position_arrow = (next_position_text[0] + draw.textbbox((0, 0), next_text, font=styles["dialogue"]["font"])[2] + 10, img.height - 40)
        draw.text(next_position_text, next_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))
        if os.path.exists("right_arrow.png"):
            right_arrow_img = Image.open("right_arrow.png")
            img.paste(right_arrow_img, next_position_arrow)
        else:
            print("right_arrow.png not found, skipping.")
    
    if show_prev:
        prev_text = "előző"
        prev_position_text = (70, img.height - 36)
        prev_position_arrow = (prev_position_text[0] - 40, img.height - 40)
        draw.text(prev_position_text, prev_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))
        if os.path.exists("left_arrow.png"):
            left_arrow_img = Image.open("left_arrow.png")
            img.paste(left_arrow_img, prev_position_arrow)
        else:
            print("left_arrow.png not found, skipping.")
    
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
                    print(f"{output_path} already exists and the text matches, skipping.")
                    continue
                else:
                    print(f"{output_path} already exists, but the text differs, regenerating.")
            create_image(text, output_path)

# Specify the directory where the .tpng files are located
directory = "tpng/"

# Process all .tpng files in the specified directory
process_all_tpng_files(directory)
