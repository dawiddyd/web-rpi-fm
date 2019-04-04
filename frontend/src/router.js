import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/mymusic',
      name: 'mymusic',
      component: () => import('./views/mymusic.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('./views/settings.vue'),
    }
  ],
});
