# Athena V4 UI

## Install & Run
```bash
    npx serve
```

## OR

 
```bash
    python3 -m http.server [port]
```

## API stuff

# message object from the server looks like 

{"category": String, "type": String, "data":{}, "metadata":{}}


category "anime":

type "latest":
"data": {"name": String, "art": {"banner": URL, "cover": URL}, "episode": Int}
(nog geen progress info)

type "list":
"data": {[String, String, String, ...]}

type "showinfo":
"data": {"name": String, "art": {"banner": URL, "cover": URL}, "episode": Int}

* required parameter "show" in data.


to request data from the server simply send a json dict that looks like

{"category": "anime", "type": "showinfo", "data": {"show":"One Piece"}, "metadata":{}}
