// networking
var ws = new WebSocket("ws://83.163.109.161:8080/");
var callbackFunc = undefined; // function specific onmessage-handler for responses of requests
var pageCallbackHandler = undefined; // page specific onmessage-handler for messages received from server

function sendmsg(ws, category, type, data = {}, metadata = {}, callback) {
    callbackFunc = callback;
    try {
        ws.send(JSON.stringify({ "category": category, "type": type, "data": data, "metadata": metadata }))
    } catch {
        console.error('socket is not yet ready!')
    }
};

function sendmessage(ws, message, callback) {
    if (callback == undefined) { }
    else {
        callbackFunc = callback;
    }

    try {
        console.log('sending', message)
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
                console.log(e)
                const message = JSON.parse(e.data);
                try {
                    if (message.status == 200) { // OP RESPONSE DOE API-LIKE CALL
                        console.log('response:', message)

                        if (callbackFunc != undefined) {
                            callbackFunc(message)
                            callbackFunc = undefined;
                        } else {
                            console.log('there was no handler set')
                            // there was no callback set
                        }
                    }
                    if (message.status != 200) { // OP EVENT DOE LOCAL STORAGE UPDATE EN/OF EVENTPAGE UPDATE
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
