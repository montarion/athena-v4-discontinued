import {
  LitElement,
  html,
  css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'

class HomePage extends LitElement {

  goToAnime() {
    document.location = '#!/anime';
  }

  goToEvents() {
    document.location = '#!/events';
  }

  render() {
    return html`
    <div class="home">
    <div class="main">
      <h1 class="site-title">Welcome to Athena</h1>
      <div class="content">
        <div class="card full system">
          <div class="title">System Stats</div>
          <div class="info">
            CPU: 62%  | RAM: 74%  |  GREEN
          </div>
        </div>
        <div class="card full anime"  @click="${this.goToAnime}">
        <div class="title">Anime</div>
          <div class="info">
            Newest release: Shagugan No Shana S3 E1 | D
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

    .card:hover {
      color: #2CB2FF;
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

