import {
  LitElement,
  html,
  css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

import networking from '../networking.js';

class HomePage extends LitElement {

  goToAnime() {
    document.location = '#!/anime';
  }

  goToEvents() {
    document.location = '#!/events';
  }

  static get properties() {
    return {
      route: { type: Object },
      client: { type: Object },
      latestAnime: { type: Object },
      test: { type: Object },
      cards: { type: Array },
      eventCard: { type: Object }
    }
  }

  connectedCallback() {
    super.connectedCallback();
    this.cards = [];
    this.eventCard = { type: "events", title: "Upcoming Events", subtitle: "FortaRock 2020", bgURL: "https://images0.persgroep.net/rcs/rp7cchjFlYAS8JMJNuHJL0oSzP0/diocontent/149781697/_fitwidth/694/?appId=21791a8992982cd8da851550a453bd7f&quality=0.8" }
    this.setPageHandler();
    this.getLatestAnime();
    // setTimeout(() => networking.connect().then(ws => networking.sendmessage(ws, { category: "test", type: "failure" })), 1000);
  }

  disconnectedCallBack() { // on element Destroy
    this.client.destroy(); // kill client
    super.disconnectedCallBack()
  }

  getLatestAnime() {
    // networking.js

    // keep correct reference 
    var self = this;

    // as soon as socket is returned, lets send a request
    networking.connect().then(ws => {

      //pass the opened connection to the function, the request and the callback 
      networking.sendmessage({ category: "anime", type: "latest" },
        function (latestAnime) { // pass the callback function
          self.latestAnime = latestAnime.data; //set latestAnime in Home.js
        });

    }).catch(error => { // errors with socket connection end up here
      console.log(error);
    });
  }



  replaceCard(id, card) {
    if (id == "events") {
      this.eventCard = card;
    }
    if (id == "anime") {
      this.animeCard = card;
    }
  }

  setPageHandler() {
    networking.setPageCallbackHandler((e) => {
      console.log("HOME-PAGE HANDLING:", e)
      if(e.type =="replace"){
      this.replaceCard("events", 
      {
        type: "events",
        title: e.data.title,
        subtitle: `${e.data.title}: Episode ${e.data.lastep}`,
         bgURL: e.data.art.cover
        });
    }
    else {
      console.log("couldnt replace anything")
    }
    });
  }

  constructor() {
    super();
  }

  clickedLatestAnime(e) {
    document.location = '#!/anime/' + e.target.id;
  }

  getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  renderCard({ type, title, subtitle, bgURL }) {
    console.log('rendering:', type, title)
    if (type == "events") {
      return html`
          <div class="card events image" @click="${this.goToEvents}"
          style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), 
          url('${bgURL}'); background-size: cover; background-position: center;">
              <div class="title">
                ${title}
              </div>
              <div class="info">
                ${subtitle}
              </div>
          </div>
      `;
    }

    if (type == "anime") {
      return html`
          <div  id="${title}" 
          @click="${this.clickedLatestAnime}" 
          class="card anime image" 
          style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), 
          url('${bgURL}'); background-size: cover; background-position: center;">
              <div id="${title}" class="title">
                ${title}
              </div>
              <div id="${title}" class="info">
                ${this.subtitle}
              </div>
          </div>
      `;
    }
  }


  render() {

    return html`
    <div class="home">
      <div class="main">
        ${JSON.stringify(this.test)}
        <h1 class="site-title">
          Welcome to Athena
        </h1>
        <div class="content">
          <div class="card system image">
            <div class="title">System Stats</div>
            <div class="info">
              CPU: 62%  | RAM: 74%  |  GREEN
            </div>
          </div>
          <div  id="${this.latestAnime.title}" 
          @click="${this.clickedLatestAnime}" 
          class="card anime image" 
          style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)), url('${this.latestAnime.art.banner}'); background-size: cover; background-position: center;">
              <div id="${this.latestAnime.title}" class="title">Latest Anime
              </div>
              <div id="${this.latestAnime.title}" class="info">
              ${this.latestAnime.title} - Episode: ${this.latestAnime.lastep}
              </div>
          </div>
          <div class="bottom-content">
            <div class="card weather image">
                  <div class="title">
                    Weather
                  </div>
                  <div class="info">
                    Dutch weather sucks anyways
                  </div>
            </div>
            <div class="divider"></div>
            ${this.renderCard(this.eventCard)}
        </div>
        <!-- <div class="bottom-content">
          <div class="card" style="flex: 2; background-color: ${this.getRandomColor()}"></div>
            <div class="divider"></div>
          <div class="card" style="background-color: ${this.getRandomColor()}"></div>
        </div>
        <div class="bottom-content">
          <div class="card" style="flex: 1; background-color: ${this.getRandomColor()}"></div>
        </div>
      </div>-->
      </div>

   </div>
  `;
  }
  static get styles() {
    return css`

    .divider {
    }

    .title, site-title { 
      padding-top: 0.3rem;
      padding-bottom: 0.3rem;
      width:100%;
      text-shadow: 1px 1px #000000;
      background-image: linear-gradient(to bottom, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0));
    }
    .title{
        font-size: xx-large;
    }

    .info {
      background-color: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0));
      text-shadow: 1px 1px #000000;
    }

    .card {
      flex: 1 1;
      border: 1px solid #2cb2ff; 
      min-height: 15em;

      border-radius: 2em !important;
      margin-bottom: 1em;
      
      box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.3);
      transition: box-shadow 0.5s ease-in-out;
  }

  .card:hover {
    box-shadow: 0 1rem 1.5rem 0 rgba(0,0,0,0.8);
  }

  .system {
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://media.idownloadblog.com/wp-content/uploads/2014/10/iStat-Mini.png");
  }
  
  .bottom-content {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-between;
    align-items: flex-start;
    align-content: flex-start;
  }

  .weather {
    flex: 3 1;
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://www.holland.com/upload_mm/1/1/e/68507_fullimage_utrecht.jpg");
  }

  .divider {
    flex: 0.1 0.1;
  }

  .events {
    flex: 2 1;
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://images0.persgroep.net/rcs/rp7cchjFlYAS8JMJNuHJL0oSzP0/diocontent/149781697/_fitwidth/694/?appId=21791a8992982cd8da851550a453bd7f&quality=0.8");
  }
    
  .title {
    color: white;
  }

   .subtitle {
      margin: 0;
      padding: 0;
      color: white;
      font-weight: 600; // border:
  }
  
   .image {
      width: 100%;
      height: 100%;
      overflow: hidden;
      border-radius: inherit;
      background-position: center; /* Center the image */
      background-repeat: no-repeat; /* Do not repeat the image */
      background-size: cover; /* Resize the background image to cover the entire container */
      color: white;
  }
   
   .content {
     padding-left: 1em;
    display: flex;
     flex-direction: column;
  }

  }

      `;
  }
}

customElements.define('home-page', HomePage)

