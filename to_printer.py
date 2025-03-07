import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Funkcja generująca kartę z datą i godziną
def generate_date_time_card(date_str, time_str):
    # Tworzenie pustego obrazka z białym tłem
    width_mm = 187  # Szerokość karty w mm
    height_mm = 72  # Wysokość karty w mm
    dpi = 300  # Rozdzielczość obrazu (w dpi, odpowiednia do wydruku)
    
    # Konwersja rozmiarów w mm na piksele przy zadanej rozdzielczości
    width_px = int(width_mm * dpi / 25.4)  # Przeliczenie mm na piksele
    height_px = int(height_mm * dpi / 25.4)  # Przeliczenie mm na piksele
    
    # Tworzenie pustego obrazka o wymiarach karty
    image = Image.new('RGB', (width_px, height_px), 'white')  # Kolor tła to biały
    draw = ImageDraw.Draw(image)  # Utworzenie obiektu do rysowania na obrazie

    # Ładowanie czcionki
    font_path = os.path.join('FONTS', 'RomeoDN.ttf')  # Ścieżka do czcionki
    font_size = 200  # Rozmiar czcionki
    font = ImageFont.truetype(font_path, font_size)  # Załadowanie czcionki w określonym rozmiarze
    
    # Obliczenie wymiarów tekstu
    date_text = date_str  # Tekst z datą
    time_text = time_str  # Tekst z godziną
    date_bbox = draw.textbbox((0, 0), date_text, font=font)  # Obliczanie wymiarów tekstu daty
    time_bbox = draw.textbbox((0, 0), time_text, font=font)  # Obliczanie wymiarów tekstu godziny

    # Obliczenie pozycji, w której wyświetli się tekst daty
    date_width = date_bbox[2] - date_bbox[0]  # Szerokość tekstu daty
    date_height = date_bbox[3] - date_bbox[1]  # Wysokość tekstu daty
    time_width = time_bbox[2] - time_bbox[0]  # Szerokość tekstu godziny
    time_height = time_bbox[3] - time_bbox[1]  # Wysokość tekstu godziny

    # Wyśrodkowanie tekstu na obrazie
    date_x = (width_px - date_width) // 2  # Współrzędna X dla tekstu daty
    date_y = (height_px - date_height) // 2 - font_size // 2 - 20  # Współrzędna Y dla tekstu daty
    time_x = (width_px - time_width) // 2  # Współrzędna X dla tekstu godziny
    time_y = (height_px - time_height) // 2 + font_size // 2 + 20  # Współrzędna Y dla tekstu godziny

    # Rysowanie tekstu daty i godziny na obrazie
    draw.text((date_x, date_y), date_text, font=font, fill='black')  # Tekst daty
    draw.text((time_x, time_y), time_text, font=font, fill='black')  # Tekst godziny

    # Dodanie czarnej ramki wokół karty
    border_width = 1  # Grubość ramki
    for i in range(border_width):
        draw.rectangle([i, i, width_px-i-1, height_px-i-1], outline='black')  # Rysowanie ramki

    return image  # Zwrócenie wygenerowanego obrazu karty

# Funkcja do tworzenia obrazu A4 z trzema kartami
def create_a4_canvas_with_cards(card_image):
    # Tworzenie pustego obrazu o rozmiarze A4
    a4_width_mm = 210  # Szerokość kartki A4 w mm
    a4_height_mm = 297  # Wysokość kartki A4 w mm
    dpi = 300  # Rozdzielczość obrazu (300 dpi, standard dla wydruku)
    
    # Konwersja rozmiaru A4 z mm na piksele
    a4_width_px = int(a4_width_mm * dpi / 25.4)  # Szerokość w pikselach
    a4_height_px = int(a4_height_mm * dpi / 25.4)  # Wysokość w pikselach
    
    # Tworzenie pustego obrazu o rozmiarze A4
    a4_image = Image.new('RGB', (a4_width_px, a4_height_px), 'white')  # Białe tło
    
    # Obliczanie pozycji, w której będą umieszczone karty
    card_width, card_height = card_image.size  # Pobranie wymiarów karty
    top_margin = 135  # Odstęp od górnej krawędzi A4
    vertical_spacing = 50  # Odstęp pionowy między kartami
    x_offset = (a4_width_px - card_width) // 2  # Wyśrodkowanie kart poziomo na A4

    # Wklejanie trzech kart na obrazie A4
    for i in range(3):  # Iteracja przez 3 karty
        y_offset = top_margin + i * (card_height + vertical_spacing)  # Obliczenie pozycji Y
        a4_image.paste(card_image, (x_offset, y_offset))  # Wklejanie karty na obraz A4

    return a4_image  # Zwrócenie wygenerowanego obrazu A4

# Sprawdzenie argumentów wiersza poleceń
if len(sys.argv) != 4:
    print("Usage: python to_printer.py <ptf_num> <date_str> <time_str>")
    sys.exit(1)

# Przypisanie argumentów wiersza poleceń
ptf_num = sys.argv[1]  # Numer PT-F
date_str = sys.argv[2]  # Data (w formacie DD.MM.YYYY)
time_str = sys.argv[3]  # Godzina (w formacie HH:MM)

# Generowanie karty z datą i godziną
card_image = generate_date_time_card(date_str, time_str)

# Tworzenie obrazu A4 z trzema kartami
a4_image = create_a4_canvas_with_cards(card_image)

# Zapisanie finalnego obrazu
if not os.path.exists('outputs'):
    os.makedirs('outputs')  # Tworzenie folderu outputs, jeśli nie istnieje

output_path = os.path.join('outputs', f'{ptf_num}_date_time_cards_A4.png')  # Ścieżka do zapisu
a4_image.save(output_path)  # Zapisanie obrazu do pliku
print(f"Image saved to {output_path}")  # Potwierdzenie zapisu
