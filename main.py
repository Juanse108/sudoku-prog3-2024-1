import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from azure.communication.email import EmailClient

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

with open("ejemploTablero.json") as sudoku:
    tablero = json.load(sudoku)


def validar_fila_columna(sudoku, numero, fila, columna):
    fila = (fila - 1) // 3
    columna1 = (columna - 1) // 3
    columna2 = (columna - 1) % 3
    columna3 = (fila - 1) % 3

    if sudoku[fila]["columnas"][columna1][columna2][columna3] == numero:
        return False

    for i in range(3):
        for j in range(3):
            if sudoku[i]["columnas"][columna1][columna2][j] == numero:
                return False

    for k in range(3):
        for l in range(3):
            if sudoku[fila]["columnas"][columna1][l][columna3] == numero:
                return False

    return True


def generate_sudoku_table(sudoku):
    html = '<html><body><table border="1">'
    for row in sudoku:
        html += '<tr>'
        for cell in row:
            html += '<td>{}</td>'.format(cell)
        html += '</tr>'
    html += '</table></body></html>'
    return html


@app.route('/validar', methods=['POST'])
def validar_numero():
    data = request.json
    numero = data['numero']
    fila = data['fila']
    columna = data['columna']
    email = data['email']

    if validar_fila_columna(tablero, numero, fila, columna):
        # Si el número es válido, enviar el correo electrónico con el tablero
        send_email(email, generate_sudoku_table(tablero))
        return jsonify({'message': 'Dato ubicado correctamente. Correo electrónico enviado'}), 200
    else:
        return jsonify({'message': 'El dato no puede ser ubicado, cambie de posición'}), 400


# Función para enviar el correo electrónico con el tablero en formato HTML
def send_email(email, sudoku_table):
    try:
        # Actualiza la cadena de conexión con el formato correcto
        connection_string = ("endpoint=https://sudokuprog3.unitedstates.communication.azure.com/;accesskey="
                             "qSZIprLi6BZBqPUG7z4rScmnfw6LD5/YVH2X0bvErG8yTopiU8dTrcVANznloyACE1X2L0eN+6/LmCavGf+VCg==")
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@ecac96ec-69a5-4a6d-90a0-0ed270d0b012.azurecomm.net",
            "recipients": {
                "to": [{"address": email}],
            },
            "content": {
                "subject": "Tablero de Sudoku",
                "html": f"<h1>Tablero de Sudoku</h1>{sudoku_table}"
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        print(ex)

    return


if __name__ == '__main__':
    # Utiliza Waitress como servidor en lugar del servidor de desarrollo de Flask para producción
    from waitress import serve

    print("Server running ")
    serve(app, host='0.0.0.0', port=5000)
