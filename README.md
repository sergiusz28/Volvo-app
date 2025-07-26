# Volvo Car Integration App

## Opis

Aplikacja do integracji z samochodami Volvo przez ich oficjalne API. 
**Tylko do użytku prywatnego - używaj na własne ryzyko.**

## Funkcje

- Uwierzytelnianie z Volvo Cars API
- Pobieranie listy pojazdów
- Sprawdzanie statusu pojazdu
- Zdalne sterowanie:
  - Zamykanie/otwieranie zamków
  - Uruchamianie/zatrzymywanie silnika
  - Pobieranie informacji o lokalizacji

## Wymagania

- Python 3.9+
- Konto dewelopera Volvo Cars
- Klucze API od Volvo

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone <repo-url>
cd Volvo-app
```

2. Utwórz środowisko wirtualne:
```bash
python -m venv .venv
source .venv/bin/activate  # Na macOS/Linux
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skonfiguruj zmienne środowiskowe:
```bash
cp .env.example .env
# Edytuj .env i wpisz swoje dane API
```

## Użycie

```bash
python main.py
```

## Konfiguracja API

1. Zarejestruj się na [Volvo Developer Portal](https://developer.volvocars.com/)
2. Utwórz nową aplikację
3. Skopiuj Client ID i Client Secret do pliku `.env`
4. Skonfiguruj Redirect URI

## Struktura projektu

```
volvo_app/
├── volvo_app/           # Główny pakiet aplikacji
│   ├── __init__.py      # Inicjalizacja pakietu
│   ├── config.py        # Konfiguracja aplikacji
│   └── api_client.py    # Klient API Volvo
├── tests/               # Testy jednostkowe
├── config/              # Pliki konfiguracyjne
├── main.py              # Punkt wejścia aplikacji
├── requirements.txt     # Zależności Python
├── .env.example         # Przykład konfiguracji
└── README.md            # Ta dokumentacja
```

## Bezpieczeństwo

- Nigdy nie commituj pliku `.env` z prawdziwymi danymi
- Używaj silnych kluczy API
- Regularnie odnawiaj tokeny dostępu

## Kontakt

Email: sergiusz28@gmail.com

## Licencja

Wyłącznie do użytku prywatnego. Autor nie ponosi odpowiedzialności za szkody lub utratę danych.
