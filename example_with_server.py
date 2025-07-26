#!/usr/bin/env python3
"""
Przykład z lokalnym serwerem do obsługi OAuth callback
"""

import asyncio
import logging
import aiohttp
from aiohttp import web
import webbrowser
from volvocarsapi.auth import VolvoCarsAuth
from volvocarsapi.scopes import DEFAULT_SCOPES
from volvo_app.config import config


# Zmienna globalna do przechowania kodu autoryzacji
auth_code = None


async def handle_callback(request):
    """Obsługa callback'a OAuth z kodem autoryzacji."""
    global auth_code
    
    # Pobierz kod z parametrów URL
    code = request.query.get('code')
    error = request.query.get('error')
    
    if error:
        return web.Response(
            text=f"❌ Błąd autoryzacji: {error}",
            content_type='text/html'
        )
    
    if code:
        auth_code = code
        return web.Response(
            text="""
            <!DOCTYPE html>
            <html><body>
            <h2>✅ Autoryzacja pomyślna!</h2>
            <p>Kod autoryzacji otrzymany. Możesz zamknąć to okno.</p>
            <p>Wróć do terminala aby kontynuować.</p>
            </body></html>
            """,
            content_type='text/html'
        )
    
    return web.Response(
        text="❌ Brak kodu autoryzacji",
        content_type='text/html'
    )


async def start_callback_server():
    """Uruchom lokalny serwer do obsługi callback'a."""
    app = web.Application()
    app.router.add_get('/callback', handle_callback)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    
    print("🌐 Serwer callback uruchomiony na http://localhost:8000")
    return runner


async def oauth_flow_with_server():
    """Przepływ OAuth z lokalnym serwerem."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Sprawdź konfigurację
    required_fields = {
        'CLIENT_ID': config.VOLVO_CLIENT_ID,
        'CLIENT_SECRET': config.VOLVO_CLIENT_SECRET,
    }
    
    missing_fields = [name for name, value in required_fields.items() if not value]
    
    if missing_fields:
        logger.error(f"Brak wymaganych pól konfiguracji: {', '.join(missing_fields)}")
        return
    
    global auth_code
    auth_code = None
    
    try:
        # Uruchom serwer callback
        callback_server = await start_callback_server()
        
        async with aiohttp.ClientSession() as session:
            logger.info("🔐 Inicjalizacja autoryzacji Volvo...")
            
            # Użyj tylko podstawowe zakresy
            basic_scopes = ["openid", "conve:vehicle_relation"]
            
            auth = VolvoCarsAuth(
                websession=session,
                client_id=config.VOLVO_CLIENT_ID,
                client_secret=config.VOLVO_CLIENT_SECRET,
                scopes=basic_scopes,
                redirect_uri=config.VOLVO_REDIRECT_URI
            )
            
            # Pobierz URL autoryzacji
            auth_url = auth.get_auth_uri()
            logger.info(f"URL autoryzacji: {auth_url}")
            
            print("\n🔐 PROCES AUTORYZACJI:")
            print("="*50)
            print("1. Za chwilę otworzy się przeglądarka")
            print("2. Zaloguj się do Volvo ID")
            print("3. Zaakceptuj uprawnienia")
            print("4. Poczekaj na przekierowanie...")
            print()
            
            # Otwórz przeglądarkę automatycznie
            webbrowser.open(auth_url)
            
            # Czekaj na kod autoryzacji
            print("⏳ Czekam na autoryzację...")
            for i in range(120):  # 2 minuty timeout
                if auth_code:
                    break
                await asyncio.sleep(1)
                if i % 10 == 0:
                    print(f"⏳ Czekam... ({120-i}s pozostało)")
            
            if not auth_code:
                logger.error("❌ Timeout - nie otrzymano kodu autoryzacji")
                return
            
            print(f"✅ Otrzymano kod autoryzacji: {auth_code[:10]}...")
            
            # Wymień kod na token
            logger.info("🔄 Wymiana kodu na token dostępowy...")
            await auth.async_request_token(auth_code)
            logger.info("✅ Token dostępowy otrzymany!")
            
            print("\n🎉 AUTORYZACJA ZAKOŃCZONA POMYŚLNIE!")
            print("Teraz możesz używać API do komunikacji z pojazdem.")
            
            # Zapisz token do dalszego użytku (opcjonalnie)
            token_info = {
                'access_token': auth.access_token,
                'refresh_token': auth.refresh_token,
                'expires_at': auth.token_expires_at.isoformat() if auth.token_expires_at else None
            }
            print(f"Token info: {token_info}")
            
    except Exception as e:
        logger.error(f"Błąd podczas autoryzacji: {e}")
        logger.exception("Szczegóły błędu:")
    
    finally:
        # Wyłącz serwer
        if 'callback_server' in locals():
            await callback_server.cleanup()
            print("🔴 Serwer callback zatrzymany")


def show_setup_info():
    """Pokaż informacje o konfiguracji."""
    print("📋 KONFIGURACJA REDIRECT URI:")
    print("="*50)
    print("W Volvo Developer Portal upewnij się, że:")
    print("Redirect URI = http://localhost:8000/callback")
    print()
    print("🔧 URUCHAMIANIE:")
    print("1. Ta aplikacja uruchomi lokalny serwer na porcie 8000")
    print("2. Automatycznie otworzy przeglądarkę")
    print("3. Po autoryzacji zostaniesz przekierowany z powrotem")
    print("4. Kod zostanie automatycznie przechwycony")
    print()


if __name__ == "__main__":
    show_setup_info()
    print("Uruchamianie autoryzacji z serwerem callback...")
    asyncio.run(oauth_flow_with_server())