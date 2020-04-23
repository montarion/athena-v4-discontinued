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


var ws = new WebSocket("ws://83.163.109.161:8080/");

function connect() {

    return new Promise(function (resolve, reject) {

        if (ws.readyState != 1) {

            console.info("socket is connecting...");
            ws.onopen = function () {
                console.info('socket is connected')
                resolve(ws); // new socket is returned
            };
            ws.onmessage = function (e) {
                callbackFunc(JSON.parse(e.data))
            };
            ws.onerror = function (err) {
                reject(err);
            };

        } else {
            console.info('socket was already connected')
            resolve(ws); // existing socket is returned
        }
    });
}

const networking = { connect, sendmsg, sendmessage }; // export the needed functions
// this is a shorthand for: { connect: connect, sendmsg: sendmsg, sendmessage: sendmessage};

export default networking;
