import '@babel/polyfill';
import Vue from 'vue';
import './plugins/fontawesome';
import './plugins/bootstrap-vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import {
  api,
} from './api';

window.$ = window.jQuery = require('jquery');

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

axios.defaults.baseURL = 'http://192.168.0.107:9000';
api.baseurl = axios.defaults.baseURL;

Vue.mixin({
    data() {
      return {
        get api() {
          return api;
        },
      };
    },
  }),

  new Vue({
    router,
    render: h => h(App),
  }).$mount('#app');
