from PIL import Image, ImageDraw, ImageFont, ImageFilter, PngImagePlugin
import os
# narratorc stílus hozzáadva
#tpng feature hozzáadva
#kihagyja a létező fileokat, META adatok alpján
#[NLA] & [NRA] felismerése DOCTYPE5-től OK
def create_image(text, output_path):
    # Kép létrehozása
    img = Image.new('RGB', (512, 448), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Betűtípusok és méretek beállítása
    regular_font = ImageFont.truetype("arial.ttf", 14, encoding="unic")
    italic_font = ImageFont.truetype("ariali.ttf", 14, encoding="unic")
    title_font = ImageFont.truetype("arial.ttf", 24, encoding="unic")
    centered_font = ImageFont.truetype("arial.ttf", 14, encoding="unic")
    white_bg_font = ImageFont.truetype("arial.ttf", 26, encoding="unic")
    blue_center_font = ImageFont.truetype("arial.ttf", 24, encoding="unic")
    
    # Szöveg stílusok
    styles = {
        "title": {"font": title_font, "fill": (245, 245, 245)},
        "narrator": {"font": italic_font, "fill": (80, 131, 213)},
        "dialogue": {"font": regular_font, "fill": (171, 171, 171)},
        "centered": {"font": centered_font, "fill": (255, 255, 255)},
        "narratorc": {"font": italic_font, "fill": (80, 131, 213)},
        "white_bg": {"font": white_bg_font, "fill": (255, 255, 255)},
        "blue_center": {"font": blue_center_font, "fill": (5, 20, 220)}
    }
    
    # Sortávolságok és extra sorközök beállítása
    line_spacing = {
        "title": 15,
        "narrator": 6,
        "dialogue": 6,
        "centered": 6,
        "narratorc": 6
    }
    extra_spacing = {
        "title": 0,
        "narrator": 0,
        "dialogue": 0,
        "centered": 0,
        "narratorc": 0
    }
    
    # Szöveg hozzáadása stílusokkal
    y_position = 20
    max_width = img.width - 40

    # Új változók a [NLA] és [NRA] kódok kezeléséhez
    show_prev = True
    show_next = True
    
    for line in text.split('\n'):
        
        if "[NLA]" in line:
            show_prev = False
        
        if "[NRA]" in line:
            show_next = False
        
        if line.startswith("+"):
            y_position += extra_spacing["dialogue"]
            line = line[1:].strip()
        
        if line.startswith("[title]"):
            style = styles["title"]
            line = line.replace("[title]", "")
            position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
            
            # Háttér fehér felirat hozzáadása nagyobb blur effekttel
            draw.text((position[0], position[1]), line, font=styles["white_bg"]["font"], fill=styles["white_bg"]["fill"])
            img_blur_white = img.filter(ImageFilter.GaussianBlur(radius=15))
            img.paste(img_blur_white)            
            # Középső világoskék felirat hozzáadása közepes blur effekttel
            draw.text((position[0], position[1]), line, font=styles["blue_center"]["font"], fill=styles["blue_center"]["fill"])
            img_blur_blue = img.filter(ImageFilter.GaussianBlur(radius=5))
            img.paste(img_blur_blue)
            
            # Elülső fehér felirat hozzáadása
            draw.text(position, line, font=style["font"], fill=style["fill"])
            
            y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing["title"] + extra_spacing["title"]
        elif line.startswith("[narrator]"):
            style = styles["narrator"]
            line = line.replace("[narrator]", "")
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
            y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["narrator"] + extra_spacing["narrator"]
        elif line.startswith("[dialogue]"):
            style = styles["dialogue"]
            line = line.replace("[dialogue]", "")
            words = line.split(' ')
            current_line = ""
            for word in words:
                if word == "+":
                    y_position += extra_spacing["dialogue"]
                elif word == "/":
                    draw.text((70, y_position), current_line.strip(), font=style["font"], fill=style["fill"])
                    y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["dialogue"] + extra_spacing["dialogue"]
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
            y_position += draw.textbbox((0, 0), current_line.strip(), font=style["font"])[3] + line_spacing["dialogue"] + extra_spacing["dialogue"]
        elif line.startswith("[centered]"):
            y_position += extra_spacing["centered"]
            style = styles["centered"]
            line = line.replace("[centered]", "")
            position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
            draw.text(position, line, font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing["centered"] + extra_spacing["centered"]
        elif line.startswith("[narratorc]"):
            y_position += extra_spacing["narratorc"]
            style = styles["narratorc"]
            line = line.replace("[narratorc]", "")
            position = (img.width // 2 - draw.textbbox((0, 0), line, font=style["font"])[2] // 2, y_position)
            draw.text(position, line, font=style["font"], fill=style["fill"])
            y_position += draw.textbbox((0, 0), line, font=style["font"])[3] + line_spacing["narratorc"] + extra_spacing["narratorc"]
    
    # "Következő" felirat és nyíl hozzáadása
    next_text = ""  # Alapértelmezett érték
    if show_next:
        next_text = "következő"
    next_position_text = (img.width - draw.textbbox((0, 0), next_text, font=styles["dialogue"]["font"])[2] - 70,
                          img.height - 36) # Move text down by 4 pixels
    next_position_arrow = (next_position_text[0] + draw.textbbox((0, 0), next_text,
                                                                 font=styles["dialogue"]["font"])[2] + 10,
                           img.height - 40) # Arrow position remains the same
    if show_next:
        draw.text(next_position_text, next_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))

        # Ellenőrizd, hogy a right_arrow.png létezik-e
        if os.path.exists("right_arrow.png"):
            right_arrow_img = Image.open("right_arrow.png")
            img.paste(right_arrow_img, next_position_arrow)
        else:
            print("right_arrow.png nem található, kihagyva.")

# "Előző" felirat és nyíl hozzáadása
    prev_text = ""  # Alapértelmezett érték
    if show_prev:
        prev_text = "előző"
    prev_position_text = (70, img.height - 36) # Move text down by 4 pixels
    prev_position_arrow = (prev_position_text[0] - 40, img.height - 40) # Arrow position remains the same
    if show_prev:
        draw.text(prev_position_text, prev_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))

        # Ellenőrizd, hogy a left_arrow.png létezik-e
        if os.path.exists("left_arrow.png"):
            left_arrow_img = Image.open("left_arrow.png")
            img.paste(left_arrow_img, prev_position_arrow)
        else:
            print("left_arrow.png nem található, kihagyva.")

    # Oldalszám hozzáadása a lábléc közepére
    page_number_text = "1"  # Alapértelmezett oldalszám
    for line in text.split('\n'):
        if line.startswith("[pn]"):
            page_number_text = line.replace("[pn]", "").strip()
            break
    page_number_position = (img.width // 2 - draw.textbbox((0, 0), page_number_text, font=styles["dialogue"]["font"])[2] // 2, img.height - 40)
    draw.text(page_number_position, page_number_text, font=styles["dialogue"]["font"], fill=(255, 255, 255))

    # Szöveg beágyazása metaadatként
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Description", text)

    # Kép mentése
    img.save(output_path, pnginfo=meta)

def verify_image_text(image_path, original_text):
    img = Image.open(image_path)
    meta = img.info
    embedded_text = meta.get("Description", "")
    #print(f"Original text: {original_text}")
    #print(f"Embedded text: {embedded_text}")
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

# Szöveg és kimeneti fájl megadása
process_all_tpng_files(directory)
