import {
    LitElement,
    html,
    css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

import networking from '../scripts/networking.js';

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
                    self.animeListHorizontal = self.animeList.slice(); // clone without reference
                    self.animeList.sort(function(a,b){return b.aired_at - a.aired_at}); // sort by epoch
                    self.animeListHorizontal.sort(function(a,b){return a.aired_at - b.aired_at}); // same, but reverse, since that way it'll end up left-to-right
                    console.log(self.animeList);
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
                <!-- <h1 class="title">Anime</h1> -->
                <div class="content">
                <div class="card" style="margin-top: 0; padding-top: 0; margin-bottom: 3em;">
                Selected-Anime
                </div>
                <div class="horizontal-list"> 
                    ${this.animeListHorizontal.map(anime => {
            return html`
                        <div class="small-card" style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), url('${anime.art.cover}'); background-size: cover">
                            <div class="small-card-content">
                                    ${anime.title}
                            </div>
                        </div>
                        `;
        })}
                    </div>

                    <!-- Display "selectedAnime"-single-card instead of this cards-list -->
                    ${this.animeList.map(anime => {
            return html`
                        <div class="card" style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
                        url('${anime.art.cover}'); background-size: cover">
                            <div style="display: flex; flex-direction: column; justify-content: center;">
                                <p>
                                    ${anime.title}
                                </p>
                                <p>
                                    Latest episode: ${anime.lastep}
                                </p>
                                <p>
                                    Aired on: ${new Date(anime.aired_at * 1000).toUTCString()}
                                </p> <!-- more shows will be getting it -->
                            </div>
                        </div>
                        `;
        })}


                </div>
            </div>
        </div>
    `;
    }
    static get styles() {
        return css`
        .horizontal-list {
            overflow: auto;
            white-space: nowrap;
            margin-left: 3em;
        }

        .small-card {
            display: inline-block;
            background-color: white;
            border-radius: 2em;
            
            min-width: 20em;
            max-width: 20em;
            min-height: 15em;
            margin-right: 1em;
            margin-bottom: 1em;
            // word-break: break-all;

            color: white;
            font-size: 12px;

            box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.3);
        }

        .small-card-content {
            padding-top: 2em;
        }

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
            transition: box-shadow 0.5s ease-in-out;
          }
          .card:hover {
            box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.8);
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
