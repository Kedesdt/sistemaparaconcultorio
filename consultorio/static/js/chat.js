
const TEMPO_MAX = 30 * 24 * 60 * 60;


var ws = new WebSocket("ws://localhost:5010/");

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


ws.onmessage = function (event) {
    data = JSON.parse(event.data);
    console.log(data);
	console.log(data.tipo);
	if (data.tipo = "msgs"){
		for(var i = 0; i < data.data.length; i++){
			//var l = document.createElement("td");
			var msg = document.createElement("td");
			msg.setAttribute("width", "100%");
			if (data.data[i].de == 0){
				msg.setAttribute("class", "btn float-left btn-success");
			}
			else{
				msg.setAttribute("class", "btn float-rigth btn-warning");
			}
			msg.innerHTML = data.data[i].texto;
			tbody.appendChild(msg);
			//l.appendChild(msg)
		}

	}

}


var idp = document.getElementById('nome_paciente').title;
console.log(idp);
setTimeout(consulta, 1000, idu, idp);

