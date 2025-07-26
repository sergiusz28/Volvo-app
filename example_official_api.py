#!/usr/bin/env python3
"""
Przykład użycia oficjalnej biblioteki volvocarsapi
==================================================

Ten plik pokazuje jak używać oficjalnej biblioteki volvocarsapi
do komunikacji z samochodami Volvo.
"""

import asyncio
import logging
import os
import aiohttp
from volvocarsapi.api import VolvoCarsApi, AccessTokenManager
from volvocarsapi.auth import VolvoCarsAuth
from volvocarsapi.scopes import ALL_SCOPES, DEFAULT_SCOPES
from volvo_app.config import config


async def main_with_official_api():
    """Główna funkcja używająca oficjalnej biblioteki volvocarsapi."""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Sprawdzenie czy są skonfigurowane klucze API
    if not config.VOLVO_CLIENT_ID or not config.VOLVO_CLIENT_SECRET:
        logger.error("Brak konfiguracji VOLVO_CLIENT_ID lub VOLVO_CLIENT_SECRET w pliku .env")
        logger.info("Skopiuj .env.example do .env i wypełnij danymi z Volvo Developer Portal")
        return
    
    try:
        # Sprawdzenie dostępnych zakresów uprawnień
        print("Dostępne zakresy uprawnień (scopes):")
        for scope in ALL_SCOPES:
            print(f"  • {scope}")
        print()
        print("Domyślne zakresy uprawnień:")
        for scope in DEFAULT_SCOPES:
            print(f"  • {scope}")
        print()
        
        # Utworzenie sesji HTTP
        async with aiohttp.ClientSession() as session:
            logger.info("Inicjalizacja Volvo Auth...")
            
            # Inicjalizacja uwierzytelniania
            auth = VolvoCarsAuth(
                websession=session,
                client_id=config.VOLVO_CLIENT_ID,
                client_secret=config.VOLVO_CLIENT_SECRET,
                scopes=list(ALL_SCOPES),  # Wszystkie dostępne uprawnienia
                redirect_uri=config.VOLVO_REDIRECT_URI or "http://localhost:8080/callback"
            )
            
            # Generowanie URL autoryzacji
            auth_url = auth.get_authorization_url()
            logger.info(f"URL autoryzacji: {auth_url}")
            
            print("🔐 Proces autoryzacji:")
            print(f"1. Otwórz w przeglądarce: {auth_url}")
            print("2. Zaloguj się do Volvo ID")
            print("3. Skopiuj kod autoryzacji z URL przekierowania")
            
            # W prawdziwej aplikacji tutaj byłby kod do obsługi OAuth2 callback
            # authorization_code = input("Wprowadź kod autoryzacji: ")
            # token_response = await auth.get_access_token(authorization_code)
            
            logger.info("Implementacja OAuth2 wymaga dalszej konfiguracji")
            logger.info("Zobacz dokumentację: https://github.com/thomasddn/volvo-cars-api")
            
            # Po uzyskaniu tokenu:
            # token_manager = AccessTokenManager(token_response)
            # api = VolvoCarsApi(session, token_manager, api_key="your_api_key", vin="")
            # vehicles = await api.get_vehicles()
        
    except Exception as e:
        logger.error(f"Błąd podczas pracy z Volvo API: {e}")
        

def show_api_info():
    """Wyświetl informacje o dostępnych funkcjach API."""
    print("🚗 Volvo Cars API - Dostępne funkcje:")
    print("="*50)
    print("📋 Podstawowe operacje:")
    print("  • Pobieranie listy pojazdów")
    print("  • Sprawdzanie statusu pojazdu")
    print("  • Informacje o paliwie/baterii")
    print("  • Lokalizacja pojazdu")
    print("")
    print("🔐 Sterowanie zdalene:")
    print("  • Zamykanie/otwieranie zamków")
    print("  • Uruchamianie/zatrzymywanie silnika")
    print("  • Klimatyzacja")
    print("  • Sygnalizacja dźwiękowa i świetlna")
    print("")
    print("⚙️ Konfiguracja:")
    print("  1. Utwórz konto na https://developer.volvocars.com/")
    print("  2. Zarejestruj aplikację i otrzymaj Client ID/Secret")
    print("  3. Skopiuj .env.example do .env")
    print("  4. Wypełnij dane w pliku .env")
    print("")


if __name__ == "__main__":
    show_api_info()
    print("Uruchamianie przykładu...")
    asyncio.run(main_with_official_api())
