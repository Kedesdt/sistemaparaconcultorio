import time


def gera_mes(ano, mes):

    t = time.strptime("%s%s" %(ano, mes), "%Y%m")
    primeiro_dia_do_mes = t.tm_wday + 1 if t.tm_wday + 1 < 8 else 0
    l = []
    data_em_segundos = time.mktime(t)

    for i in range(35):
        l.append(time.localtime(data_em_segundos + ((i - primeiro_dia_do_mes) * 24 * 60 * 60)).tm_mday)

    return l