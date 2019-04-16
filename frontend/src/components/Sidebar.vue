<template>
  <div>
    <div class="d-flex" id="wrapper">
      <div id="sidebar-wrapper">
        <button class="btn hover-scale" id="menu-toggle">
          <font-awesome-icon icon="bars" style="color: white; font-size: 1.5rem;" /> </button>
        <div class="sidebar-heading">web-rpi-fm</div>
        <div class="list-group">
          <router-link class="list-group-item" to="/">Now playing</router-link>
          <router-link class="list-group-item" to="/mymusic">My Music</router-link>
          <router-link class="list-group-item" to="/settings">Settings</router-link>
        </div>
        <form @submit.prevent="uploadFile" class="mb-2">
          <div class="upload-btn-wrapper d-flex justify-content-center">
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
      });
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
        } else {
          await this.api.setError('Error', 'File cannot be sent');
        }
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
    font-weight: 200;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    height: 100%;
    margin-left: -21rem;
    z-index: 9999;
    -webkit-transition: margin .25s ease-out;
    -moz-transition: margin .25s ease-out;
    -o-transition: margin .25s ease-out;
    transition: margin .25s ease-out;
  }

  #menu-toggle {
    border: 0px solid;
    position: absolute;
    top: 5px;
    right: -50px;
    border-radius: 10px;

    &:active {
      outline: 0px !important;
    }
  }

  @media (max-width: 768px) {
    #wrapper.toggled #menu-toggle {
      position: absolute;
      top: 5px;
      right: 10px;
      border-radius: 10px;
    }
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
    width: 21rem;
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
      height: 100vh;
    }

    #wrapper.toggled #sidebar-wrapper {
      margin-left: -21rem;
    }
  }

</style>
