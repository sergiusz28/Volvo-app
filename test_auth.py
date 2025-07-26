#!/usr/bin/env python3
"""
Uproszczony test autoryzacji Volvo API
=====================================
"""

import asyncio
import logging
import aiohttp
from volvocarsapi.auth import VolvoCarsAuth
from volvo_app.config import config


async def test_authorization():
    """Test procesu autoryzacji."""
    
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    print("🔍 SPRAWDZENIE KONFIGURACJI:")
    print(f"Client ID: {config.VOLVO_CLIENT_ID}")
    print(f"Client Secret: {config.VOLVO_CLIENT_SECRET[:5]}...")
    print(f"Redirect URI: {config.VOLVO_REDIRECT_URI}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            # Użyj tylko podstawowych zakresów
            simple_scopes = ["openid", "conve:vehicle_relation"]
            
            auth = VolvoCarsAuth(
                websession=session,
                client_id=config.VOLVO_CLIENT_ID,
                client_secret=config.VOLVO_CLIENT_SECRET,
                scopes=simple_scopes,
                redirect_uri=config.VOLVO_REDIRECT_URI
            )
            
            # Pobierz URL autoryzacji
            auth_url = auth.get_auth_uri()
            print(f"🔗 URL autoryzacji:")
            print(auth_url)
            print()
            print("📋 INSTRUKCJE:")
            print("1. Skopiuj powyższy URL i otwórz w przeglądarce")
            print("2. Zaloguj się do Volvo ID")
            print("3. Zaakceptuj uprawnienia")
            print("4. Po przekierowaniu, skopiuj wartość parametru 'code' z URL")
            print("   Przykład: http://localhost:8000/callback?code=TWÓJ_KOD")
            print()
            
            # Pobierz kod od użytkownika
            auth_code = input("Wklej kod autoryzacji: ").strip()
            
            if not auth_code:
                print("❌ Nie podano kodu")
                return
            
            print(f"🔄 Próba wymiany kodu na token...")
            print(f"Kod: {auth_code}")
            
            try:
                # Wymień kod na token
                await auth.async_request_token(auth_code)
                print("✅ Autoryzacja zakończona sukcesem!")
                
                # Sprawdź czy token został otrzymany
                if hasattr(auth, 'access_token') and auth.access_token:
                    print(f"Token otrzymany: {auth.access_token[:20]}...")
                else:
                    print("⚠️ Token nie został ustawiony")
                    
            except Exception as token_error:
                print(f"❌ Błąd podczas wymiany tokenu:")
                print(f"   {token_error}")
                print()
                print("🔧 MOŻLIWE PRZYCZYNY:")
                print("1. Kod autoryzacji został już użyty")
                print("2. Kod wygasł (spróbuj ponownie z nowym kodem)")
                print("3. Nieprawidłowy redirect URI w aplikacji Volvo")
                print("4. Nieprawidłowe Client ID/Secret")
                print()
                print("💡 ROZWIĄZANIA:")
                print("- Sprawdź redirect URI w Volvo Developer Portal")
                print("- Wygeneruj nowy kod autoryzacji")
                print("- Sprawdź dane aplikacji w portalu deweloperskim")
                
    except Exception as e:
        print(f"❌ Ogólny błąd: {e}")


if __name__ == "__main__":
    asyncio.run(test_authorization())
