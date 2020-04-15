import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
Vue.use(VueSidebarMenu)



import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faUser, faChartArea, faArrowAltCircleRight, faArrowAltCircleLeft, faHome, faBullhorn, faDragon, faBorderAll
, faBars } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret, faUser, faChartArea, faArrowAltCircleRight, faArrowAltCircleLeft, faHome, faBullhorn, faDragon, faBorderAll
  , faBars)


Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
