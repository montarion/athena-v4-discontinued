import {
  LitElement,
  html,
  css
} from 'https://unpkg.com/lit-element@2.1.0/lit-element.js?module'
import Navigo from 'https://unpkg.com/navigo@7.1.2/lib/navigo.es.js'

console.log('%c Athena: Hello', 'background-color: black; color: red;')

class AthenaRouterOutlet extends LitElement {
  static get properties() {
    return {
      route: { type: Object },

    }
  }

  constructor() {
    super()
    // const test = JSON.stringify({ category: "anime", type: "latest" });
    // const test2 = JSON.stringify({ category: "anime", type: "list" });
    // const test3 = JSON.stringify({ category: "anime", type: "showinfo", data: { show: "One Piece" } });
    // this.client.send(test);
    // this.client.send(test2);
    // this.client.send(test3);


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


  render() {
    return html`
      <div>
        ${this.route}
      </div>
    `
  }
}
customElements.define('athena-router-outlet', AthenaRouterOutlet)
