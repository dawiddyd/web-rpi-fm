<template>
  <div id="app">
    <div v-show="api.loading" class="overlay">
      <div class="lds-default">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <div v-if="api.status.img" id="background"
      :style="'background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(' + api.baseurl + '/static/img/' + api.status.img">
    </div>

    <div v-else-if="api.status.img == null" id="background"
      style="background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('./assets/default-cover.jpg')">
    </div>

    <!-- do naprawy -->

    <div class="d-flex" id="wrapper">
      <!-- Sidebar -->
      <div id="sidebar-wrapper">
        <button class="btn btn-primary" id="menu-toggle">
          <font-awesome-icon icon="bars" style="color: white; font-size: 1rem;" /> </button>
        <div class="sidebar-heading">web-rpi-fm</div>
        <div class="list-group">
          <router-link class="list-group-item" to="/">Now playing</router-link>
          <router-link class="list-group-item" to="/mymusic">My Music</router-link>
          <router-link class="list-group-item" to="/settings">Settings</router-link>
        </div>

        <form @submit.prevent="uploadFile" class="mb-2">
          <div class="upload-btn-wrapper d-flex justify-content-center">
            <!-- <button class="btn btn-primary mb-2">Upload a file</button> -->
            <input type="file" @change="onFileChange" id="changeFile" />
          </div>
          <button type="submit" class="btn btn-primary">Upload music</button>
        </form>
      </div>

    </div>
    <!-- /#sidebar-wrapper -->

    <!-- Page Content -->
    <div class="mt-1" id="page-content-wrapper">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>

    </div>
    <!-- /#page-content-wrapper -->

    <div class="bar d-flex align-items-center justify-content-center">
      <div class="media-progress-bar">

      </div>
      <img src="./assets/back.svg" height="40px" class="ml-2 mr-2">

      <img v-if="!api.status.name" src="./assets/play-button.svg" class="ml-2 mr-2" height="40px">
      <img v-else @click="stopPlaying()" src="./assets/pause.svg" class="ml-2 mr-2" height="40px">

      <img src="./assets/next.svg" height="40px" class="ml-2 mr-2">
    </div>

  </div>
  <!-- /#wrapper -->
  </div>
</template>

<script>
  export default {

    data() {
      return {
        file: '',
      }
    },

    async created() {
      this.api.status = await this.api.getStatus();
    },

    mounted() {
      $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        // $("#menu-toggle").css("display", "none");
      });

      $(".media-progress-bar").animate({
        width: "100%"
      }, 6000)

      // var width = $('.media-progress-bar').css("width");
      //         if (width == "100%"){
      //           $('.media-progress-bar').css("width", "0%");
      //         };

    },

    methods: {
      onFileChange(event) {
        this.file = event.target.files[0]
      },
      async uploadFile() {
        let formData = new FormData();
        formData.append('audio', this.file);
        if (this.file) {
          console.log(this.file);
          try {
            await this.api.uploadFile(formData);
            this.api.songs = await this.api.getLs();
          } catch (e) {
            this.api.processException(e);
          }
        } else
          await this.api.setError("Błąd!", "Nie udało się wysłąć pliku");
      },
      async startPlaying() {
        try {
          await this.api.startPlaying();
          this.api.status = await this.api.getStatus();
        } catch (e) {
          this.api.processException(e);
        }
      },

      async stopPlaying() {
        try {
          await this.api.stopPlaying();
          this.api.status = await this.api.getStatus();
        } catch (e) {
          this.api.processException(e);
        }
      },
    },
  };

</script>


<style lang="scss">
  @import url('https://fonts.googleapis.com/css?family=Raleway:100,200,300,400,700');

  .upload-btn-wrapper {
    position: relative;
    overflow: hidden;
    display: inline-block;
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
    overflow: hidden;
  }

  #app {
    font-family: 'Raleway', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: white;
  }

  #background {
    position: absolute;
    height: 100%;
    width: 100%;
    /* background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(../assets/background.jpg); */
    filter: blur(15px);
    background-size: cover;
    background-position: center;
    z-index: -9999;
    transform: scale(1.1);
  }

  #sidebar-wrapper {
    position: fixed;
    /*do zmiany na absolute */
    font-weight: 200;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    min-height: 100vh;
    margin-left: -20rem;
    z-index: 9999;
    -webkit-transition: margin .25s ease-out;
    -moz-transition: margin .25s ease-out;
    -o-transition: margin .25s ease-out;
    transition: margin .25s ease-out;
  }

  #menu-toggle {
    position: absolute;
    top: 5px;
    right: -70px;
    border-radius: 10px;
  }

  .list-group-item {
    font-size: 2rem;
    font-weight: 100;
    color: white;
    background: transparent;
    border: 0px;
  }

  #sidebar-wrapper .sidebar-heading {
    padding: 0.875rem 1.25rem;
    font-size: 2.5rem;
  }

  #sidebar-wrapper .list-group {
    width: 20rem;
  }

  #page-content-wrapper {
    position: relative;
    min-width: 100vw;
    /*Do naprawy (urzadzenia mobilne)*/
    min-height: 100vh;
    padding-top: 50px;
  }

  #wrapper.toggled #sidebar-wrapper {
    margin-left: 0;
  }

  @media (min-width: 768px) {
    #sidebar-wrapper {
      margin-left: 0;
    }

    #page-content-wrapper {
      min-width: 0;
      width: 100%;
    }

    #wrapper.toggled #sidebar-wrapper {
      margin-left: -20rem;
    }
  }

  .btn-primary {
    border: 1px solid white;
    background: transparent;
    border-radius: 25px;
    padding-right: 20px;
    padding-left: 20px;
  }


  .bar {
    height: 50px;
    width: 100%;
    position: fixed;
    bottom: 0px;
    background-color: rgba(255, 255, 255, 0.3);
  }

  .media-progress-bar {
    height: 5px;
    width: 0%;
    background-color: white;
    position: absolute;
    top: -5px;
    left: 0;
  }






  .overlay {
    height: 100%;
    width: 100%;
    position: fixed;
    /* Stay in place */
    z-index: 9999;
    /* Sit on top */
    left: 0;
    top: 0;
    background-color: rgb(0, 0, 0);
    /* Black fallback color */
    background-color: rgba(0, 0, 0, 0.6);
    /* Black w/opacity */

    display: flex;
    align-items: center;
    justify-content: center;
  }

  .lds-default {
    display: inline-block;
    position: relative;
    width: 64px;
    height: 64px;
  }

  .lds-default div {
    position: absolute;
    width: 5px;
    height: 5px;
    background: #fff;
    border-radius: 50%;
    animation: lds-default 1.2s linear infinite;
  }

  .lds-default div:nth-child(1) {
    animation-delay: 0s;
    top: 29px;
    left: 53px;
  }

  .lds-default div:nth-child(2) {
    animation-delay: -0.1s;
    top: 18px;
    left: 50px;
  }

  .lds-default div:nth-child(3) {
    animation-delay: -0.2s;
    top: 9px;
    left: 41px;
  }

  .lds-default div:nth-child(4) {
    animation-delay: -0.3s;
    top: 6px;
    left: 29px;
  }

  .lds-default div:nth-child(5) {
    animation-delay: -0.4s;
    top: 9px;
    left: 18px;
  }

  .lds-default div:nth-child(6) {
    animation-delay: -0.5s;
    top: 18px;
    left: 9px;
  }

  .lds-default div:nth-child(7) {
    animation-delay: -0.6s;
    top: 29px;
    left: 6px;
  }

  .lds-default div:nth-child(8) {
    animation-delay: -0.7s;
    top: 41px;
    left: 9px;
  }

  .lds-default div:nth-child(9) {
    animation-delay: -0.8s;
    top: 50px;
    left: 18px;
  }

  .lds-default div:nth-child(10) {
    animation-delay: -0.9s;
    top: 53px;
    left: 29px;
  }

  .lds-default div:nth-child(11) {
    animation-delay: -1s;
    top: 50px;
    left: 41px;
  }

  .lds-default div:nth-child(12) {
    animation-delay: -1.1s;
    top: 41px;
    left: 50px;
  }

  @keyframes lds-default {

    0%,
    20%,
    80%,
    100% {
      transform: scale(1);
    }

    50% {
      transform: scale(1.5);
    }
  }

</style>
