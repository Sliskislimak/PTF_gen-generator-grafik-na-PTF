import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import subprocess
import re

# Klasa do obsługi okna dialogowego, w którym użytkownik dodaje szczegóły imprezy
class EventEntryDialog(tk.Toplevel):
    def __init__(self, parent, selected_date):
        super().__init__(parent)
        self.title("Dodaj imprezę")  # Ustawia tytuł okna dialogowego
        self.selected_date = selected_date  # Zapisuje wybraną datę
        self.result = None  # Zmienna do przechowywania wyników wprowadzonych przez użytkownika

        # Wyświetlenie wybranej daty w oknie dialogowym
        ttk.Label(self, text=f"Data: {selected_date}").grid(row=0, column=0, padx=10, pady=5)

        # Pole do wpisania numeru turnieju
        ttk.Label(self, text="Numer turnieju:").grid(row=1, column=0, padx=10, pady=5)
        self.tournament_entry = ttk.Entry(self)  # Pole tekstowe do wpisania numeru turnieju
        self.tournament_entry.grid(row=1, column=1, padx=10, pady=5)

        # Pole do wpisania godziny
        ttk.Label(self, text="Godzina (HH:MM):").grid(row=2, column=0, padx=10, pady=5)
        self.time_entry = ttk.Entry(self)  # Pole tekstowe do wpisania godziny
        self.time_entry.insert(0, "20:00")  # Ustawienie domyślnej godziny
        self.time_entry.grid(row=2, column=1, padx=10, pady=5)

        # Przycisk "Dodaj", który uruchamia metodę `on_add` po kliknięciu
        ttk.Button(self, text="Dodaj", command=self.on_add).grid(row=3, columnspan=2, pady=10)
        # Powiązanie klawisza "Enter" z metodą `on_add`
        self.bind('<Return>', lambda event: self.on_add())

    # Metoda do obsługi kliknięcia przycisku "Dodaj"
    def on_add(self):
        tournament = self.tournament_entry.get().strip()  # Pobiera numer turnieju
        time = self.time_entry.get().strip()  # Pobiera godzinę

        # Sprawdzenie, czy numer turnieju nie jest pusty
        if not tournament:
            messagebox.showwarning("Błąd", "Podaj numer turnieju.")  # Wyświetlenie komunikatu, jeśli brak numeru
            return
        
        # Walidacja formatu godziny (HH:MM)
        try:
            hour, minute = map(int, time.split(':'))  # Próba rozdzielenia godziny i minut
            if not (0 <= hour < 24 and 0 <= minute < 60):  # Sprawdzenie, czy godzina i minuta są poprawne
                raise ValueError
        except Exception:
            messagebox.showwarning("Błąd", "Niepoprawny format godziny (HH:MM).")  # Komunikat o błędzie formatu godziny
            return

        # Zapisanie danych (data, numer turnieju, godzina)
        self.result = (self.selected_date, tournament, time)
        self.destroy()  # Zamknięcie okna dialogowego

# Główna klasa aplikacji, odpowiedzialna za interfejs użytkownika i logikę aplikacji
class PTFGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PTF_Gen 2.0 by Graft and Profugus - Multi Event")  # Tytuł okna głównego aplikacji

        # Tworzenie kalendarza do wyboru daty
        self.cal = Calendar(self, selectmode='day', date_pattern='dd.mm.yyyy')
        self.cal.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Przycisk "Dodaj imprezę" otwierający okno do dodania nowej imprezy
        ttk.Button(self, text="Dodaj imprezę", command=self.add_event).grid(row=1, column=0, padx=10, pady=5)
        # Przycisk "Generuj grafiki", który uruchamia metodę generowania grafik
        ttk.Button(self, text="Generuj grafiki", command=self.generate_graphics).grid(row=1, column=1, padx=10, pady=5)

        # Listbox wyświetlający listę dodanych imprez
        self.events_listbox = tk.Listbox(self, width=50)
        self.events_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Lista imprez - każda impreza to krotka (data, numer_turnieju, godzina)
        self.events = []

    # Metoda do otwarcia okna dialogowego i dodania imprezy
    def add_event(self):
        selected_date = self.cal.get_date()  # Pobranie wybranej daty
        dialog = EventEntryDialog(self, selected_date)  # Tworzenie obiektu okna dialogowego
        self.wait_window(dialog)  # Czekanie na zamknięcie okna dialogowego
        if dialog.result:
            # Dodanie imprezy do listy, jeśli została poprawnie wprowadzona
            self.events.append(dialog.result)
            self.events_listbox.insert(tk.END, f"Data: {dialog.result[0]}, Turniej: {dialog.result[1]}, Godzina: {dialog.result[2]}")

    # Metoda do generowania grafik na podstawie dodanych imprez
    def generate_graphics(self):
        if not self.events:  # Sprawdzenie, czy lista imprez nie jest pusta
            messagebox.showwarning("Błąd", "Dodaj przynajmniej jedną imprezę.")  # Komunikat o błędzie
            return

        # Przetwarzanie każdej imprezy z listy
        for event in self.events:
            date_str, tournament, time_str = event
            try:
                ptf_number = int(tournament)  # Próba konwersji numeru turnieju na liczbę
            except ValueError:
                messagebox.showwarning("Błąd", f"Numer turnieju '{tournament}' nie jest liczbą.")  # Komunikat o błędzie
                continue

            # Wybór odpowiedniego skryptu w zależności od numeru turnieju
            if ptf_number % 10 == 0:
                script_to_run = 'red.py'  # Jeśli numer turnieju jest podzielny przez 10, użyj skryptu 'red.py'
            else:
                script_to_run = 'yellow.py'  # W przeciwnym razie użyj skryptu 'yellow.py'

            # Uruchomienie skryptu do generowania grafik
            result = subprocess.run(['python', script_to_run, tournament, date_str, time_str],
                                    capture_output=True, text=True)
            print(result.stdout)  # Wyświetlenie wyników działania skryptu
            print(result.stderr)  # Wyświetlenie błędów, jeśli wystąpiły

            # Zawsze uruchamiamy 'to_printer.py' do generowania dodatkowej grafiki
            result2 = subprocess.run(['python', 'to_printer.py', tournament, date_str, time_str],
                                     capture_output=True, text=True)
            print(result2.stdout)  # Wyświetlenie wyników
            print(result2.stderr)  # Wyświetlenie błędów

        # Komunikat o zakończeniu procesu generowania grafik
        messagebox.showinfo("Sukces", "Proces generowania grafik zakończony.")

# Uruchomienie aplikacji, jeśli skrypt jest uruchamiany jako główny
if __name__ == "__main__":
    app = PTFGenerator()  # Utworzenie instancji aplikacji
    app.mainloop()  # Uruchomienie głównej pętli aplikacji
