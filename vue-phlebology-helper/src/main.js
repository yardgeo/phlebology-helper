import Vue from 'vue'
import App from './App.vue'
import AuthService from './services/auth.service';
import router from './router'
import store from './store'
import moment from 'moment';

import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.prototype.$auth = AuthService;

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM/DD/YYYY hh:mm')
  }
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
