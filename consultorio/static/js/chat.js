
const TEMPO_MAX = 30 * 24 * 60 * 60;


var ws = new WebSocket("ws://localhost:5010/");


function consulta(usuario, paciente, tempo){
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
}