import pytz, datetime


BR = pytz.timezone('America/Sao_Paulo')

def gera_mes(ano, mes):

<<<<<<< Updated upstream
    t = time.strptime("%s%s" %(ano, mes), "%Y%m")
    primeiro_dia_do_mes = t.tm_wday + 1 if t.tm_wday + 1 < 8 else 0
    l = []
    data_em_segundos = time.mktime(t)

    for i in range(35):
        l.append(time.localtime(data_em_segundos + ((i - primeiro_dia_do_mes) * 24 * 60 * 60)).tm_mday)
=======
    t = datetime.datetime.strptime("%s%s" %(ano, mes), "%Y%m")
    primeiro_dia_do_mes = t.weekday() + 1 if t.weekday() + 1 < 7 else 0
    l = {}

    for i in range(42):
        now = datetime.datetime.now(BR)
        t_dia = t + datetime.timedelta(i - primeiro_dia_do_mes)
        l[i] = {'dia': t_dia.day}
        l[i]['hoje'] = True if t_dia.date() == now.date() else False
        l[i]['outro_mes'] = True if not t_dia.month == mes else False
        l[i]['compromissos'] = []
>>>>>>> Stashed changes

    return l, primeiro_dia_do_mes