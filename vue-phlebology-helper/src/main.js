import Vue from 'vue'
import App from './App.vue'
import AuthService from './services/auth.service';
import router from './router'
import store from './store'

import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.prototype.$auth = AuthService;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
