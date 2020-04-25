import {
    LitElement,
    html,
    css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

import networking from '../networking.js';

class AnimeDetailPage extends LitElement {

    static get properties() {
        return {
            animeName: { type: String },
            anime: { type: Object },
            animeList: { type: Array }
        }
    }

    connectedCallback() {
        super.connectedCallback();
        this.setPageHandler();
        this.animeList = [{ title: "A" }, { title: "B" }, { title: "C" }, { title: "D" }, { title: "E" }, { title: "F" }, { title: "G" }];
        this.loadAnime();
        var dtf = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' });

    }

    disconnectedCallBack() { // on element Destroy
        this.client.destroy(); // kill client
        super.disconnectedCallBack()
    }

    setPageHandler() {
        networking.setPageCallbackHandler((e) => {
            console.log("ANIME-DETAILS-PAGE RECEIVED EVENT FROM SERVER:", e)
            // if(e.type=="anime-added-to-list") {do stuff with event}
            // if(e.type=="new-latest-anime") { do stuff with event}
            //etc.
        });
    }

    loadAnime() {
        var that = this;
        var locationParts = window.location.href.split('/')
        const animeName = locationParts[locationParts.length - 1];
        console.log("Anime to load:", animeName)
        networking.connect().then(_ => {
            networking.sendmessage(
                {
                    category: "anime",
                    type: "showinfo",
                    data: {
                        show: this.animeName
                    }
                }, (res) => that.anime = res.data)
        })
    }

    constructor() {
        super();
    }


    render() {
        return html`
        <div class= "anime">
            <div class="main">
                <div class="content">
                    <div class="selected card" style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), url('${this.anime.art.cover}'); background-size: cover; background-position: center;">
                        <div style="display: flex; flex-direction: column; justify-content: center;" id="${this.anime.title}">
                                <p id="${this.anime.title}">
                                    ${this.anime.title}
                                </p>
                                <p id="${this.anime.title}">
                                    Latest episode: ${this.anime.lastep}
                                </p>
                                <p id="${this.anime.title}">
                                    Aired on: ${new Date(this.anime.aired_at * 1000).toUTCString()}
                                </p> <!-- more shows will be getting it -->
                        </div>
                    </div> 

                    <div class="horizontal-list"> 
                    ${this.animeList.map(anime => {
            return html`
                            <div class="small-card" > 
                                <div class="small-card-content">
                                    ${anime.title}
                            </div>
                        </div>
                        `;
        })}
                </div>
    
    `;
    }
    static get styles() {
        return css`
        .horizontal-list {
            overflow-x: auto;
            white-space: nowrap;
            // margin-left: 3em;
            margin-top: 2em;
        }

        ::-webkit-scrollbar{
            height: 6px;
            width: 6px;
            background: gray;
        }
        ::-webkit-scrollbar-thumb:horizontal{
            background: #2CB2FF;
            border-radius: 10px;
        }

        .small-card {
            display: inline-block;
            background-color: black;
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
            flex-basis: 15em;
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

customElements.define('anime-detail-page', AnimeDetailPage)
