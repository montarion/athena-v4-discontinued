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
      test: { type: Object }
    }
  }

  connectedCallback() {
    super.connectedCallback();
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

  setPageHandler() {
    networking.setPageCallbackHandler((e) => {
      console.log("HOME-PAGE HANDLING:", e)
      // if(e.type=="new-latest-anime") { do stuff with event }
      // if(e.type=="new-weather-forecast") { do stuff with event }
      //etc.
    });
  }

  constructor() {
    super();
  }

  clickedLatestAnime(e) {
    document.location = '#!/anime/' + e.target.id;
}

  render() {

    return html`
    <div class="home">
    <div class="main">
      ${JSON.stringify(this.test)}
      <h1 class="site-title">Welcome to Athena</h1>
      <div class="content">
        <div class="card full system">
          <div class="title">System Stats</div>
          <div class="info">
            CPU: 62%  | RAM: 74%  |  GREEN
          </div>
        </div>
        <div  id="${this.latestAnime.title}" @click="${this.clickedLatestAnime}" class="card full anime" style="background-image: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url('${this.latestAnime.art.banner}');">
        <div id="${this.latestAnime.title}" class="title">Latest Anime</div>
          <div id="${this.latestAnime.title}" class="info">
            ${this.latestAnime.title} - Episode: ${this.latestAnime.lastep}
          </div>
        </div>
        <div class="card half weather">
        <div class="title">Weather</div>
          <div class="info">
           Dutch weather sucks anyways
          </div>
        </div>
        <div class="card half events" @click="${this.goToEvents}">
        <div class="title">Upcoming Events</div>
          <div class="info">
           FortaRock 2020 \\m/
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
  }
  static get styles() {
    return css`
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
      padding-top: 0.3rem;
      padding-bottom: 0.3rem;
      width: 100%;
      background-color: linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0));
      text-shadow: 1px 1px #000000;
    }

    .full {
      flex-basis: 90% !important;
    }
    .half {
      margin-top: 3em !important;
      flex-basis: 40% !important;
    }

    .card {
      min-height: 10em;
      max-height: 10em;
      border-radius: 10px;
      margin-bottom: 1em;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: flex-start;
      
      box-shadow: 0 1rem 2rem 0 rgba(0,0,0,0.3);
      transition: box-shadow 0.5s ease-in-out;
  }

  .card:hover {
    box-shadow: 0 1rem 1.5rem 0 rgba(0,0,0,0.8);
  }

  .system {
    /*I really want linear gradient to be part of .card... [TODO]*/ 
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://media.idownloadblog.com/wp-content/uploads/2014/10/iStat-Mini.png");
    height: 10em; /* You must set a specified height */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-size: cover; /* Resize the background image to cover the entire container */

    color: white;
  }

  .anime {
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://tokyo.nl/wp-content/uploads/2014/10/manga-tekeningen.jpg");
    height: 10em; /* You must set a specified height */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-size: cover; /* Resize the background image to cover the entire container */

    color: white;

  }

  .weather {
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://www.holland.com/upload_mm/1/1/e/68507_fullimage_utrecht.jpg");
    height: 10em; /* You must set a specified height */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-size: cover; /* Resize the background image to cover the entire container */

    color: white;
  }

  .events {
    background-image: 
        linear-gradient(to top, rgba(0,0,0, 0.8), rgba(0,0,0, 0.0)),
        url("https://images0.persgroep.net/rcs/rp7cchjFlYAS8JMJNuHJL0oSzP0/diocontent/149781697/_fitwidth/694/?appId=21791a8992982cd8da851550a453bd7f&quality=0.8");
    height: 10em; /* You must set a specified height */
    background-position: center; /* Center the image */
    background-repeat: no-repeat; /* Do not repeat the image */
    background-size: cover; /* Resize the background image to cover the entire container */

    color: white;
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
  }
   
   .content {
      display: flex;
      flex-wrap: wrap;
      flex-grow: 1;
      justify-content: space-evenly;
  }
  }

      `;
  }
}

customElements.define('home-page', HomePage)

