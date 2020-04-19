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

    this.client = new WebSocket("wss://echo.websocket.org"); // this socket echo's everything back that you send to it
    this.client.onopen = () => {
      console.log('connected to socket:', this.client.url)
      this.client.send(`Hello from ${this.id}`)
    };

    this.client.onmessage = (event) => {
      console.log('RECEIVED: ' + event.data);
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
      .on('motd', () => {
        this.route = html`
        <motd-page></motd-page>
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
