// networking
var ws = new WebSocket("ws://83.163.109.161:8080/");
var callbackFunc = () => null; // function specific onmessage-handler for responses of requests
var pageCallbackHandler = () => null; // page specific onmessage-handler for messages received from server

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

function setPageCallbackHandler(callback) {
    pageCallbackHandler = callback;
}

function connect() {

    return new Promise(function (resolve, reject) {

        if (ws.readyState != 1) {

            console.info("socket is connecting...");
            ws.onopen = function () {
                console.info('socket is connected')
                resolve(ws); // new socket is returned
            };
            ws.onmessage = function (e) {
                const message = JSON.parse(e.data);
                try {
                    // if (e.data.type == "response") // if message is a response from server
                    if (message.status == 200) {

                        console.log('response:', message)
                        // console.log('custom handler')
                        callbackFunc(message)
                        callbackFunc = () => null;
                    }
                    // if (e.data.type == "event") { // if message is from server and not initiated by a request
                    if (message.status != 200) {
                        // console.log('page handler')
                        console.log('event:', message)
                        pageCallbackHandler(message)
                    }
                } catch {
                    console.error('Something went wrong')
                }
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

const networking = { connect, sendmsg, sendmessage, setPageCallbackHandler }; // export the needed functions
// this is a shorthand for: { connect: connect, sendmsg: sendmsg, sendmessage: sendmessage};

export default networking;
