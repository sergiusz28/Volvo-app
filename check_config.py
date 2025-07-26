#!/usr/bin/env python3
"""
Sprawdzenie konfiguracji Volvo API
"""

from volvo_app.config import config
import requests


def check_volvo_config():
    """Sprawdź konfigurację Volvo API."""
    
    print("🔍 SPRAWDZENIE KONFIGURACJI VOLVO:")
    print("="*50)
    
    # Sprawdź podstawowe dane
    print(f"Client ID: {config.VOLVO_CLIENT_ID}")
    print(f"Client Secret: {config.VOLVO_CLIENT_SECRET[:10]}...")
    print(f"API Key: {config.VOLVO_API_KEY}")
    print(f"VIN: {config.VOLVO_VIN}")
    print(f"Redirect URI: {config.VOLVO_REDIRECT_URI}")
    print()
    
    # Sprawdź dostępność serwera Volvo
    print("🌐 SPRAWDZENIE DOSTĘPNOŚCI SERWERA:")
    print("="*50)
    
    try:
        # Test podstawowej dostępności
        response = requests.get("https://volvoid.eu.volvocars.com", timeout=10)
        print(f"Volvo ID serwer: ✅ dostępny (status: {response.status_code})")
    except Exception as e:
        print(f"Volvo ID serwer: ❌ niedostępny ({e})")
    
    try:
        # Test API endpoint
        response = requests.get(f"{config.VOLVO_API_BASE_URL}/connected-vehicle/v2/vehicles", timeout=10)
        print(f"Volvo API serwer: ✅ dostępny (status: {response.status_code})")
    except Exception as e:
        print(f"Volvo API serwer: ❌ niedostępny ({e})")
    
    print()
    print("💡 ZALECENIA:")
    print("="*50)
    print("1. Sprawdź status aplikacji w Volvo Developer Portal")
    print("2. Upewnij się, że aplikacja jest zatwierdzona")
    print("3. Sprawdź czy redirect URI jest dokładnie: http://localhost:8000/callback")
    print("4. Spróbuj ponownie za kilka minut (może być tymczasowy problem)")
    print("5. Sprawdź czy nie ma limitu żądań (rate limiting)")


def test_simple_auth_url():
    """Test generowania URL autoryzacji bez serwera."""
    
    print("\n🔗 TEST URL AUTORYZACJI:")
    print("="*50)
    
    # Minimalna konfiguracja OAuth2
    client_id = config.VOLVO_CLIENT_ID
    redirect_uri = config.VOLVO_REDIRECT_URI
    scopes = "openid"
    
    # Ręczne stworzenie URL (bez biblioteki)
    auth_url = (
        f"https://volvoid.eu.volvocars.com/as/authorization.oauth2"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
    )
    
    print(f"Podstawowy URL autoryzacji:")
    print(auth_url)
    print()
    print("Spróbuj otworzyć ten URL ręcznie w przeglądarce.")
    print("Jeśli też daje błąd 500, problem jest w konfiguracji aplikacji.")


if __name__ == "__main__":
    check_volvo_config()
    test_simple_auth_url()
