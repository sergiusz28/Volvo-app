#!/usr/bin/env python3
"""
Kompletny przykład pracy z Volvo Cars API
========================================

Ten plik pokazuje pełny przepływ OAuth2 i wykonywanie operacji na pojeździe.
"""

import asyncio
import logging
import aiohttp
from volvocarsapi.api import VolvoCarsApi
from volvocarsapi.auth import VolvoCarsAuth
from volvocarsapi.scopes import ALL_SCOPES
from volvo_app.config import config


async def complete_volvo_api_flow():
    """Kompletny przepływ pracy z Volvo Cars API."""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Sprawdzenie konfiguracji
    required_fields = {
        'CLIENT_ID': config.VOLVO_CLIENT_ID,
        'CLIENT_SECRET': config.VOLVO_CLIENT_SECRET, 
        'API_KEY': config.VOLVO_API_KEY,
        'VIN': config.VOLVO_VIN
    }
    
    missing_fields = [name for name, value in required_fields.items() if not value]
    
    if missing_fields:
        logger.error(f"Brak wymaganych pól konfiguracji: {', '.join(missing_fields)}")
        logger.info("Wypełnij plik .env zgodnie z .env.example")
        return
    
    try:
        # Utworzenie sesji HTTP
        async with aiohttp.ClientSession() as session:
            logger.info("🔐 Inicjalizacja autoryzacji Volvo...")
            
            # Inicjalizacja klienta autoryzacyjnego
            # Używamy tylko podstawowych zakresów bez sterowania pojazdem
            basic_scopes = [
                "openid",
                "conve:fuel_status",
                "conve:battery_charge_level", 
                "conve:engine_status",
                "conve:lock_status",
                "conve:vehicle_relation",
                "location:read"
            ]
            
            auth = VolvoCarsAuth(
                websession=session,
                client_id=config.VOLVO_CLIENT_ID,
                client_secret=config.VOLVO_CLIENT_SECRET,
                scopes=basic_scopes,
                redirect_uri=config.VOLVO_REDIRECT_URI
            )
            
            # Krok 1: Pobierz URL autoryzacji
            auth_url = auth.get_auth_uri()
            logger.info(f"URL autoryzacji: {auth_url}")
            
            print("🔐 PROCES AUTORYZACJI:")
            print("="*50)
            print(f"1. Otwórz w przeglądarce: {auth_url}")
            print("2. Zaloguj się do Volvo ID")
            print("3. Zaakceptuj uprawnienia")
            print("4. Skopiuj kod autoryzacji z URL przekierowania")
            print("   (parametr 'code' z URL: http://localhost:8000/callback?code=...)")
            print()
            
            # Krok 2: Pobierz kod autoryzacji od użytkownika
            auth_code = input("Wprowadź kod autoryzacji: ").strip()
            
            if not auth_code:
                logger.error("Nie podano kodu autoryzacji")
                return
            
            # Krok 3: Wymień kod na token dostępowy
            logger.info("🔄 Wymiana kodu na token dostępowy...")
            await auth.async_request_token(auth_code)
            logger.info("✅ Token dostępowy otrzymany!")
            
            # Krok 4: Stwórz klienta API
            logger.info("🚗 Inicjalizacja klienta Volvo Cars API...")
            api = VolvoCarsApi(
                websession=session,
                auth=auth,
                api_key=config.VOLVO_API_KEY,
                vin=config.VOLVO_VIN
            )
            
            # Krok 5: Wykonaj przykładowe operacje
            await perform_vehicle_operations(api, logger)
            
    except Exception as e:
        logger.error(f"Błąd podczas pracy z Volvo API: {e}")
        logger.exception("Szczegóły błędu:")


async def perform_vehicle_operations(api: VolvoCarsApi, logger):
    """Wykonaj przykładowe operacje na pojeździe."""
    
    print("\n🚗 OPERACJE NA POJEŹDZIE:")
    print("="*50)
    
    try:
        # Pobierz ostrzeżenia silnika
        logger.info("📊 Sprawdzanie ostrzeżeń silnika...")
        engine_warnings = await api.async_get_engine_warnings()
        print(f"Ostrzeżenia silnika: {engine_warnings}")
        
        # Pobierz status paliwa
        logger.info("⛽ Sprawdzanie poziomu paliwa...")
        fuel_status = await api.async_get_fuel_status()
        print(f"Status paliwa: {fuel_status}")
        
        # Pobierz status baterii (dla hybryd/elektrycznych)
        logger.info("🔋 Sprawdzanie statusu baterii...")
        try:
            battery_status = await api.async_get_battery_status()
            print(f"Status baterii: {battery_status}")
        except Exception as e:
            print(f"Status baterii niedostępny (prawdopodobnie pojazd spalinowy): {e}")
        
        # Pobierz lokalizację pojazdu
        logger.info("📍 Sprawdzanie lokalizacji pojazdu...")
        location = await api.async_get_location()
        print(f"Lokalizacja: {location}")
        
        # Pobierz status zamków
        logger.info("🔒 Sprawdzanie statusu zamków...")
        lock_status = await api.async_get_lock_status()
        print(f"Status zamków: {lock_status}")
        
        # Przykład sterowania - UWAGA: te operacje wpływają na prawdziwy pojazd!
        print("\n⚠️  OPERACJE STEROWANIA (odkomentuj jeśli chcesz użyć):")
        print("# await api.async_lock()     # Zamknij pojazd")
        print("# await api.async_unlock()   # Otwórz pojazd") 
        print("# await api.async_honk()     # Zasygalizuj")
        print("# await api.async_flash()    # Migaj światłami")
        
    except Exception as e:
        logger.error(f"Błąd podczas wykonywania operacji: {e}")


def show_required_setup():
    """Pokaż wymagane kroki konfiguracji."""
    print("📋 WYMAGANA KONFIGURACJA:")
    print("="*50)
    print("1. Zarejestruj się na: https://developer.volvocars.com/")
    print("2. Utwórz aplikację i otrzymaj:")
    print("   - Client ID (już masz)")
    print("   - Client Secret (już masz)")
    print("   - API Key (potrzebne)")
    print("3. Znajdź VIN swojego pojazdu (17-znakowy kod)")
    print("4. Wypełnij plik .env:")
    print("   VOLVO_API_KEY=twój_api_key")
    print("   VOLVO_VIN=twój_vin_pojazdu")
    print()


if __name__ == "__main__":
    show_required_setup()
    print("Uruchamianie aplikacji...")
    asyncio.run(complete_volvo_api_flow())