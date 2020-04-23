// networking
var callbackFunc = () => null; // function holder to call on message receive

function sendmsg(ws, category, type, data = {}, metadata = {}, callback) {
    callbackFunc = callback;
    try {
        ws.send(JSON.stringify({ "category": category, "type": type, "data": data, "metadata": metadata }))
    } catch {
        console.error('socket is not yet ready!')
    }
};

function sendmessage(ws, message, callback) {
    callbackFunc = callback;
    try {
        ws.send(JSON.stringify(message))
    } catch {
        console.error('socket is not yet ready!')
    }
}

function connect() {
    console.info("socket is connecting...");
    return new Promise(function (resolve, reject) {
        const ws = new WebSocket("ws://83.163.109.161:8080/");
        ws.onopen = function () {
            resolve(ws);
        };
        ws.onmessage = function (e) {
            callbackFunc(JSON.parse(e.data))
        };
        ws.onerror = function (err) {
            reject(err);
        };

    });
}

const networking = { connect, sendmsg, sendmessage }; // export the needed functions
// this is a shorthand for: { connect: connect, sendmsg: sendmsg, sendmessage: sendmessage};

export default networking;
