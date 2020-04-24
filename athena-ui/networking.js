// networking
var ws = new WebSocket("ws://83.163.109.161:8080/");
var pageCallbackHandler = undefined; // page specific onmessage-handler for messages received from server
var requests = []; // array to register callback functions by their GUID

function Guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function sendmsg(category, type, data = {}, metadata = {}, callback) {
    callbackFunc = callback;
    try {
        ws.send(JSON.stringify({ "category": category, "type": type, "data": data, "metadata": metadata }))
    } catch {
        console.error('socket is not yet ready! Did you use connect()?')
    }
};

function sendmessage(message, callback) {
    if (message.metadata == undefined) { message.metadata = {} }

    try {
        const guid = Guid();
        message.metadata.guid = guid;
        requests[guid] = callback != undefined ? callback : null;
        console.log('sending:', message.metadata.guid)
        ws.send(JSON.stringify(message))
    } catch (error) {
        console.error('socket is not yet ready! Did you use connect()?')
        console.error('readyState:', ws.readyState)
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
                    if (message.status == 200) { // OP RESPONSE DOE API-LIKE CALL
                        console.log(requests)
                        if (requests[message.metadata.guid] != null) {
                            console.log('response:', message.metadata.guid)
                            requests[message.metadata.guid](message);
                            delete requests[message.metadata.guid];
                        } else {
                            console.log('there was no request handler set for Guid:', message.metadata.guid);
                            pageCallbackHandler(message);
                        }
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
