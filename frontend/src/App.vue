<template>
  <div id="app">
    <div id="background"
      :style="'background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(' + this.api.now_playing + ');'">
    </div>
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
        <!-- <button class="btn btn-primary">Upload music</button>


        <div class="upload-btn-wrapper">
          <button class="btn">Upload a file</button>
          <input type="file" name="myfile" /> -->

        <form @submit.prevent="uploadFile" class="mb-2">
          <div class="upload-btn-wrapper">
            <button class="btn btn-primary">Upload a file</button>
            <input type="file" @change="onFileChange" id="changeFile" />
          </div>
          <button type="submit" class="btn btn-primary">Upload music</button>
        </form>

        <!-- <form @submit.prevent="uploadFile" class="mb-2">
          <div class="row mb-3">
            <input class="" type="file" @change="onFileChange" id="changeFile">
          </div>
          <button type="submit" class="btn btn-primary">Upload music</button>
        </form> -->


      </div>


    </div>
    <!-- /#sidebar-wrapper -->

    <!-- Page Content -->
    <div id="page-content-wrapper">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>

    </div>
    <!-- /#page-content-wrapper -->

    <div class="bar d-flex align-items-center justify-content-center">
      <div class="media-progress-bar">

      </div>
      <img src="./assets/back.svg" height="40px" class="ml-2 mr-2">
      <img src="./assets/play-button.svg" class="ml-2 mr-2" height="40px">
      <img src="./assets/next.svg" height="40px" class="ml-2 mr-2">
    </div>

  </div>
  <!-- /#wrapper -->
  </div>
</template>

<script>
  // @ is an alias to /src
  // import HelloWorld from '@/components/HelloWorld.vue';

  export default {

    data() {
      return {
        file: '',
      }
    },

    mounted() {
      $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
        // $("#menu-toggle").css("display", "none");
      });

      $(".media-progress-bar").animate({
        width: "100%"
      }, 40000)

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



  .upload-btn-wrapper input[type=file] {
    font-size: 100px;
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity .3s;
  }

  .fade-enter,
  .fade-leave-to

  /* .fade-leave-active below version 2.1.8 */
    {
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
    background-color: rgba(255, 255, 255, 0.5);
  }

  .media-progress-bar {
    height: 5px;
    width: 0%;
    background-color: white;
    position: absolute;
    top: -5px;
    left: 0;
  }

</style>
