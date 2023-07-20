from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route('/rubrica', methods=['GET'])
def get_rubrica():
    cnx = mysql.connector.connect(user='arca', password='arca', host='localhost', database='rubrica')

    cursor = cnx.cursor()

    query = "SELECT * FROM rubrica"
    cursor.execute(query)

    rubrica = []
    for (nome, cognome, sesso, data_di_nascita, numero_di_telefono, email, citta, id) in cursor:
        rubrica.append({
            "nome": nome,
            "cognome": cognome,
            "sesso": sesso,
            "data_di_nascita": str(data_di_nascita),
            "numero_di_telefono": numero_di_telefono,
            "email": email,
            "citta": citta,
            "id": id
        })

    cursor.close()
    cnx.close()

    return jsonify(rubrica)

@app.route('/citta', methods=['GET'])
def get_citta():
    connection = mysql.connector.connect(user='arca', password='arca', host='localhost', database='rubrica')

    cursor = connection.cursor()

    query = "SELECT nome FROM citta"
    cursor.execute(query)

    citta = [row[0] for row in cursor]

    cursor.close()
    connection.close()

    return jsonify(citta)

@app.route('/rubrica', methods=['POST'])
def add_contatto():
    nome = request.json.get('nome')
    cognome = request.json.get('cognome')
    sesso = request.json.get('sesso')
    data_di_nascita = request.json.get('data_di_nascita')
    numero_di_telefono = request.json.get('numero_di_telefono')
    email = request.json.get('email')
    citta = request.json.get('citta')

    cnx = mysql.connector.connect(user='arca', password='arca', host='localhost', database='rubrica')

    cursor = cnx.cursor()

    query = ("INSERT INTO rubrica (nome, cognome, sesso, data_di_nascita, numero_di_telefono, email, citta) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (nome, cognome, sesso, data_di_nascita, numero_di_telefono, email, citta))

    cnx.commit()
    cursor.close()
    cnx.close()

    return jsonify(success=True)

@app.route('/rubrica', methods=['DELETE'])
def delete_contatto():
    id = request.json.get('id')

    cnx = mysql.connector.connect(user='arca', password='arca', host='localhost', database='rubrica')

    cursor = cnx.cursor()

    query = ("DELETE FROM rubrica WHERE id = %s")
    cursor.execute(query, (id,))

    if cursor.rowcount == 0:
        cursor.close()
        cnx.close()
        abort(404)

    cnx.commit()
    cursor.close()
    cnx.close()

    return jsonify(success=True)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    cnx = mysql.connector.connect(user='arca', password='arca', host='localhost', database='rubrica')

    cursor = cnx.cursor()

    query = "SELECT * FROM utenti WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()
    cnx.close()

    if user is None:
        abort(404)
    else:
        return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
