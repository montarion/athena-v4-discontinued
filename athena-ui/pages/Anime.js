import {
    LitElement,
    html,
    css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

class AnimePage extends LitElement {

    static get properties() {
        return {
            route: { type: Object },
            client: { type: Object },
            clientIsConnected: { type: Boolean },
            id: { type: Object }, // id can be between 0-999  
            latestAnime: { type: Object },
            animeList: { type: Array }

        }
    }

    connectedCallback() {
        this.id = Math.floor(Math.random() * Math.floor(999));
        console.log(`Connecting to socket as: ${this.id}`)

        this.client = new WebSocket("ws://83.163.109.161:8080"); //wss://echo.websocket.org
        this.client.onopen = () => {
            this.clientIsConnected = true;
            console.log('connected to socket at:', this.client.url)

            this.getLatestAnime();
            this.getAnimeList();
            super.connectedCallback();
        }


        this.client.onmessage = (event) => {
            const msg = JSON.parse(event.data)
            console.log('RECEIVED: ', msg);

            if (msg.status == 200) {

                if (msg.category == 'anime') {
                    if (msg.type == 'latest') {
                        this.latestAnime = msg.data;
                    }

                    if (msg.type == 'list') {
                        this.animeList = msg.data.list;
                    }
                }

            } else { //not status 200
                console.log('Got message without code 200', msg);
            }
        };
    }

    disconnectedCallBack() { // on element Destroy
        this.client.destroy(); // kill client
        super.disconnectedCallBack()
    }

    getLatestAnime() {
        this.client.send(JSON.stringify({ category: "anime", type: "latest" }))
    }

    getAnimeList() {
        this.client.send(JSON.stringify({ category: "anime", type: "list" }))
    }


    render() {
        return html`
        <div class= "anime">
            <div class="main">
                <h1 class="title">Anime</h1>
                <div class="content">
                    ${this.animeList.map(anime => {
                        return html`
                        <div class="card">
                        ${anime}
                        </div>
                        `;
                    })}
                    <!-- <div class="card"></div>
                    <div class="card"></div>

                    <div class="card"></div>
                    <div class="card"></div> -->
                </div>
            </div>
        </div>
    `;
    }
    static get styles() {
        return css`
        .card {
            background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), 
                url(https://tokyo.nl/wp-content/uploads/2014/10/manga-tekeningen.jpg);
            background-color: white;
            flex-basis: 40%;
            min-height: 15em;
            border-radius: 2em;
            margin-top: 2em;
          
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            color: white;
            font-size: 26px;
          }
          
          .content {
            display: flex;
            flex-wrap: wrap;
            flex-grow: 1;
            justify-content: space-evenly;
          }
          .title {
            color: white;
          }
        `;
    }
}

customElements.define('anime-page', AnimePage)
