<template>
  <div id="app">
    <LoadingScreen />

    <div v-if="api.status.img" id="background"
      :style="'background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(' + api.baseurl + '/static/img/' + api.status.img">
    </div>
    <div v-else id="background" style="background: grey;"></div>

    <div @click="closePopup" v-if="api.error && api.error.isError == true"
      class="popup-small popup-error">
      <div class="popup-title">
        <span v-if="api.error.title">{{api.error.title}}</span>
        <span v-else>Error</span>
      </div>
      <div class="popup-content">
        <span>{{api.error.body}}</span>
      </div>
      <span class="popup-dismiss"></span>
    </div>

    <div @click="closePopup" v-if="api.error && api.error.isError == false"
      class="popup-small popup-success">
      <div class="popup-title">
        <span v-if="api.error.title">{{api.error.title}}</span>
        <span v-else>Success</span>
      </div>
      <div class="popup-content">
        <span>{{api.error.body}}</span>
      </div>
      <span class="popup-dismiss"></span>
    </div>

    <Sidebar />

    <div class="mt-1" id="page-content-wrapper">

      <transition name="fade" mode="out-in">
        <router-view />
      </transition>

    </div>

    <PlaybackBar />

  </div>
</template>

<script>
  import PlaybackBar from '@/components/PlaybackBar.vue';
  import LoadingScreen from '@/components/LoadingScreen.vue';
  import Sidebar from '@/components/Sidebar.vue';

  export default {

    data() {
      return {
        file: '',
      };
    },
    components: {
      PlaybackBar,
      LoadingScreen,
      Sidebar,
    },

    async created() {
      this.api.status = await this.api.getStatus();
    },

    methods: {
      closePopup() {
        $('.popup-small').hide();
        this.api.clearError();
      },
    },
  };

</script>

<style lang="scss">
  @import url('https://fonts.googleapis.com/css?family=Raleway:100,200,300,400,700');

  .hover-scale {
    cursor: pointer;
    transition: 100ms;

    &:hover {
      transform: scale(1.1)
    }
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity .3s;
  }

  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }

  html {
    overflow-x: hidden;
  }

  #app {
    font-family: 'Raleway', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: white;
  }

  #background {
    position: fixed;
    height: 100%;
    width: 100%;
    filter: blur(15px);
    background-size: cover;
    background-position: center;
    z-index: -9999;
    transform: scale(1.1);
  }

  #page-content-wrapper {
    position: relative;
    min-width: 100vw;
    height: 100%;
    padding-top: 40px;
  }

  .btn-primary {
    border: 1px solid white;
    background: transparent;
    border-radius: 25px;
    padding-right: 20px;
    padding-left: 20px;
  }

  .popup-small {
    position: absolute;
    right: 5px;
    top: 5px;
    display: inline-block;
    min-width: 200px;
    height: 100px;
    padding: 20px;
    border-radius: 25px;
    cursor: pointer;
    z-index: 9999;
  }

  .popup-small:hover {
    opacity: 0.8;
  }

  .popup-success {
    background: linear-gradient(to bottom right, rgb(134, 254, 174), rgb(114, 219, 158));
  }

  .popup-error {
    background: linear-gradient(to bottom right, rgb(255, 177, 177), rgb(255, 104, 104));
  }

  .popup-title {
    font-size: 24px;
  }

  .popup-content {
    margin-top: 5px;
  }

</style>
