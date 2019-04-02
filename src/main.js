import '@babel/polyfill'
import Vue from 'vue';
import './plugins/fontawesome'
import './plugins/bootstrap-vue'
import axios from 'axios';
import App from './App.vue';
import router from './router';
import {
  api
} from './api';

window.$ = window.jQuery = require('jquery');

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

axios.defaults.baseURL = "http://localhost:9000";
// api.authToken = localStorage.authToken;

// axios.interceptors.request.use((config) => {
//   var authToken = api.authToken;
//   if (authToken) {
//     config.headers.Authorization = `Bearer ${authToken}`;
//   }
//   return config;
// }, (err) => {
//   return Promise.reject(err);
// });

// axios.interceptors.response.use(response => {
//   return response;
// }, error => {
//   if (error.response && error.response.status == 403)
//     api.processException(error);

//   return Promise.reject(error);
// });

Vue.mixin({
    data: function () {
      return {
        get api() {
          return api;
        }
      }
    }
  }),

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
