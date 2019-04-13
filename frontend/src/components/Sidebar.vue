<template>
  <div>
    <div class="d-flex" id="wrapper">
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
  </div>
</template>

<script>
export default {
  name: 'Sidebar',

  mounted() {
    $('#menu-toggle').click((e) => {
      e.preventDefault();
      $('#wrapper').toggleClass('toggled');
      // $("#menu-toggle").css("display", "none");
    });

    // var width = $('.media-progress-bar').css("width");
    //         if (width == "100%"){
    //           $('.media-progress-bar').css("width", "0%");
    //         };
  },
  methods: {
    onFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadFile() {
      const formData = new FormData();
      formData.append('audio', this.file);
      if (this.file) {
        console.log(this.file);
        try {
          await this.api.uploadFile(formData);
          this.api.songs = await this.api.getLs();
        } catch (e) {
          this.api.processException(e);
        }
      } else { await this.api.setError('Error', 'File cannot be sent'); }
    },
  },
};

</script>

<style scoped lang="scss">
  .upload-btn-wrapper {
    position: relative;
    overflow: hidden;
    display: inline-block;
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

</style>
