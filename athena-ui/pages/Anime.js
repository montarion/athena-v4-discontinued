import {
    LitElement,
    html,
    css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

import networking from '../networking.js';

class AnimePage extends LitElement {

    static get properties() {
        return {
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
        super.disconnectedCallBack()
    }

    getAnimeList() {
        var self = this;
        networking.connect().then(ws => {
            networking.sendmessage({ category: "anime", type: "list" },
                (animeList) => {
                    self.animeList = animeList.data.list;
                    self.animeList = self.animeList.sort((anime1, anime2) => anime2.aired_at - anime1.aired_at);
                    console.log(animeList)
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

    clickedAnimeCard(e) {
        document.location = '#!/anime/' + e.target.id;
    }

    constructor() {
        super();
    }


    render() {
        return html`
        <div class= "anime">
            <div class="main">
                <div class="content">
                <div class="grid-container">
                <div class="latest card" @click="${this.clickedAnimeCard}" id="${this.animeList[0].title}"
                            style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
                            url('${this.animeList[0].art.banner}');  background-size: cover; background-position: center;">
                                <div style="display: flex; flex-direction: column; justify-content: center;" id="${this.animeList[0].title}">
                                    <p id="${this.animeList[0].title}">
                                        ${this.animeList[0].title}
                                    </p>
                                    <p id="${this.animeList[0].title}">
                                        Latest episode: ${this.animeList[0].lastep}
                                    </p>
                                    <p id="${this.animeList[0].title}">
                                        Aired on: ${new Date(this.animeList[0].aired_at * 1000).toUTCString()}
                                    </p>
                                </div>
                            </div>
                            <!-- Older anime's-->
                     ${this.animeList.slice(1).map(anime => {
            return html`
                            <div class="older card" @click="${this.clickedAnimeCard}" id="${anime.title}"
                            style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
                            url('${anime.art.cover}');  background-size: cover; background-position: center;">
                                <div style="display: flex; flex-direction: column; justify-content: center;" id="${anime.title}">
                                    <p id="${anime.title}">
                                        ${anime.title}
                                    </p>
                                    <p id="${anime.title}">
                                        Latest episode: ${anime.lastep}
                                    </p>
                                    <p id="${anime.title}">
                                        Aired on: ${new Date(anime.aired_at * 1000).toUTCString()}
                                    </p>
                                </div>
                            </div>
                            `;
        })}
                </div>
                   
                </div>
            </div>
        </div>
    `;
    }
    static get styles() {
        return css`
        .grid-container {
            background-color: #101018;
            padding-left: 1em;
            display: grid;
            grid-auto-columns: repeat(auto-fill, 1fr);
            grid-auto-rows: repeat(4, 1fr);
            gap: 1rem;
            grid-template-areas: 
            "latest latest" 
            "latest latest" 
            "latest latest" 
            "latest latest";
          }
          
        .latest { 
            grid-area: latest; 
            border: 3px solid #A646FF !important; 
        }

        .card {
            border: 1px solid #2cb2ff; 
            background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0));
            background-color: white;
            flex-basis: 40%;
            min-height: 15em;
            border-radius: 2em;
            margin-top: 1em;
          
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
            
          }
          .title {
            color: white;
          }
        `;
    }
}

customElements.define('anime-page', AnimePage)
