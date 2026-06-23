import yfinance as yf
from utils.sanitizar import sanitizar

# Diccionario con las empresasa y sus acciones
COMPANY_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "meta": "META",
}

def obtener_precio_accion(user_input):
    ticker = COMPANY_TICKERS.get(company_name)

    company_name = sanitizar(user_input)

    # Buscar si el nombre que el usuario está buscando está en nuestro mapa o diccionario

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