from flask import Flask, jsonify
import mysql.connector as mysql
import json

servico = Flask("comentarios")

DESCRICAO = "serviço de listagem e cadastro de comentários!"
VERSAO = "1.0"

SERVIDOR_BANCO = "banco"
USUARIO_BANCO = "root"
SENHA_BANCO = "admin"
NOME_BANCO = "animes"

# conexão com o banco de dados
def get_conexao_com_bd():
    conexao = mysql.connect(host=SERVIDOR_BANCO,
                             user=USUARIO_BANCO,
                               password=SENHA_BANCO,
                                 database=NOME_BANCO)

    return conexao


@servico.get("/info")
def get_info():
    return jsonify(descricao = DESCRICAO, versao = VERSAO)

@servico.get("/comentarios/<int:anime>/<int:ultimo_comentario>/<int:tamanho_pagina>")
def get_comentarios(anime, ultimo_comentario, tamanho_pagina):
    comentarios = []

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id as comentario_id, feed as anime_id, comentario, nome, conta, DATE_FORMAT(data, '%Y-%m-%d %H:%i') as data " +
                   "FROM comentarios " +
                   "WHERE feed = " + str(anime) + " AND id < " + str(ultimo_comentario) + " ORDER BY comentario_id DESC, data DESC " +
                   "LIMIT " + str(tamanho_pagina))
    comentarios = cursor.fetchall()
    conexao.close()

    return jsonify(comentarios)


@servico.post("/adicionar/<int:anime>/<string:nome>/<string:conta>/<string:comentario>")
def add_comentario(anime, nome, conta, comentario):
    resultado = jsonify(situacao = "ok", erro = "")

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            f"INSERT INTO comentarios(feed, nome, conta, comentario, data) VALUES({anime}, '{nome}', '{conta}', '{comentario}', NOW())")
        conexao.commit()
    except:
        conexao.rollback()
        resultado = jsonify(situacao = "erro", erro = "erro adicionando comentário")

    conexao.close()

    return resultado


@servico.delete("/remover/<int:comentario_id>")
def remover_comentario(comentario_id):
    resultado = jsonify(situacao = "ok", erro = "")

    conexao = get_conexao_com_bd()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            f"DELETE FROM comentarios WHERE id = {comentario_id}")
        conexao.commit()
    except:
        conexao.rollback()
        resultado = jsonify(situacao = "erro", erro = "erro removendo o comentário")

    conexao.close()

    return resultado

if __name__ == "__main__":
    servico.run(host = "0.0.0.0", debug = True)