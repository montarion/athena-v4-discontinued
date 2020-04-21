import {
  LitElement,
  html,
  css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'
import Navigo from 'https://unpkg.com/navigo@7.1.2/lib/navigo.es.js'

console.log('%c Athena: Hello', 'background-color: black; color: blue;')

class AthenaRouterOutlet extends LitElement {
  static get properties() {
    return {
      route: { type: Object },
      client: { type: Object },
      id: { type: Object } // id can be between 0-999  
    }
  }
  constructor() {
    super()
    this.id = Math.floor(Math.random() * Math.floor(999));
    console.log(`Connecting to socket as: ${this.id}`)

    this.client = new WebSocket("ws://83.163.109.161:8080"); //wss://echo.websocket.org
    this.client.onopen = () => {
      console.log('connected to socket at:', this.client.url)
      const test = JSON.stringify({category: "anime", type:"list"});
      this.client.send(test);
    };

    this.client.onmessage = (event) => {
      console.log('RECEIVED: ', JSON.parse(event.data));
    };

    let router = new Navigo('/', true, '#!')
    router
      .on('home', () => {
        this.route = html`
        <home-page></home-page>
        `
      })
      .on('anime', () => {
        this.route = html`
        <anime-page></anime-page>
        `
      })
      .on('events', () => {
        this.route = html`
        <events-page></events-page>
        `
      })
      //should be the last 'catch'
      .on('*', () => {
        console.log('routing wildcard')
        this.route = html`
        <home-page></home-page>
        `
      })
    router.resolve()
  }

  disconnectedCallBack() { // on element Destroy
    this.client.destroy(); // kill client
    super.disconnectedCallBack()
  }

  render() {
    return html`
      <div>
        ${this.route}
      </div>
    `
  }
}
customElements.define('athena-router-outlet', AthenaRouterOutlet)
