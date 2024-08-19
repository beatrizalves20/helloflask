from helpers.database import get_db_connection
from flask import Flask, request, jsonify, g, abort
from helpers.logging import logger

app = Flask(__name__)


@app.route("/")
def index():
    logger.info('Entrou no index da aplicacao')
    return (jsonify({"versao": 1}), 200)


def getUsuarios():
    conn = get_db_connection()
    cursor  = conn.cursor()
    resultset = cursor.execute('SELECT * FROM tb_usuario').fetchall()
    usuarios = []
    for linha in resultset:
        id = linha[0]
        nome = linha[1]
        nascimento = linha[2]
        # usuarioObj = Usuario(nome, nascimento)
        usuarioDict = {
            "id": id,
            "nome": nome,
            "nascimento": nascimento
        }
        usuarios.append(usuarioDict)
    conn.close()
    return usuarios


def setUsuario(data):
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    # Persistir os dados no banco.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO tb_usuario(nome, nascimento) values ("{nome}", "{nascimento}")')
    conn.commit()
    id = cursor.lastrowid
    data['id'] = id
    conn.close()
    # Retornar o usuário criado.
    return data


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        # Listagem dos usuários
        usuarios = getUsuarios()
        return jsonify(usuarios), 200
    elif request.method == 'POST':
        # Recuperar dados da requisição: json.
        data = request.json
        data = setUsuario(data)
        return jsonify(data), 201


def getUsuarioById(id):
    usuarioDict = None
    conn = get_db_connection()
    cursor = conn.cursor()
    linha = cursor.execute(
        f'SELECT * FROM tb_usuario WHERE id = {id}').fetchone()
    if linha is not None:
        id = linha[0]
        nome = linha[1]
        nascimento = linha[2]
        # usuarioObj = Usuario(nome, nascimento)
        usuarioDict = {
            "id": id,
            "nome": nome,
            "nascimento": nascimento
        }
    conn.close()
    return usuarioDict


def updateUsuario(id, data):
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')

    # Persistir os dados no banco.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_usuario SET nome = ?, nascimento = ? WHERE id = ?', (nome, nascimento, id))
    conn.commit()

    rowupdate = cursor.rowcount

    conn.close()
    # Retornar a quantidade de linhas.
    return rowupdate

#Rota para deletar um id (DELETE)
def deleteUsuario(id):
    # Persistir os dados no banco.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_usuario SET WHERE id = ?', (id))
    conn.commit()

    rowdelete = cursor.rowcount

    conn.close()
    # Retornar a quantidade de linhas.
    return rowdelete


@app.route("/usuarios/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(id):
    if request.method == 'GET':
        usuario = getUsuarioById(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return {}, 404
    elif request.method == 'PUT':
        # Recuperar dados da requisição: json.
        data = request.json
        rowupdate = updateUsuario(id, data)
        if rowupdate != 0:
            return (data, 201)
        else:
            return (data, 304)
    elif request.method == 'DELETE':
        rowdelete = deleteUsuario(id)
        if rowdelete != 0:
            return {}, 404
        else:
            return {}, 200