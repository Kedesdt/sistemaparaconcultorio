#!usr/bin/python3

import sqlite3, time, datetime, os

s = os.sep
caminho = "..%s..%s..%sbanco%sdb.db"%(s, s, s, s)
caminho = "/var/banco/db.db"

def salva(dados = None, ID = None):

    hora = dados['time']
    nivel = dados['nivel']
    dpl = dados['Dpl']
    dpr = dados['Dpr']
    freq = dados['Freq']
    estereo = True if dados['estereo'] > 0.5 else False
    rds = True if dados['RDS'] > 0.5 else False
    fmstation = True if dados['FMStation'] > 0.5 else False
    audiol = True if dados['AudioL'] > 0.5 else False
    audior = True if dados['AudioR'] > 0.5 else False
    fmready = True if dados['FMready'] > 0.5 else False


    #dictData = {'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - (60*60*3))), "nivel": nivel, "estereo": estereo, "RDS": RDS,
    # "FMStation": FMstation, "Freq": freq , "AudioL": audioL, "AudioR": audioR, "FMready": FMready, "Dpl": dpl, "Dpr": dpr}
    sql = "insert into dados (ID, time, nivel, estereo, rds, fmstation, freq, audiol, audior, fmready, dpl, dpr) values "
    #sql+= "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql += "(%i, '%s', %d, %i, %i, %i, %s, %i, %i, %i, %d, %d)" %(ID, hora, nivel, estereo, rds, fmstation, freq, audiol, audior, fmready, dpl, dpr)
    
    #print(caminho)
    #print(sql)
    conexao = sqlite3.connect(caminho)
    conexao.execute(sql)
    conexao.commit()
    conexao.close()

def pegaUltimo(ID):

    query = "select * from dados where time = (select max(time) from dados where ID=%i) and ID = %i;" %(ID, ID)
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexao.close()
    return resultado[0]

def executaCommit(caminhoBanco, query):

    conexao = sqlite3.connect(caminhoBanco)
    cursor = conexao.cursor()
    cursor.execute(query)
    conexao.commit()
    conexao.close()


def executa(caminhoBanco, query):

    conexao = sqlite3.connect(caminhoBanco)
    cursor = conexao.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexao.close()

    return resultado

def binario(x):
    BIN = "%s" %bin(x)[2:]
    while len(BIN) < 8:
        BIN = '0' + BIN

    return BIN

def salvaArray(array):
    
    entrada = array.decode().split('|')
    #print(entrada)
    #dictData = {'time': time.strftime("%Y-%m-%d %H:%M:%S.", time.gmtime(time.tim                                                                                        e() - (60*60*3))) + str(time.time() % 1)[2:5], "nivel": nivel, "estereo": estere                                                                                        o, "RDS": RDS, "FMStation": FMstation, "Freq": freq , "AudioL": audioL, "AudioR"                                                                                        : audioR, "FMready": FMready, "Dpl": dpl, "Dpr": dpr}
    dados = []
    dadosPorByte = [] 
    ID = str(entrada[0])

    for i in range(10):

        dados.append(str(entrada[i+1]))
        dadosPorByte.append(dados[-1].split('-')[:-1])


    for i in range(len(dadosPorByte)):
        for j in range(len(dadosPorByte[i])):

            dadosPorByte[i][j] = binario(int(dadosPorByte[i][j]))

    nivel = 0
    estereo = 0
    RDS = 0
    FMstation = 0
    FMready = 0
    freq = 0
    audioL = 0
    audioR = 0
    dpl =  0
    dpr = 0
    dprl = True

    for i in range(10):

        nivel += int(dadosPorByte[i][2][:-1], 2)
        estereo += int(dadosPorByte[i][0][5])
        RDS += int(dadosPorByte[i][0][3])
        FMstation += int(dadosPorByte[i][2][7])
        FMready += int(dadosPorByte[i][3][0])
        audioL += int(dadosPorByte[i][3][6])
        audioR += int(dadosPorByte[i][3][7])
        try:
            if dprl:
                dpl += int(dadosPorByte[i][4], 2)
                dpr += int(dadosPorByte[i][5], 2)
        except:
            dprl = False

        canalbin = dadosPorByte[i][0][-2:] + dadosPorByte[i][1]
        canalint = int(canalbin, 2)

        freq += (canalint / 10) + 87#canal = (Freq - 87) * 10 ***** Freq = (canal / 10) + 87

    nivel /= 10
    estereo /= 10
    RDS /= 10
    FMstation /= 10
    FMready /= 10
    freq /= 10
    audioL /= 10
    audioR /= 10
    #dpl /= 10
    #dpr /= 10

    dpl = int(dadosPorByte[9][4], 2)
    dpr = int(dadosPorByte[9][5], 2)

    canalbin = dadosPorByte[0][0][-2:] + dadosPorByte[0][1]
    canalint = int(canalbin, 2)
    freq = (canalint / 10) + 87#canal = (Freq - 87) * 10 ***** Freq = (canal / 10) + 87
    
    freqID = int(str(ID)[-4:])

    if int(FMready > 0.7) and freqID / 10 == freq:

        dictData = {'time': time.strftime("%Y-%m-%d %H:%M:%S.", time.gmtime(time.time() - (60*60*3))) + str(time.time() % 1)[2:5], "nivel": nivel, "estereo": estereo, "RDS": RDS, "FMStation": FMstation, "Freq": freq , "AudioL": audioL, "AudioR": audioR, "FMready": FMready, "Dpl": dpl, "Dpr": dpr}

        salva(dictData, int(ID))
 

if __name__ == "__main__":
    dictData = {'time': time.strftime("%Y-%m-%d %H:%M:%S.", time.gmtime(time.time() - (60*60*3))) + str(time.time() % 1)[2:5], "nivel": 90, "estereo": True, "RDS": True,
                "FMStation": False, "Freq": 955, "AudioL": True, "AudioR": True, "FMready": True, "Dpl": 250, "Dpr": 240}

    for i in dictData:
        print(dictData[i])
    ID = 10955

    salva(dictData, ID)
    """
    t = str(datetime.datetime.now())

    sql = 'insert into pulso (dataHora, IDRadio, tipo, status) ' \
          'values ("%s", %i, "%s", %i)' % (t[:-3], 10909, 'local', 1)

    executaCommit(caminho, sql)
    """
    print(pegaUltimo(ID))
    
