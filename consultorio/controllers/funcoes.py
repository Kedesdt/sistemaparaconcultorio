import time


def gera_mes(ano, mes):

    t = time.strptime("%s%s" %(ano, mes), "%Y%m")
    primeiro_dia_do_mes = t.tm_wday + 1 if t.tm_wday + 1 < 8 else 0
    l = {}
    data_em_segundos = time.mktime(t)

    for i in range(42):
        now = time.time()
        t_dia = data_em_segundos + ((i - primeiro_dia_do_mes) * 24 * 60 * 60)
        l[i] = {'dia': time.localtime(t_dia).tm_mday}
        l[i]['hoje'] = True if time.localtime(t_dia).tm_yday == time.localtime(now - (3 * 60 * 60)).tm_yday else False
        l[i]['outro_mes'] = True if not time.localtime(t_dia).tm_mon == mes else False
        l[i]['compromissos'] = []

    return l