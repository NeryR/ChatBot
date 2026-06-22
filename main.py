import re

def chatbot():
    print("*** ChatBot v1.0.0 Iniciando ***")
    print("Hola soy el chatbot v1.0.0, Puedo ayudarte a obtener información sobre precios de acciones y clima de ciudades")
    print("¿Qué quieres saber hoy?")

    # Ciclo infinito para mantener el ChatBot corriendo
    while True:
        try: 
            user_input = input("-->").strip()
            if not user_input:
                continue

            # Validar una petición de salida
            if user_input.lower() in ["salir", "adiós", "adios", "chao", "bye", "exit"]:
                print("ChatBot: Hasta luego!!")
                break
            # Reglas para detectar intención de preguntas por acciones

            stock_match = re.search(r"(?:precio|stock|accion|acción)\s+(?:de|en|de la)\s+(?:de\s, de la|de las)\s+(\w+)", user_input, re.IGNORECASE)

            #Reglas para detectar intención de preguntas por clima
            weather_match = re.search(r"(?:clima|tiempo|temperatura)\s+(?:en|de)\s+(\w+)", user_input, re.IGNORECASE)

            # Caso 1: El usuario pregunta por acciones
            if stock_match:
                # Debemos esperar si el usuario indica alguna acción
                price = obtener_precio_accion(None, user_input)
                if price:
                    print(f">> {price}")
                else:
                    print("ChatBot: No pude obtener el precio, ¿podrías intentar con otra acción?")

            # Caso 2: El usuario pregunta por el clima
            if weather_match:
                temp = obtener_temperatura(None, user_input)
                if temp:
                    print(f">> {temp}")
                else:
                    print("ChatBot: No pude obtener la temperatura, ¿podrías intentar con otra ciudad?")
            
            # Caso 3: El usuario no ejecuta alguna petición
            else: 
                print("Chatbot: No entendí tu petición, ¿podrías replantearla?")

        except KeyboardInterrupt:
            # Comando de salida
            print("ChatBot: Hasta luego!!")