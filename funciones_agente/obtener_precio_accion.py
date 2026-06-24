import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import yfinance as yf
from utils.sanitizar import sanitizar

# Diccionario con las empresasa y sus acciones
COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "apple inc": "AAPL",
    "microsoft corp": "MSFT",
}

def obtener_precio_accion(driver, user_input):
    company_name = sanitizar(user_input)

    ticker = COMPANY_TICKERS.get(company_name)

    # Buscar coincidencias parciales en nuestro diccionario de empresas
    if not ticker and company_name:
        for key, value in COMPANY_TICKERS.items():
            if key in company_name:
                ticker = value
                break

    if not ticker:
        ticker = company_name.upper()

    try:
        # Inicializar el objeto Ticker de yfinance
        stock = yf.Ticker(ticker)

        # Obtener la información actualizada de dicha acción
        data = stock.history(period="1d")

        if not data.empty:
            price = data['Close'].iloc[-1]
            return f"${price:.2f}"
        else:
            return "ChatBot: No pude encontrar los datos que me solicitaste"
        
    except Exception as e:
        return f"ChatBot: Error al consultar la información: {e}"