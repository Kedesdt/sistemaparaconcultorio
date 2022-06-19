
const TEMPO_MAX = 30 * 24 * 60 * 60;

var botaop = document.getElementById('botaop');
var boatom = document.getElementById('botaom');

var fonte_inicial = 15;

botaop.addEventListener('click', zoomin);
botaom.addEventListener('click', zoomout);

function zoomout(element){
	//console.log("Zoom -");
	fonte_inicial = fonte_inicial - 5;
	var linhas = document.getElementsByTagName("td");
	for (var i =0; i < linhas.length; i++){
		linhas[i].style.fontSize = fonte_inicial + "px";
	}
}

function zoomin(){
	//console.log("Zoom +");
	fonte_inicial = fonte_inicial + 5;
	var linhas = document.getElementsByTagName("td");
	//console.log(linhas);
	for (var i =0; i < linhas.length; i++){
		linhas[i].style.fontSize = fonte_inicial + 'px';
	}

}

var inseridas = [];
var ws = new WebSocket("ws://localhost:5010/");

var entrada = document.getElementById("entrada_de_texto");
entrada.addEventListener("keypress", function(e) {
	if (e.code == "Enter"){
		envia(info.tipo);
	}
  });
var botao_enviar = document.getElementById("button-addon2");
botao_enviar.addEventListener("click", envia);

var tabela_chat = document.getElementById('tabela_chat');
var tbody = document.createElement("tbody");
tabela_chat.appendChild(tbody);
var idp = document.getElementById('nome_paciente').title;
var idu = tabela_chat.title;

function consulta(usuario, paciente, tempo = TEMPO_MAX){
	console.log("Consulta");
	ws.send(JSON.stringify({tipo: "consulta", usuario: usuario, paciente: paciente, tempo: tempo}));
}

function nova_mensagem(usuario, paciente, de, texto){
	console.log("Mensagem");
	ws.send(JSON.stringify({tipo: "nova_mensagem", usuario: usuario, paciente: paciente, de: de, texto: texto}));
}

function envia(de = 1){

	nova_mensagem(idu, idp, de, entrada.value);
	//insere_msg(de, entrada.value);
	entrada.value = "";

}

function insere_msg(de, texto){
	var tr = document.createElement("tr");
	var msg = document.createElement("td");
	tr.setAttribute("width", "100%");

	console.log(info.tipo);
	console.log(de);
	if (de != info.tipo){
		msg.setAttribute("class", "btn float-left btn-success");
	}
	else{
		msg.setAttribute("class", "btn float-right btn-warning");
	}
	msg.style.fontSize= fonte_inicial + "px";
	msg.innerHTML = texto;
	tr.appendChild(msg);
	tbody.appendChild(tr);
}

ws.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);
	console.log(data.tipo);
	if (data.tipo = "msgs"){
		for(var i = 0; i < data.data.length; i++){
			
			if (!inseridas.includes(data.data[i].id)){
				insere_msg(data.data[i].de, data.data[i].texto);
				inseridas.push(data.data[i].id)
			}
			/*var tr = document.createElement("tr");
			var msg = document.createElement("td");
			tr.setAttribute("width", "100%");
			if (data.data[i].de == 0){
				msg.setAttribute("class", "btn float-left btn-success");
			}
			else{
				msg.setAttribute("class", "btn float-right btn-warning");
			}
			msg.innerHTML = data.data[i].texto;
			tr.appendChild(msg);
			tbody.appendChild(tr);
			//l.appendChild(msg)
			*/
		}

	}

}


var idp = document.getElementById('nome_paciente').title;
console.log(idp);
setInterval(consulta, 5000, idu, idp);

