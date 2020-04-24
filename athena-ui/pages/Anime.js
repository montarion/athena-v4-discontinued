import {
    LitElement,
    html,
    css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

import networking from '../networking.js';

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
        super.connectedCallback();
        this.setPageHandler();
        this.getAnimeList();
        var dtf = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' });

    }

    disconnectedCallBack() { // on element Destroy
        this.client.destroy(); // kill client
        super.disconnectedCallBack()
    }

    getAnimeList() {
        // networking.js

        // keep correct reference 
        var self = this;

        // as soon as socket is returned, lets send a request
        networking.connect().then(ws => {

            //pass the opened connection to the function, the request and the callback 
            networking.sendmessage({ category: "anime", type: "list" },
                (animeList) => { // pass the callback function
                    self.animeList = animeList.data.list; //set latestAnime in Home.js
                    console.log(self.animeList);
                    console.log(self.animeList[0].aired_at);
                });

        }).catch(error => { // errors with socket connection end up here
            console.log(error);
        });
    }

    setPageHandler() {
        networking.setPageCallbackHandler((e) => {
            console.log("ANIME-PAGE RECEIVED EVENT FROM SERVER:", e)
            // if(e.type=="anime-added-to-list") {do stuff with event}
            // if(e.type=="new-latest-anime") { do stuff with event}
            //etc.
        });
    }

    constructor() {
        super();
    }


    render() {
        return html`
        <div class= "anime">
            <div class="main">
                <h1 class="title">Anime</h1>
                <div class="content">
                    ${this.animeList.map(anime => {
            return html`
                        <div class="card" style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
                        url('${anime.art.cover}'); background-size: cover">
                        ${anime.title}<br> Latest episode: ${anime.lastep} <br>
                        Aired on: ${new Date(anime.aired_at * 1000).toUTCString()} // more shows will be getting it
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
            background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0));
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

            box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.3);
          }
          .card:hover {
            box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.6);
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
