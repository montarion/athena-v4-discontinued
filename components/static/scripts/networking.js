// networking

var ws = new WebSocket("ws://83.163.109.161:8080/");
console.log("connecting");

console.log(ws.readyState);

ws.onopen = function(e) {
    console.log("open");
    var test = {category: "anime", type:"list"};
    ws.send(JSON.stringify(test));
};

ws.onmessage = function(e) {
    console.log("Message received: " , e);
};

function sendmsg(category, type, data = {}, metadata = {}) {
    var msg = {"category": category, "type": type, "data": data, "metadata": metadata};
    ws.send(JSON.stringify(msg));
    console.log("Sent message");
};
