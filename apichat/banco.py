#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


import mysql.connector
import datetime

banco = None

def init():

	global banco

	banco = mysql.connector.connect(
		host = 'diastorres.com',
		user = 'root', 
		password = '!Q@W#E$R5t6y7u8i',
		database = 'testechat'
		)

def execute(query, cursor):

	global banco

	if banco is None:
		return False

	cursor = banco.cursor()

	cursor.execute(query)

	return True

def consulta(usuario, paciente, tempo):

	global banco

	cursor = banco.cursor()

	t = datetime.datetime.now() - datetime.timedelta(seconds = tempo)

	t =t.strftime("%Y-%m-%d %H:%M:%S")

	cursor.execute("select conversa_ID from conversa where paciente_ID=%s and usuario_ID=%s" %(paciente, usuario))
	conversa_ID = cursor.fetchall()[0][0]
	cursor.execute('select * from mensagem where conversa_ID=%s and time>"%s"' %(conversa_ID, t))

	return cursor.fetchall()

def nova_mensagem(usuario, paciente, de, texto):

	global banco

	cursor = banco.cursor()
	t = datetime.datetime.now()
	t =t.strftime("%Y-%m-%d %H:%M:%S")

	cursor.execute("select conversa_ID from conversa where paciente_ID=%s and usuario_ID=%s" %(paciente, usuario))
	conversa_ID = cursor.fetchall()[0][0]

	cursor.execute('insert into mensagem (conversa_ID, de, mensagem_texto, time) values(%s, %s, "%s", "%s")' %(conversa_ID, de, texto, t))

	banco.commit()

	return True