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
        // var that = this;
        console.log('loading:', this.animeName)
        networking.connect().then(_ => {
            this.loadAnime();
            this.getAnimeList();
        })

        var dtf = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' });
    }

    disconnectedCallBack() { // on element Destroy
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
        networking.sendmessage(
            {
                category: "anime",
                type: "showinfo",
                data: {
                    show: this.animeName
                }
            }, (res) => { that.anime = res.data; })
    }

    getAnimeList() {
        var that = this;
        networking.sendmessage(
            { category: "anime", type: "list" },
            (animeList) => {
                that.animeList = animeList.data.list;
                that.animeList = that.animeList.sort((anime1, anime2) => anime2.aired_at - anime1.aired_at);
            });
    }

    clickedAnimeCard(e) {
        document.location = '#!/anime/' + e.target.id;
        this.animeName = e.target.id;
        console.log('clicked', e.target.id)
        
        networking.connect().then(_ => {
            this.loadAnime();
        })
    }

    constructor() {
        super();
    }


    render() {
        console.log(this.animeList)
        return html`
        <div class= "anime">
            <div class="main">
                <div class="content">
                    <div class="selected card current" 
                    style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), url('${this.anime.art.banner}'); 
                    background-size: cover; background-position: center;">
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
                  ${
            this.animeList.map((anime, i) => {
                return html`
                         <div id="${anime.title}" @click="${this.clickedAnimeCard}" class="small-card ${i == 0 ? 'latest' : ''} ${anime.title == this.anime.title ? 'current' : ''}" 
                             style="background-image: linear-gradient(to bottom, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), url('${anime.art.cover}'); 
                             background-size: cover; background-position: center;">
                             <div id="${anime.title}" class="small-card-content">
                                 ${anime.title}
                             </div>
                         </div>
                         `;
            })
            }
                </div>
    
    `;
    }
    static get styles() {
        return css`
        .latest {
            border: 2px solid #A646FF !important; 
        }

        .current {
            border: 2px solid #2CB2FF !important; 
        }

        .unavailable {
            border: 2px solid #CF5959 !important;
        }

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
            border: 2px solid #596ACF; 
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
            border: 3px solid #2cb2ff; 
            background-color: white;
            flex-basis: 30em;
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
