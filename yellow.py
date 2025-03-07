from PIL import Image, ImageDraw, ImageFont  # Importowanie modułów do pracy z obrazkami
import os  # Moduł do pracy z systemem plików
import sys  # Moduł do obsługi argumentów wiersza poleceń
import glob  # Moduł do wyszukiwania plików

# Funkcja generująca obrazek z tekstem PTF
def generate_text_image(ptf_number):
    # Wymiary obrazka
    width, height = 1080, 500

    # Tworzenie przezroczystego obrazka
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Załadowanie fontu
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')  # Ścieżka do czcionki
    font_size = 150
    font = ImageFont.truetype(font_path, font_size)
    
    # Załadowanie fontu dla liczby
    number_font_size = 474
    number_font = ImageFont.truetype(font_path, number_font_size)

    # Utworzenie obiektu do rysowania na obrazie
    draw = ImageDraw.Draw(image)

    # Litery do narysowania
    letters = ["P", "T", "F"]
    interline = 12  # Odstęp między literami

    # Obliczenie wysokości całego bloku tekstu
    total_text_height = sum(draw.textbbox((0, 0), letter, font=font)[3] - draw.textbbox((0, 0), letter, font=font)[1] for letter in letters) + interline * (len(letters) - 1)

    # Obliczenie pozycji startowej (środek obrazka)
    y_start = (height - total_text_height) // 2

    # Rysowanie liter jedna pod drugą, wyśrodkowane
    for letter in letters:
        text_bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2 + 400  # Pozycjonowanie w poziomie
        draw.text((x, y_start), letter, font=font, fill="black")
        y_start += text_height + interline  # Przesuwanie pozycji Y dla następnej litery

    # Dodanie liczby po prawej stronie z odstępem 10 pikseli
    number_bbox = draw.textbbox((0, 0), ptf_number, font=number_font)
    number_width = number_bbox[2] - number_bbox[0]
    number_x = width - number_width - 220  # Pozycjonowanie liczby w poziomie
    number_y = (height - number_font_size) // 2  # Wyśrodkowanie liczby w pionie

    draw.text((number_x, number_y), ptf_number, font=number_font, fill="black")

    # Cropowanie obrazka, usuwanie przezroczystych marginesów
    bbox = image.getbbox()
    cropped_image = image.crop(bbox)

    return cropped_image  # Zwrócenie wygenerowanego obrazka

# Funkcja generująca przezroczysty obrazek z tekstem dla identyfikatora
def transp_ID_gen(ptf_number):
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')  # Ścieżka do czcionki

    # Wymiary obrazka
    width, height = 1080, 250

    # Tworzenie przezroczystego obrazka
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # Załadowanie fontu
    font_size = 57
    font = ImageFont.truetype(font_path, font_size)

    # Załadowanie fontu dla liczby
    number_font_size = 227
    number_font = ImageFont.truetype(font_path, number_font_size)

    # Utworzenie obiektu do rysowania na obrazie
    draw = ImageDraw.Draw(image)

    # Litery do narysowania
    letters = ["PODZIEMNY", "TURNIEJ we", "FLANKI"]
    interline = 15  # Odstęp między liniami tekstu

    # Obliczenie wysokości całego bloku tekstu
    total_text_height = sum(draw.textbbox((0, 0), letter, font=font)[3] - draw.textbbox((0, 0), letter, font=font)[1] for letter in letters) + interline * (len(letters) - 1)

    # Obliczenie pozycji startowej (środek obrazka)
    y_start = (height - total_text_height) // 2

    # Rysowanie tekstu linia za linią
    draw.text((550, 15), "PODZIEMNY", font=font, fill="black")
    draw.text((550, 100), "TURNIEJ we", font=font, fill="black")
    draw.text((550, 185), "FLANKI", font=font, fill="black")

    # Dodanie liczby po lewej stronie
    number_bbox = draw.textbbox((0, 0), ptf_number, font=number_font)
    number_width = number_bbox[2] - number_bbox[0]
    number_x = width - number_width - 530  # Pozycjonowanie liczby w poziomie
    number_y = (height - number_font_size) // 2  # Wyśrodkowanie liczby w pionie

    draw.text((number_x, number_y), ptf_number, font=number_font, fill="black")

    # Cropowanie obrazka, usuwanie przezroczystych marginesów
    bbox = image.getbbox()
    cropped_image = image.crop(bbox)

    return cropped_image  # Zwrócenie wygenerowanego obrazka

# Funkcja do generowania obrazów z różnymi formatami
def generate_image(ptf_num, date_str, time_str):
    generate_y_event_fb(ptf_num, date_str, time_str)
    generate_y_reel_ig(ptf_num, date_str, time_str)
    generate_y_tile_ig(ptf_num, date_str, time_str)

# Funkcja do pobierania pliku szablonu z folderu
def get_template_file(folder, filename):
    files = glob.glob(os.path.join(folder, filename + ".*"))  # Szuka dowolnego rozszerzenia
    if files:
        return files[0]  # Zwraca pierwszy znaleziony plik
    else:
        raise FileNotFoundError(f"Plik {filename} nie został znaleziony w folderze {folder}")  # Błąd, gdy plik nie istnieje

# Funkcja do generowania obrazu na szablonie 'y_event_fb'
def generate_y_event_fb(ptf_num, date_str, time_str):
    template_path = get_template_file('templates', 'y_event_fb')  # Ścieżka do szablonu  
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')  # Ścieżka do czcionki

    image = Image.open(template_path)  # Wczytanie szablonu
    draw = ImageDraw.Draw(image)  # Utworzenie obiektu do rysowania na obrazie

    # Generowanie obrazu z numerem i tekstem
    id_image = transp_ID_gen(ptf_num)

    # Pozycjonowanie obrazu na szablonie
    id_image_width, id_image_height = id_image.size
    x_position = (image.width - id_image_width) // 2
    y_position = 273

    # Wstawienie wygenerowanego obrazu na szablon
    image.paste(id_image, (x_position, y_position), id_image)

    # Dodanie daty i godziny na szablonie
    date_time_text = f"{date_str} {time_str}"
    date_time_font_size = 50
    date_time_font = ImageFont.truetype(font_path, date_time_font_size)

    date_time_bbox = draw.textbbox((0, 0), date_time_text, font=date_time_font)
    date_time_text_width = date_time_bbox[2] - date_time_bbox[0]

    date_time_x_position = (image.width - date_time_text_width) / 2
    date_time_y_position = image.height - date_time_bbox[3] - 265

    draw.text((date_time_x_position, date_time_y_position), date_time_text, font=date_time_font, fill="black")

    # Zapisanie obrazu
    output_path = os.path.join('outputs', f'{ptf_num}_y_event_fb.jpg')  
    image.save(output_path, "PNG")

    print(f"Image has been saved as {output_path}")  # Informacja o zapisanym obrazie

# Funkcja do generowania obrazu na szablonie 'y_reel_ig'
def generate_y_reel_ig(ptf_num, date_str, time_str):
    template_path = get_template_file('templates', 'y_reel_ig')  # Ścieżka do szablonu
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')  # Ścieżka do czcionki

    image = Image.open(template_path)  # Wczytanie szablonu
    draw = ImageDraw.Draw(image)  # Utworzenie obiektu do rysowania na obrazie

    # Generowanie obrazu z numerem i tekstem
    id_image = transp_ID_gen(ptf_num)

    # Pozycjonowanie obrazu na szablonie
    id_image_width, id_image_height = id_image.size
    x_position = (image.width - id_image_width) // 2
    y_position = 234

    # Wstawienie wygenerowanego obrazu na szablon
    image.paste(id_image, (x_position, y_position), id_image)

    # Dodanie daty na szablonie
    date_time_text = date_str
    font_size2 = 83
    font2 = ImageFont.truetype(font_path, font_size2)
    date_time_bbox = draw.textbbox((0, 0), date_time_text, font=font2)
    date_time_text_width = date_time_bbox[2] - date_time_bbox[0]

    date_time_x_position = (image.width - date_time_text_width) / 2
    date_time_y_position = image.height - date_time_bbox[3] - 1000

    draw.text((date_time_x_position, date_time_y_position), date_time_text, font=font2, fill="black")

    # Dodanie godziny na szablonie
    time_text = f"godz. {time_str}"
    time_bbox = draw.textbbox((0, 0), time_text, font=font2)
    time_text_width = time_bbox[2] - time_bbox[0]

    time_x_position = (image.width - time_text_width) / 2
    time_y_position = image.height - time_bbox[3] - 800

    draw.text((time_x_position, time_y_position), time_text, font=font2, fill="black")

    # Zapisanie obrazu
    output_path = os.path.join('outputs', f'{ptf_num}_y_reel_ig.jpg')  
    image.save(output_path, "PNG")

    print(f"Image has been saved as {output_path}")  # Informacja o zapisanym obrazie

# Funkcja do generowania obrazu na szablonie 'y_tile_ig'
def generate_y_tile_ig(ptf_number, date_str, time_str):
    # Generowanie obrazka z tekstem i numerem
    text_image = generate_text_image(ptf_number)

    # Wczytanie template
    template_path = get_template_file('templates', 'y_tile_ig')  
    template = Image.open(template_path)
    template_width, template_height = template.size

    # Wstawienie wygenerowanego obrazka na template
    text_image_width, text_image_height = text_image.size
    position = ((template_width - text_image_width) // 2, (template_height - text_image_height) // 2)
    template.paste(text_image, position, text_image)

    # Dodanie daty i godziny na template
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')
    date_font_size = 57
    date_font = ImageFont.truetype(font_path, date_font_size)

    draw = ImageDraw.Draw(template)  # Utworzenie obiektu do rysowania na template

    # Obliczanie pozycji dla daty i godziny
    date_text = date_str
    time_text = f"godz. {time_str}"
    
    date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
    time_bbox = draw.textbbox((0, 0), time_text, font=date_font)
    
    date_text_width = date_bbox[2] - date_bbox[0]
    time_text_width = time_bbox[2] - time_bbox[0]
    
    # Pozycje daty i godziny w prawym dolnym rogu
    date_x = template_width - 60 - date_text_width
    date_y = position[1] + text_image_height + 110
    
    time_x = template_width - 60 - time_text_width
    time_y = date_y + date_font_size + 20  # Poniżej daty

    draw.text((date_x, date_y), date_text, font=date_font, fill="black")
    draw.text((time_x, time_y), time_text, font=date_font, fill="black")

    # Zapisanie obrazka
    if not os.path.exists('outputs'): os.makedirs('outputs')

    output_path = os.path.join('outputs', f"{ptf_number}_y_tile_ig.jpg")  
    template.save(output_path, "PNG")

    print(f"Obraz został zapisany jako {output_path}")  # Informacja o zapisanym obrazie

# Główna część programu
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Please provide the arguments in the format: <ptf_num> <DD.MM.YYYY> <HH:MM>")
    else:
        ptf_num = sys.argv[1]  # Numer PTG
        date_str = sys.argv[2]  # Data
        time_str = sys.argv[3]  # Godzina

        generate_image(ptf_num, date_str, time_str)  # Wywołanie funkcji generującej obrazy
