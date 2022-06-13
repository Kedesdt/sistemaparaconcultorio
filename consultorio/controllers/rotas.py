import base64
import io
import time, datetime, pytz
from sqlalchemy.sql import *
from base64 import b64encode
from flask import render_template, session, request, redirect, url_for, flash
from consultorio.controllers.funcoes import *
from consultorio.models.forms import *
from consultorio import app, db, bcrypt
from consultorio.models.models import Atendimento, Coordenador, Escola, Psicopedagogo, Situacao, Tipo_contato, Tipo_endereco, Usuario, Sala, Paciente, Pessoa, Contato, Endereco
"""
Escola
Endereço da escola 
Telefone da escola 
Coordenadora (o)
série atual 
Período 
"""

BR = pytz.timezone('America/Sao_Paulo')
@app.route('/addPaciente/<string:value>')
def pagina(value):
   if value == 'addPedagogo':
       return redirect(url_for('add_psicopedagogo'))
   elif value == 'addPaciente':
      return redirect(url_for('add_paciente'))
   elif value == 'addCoordenador':
       return redirect(url_for('add_coordenador'))
   elif value == 'addEscola':
       return redirect(url_for('add_escola'))
   elif value == 'addSituacao':
       return redirect(url_for('add_situacao'))
   elif value == 'addSala':
       return redirect(url_for('add_sala'))
   elif value == 'home':
       return redirect(url_for('home'))
   elif value == 'calendario':
       return redirect(url_for('esse_mes'))
   elif value == 'psicopedagogos':
       return redirect(url_for('psicopedagogos'))
   elif value == 'escolas':
       return redirect(url_for('escolas'))
   elif value == 'salas':
       return redirect(url_for('salas'))
   elif value == 'pacientes':
       return redirect(url_for('pacientes'))
   elif value == 'coordenadores':
       return redirect(url_for('coordenadores'))
   else:
       return redirect(url_for('loginacesso'))
@app.route('/')
def loginacesso():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    if 'email' not in session:
       #return redirect(url_for('primeiro'))
        return redirect(url_for('loginacesso'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('loginacesso'))

    ano = time.localtime(time.time()).tm_year
    mes = time.localtime(time.time()).tm_mon
    dia = time.localtime().tm_mday

    #return render_template('index.html', title = 'Inicio', email = session['email'], nome = usuario.nome_consultorio)
    return redirect(url_for('index'))


@app.route('/esse_mes')
def esse_mes():

    hoje = datetime.datetime.now(BR)

    return redirect(url_for('agenda', ano = hoje.year, mes = hoje.month))


@app.route('/agenda/<int:ano>/<int:mes>/<int:dia>')
def dia(ano, mes, dia):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    date = datetime.date(year=ano,month=mes,day=dia)
    di = datetime.datetime.combine(date, datetime.time(0,0,0))
    df = datetime.datetime.combine(date, datetime.time(23,59,59))

    horas = {}

    salas = Sala.query.filter_by(usuario_ID = usuario.id).all()
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()

    for i in range(24):
        horas[i] = {'agora' : False}
        horas[i]['hora'] = "%s:00" %str(i).zfill(2)
        horas[i]["compromissos"] = []
        horas[i]['marcado'] = False
    
    hoje = datetime.datetime.now(BR)

    hoje = hoje.day == date.day and hoje.month == date.month

    horas[datetime.datetime.now(BR).hour]['agora'] = True

    atendimentos = Atendimento.query.filter_by(usuario_ID = usuario.id).filter(Atendimento.data_hora >= di).filter(Atendimento.data_hora <= df).all()
    salas = Sala.query.filter_by(usuario_ID = usuario.id).all()

    for i in atendimentos:
        horas[i.data_hora.hour]["compromissos"].append(i)
        horas[i.data_hora.hour]['marcado'] = True

    return render_template('dia.html', nome = usuario.nome_consultorio, title = 'Agenda', email = session['email'],
                            horas = horas, dia = dia, mes = mes, ano = ano, salas = salas, psicopedagogos = psicopedagogos, hoje = hoje)

@app.route('/proximo_dia/<int:ano>/<int:mes>/<int:dia>')
def proximo_dia(ano, mes, dia):

    t = time.mktime(time.strptime("%s-%s-%s" %(ano, mes, dia), "%Y-%m-%d"))
    t += (24 * 60* 60)
    t = time.localtime(t)

    print(t.tm_mday)
    print(t.tm_mon)
    print(t.tm_year)

    return redirect(url_for('dia', ano = t.tm_year, mes = t.tm_mon, dia = t.tm_mday))

@app.route('/dia_anterior/<int:ano>/<int:mes>/<int:dia>')
def dia_anterior(ano, mes, dia):
    
    t = time.mktime(time.strptime("%s-%s-%s" %(ano, mes, dia), "%Y-%m-%d"))
    t -= (24 * 60* 60)
    t = time.localtime(t)

    print(t.tm_mday)
    print(t.tm_mon)
    print(t.tm_year)

    return redirect(url_for('dia', ano = t.tm_year, mes = t.tm_mon, dia = t.tm_mday))

@app.route('/atendimento/<int:ID>', methods = ['GET', 'POST'])
def atendimento(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    atendimento = Atendimento.query.filter_by(atendimento_ID = ID).first()

    return render_template('atendimento.html', nome = atendimento.paciente.pessoa.nome, atendimento= atendimento)


@app.route('/atendimento/apagar/<int:ID>', methods = ['GET', 'POST'])
def apagar_atendimento(ID):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    atendimento = Atendimento.query.filter_by(atendimento_ID = ID).first()
    db.session.delete(atendimento)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/atendimento/editar/<int:ID>', methods = ['GET', 'POST'])
def editar_atendimento(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_resgistro_agendamento(request.form)

    atendimento = Atendimento.query.filter_by(atendimento_ID = ID).first()

    if request.method == "POST" and form.validate():

        atendimento.sala_ID = request.form.get("sala")
        atendimento.psicopedagogo_ID = request.form.get("psicopedagogo")
        atendimento.paciente_ID = request.form.get("paciente")
        #hora = datetime.datetime.strptime(form.hora.data, '%H:%M:%S').hour

        data_hora = datetime.datetime.combine(datetime.date(atendimento.data_hora.year, atendimento.data_hora.month, atendimento.data_hora.day), form.hora.data)
        atendimento.data_hora = data_hora
        atendimento.obs = form.obs.data
        db.session.commit()
        return render_template('atendimento.html', nome = atendimento.paciente.pessoa.nome, atendimento= atendimento)
    
    
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()
    pacientes = Paciente.query.filter_by(usuario_ID = usuario.id).all()
    salas = Sala.query.filter_by(usuario_ID = usuario.id).all()

    form.obs.data = atendimento.obs

    hora = str(atendimento.data_hora.hour).zfill(2)
    
    return render_template('editar_atendimento.html', nome = 'atendimento.paciente.pessoa.nome', atendimento= atendimento, psicopedagogos=psicopedagogos,
                            pacientes = pacientes, salas = salas, form = form, hora=hora)


@app.route('/agendamento/<int:ano>/<int:mes>/<int:dia>/<int:hora>', methods = ['GET', 'POST'])
def agendamento(ano, mes, dia, hora):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    form = Formulario_resgistro_agendamento(request.form)

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if request.method == "POST" and form.validate():

        time = datetime.time(hora, 0)

        data = datetime.date(ano, mes, dia)

        date_time = datetime.datetime.combine(data, time)

        atendimento = Atendimento(psicopedagogo_ID = request.form.get("psicopedagogo"), data_hora = date_time, paciente_ID = request.form.get("paciente"), sala_ID = request.form.get("sala"), usuario_ID = usuario.id)

        db.session.add(atendimento)
        db.session.commit()

        flash(f'Atendimento agendado com sucesso')
        return redirect(url_for('home'))
        
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()
    pacientes = Paciente.query.filter_by(usuario_ID = usuario.id).all()
    salas = Sala.query.filter_by(usuario_ID = usuario.id).all()

    date = datetime.date(year=ano,month=mes,day=dia)

    agendamentos = Atendimento.query.filter(Atendimento.data_hora <= date)

    return render_template('agendamento.html', nome = usuario.nome_consultorio, title = 'Agenda', 
    email = session['email'], agendamentos = agendamentos, form = form, psicopedagogos = psicopedagogos, 
    salas= salas, pacientes=pacientes)


@app.route('/agenda/<int:ano>/<int:mes>')
def agenda(ano, mes):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    meses = ["Janeiro", 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    l_mes = gera_mes(ano, mes)

    proximo_mes = 1 if mes + 1 > 12 else mes + 1
    proximo_ano = ano + 1 if proximo_mes == 1 else ano

    mes_anterior = 12 if mes - 1 < 1 else mes - 1
    ano_anterior = ano - 1 if mes_anterior == 12 else ano

    usuario = Usuario.query.filter_by(email = session['email']).first()
    di = datetime.date(ano, mes, 1)
    df = datetime.date(proximo_ano, proximo_mes, 1)
    atendimentos = Atendimento.query.filter_by(usuario_ID = usuario.id).filter(Atendimento.data_hora >= di).filter(Atendimento.data_hora <= df).order_by(Atendimento.data_hora)

    for atendimento in atendimentos:

        l_mes[atendimento.data_hora.day]['compromissos'].append(atendimento)

    horas = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
             "12:00","13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

    return render_template('agenda.html', title = 'Agenda', email = session['email'], 
    nome = usuario.nome_consultorio, usuario = usuario, l_mes = l_mes, mes = mes, ano = ano, proximo_mes = proximo_mes, proximo_ano = proximo_ano,
    mes_anterior = mes_anterior, ano_anterior = ano_anterior, nome_atual = meses[mes - 1], nome_anterior = meses[mes_anterior - 1], proximo_nome = meses[proximo_mes - 1], horas = horas)


@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    form = Formulario_de_registro(request.form)
    if request.method == "POST" and form.validate():
        hash_pass = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(nome = form.nome.data , nome_consultorio = form.nome_consultorio.data, email = form.email.data, senha = hash_pass,foto='1000')
        db.session.add(usuario)
        db.session.commit()

        flash(f'Bem vindo {form.nome.data} Obrigado por registrar')
        return redirect(url_for('index'))
    #return render_template('registrar.html', title= "Página de Registro", form = form)


@app.route('/login', methods = ["GET", "POST"])
def login():
   form = Formulario_login(request.form)
   Email = request.form.get("Email")
   Senha = request.form.get("Senha")

   if request.method == "POST":
       usuario = Usuario.query.filter_by(email = Email).first()
       senha = Usuario.query.filter_by(senha = Senha).first()

       if usuario and senha:
           session['email'] = Email
           bfoto = Usuario.query.filter_by(email=Email).first()
           with open(bfoto,'rb') as f:
               foto = io.IOBase(f.read())
           flash(f'Bem vindo {Email} Você está logado', 'success')
           return render_template('index.html',Foto = foto)
       else:
        #  flash(f'Não foi possivel logar')

        #return redirect(url_for('index'))
        return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    del session['email']
    return redirect(url_for('loginacesso'))

@app.route('/cadastro/sala', methods = ['GET', 'POST'])
def add_sala():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_cadastro_sala(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        sala = Sala(nome = form.nome.data, usuario_ID = usuario.id) 
        db.session.add(sala)
        db.session.commit()

        flash(f'Sala {form.nome.data} Cadastrada com sucesso')

        next = request.form.get('next')
        if next:
            return redirect(url_for(next))
        return redirect(url_for('home'))
    return render_template('addsala.html', title= "Cadastro de sala", form = form)

@app.route('/cadastro/situacao', methods = ['GET', 'POST'])
def add_situacao():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_cadastro_situacao(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        situacao = Situacao(nome = form.nome.data, usuario_ID = usuario.id) 
        db.session.add(situacao)
        db.session.commit()

        flash(f'Situação {form.nome.data} Cadastrada com sucesso')
        next = request.form.get('next')
        if next:
            return redirect(url_for(next))
        return redirect(url_for('home'))
    return render_template('add_situacao.html', title= "Cadastro de situação", form = form)

@app.route('/cadastro/escola', methods = ['GET', 'POST'])
def add_escola():
    
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_registro_escola(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        escola = Escola(escola_nome = form.nome.data, usuario_ID = usuario.id)
        ultima = Escola.query.order_by(Escola.escola_ID.desc()).first()

        if ultima:
            ID = int(ultima.escola_ID) + 1
        else:
            ID = 1

        tipo_contato = Tipo_contato.query.filter_by(tipo = "Telefone").first()
        
        if not tipo_contato is None:
            telefone = Contato(escola_ID = ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        else:
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()
            telefone = Contato(escola_ID = ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)

        tipo_endereco = Tipo_endereco.query.filter_by(tipo = "Comercial").first()
        if not tipo_endereco is None:
            endereco = Endereco(escola_ID = ID, tipo_ID = tipo_endereco.tipo_ID, endereco = form.endereco.data)
        else:
            tipo_endereco = Tipo_endereco(tipo = "Comercial")
            db.session.add(tipo_endereco)
            tipo_endereco = Tipo_endereco.query.filter_by(tipo= "Comercial").first()
            endereco = Endereco(escola_ID = ID, tipo_ID = tipo_endereco.tipo_ID, endereco = form.endereco.data)

        db.session.add(endereco)
        db.session.add(telefone)
        db.session.add(escola)
        db.session.commit()

        flash(f'Escola {form.nome.data} Cadastrada com sucesso')

        next = request.form.get('next')
        if next:
            return redirect(url_for(next))
        return redirect(url_for('home'))
    return render_template('add_escola.html', title= "Cadastro de Escola", form = form)


@app.route('/cadastro/coordenador', methods = ['GET', 'POST'])
def add_coordenador():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_registro_coordenador(request.form)
    usuario = Usuario.query.filter_by(email = session['email']).first()
    escolas = Escola.query.filter_by(usuario_ID = usuario.id).all()
    
    if request.method == "POST" and form.validate():

        
        escola = request.form.get("escola")
        coordenador = Coordenador(coordenador_nome = form.nome.data, escola_ID = escola, usuario_ID = usuario.id)
        ultimo = Coordenador.query.order_by(Coordenador.coordenador_ID.desc()).first()

        if ultimo:
            ID = int(ultimo.escola_ID) + 1
        else:
            ID = 1

        tipo_contato = Tipo_contato.query.filter_by(tipo = "Telefone").first()
        
        if not tipo_contato is None:
            telefone = Contato(coordenador_ID = ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        else:
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()
            telefone = Contato(coordenador_ID = ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)

        db.session.add(telefone)
        db.session.add(coordenador)
        db.session.commit()

        flash(f'Coordenador {form.nome.data} Cadastrado com sucesso')
        
        next = request.form.get('next')
        if next:
            return redirect(url_for(next))
        return redirect(url_for('home'))

    return render_template('add_coordenador.html', title= "Cadastro de Coordenador", form = form, escolas = escolas)

@app.route('/cadastro/psicopedagogo', methods = ['GET', 'POST'])
def add_psicopedagogo():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_registro_psicopedagogo(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        pessoa = Pessoa(nome = form.nome.data, usuario_ID = usuario.id, cpf = form.cpf.data, rg = form.rg.data)
        db.session.add(pessoa)
        pessoa = Pessoa.query.filter_by(cpf = form.cpf.data).first()
        tipo_contato = Tipo_contato.query.filter_by(tipo = "Telefone").first()
        
        if not tipo_contato is None:
            telefone = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        else:
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()
            telefone = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        

        tipo_contato = Tipo_contato.query.filter_by(tipo = "Email").first()
        if not tipo_contato is None:
            email = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email.data)
        else:
            tipo_contato = Tipo_contato(tipo = "Email")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Email").first()
            email = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email.data)


        db.session.add(telefone)
        db.session.add(email)
        psic = Psicopedagogo(usuario_ID = usuario.id, pessoa_ID = pessoa.pessoa_ID)
        db.session.add(psic)
        db.session.commit()

        flash(f'{form.nome.data} Cadastrado com sucesso')

        next = request.form.get('next')
        if next:
            return redirect(url_for(next))
        return redirect(url_for('home'))
    return render_template('addpsic.html', title= "Cadastro de Psicopedagogo", form = form)

@app.route('/escolas')
def escolas():

    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    escolas = Escola.query.filter_by(usuario_ID = usuario.id).all()

    return render_template('escolas.html', nome=usuario.nome_consultorio, title = 'Escolas', escolas = escolas)

@app.route('/salas')
def salas():

    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    salas = Sala.query.filter_by(usuario_ID = usuario.id).all()

    return render_template('salas.html', nome=usuario.nome_consultorio, title = 'Salas', salas = salas)

@app.route('/sala/<int:ID>')
def sala(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    sala = Sala.query.filter_by(sala_ID = ID).first()

    return render_template('sala.html', title = sala.nome, sala =sala)

@app.route('/escola/<int:ID>')
def escola(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))


    escola = Escola.query.filter_by(escola_ID = ID).first()
    contatos = Contato.query.filter_by(escola_ID = ID)
    enderecos = Endereco.query.filter_by(escola_ID = ID)

    return render_template('escola.html', title = escola.escola_nome, contatos = contatos, enderecos=enderecos, escola=escola)

@app.route('/psicopedagogos')
def psicopedagogos():
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()

    return render_template('psicopedagogos.html', nome=usuario.nome_consultorio, title = 'Psicopedagogos', psicopedagogos = psicopedagogos)

@app.route('/coordenadores')
def coordenadores():
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    coordenadores = Coordenador.query.filter_by(usuario_ID = usuario.id).all()

    return render_template('coordenadores.html', nome=usuario.nome_consultorio, title = 'Coordenadores', coordenadores = coordenadores)

@app.route('/coordenador/<int:ID>')
def coordenador(ID):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    coordenador = Coordenador.query.filter_by(coordenador_ID = ID).first()
    contatos = Contato.query.filter_by(coordenador_ID = ID)

    return render_template('coordenador.html', title = coordenador.coordenador_nome, coordenador = coordenador, contatos=contatos)


@app.route('/apagar_coordenador/<int:ID>')
def apagar_coordenador(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    coordenador = Coordenador.query.filter_by(coordenador_ID = ID).first()
    db.session.delete(coordenador)
    db.session.commit()

    return redirect(url_for('coordenadores'))

@app.route('/apagar_paciente/<int:ID>')
def apagar_paciente(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    paciente = Paciente.query.filter_by(paciente_ID = ID).first()
    db.session.delete(paciente)
    db.session.commit()

    return redirect(url_for('pacientes'))


@app.route('/apagar_sala/<int:ID>')
def apagar_sala(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    sala = Sala.query.filter_by(sala_ID = ID).first()
    db.session.delete(sala)
    db.session.commit()

    return redirect(url_for('salas'))

@app.route('/apagar_psicopedagogo/<int:ID>')
def apagar_psicopedagogo(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    psicopedagogo = Psicopedagogo.query.filter_by(psicopedagogo_ID = ID).first()
    db.session.delete(psicopedagogo)
    db.session.commit()

    return redirect(url_for('psicopedagogos'))

@app.route('/apagar_escola/<int:ID>')
def apagar_escola(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    escola = Escola.query.filter_by(escola_ID = ID).first()
    db.session.delete(escola)
    db.session.commit()

    return redirect(url_for('escolas'))


@app.route('/paciente/<int:ID>')
def paciente(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    paciente = Paciente.query.filter_by(paciente_ID = ID).first()
    contatos_paciente = Contato.query.filter_by(pessoa_ID = paciente.pessoa.pessoa_ID)
    contatos_responsavel = Contato.query.filter_by(pessoa_ID = paciente.responsavel.pessoa_ID)
    contatos_coordenador = Contato.query.filter_by(coordenador_ID = paciente.coordenador.coordenador_ID)

    return render_template('paciente.html', title = paciente.pessoa.nome, contatos_coordenador = contatos_coordenador, paciente = paciente, contatos_paciente = contatos_paciente, contatos_responsavel = contatos_responsavel)

@app.route('/paciente/historico/<int:ID>')
def historico(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    date = datetime.datetime.now(BR)

    paciente = Paciente.query.filter_by(paciente_ID = ID).first()
    atendimentos = Atendimento.query.filter(Atendimento.data_hora < date).filter(Atendimento.paciente_ID == ID)


    return render_template('historico.html', title = paciente.pessoa.nome, paciente = paciente, atendimentos = atendimentos)


@app.route('/paciente/proximas/<int:ID>')
def proximas(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    date = datetime.datetime.now(BR)

    paciente = Paciente.query.filter_by(paciente_ID = ID).first()
    atendimentos = Atendimento.query.filter(Atendimento.data_hora > date).filter(Atendimento.paciente_ID == ID)

    return render_template('proximas.html', title = paciente.pessoa.nome, paciente = paciente, atendimentos = atendimentos)

@app.route('/pacientes')
def pacientes():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    pacientes = Paciente.query.filter_by(usuario_ID = usuario.id).all()
    
    return render_template('pacientes.html', nome=usuario.nome_consultorio, title = 'Pacientes', pacientes = pacientes)

@app.route('/psicopedagogo/<int:ID>')
def psicopedagogo(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    psicopedagogo = Psicopedagogo.query.filter_by(psicopedagogo_ID = ID).first()
    contatos = Contato.query.filter_by(pessoa_ID = psicopedagogo.pessoa.pessoa_ID)

    return render_template('psicopedagogo.html', title = psicopedagogo.pessoa.nome, psicopedagogo = psicopedagogo, contatos=contatos)

@app.route('/cadastro/paciente', methods = ['GET', 'POST'])
def add_paciente():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))
    
    form = Formulario_registro_paciente(request.form)

    usuario = Usuario.query.filter_by(email = session['email']).first()
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()
    situacoes = Situacao.query.filter_by(usuario_ID = usuario.id).all()
    coordenadores = Coordenador.query.filter_by(usuario_ID = usuario.id).all()
    escolas = Escola.query.filter_by(usuario_ID = usuario.id).all()
    
    if request.method == "POST" and form.validate():

        pessoa_paciente = Pessoa.query.filter_by(nome = form.nome.data).filter_by(usuario_ID = usuario.id).first()

        if not pessoa_paciente:

            pessoa_paciente = Pessoa(nome = form.nome.data, usuario_ID = usuario.id, cpf = form.cpf.data, rg = form.rg.data)
            db.session.add(pessoa_paciente)
            pessoa_paciente = Pessoa.query.filter_by(nome = form.nome.data).filter_by(usuario_ID = usuario.id).first()
        
        pessoa_responsavel = Pessoa.query.filter_by(usuario_ID = usuario.id).filter_by(cpf = form.cpf_r.data).first()

        if not pessoa_responsavel:

            pessoa_responsavel = Pessoa(nome = form.nome_r.data, usuario_ID = usuario.id, cpf = form.cpf_r.data, rg = form.rg_r.data)
            db.session.add(pessoa_responsavel)
            pessoa_responsavel = Pessoa.query.filter_by(cpf = form.cpf_r.data).first()
            
        paciente = Paciente(usuario_ID = usuario.id, pessoa_ID = pessoa_paciente.pessoa_ID, responsavel_ID = pessoa_responsavel.pessoa_ID, 
                            situacao_ID = request.form.get("situacao"), psicopedagogo_ID= request.form.get("psicopedagogo"), 
                            coordenador_ID= request.form.get("coordenador"), escola_ID= request.form.get("escola"), obs = form.obs.data)

        tipo_contato = Tipo_contato.query.filter_by(tipo = "Telefone").first()
        
        if tipo_contato is None:
            
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()

        
        telefone_paciente = Contato.query.filter_by(pessoa_ID = pessoa_paciente.pessoa_ID).filter_by(contato = form.tel.data).first()
        
        if not telefone_paciente:
            telefone_paciente = Contato(pessoa_ID = pessoa_paciente.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.tel.data)
            db.session.add(telefone_paciente)
       
        
        telefone_responsavel = Contato.query.filter_by(pessoa_ID = pessoa_responsavel.pessoa_ID).filter_by(contato = form.tel_r.data).first()
        
        if not telefone_responsavel:
            telefone_responsavel = Contato(pessoa_ID = pessoa_responsavel.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.tel_r.data)
            db.session.add(telefone_responsavel)
        
        tipo_contato = Tipo_contato.query.filter_by(tipo = "Email").first()
        
        if tipo_contato is None:

            tipo_contato = Tipo_contato(tipo = "Email")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Email").first()

        email_paciente = Contato.query.filter_by(pessoa_ID = pessoa_paciente.pessoa_ID).filter_by(contato = form.email.data).first()
        
        if not email_paciente:
            email_paciente = Contato(pessoa_ID = pessoa_paciente.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email.data)
            db.session.add(email_paciente)

        email_responsavel = Contato.query.filter_by(pessoa_ID = pessoa_responsavel.pessoa_ID).filter_by(contato = form.email_r.data).first()
        if not email_responsavel:
            email_responsavel = Contato(pessoa_ID = pessoa_responsavel.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email_r.data)
            db.session.add(email_responsavel)
        

        db.session.add(paciente)        
        db.session.commit()

        flash(f'{form.nome.data} Cadastrado com sucesso')
        return redirect(url_for('home'))
    return render_template('addpaciente.html', title= "Cadastro de Paciente", form = form, psicopedagogos = psicopedagogos, situacoes = situacoes, coordenadores = coordenadores, escolas = escolas)


@app.route('/procurar', methods = ['GET', 'POST'])
def procurar():

    if 'email' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email = session['email']).first()

    if usuario is None:
        del session['email']
        return redirect(url_for('login'))

    if request.method == "POST":

        nome = request.form.get('nome')

        pacientes = Paciente.query.join(Paciente.pessoa).filter(Pessoa.nome.like('%%'+nome+"%%"))

        return render_template('pacientes.html', nome=usuario.nome_consultorio, title = 'Pacientes', pacientes = pacientes)
