# Antes de iniciar el proyecto, asegurate de utilizar el comando
# pip install openpyxl

# Ahora, asegurate de crear un archivo exel llamado "data.xlsx" en la misma ubicación que este archivo
# y de rellenar las columnas "BLOQUE DE PREMISAS" y "CONCLUSIONES"
# Siempre debe tener como mínimo dos premisas y una conclusión
# Para que se puedan formar pares de premisas, asegurate de que las premisas no esten vacías
# De lo contrario, no se formaran pares de premisas.

# Ejemplos de premisas y conclusiones:
# BLOQUE DE PREMISAS	CONCLUSIONES
# -----------------     ------------
# -----------------

# Inicio del proyecto chatbot.py

import pandas as pd
import difflib
from flask import Flask, request, render_template_string

# Especifica la ruta de tu archivo Excel
file_path = r"C:\Users\House\Desktop\data.xlsx"  # Reemplaza con la ruta correcta de tu archivo Excel

# Cargar el archivo Excel
data = pd.read_excel(file_path)

# Eliminar posibles espacios en blanco en los nombres de las columnas
data.columns = data.columns.str.strip()

# Crear pares de premisas a partir de las filas del archivo Excel
bloque_premisas = []
conclusiones = []

# Verificar que hay un número par de filas en el bloque de premisas
if len(data['BLOQUE DE PREMISAS']) % 2 != 0:
    raise ValueError("El número de filas en 'BLOQUE DE PREMISAS' debe ser par.")

# Recorremos el DataFrame de dos en dos para formar los pares de premisas
for i in range(0, len(data['BLOQUE DE PREMISAS']), 2):
    premisa1 = data['BLOQUE DE PREMISAS'].iloc[i].strip()
    premisa2 = data['BLOQUE DE PREMISAS'].iloc[i + 1].strip()
    if premisa1 and premisa2:  # Asegurarse de que las premisas no están vacías
        # Normalizar el orden de las premisas para que siempre se almacenen en el mismo orden
        premisas_ordenadas = tuple(sorted([premisa1, premisa2]))
        bloque_premisas.append(premisas_ordenadas)
        conclusiones.append(data['CONCLUSIONES'].iloc[i // 2])  # Cada par de filas de premisas corresponde a una conclusión

# Convertir las premisas y conclusiones en un diccionario
faq = dict(zip(bloque_premisas, conclusiones))

app = Flask(__name__)

# Ruta raíz
@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = ""
    premisa1 = ""
    premisa2 = ""
    error = ""  # Variable para almacenar un mensaje de error si las premisas están vacías o repetidas
    
    if request.method == 'POST':
        # Obtener las premisas desde el formulario
        premisa1 = request.form.get('premisa1').strip()
        premisa2 = request.form.get('premisa2').strip()

        # Verificar si ambos campos están llenos y son distintos
        if not premisa1 or not premisa2:
            error = "Ambas premisas deben ser llenadas."
        elif premisa1 == premisa2:
            error = "Las premisas no deben ser iguales."
        else:
            # Normalizar el orden de las premisas para buscar en el diccionario
            entrada_premisas = tuple(sorted([premisa1, premisa2]))

            # Verificar si el par de premisas ingresado existe en el diccionario de FAQs
            if entrada_premisas in faq:
                respuesta = faq.get(entrada_premisas, "Lo siento, no tengo una conclusión para esas premisas.")
            else:
                respuesta = "Lo siento, no tengo una conclusión para esas premisas."

    # HTML con CSS para estilos
    html = '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chatbot de Premisas</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                    text-align: center;
                }
                h1 {
                    color: #333;
                }
                textarea {
                    width: 100%;
                    min-height: 40px;
                    padding: 8px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                    resize: vertical; /* Permite que el usuario ajuste la altura manualmente */
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                h2 {
                    color: #333;
                }
                p {
                    color: #666;
                }
                .error {
                    color: red;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Chatbot de Premisas</h1>
                <form method="POST">
                    <label for="premisa1">Premisa 1:</label><br>
                    <textarea id="premisa1" name="premisa1" placeholder="Introduce la primera premisa">{{ premisa1 }}</textarea><br>
                    <label for="premisa2">Premisa 2:</label><br>
                    <textarea id="premisa2" name="premisa2" placeholder="Introduce la segunda premisa">{{ premisa2 }}</textarea><br><br>
                    <input type="submit" value="Buscar conclusión">
                </form> 
                {% if error %}
                    <p class="error">{{ error }}</p>
                {% elif respuesta %}
                    <h2>Conclusión:</h2>
                    <p>{{ respuesta }}</p>
                {% endif %}
            </div>
        </body>
        </html>
    '''

    # Renderizar la plantilla con la respuesta
    return render_template_string(html, premisa1=premisa1, premisa2=premisa2, respuesta=respuesta, error=error)

# Puerto local donde estará el servidor
if __name__ == '__main__':
    app.run(port=5000)
    
# Si te pude ayudar, te agradecería que me ayudes a mejorar el chatbot. :-)