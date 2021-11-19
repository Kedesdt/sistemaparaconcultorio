import time, datetime
from .funcoes import *
from flask import render_template, session, request, redirect, url_for, flash
from consultorio.models.forms import *
from consultorio import app, db, bcrypt
from consultorio.models.models import Atendimento, Psicopedagogo, Situacao, Tipo_contato, Usuario, Sala, Paciente, Pessoa, Contato


"""
Escola
Endereço da escola 
Telefone da escola 
Coordenadora (o)
série atual 
Período 



"""

@app.route('/')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    return render_template('index.html', title = 'Inicio', email = session['email'], nome = usuario.nome_consultorio)

@app.route('/agenda/<int:ano>/<int:mes>/<int:dia>')
def dia(ano, mes, dia):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()

    date = datetime.date(year=ano,month=mes,day=dia)
    di = datetime.datetime.combine(date, datetime.time(0,0,0))
    df = datetime.datetime.combine(date, datetime.time(23,59,59))

    atendimentos = Atendimento.query.filter_by(usuario_ID = usuario.id).filter(Atendimento.data_hora >= di).filter(Atendimento.data_hora <= df).all()

    print(atendimentos)

    return render_template('dia.html', nome = usuario.nome_consultorio, title = 'Agenda', email = session['email'], atendimentos = atendimentos)


@app.route('/atendimento/<int:ID>', methods = ['GET', 'POST'])
def atendimento(ID):
    if 'email' not in session:
        return redirect(url_for('login'))
    return "OLA"

@app.route('/agendamento/<int:ano>/<int:mes>/<int:dia>', methods = ['GET', 'POST'])
def agendamento(ano, mes, dia):
    if 'email' not in session:
        return redirect(url_for('login'))

    form = Formulario_resgistro_agendamento(request.form)

    usuario = Usuario.query.filter_by(email = session['email']).first()

    if request.method == "POST" and form.validate():

        time = form.hora.data
        data = datetime.date(ano, mes, dia)

        print('#######')
        print(request.form.get("psicopedagogo"))
        print(request.form.get("paciente"))
        print(request.form.get("sala"))

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

    meses = ["Janeiro", 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    l_mes = gera_mes(ano, mes)

    proximo_mes = 1 if mes + 1 > 12 else mes + 1
    proximo_ano = ano + 1 if proximo_mes == 1 else ano

    mes_anterior = 12 if mes - 1 < 1 else mes - 1
    ano_anterior = ano - 1 if mes_anterior == 12 else ano

    usuario = Usuario.query.filter_by(email = session['email']).first()

    return render_template('agenda.html', title = 'Agenda', email = session['email'], 
    nome = usuario.nome_consultorio, usuario = usuario, l_mes = l_mes, mes = mes, ano = ano, proximo_mes = proximo_mes, proximo_ano = proximo_ano,
    mes_anterior = mes_anterior, ano_anterior = ano_anterior, nome_atual = meses[mes - 1], nome_anterior = meses[mes_anterior - 1], proximo_nome = meses[proximo_mes - 1])


@app.route('/registrar', methods = ['GET', 'POST'])
def registrar():
    form = Formulario_de_registro(request.form)
    if request.method == "POST" and form.validate():
        hash_pass = bcrypt.generate_password_hash(form.senha.data)
        usuario = Usuario(nome = form.nome.data , nome_consultorio = form.nome_consultorio.data, email = form.email.data, senha = hash_pass)
        db.session.add(usuario)
        db.session.commit()

        flash(f'Bem vindo {form.nome.data} Obrigado por registrar')
        return redirect(url_for('home'))
    return render_template('registrar.html', title= "Página de Registro", form = form)


@app.route('/login', methods = ["GET", "POST"])
def login():
    form = Formulario_login(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = form.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            session['email'] = form.email.data
            flash(f'Bem vindo {form.email.data} Você está logado', 'success')
            return redirect(request.args.get('next') or url_for('home'))
        
        else:
            flash(f'Não foi possivel logar')

        return redirect(url_for('home'))
    return render_template('login.html', title = 'Login', form = form)

@app.route('/cadastro/sala', methods = ['GET', 'POST'])
def add_sala():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    form = Formulario_cadastro_sala(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        sala = Sala(nome = form.nome.data, usuario_ID = usuario.id) 
        db.session.add(sala)
        db.session.commit()

        flash(f'Sala {form.nome.data} Cadastrada com sucesso')
        return redirect(url_for('home'))
    return render_template('addsala.html', title= "Cadastro de sala", form = form)


@app.route('/cadastro/psicopedagogo', methods = ['GET', 'POST'])
def add_psicopedagogo():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    form = Formulario_registro_psicopedagogo(request.form)
    
    if request.method == "POST" and form.validate():

        usuario = Usuario.query.filter_by(email = session['email']).first()
        pessoa = Pessoa(nome = form.nome.data, usuario_ID = usuario.id, cpf = form.cpf.data, rg = form.rg.data)
        db.session.add(pessoa)
        pessoa = Pessoa.query.filter_by(cpf = form.cpf.data).first()
        tipo_contato = Tipo_contato.query.filter_by(tipo_ID = "Telefone").first()
        
        if not tipo_contato is None:
            telefone = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        else:
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()
            telefone = Contato(pessoa_ID = pessoa.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.telefone.data)
        

        tipo_contato = Tipo_contato.query.filter_by(tipo_ID = "Email").first()
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
        return redirect(url_for('home'))
    return render_template('addpsic.html', title= "Cadastro de Psicopedagogo", form = form)


@app.route('/psicopedagogos')
def psicopedagogos():
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()

    print(psicopedagogos[0].pessoa.nome)

    return render_template('psicopedagogos.html', nome=usuario.nome_consultorio, title = 'Psicopedagogos', psicopedagogos = psicopedagogos)

@app.route('/paciente/<int:ID>')
def paciente(ID):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    paciente = Paciente.query.filter_by(paciente_ID = ID).first()
    contatos_paciente = Contato.query.filter_by(pessoa_ID = paciente.pessoa.pessoa_ID)
    contatos_responsavel = Contato.query.filter_by(pessoa_ID = paciente.responsavel.pessoa_ID)

    return render_template('paciente.html', title = paciente.pessoa.nome, paciente = paciente, contatos_paciente = contatos_paciente, contatos_responsavel = contatos_responsavel)

@app.route('/pacientes')
def pacientes():
    
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    pacientes = Paciente.query.filter_by(usuario_ID = usuario.id).all()
    

    return render_template('pacientes.html', nome=usuario.nome_consultorio, title = 'Pacientes', pacientes = pacientes)

@app.route('/psicopedagogo/<int:ID>')
def psicopedagogo(ID):
    if 'email' not in session:
        return redirect(url_for('login'))

    usuario = Usuario.query.filter_by(email = session['email']).first()
    psicopedagogo = Psicopedagogo.query.filter_by(psicopedagogo_ID = ID).first()
    contatos = Contato.query.filter_by(pessoa_ID = psicopedagogo.pessoa.pessoa_ID)

    return render_template('psicopedagogo.html', title = psicopedagogo.pessoa.nome, psicopedagogo = psicopedagogo, contatos=contatos)

@app.route('/cadastro/paciente', methods = ['GET', 'POST'])
def add_paciente():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    form = Formulario_registro_paciente(request.form)

    usuario = Usuario.query.filter_by(email = session['email']).first()
    psicopedagogos = Psicopedagogo.query.filter_by(usuario_ID = usuario.id).all()
    situacoes = Situacao.query.filter_by(usuario_ID = usuario.id).all()
    
    if request.method == "POST" and form.validate():

        pessoa_paciente = Pessoa(nome = form.nome.data, usuario_ID = usuario.id, cpf = form.cpf.data, rg = form.rg.data)
        db.session.add(pessoa_paciente)
        pessoa_paciente = Pessoa.query.filter_by(cpf = form.cpf.data).first()

        if not pessoa_paciente:
            
            pessoa_paciente = Pessoa.query.filter_by(nome = form.nome.data).first()

        
        pessoa_responsavel = Pessoa.query.filter_by(cpf = form.cpf_r.data).first()

        if not pessoa_responsavel:

            pessoa_responsavel = Pessoa(nome = form.nome_r.data, usuario_ID = usuario.id, cpf = form.cpf_r.data, rg = form.rg_r.data)
            db.session.add(pessoa_responsavel)
            pessoa_responsavel = Pessoa.query.filter_by(cpf = form.cpf_r.data).first()
            
        paciente = Paciente(usuario_ID = usuario.id, pessoa_ID = pessoa_paciente.pessoa_ID, responsavel_ID = pessoa_responsavel.pessoa_ID, situacao_ID = request.form.get("situacao"), psicopedagogo_ID= request.form.get("psicopedagogo"))

        tipo_contato = Tipo_contato.query.filter_by(tipo_ID = "Telefone").first()
        
        if tipo_contato is None:
            
            tipo_contato = Tipo_contato(tipo = "Telefone")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Telefone").first()

        
        telefone_paciente = Contato(pessoa_ID = pessoa_paciente.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.tel.data)
        telefone_responsavel = Contato(pessoa_ID = pessoa_responsavel.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.tel_r.data)
        
        tipo_contato = Tipo_contato.query.filter_by(tipo_ID = "Email").first()
        
        if tipo_contato is None:

            tipo_contato = Tipo_contato(tipo = "Email")
            db.session.add(tipo_contato)
            tipo_contato = Tipo_contato.query.filter_by(tipo= "Email").first()


        email_paciente = Contato(pessoa_ID = pessoa_paciente.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email.data)

        email_responsavel = Contato.query.filter_by(pessoa_ID = pessoa_responsavel.pessoa_ID).filter_by(contato = form.email_r.data).first()
        if not email_responsavel:
            email_responsavel = Contato(pessoa_ID = pessoa_responsavel.pessoa_ID, tipo_ID = tipo_contato.tipo_ID, contato = form.email_r.data)
            db.session.add(email_responsavel)
        
        db.session.add(pessoa_paciente)
        db.session.add(pessoa_responsavel)
        db.session.add(paciente)
        db.session.add(telefone_paciente)
        db.session.add(telefone_responsavel)
        db.session.add(email_paciente)
        
        db.session.commit()

        flash(f'{form.nome.data} Cadastrado com sucesso')
        return redirect(url_for('home'))
    return render_template('addpaciente.html', title= "Cadastro de Paciente", form = form, psicopedagogos = psicopedagogos, situacoes = situacoes)