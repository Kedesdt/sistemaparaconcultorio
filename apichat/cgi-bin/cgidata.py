#!/usr/bin/env python
# coding: utf-8

import os.path, cgi, cgitb, json, sys, sqlite3
cgitb.enable() 

caminho = 'C:\\Users\\kdtorres\\Documents\\programacao\\Python\\sistemaradios\\banco\\db.db'

def printJson(data):
    
    print('Status: 1\r\n')
    #print('Content-type: text/html\n')
    
    #print('<!DOCTYPE html>')
    print('%s' %data)
    #print('\t<head></head>')
    #print('\t<body>')
    #print('\t\t<pre style="word-wrap: break-word; white-space: pre-wrap">')
    #print('\t\t\t%s' %data)
    #print('\t\t</pre>')
    #print('\t</body>')
    #print('</html>')

radios = ['bnfm', 'bfm', 'nfm', 'pfm', 'rbfm'] 
radiosFM = ['010969', '010961', '010953', '010921', '010909']
radiosP = ['PulsoBNFM', 'PulsoBFM', 'PulsoNFM', 'Pulso921', 'PulsoRBFM']
ips = {'ip3': '8.8.8.8', 'ip2': '200.147.35.149', 'ip1': '189.69.208.89'}

IDs = ['ID000', 'ID001']

form = cgi.FieldStorage()
erro = False
nome = 'Nome'

if "nome" in form:
    
    nome = str(form['nome'].value)

else:

    erro = True

if not erro:

    if nome == "all":
        data = {}
        ####################################
        conexao = sqlite3.connect(caminho)  # conexao
        cursor = conexao.cursor()
        ####################################
        for i in range(len(radiosFM)):
            try:
                #d1 = open("../Receptor/servidorrxfm/%s.json" % radiosFM[i], 'rb').read()
                #d1 = d1.decode()
                query = 'select * from dados where time = (select max(time) from dados where ID=%s) and ID = %s;' %(radiosFM[i], radiosFM[i])
                cursor.execute(query)
                resultado = cursor.fetchall()
                d1 = '{"time": "%s", "nivel": %i, "estereo": %i, "RDS": %i, ' \
                     '"FMStation": %i, "Freq": %f, "AudioL": %i, "AudioR": %i, ' \
                     '"FMready": %i, "Dpl": %i, "Dpr": %i}' %(resultado[0][1], resultado[0][2],
                                                              resultado[0][3], resultado[0][4],
                                                              resultado[0][5], float(resultado[0][6]),
                                                              resultado[0][7], resultado[0][8],
                                                              resultado[0][9], resultado[0][10],
                                                              resultado[0][11])
            except Exception as erro:
                d1 ='{"time": "None", "nivel": "None", "estereo": "None", "RDS": "None", "FMStation": "None", "Freq": "None", "AudioL": "None", "AudioR": "None", "FMready": "None", "Dpl": "None", "Dpr": "None"}'
            try:
                #d2 = open("./%s.json" % radiosP[i], 'rb').read()
                #d2 = d2.decode()
                query = 'select * from pulso where dataHora = (select max(dataHora) from pulso where IDRadio = %s)' %radiosFM[i]
                cursor.execute(query)
                resultado = cursor.fetchall()
                d2 = '{"time": "%s", "nome": "%s", "status": %i}' %(resultado[0][0], radiosP[i], 1 if resultado[0][2] == "Local" else 0)
            except Exception as erro:
                d2 ='{"time": "None", "nome": "None", "status": "None"}'

            d1 = json.loads(d1)
            d2 = json.loads(d2)

            data[radios[i]] = {"fm": d1, "pulso": d2}
        for i in ips:

            try:
                d3 = open("./%s.json" % ips[i], 'rb').read()
                d3.decode()
            except:
                d3 = '{"time": "None", "ip": "None", "enviados": "None", "recebidos": "None", "perdidos": "None", "minimo": "None", "maximo": "None", "media": "None"}'

            d3 = json.loads(d3)
            nome = ips[i]

            data[i] = {"dados": d3}

        data['links'] = {}
        conexao.close()

        for i in IDs:

            try:
                d4 = open("./%s.json" % i, 'rb').read()
                d4.decode()
            except:
                d4 = '{"time": "None"}'

            d4 = json.loads(d4)

            data['links'][i] = {'dados': d4}

        data = json.dumps(data)

    else:
        try:
            data = open("./%s.json" % nome, 'rb').read()
            data = data.decode()
        except:
            data ='{"time": "None", "nome": "None", "status": "None"}'

printJson(data)

"""Modelo Dicionario:
   {
        nomeDaRadio: 
            {'fm': {"time": "None", "nivel": "None", "estereo": "None", "RDS": "None", "FMStation": "None", "Freq": "None", "AudioL": "None", "AudioR": "None", "FMready": "None", "Dpl": "None", "Dpr": "None"},
             'pulso': {"time": "None", "nome": "None", "status": "None"}
        }
   } 
"""


