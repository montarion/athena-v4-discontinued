# run webserver with
```bash
python3 components/website.py
```

## API stuff

# message object from the server looks like
```json
{
  "category": "String", 
  "type": "String",
  "data": {},
  "metadata": {}
}
```

## Category "anime":

type "latest":
```json
{
  "data": {
    "title": "String", 
    "art": {
        "banner": "URL", 
        "cover": "URL"
     },
    "episode": 1
   }
}
```
(nog geen progress info)

type "list":
"data": {[String, String, String, ...]}

type "showinfo":
```json
{
  "data": {
    "title": "String",
    "art": {
      "banner": "URL",
      "cover": "URL"
     }, 
   "episode": 1
   }
}
```

* required parameter "show" in data.


to **request data** from the server simply send a json dict that looks like
```json
{
  "category": "anime",
  "type": "showinfo",
  "data": {
    "show":"One Piece"
  },
  "metadata":{}
}
```

(only category and type are mandatory)
