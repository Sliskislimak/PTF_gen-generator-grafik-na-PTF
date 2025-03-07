from PIL import Image, ImageDraw, ImageFont
import os
import sys
import glob

# Funkcja ładowania obrazu
def load_image(ptf_number):
    try:
        image_path = os.path.join('mod10', f'{ptf_number}.png')
        image = Image.open(image_path).convert("RGBA")
        return image
    except FileNotFoundError:
        raise FileNotFoundError(f"Image with number {ptf_number} not found in 'mod10' folder")

# Funkcja generująca obrazek z tekstem i logo
def generate_text_image(ptf_number):
    png_logo = load_image(ptf_number)
    width, height = 1080, 500

    # Tworzenie przezroczystego obrazka
    transparent_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Załadowanie fontu
    font_path = os.path.join('fonts', 'RomeoDN.ttf')
    font_size = 150
    font = ImageFont.truetype(font_path, font_size)
    
    # Utworzenie obiektu do rysowania
    draw = ImageDraw.Draw(transparent_image)

    # Litery do narysowania
    letters = ["P", "T", "F"]
    interline = 12

    # Obliczenie wysokości całego bloku tekstu
    total_text_height = sum(draw.textbbox((0, 0), letter, font=font)[3] - draw.textbbox((0, 0), letter, font=font)[1] for letter in letters) + interline * (len(letters) - 1)

    # Obliczenie pozycji startowej (środek obrazka)
    y_start = (height - total_text_height) // 2

    # Rysowanie liter jedna pod drugą, wyśrodkowane
    for letter in letters:
        text_bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2 + 400
        draw.text((x, y_start), letter, font=font, fill="white")
        y_start += text_height + interline

    # Skalowanie logo
    scale_factor = 2.10
    new_width = int(png_logo.width * scale_factor)
    new_height = int(png_logo.height * scale_factor)
    scaled_png_logo = png_logo.resize((new_width, new_height))
    
    # Obliczenie pozycji dla wklejenia obrazka
    x_position = width - new_width - 10
    y_position = (height - new_height) // 2

    # Wstawienie obrazka PNG na główny obrazek
    transparent_image.paste(scaled_png_logo, (250, 0),scaled_png_logo)

    # Cropowanie obrazka, usuwanie przezroczystych marginesów
    bbox = transparent_image.getbbox()
    cropped_image = transparent_image.crop(bbox)

    return cropped_image

# Funkcja generująca przezroczysty ID
def transp_ID_gen(ptf_number):
    png_logo = load_image(ptf_number)

    width, height = 1080, 250

    # Tworzenie przezroczystego obrazka
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Załadowanie fontu
    font_path = os.path.join('fonts', 'RomeoDN.ttf')
    font_size = 57
    font = ImageFont.truetype(font_path, font_size)

    # Utworzenie obiektu do rysowania
    draw = ImageDraw.Draw(image)

    # Litery do narysowania
    letters = ["PODZIEMNY", "TURNIEJ we", "FLANKI"]
    interline = 15

    # Obliczenie całkowitej wysokości bloku tekstu
    total_text_height = sum(draw.textbbox((0, 0), letter, font=font)[3] - draw.textbbox((0, 0), letter, font=font)[1] for letter in letters) + interline * (len(letters) - 1)

    # Rysowanie tekstu linia po linii
    draw.text((550, 15), "PODZIEMNY", font=font, fill="white")  
    draw.text((550, 100), "TURNIEJ we", font=font, fill="white")  
    draw.text((550, 185), "FLANKI", font=font, fill="white")  

    # Pozycjonowanie logo
    x_position = width - png_logo.width - 10
    y_position = (height - png_logo.height) // 2
    image.paste(png_logo, (250, 15), png_logo)

    # Cropowanie obrazka, usuwanie przezroczystych marginesów
    bbox = image.getbbox()
    cropped_image = image.crop(bbox)

    return cropped_image

# Funkcja generująca wszystkie obrazy
def generate_image(ptf_num, date_str, time_str):
    generate_r_event_fb(ptf_num, date_str, time_str)
    generate_r_reel_ig(ptf_num, date_str, time_str)
    generate_r_tile_ig(ptf_num, date_str, time_str)

# Funkcja wyszukiwania pliku szablonu
def get_template_file(folder, filename):
    files = glob.glob(os.path.join(folder, filename + ".*"))
    if files:
        return files[0]
    else:
        raise FileNotFoundError(f"Plik {filename} nie został znaleziony w folderze {folder}")

# Generowanie obrazu na Facebooka
def generate_r_event_fb(ptf_num, date_str, time_str):
    template_path = get_template_file('templates', 'r_event_fb')
    font_path = os.path.join('fonts', 'RomeoDN.ttf')

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Generowanie obrazu z numerem i tekstem
    id_image = transp_ID_gen(ptf_num)

    # Pozycjonowanie obrazu
    id_image_width, id_image_height = id_image.size
    x_position = (image.width - id_image_width) // 2
    y_position = 273

    # Wstawienie wygenerowanego obrazu na template
    image.paste(id_image, (x_position, y_position), id_image)

    date_time_text = f"{date_str} {time_str}"
    date_time_font_size = 50
    date_time_font = ImageFont.truetype(font_path, date_time_font_size)

    date_time_bbox = draw.textbbox((0, 0), date_time_text, font=date_time_font)
    date_time_text_width = date_time_bbox[2] - date_time_bbox[0]

    date_time_x_position = (image.width - date_time_text_width) / 2
    date_time_y_position = image.height - date_time_bbox[3] - 265

    draw.text((date_time_x_position, date_time_y_position), date_time_text, font=date_time_font, fill="white")

    output_path = os.path.join('outputs', f'{ptf_num}_r_event_fb.png')
    image.save(output_path)

    print(f"Image has been saved as {output_path}")

# Generowanie obrazu na Instagram Reels
def generate_r_reel_ig(ptf_num, date_str, time_str):
    template_path = get_template_file('templates', 'r_reel_ig')
    font_path = os.path.join('fonts', 'RomeoDN.ttf')

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Generowanie obrazu z numerem i tekstem
    id_image = transp_ID_gen(ptf_num)

    # Pozycjonowanie obrazu
    id_image_width, id_image_height = id_image.size
    x_position = (image.width - id_image_width) // 2
    y_position = 234

    # Wstawienie wygenerowanego obrazu na template
    image.paste(id_image, (x_position, y_position), id_image)

    date_time_text = date_str
    font_size2 = 83
    font2 = ImageFont.truetype(font_path, font_size2)
    date_time_bbox = draw.textbbox((0, 0), date_time_text, font=font2)
    date_time_text_width = date_time_bbox[2] - date_time_bbox[0]

    date_time_x_position = (image.width - date_time_text_width) / 2
    date_time_y_position = image.height - date_time_bbox[3] - 1000

    draw.text((date_time_x_position, date_time_y_position), date_time_text, font=font2, fill="white")

    # Dodanie godziny
    time_text = f"godz. {time_str}"
    time_bbox = draw.textbbox((0, 0), time_text, font=font2)
    time_width = time_bbox[2] - time_bbox[0]
    time_x_position = (image.width - time_width) / 2
    time_y_position = date_time_y_position + 150

    draw.text((time_x_position, time_y_position), time_text, font=font2, fill="white")

    output_path = os.path.join('outputs', f'{ptf_num}_r_reel_ig.png')
    image.save(output_path)

    print(f"Image has been saved as {output_path}")

# Generowanie obrazu na Instagram Tile
def generate_r_tile_ig(ptf_num, date_str, time_str):
    template_path = get_template_file('templates', 'r_tile_ig')
    font_path = os.path.join('fonts', 'RomeoDN.ttf')

    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Generowanie obrazu z numerem i tekstem
    id_image = transp_ID_gen(ptf_num)

    # Pozycjonowanie obrazu
    id_image_width, id_image_height = id_image.size
    x_position = (image.width - id_image_width) // 2
    y_position = 219

    # Wstawienie wygenerowanego obrazu na template
    image.paste(id_image, (x_position, y_position), id_image)

    # Wstawienie daty i godziny
    date_time_text = f"{date_str} {time_str}"
    date_time_font_size = 66
    date_time_font = ImageFont.truetype(font_path, date_time_font_size)

    date_time_bbox = draw.textbbox((0, 0), date_time_text, font=date_time_font)
    date_time_text_width = date_time_bbox[2] - date_time_bbox[0]

    date_time_x_position = (image.width - date_time_text_width) / 2
    date_time_y_position = image.height - date_time_bbox[3] - 265

    draw.text((date_time_x_position, date_time_y_position), date_time_text, font=date_time_font, fill="white")

    output_path = os.path.join('outputs', f'{ptf_num}_r_tile_ig.png')
    image.save(output_path)

    print(f"Image has been saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Please provide the arguments in the format: <ptf_num> <DD.MM.YYYY> <HH:MM>")
    else:
        ptf_num = sys.argv[1]
        date_str = sys.argv[2]
        time_str = sys.argv[3]

        generate_image(ptf_num, date_str, time_str)
