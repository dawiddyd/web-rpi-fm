<template>
  <div class="home">
    <div class="container-fluid">
      <img :src="this.api.now_playing_cover" class="media-cover">
      <h1 class="media-title">{{ this.api.now_playing_title }}</h1>
      <h5 class="media-artist">{{ this.api.now_playing_artist }}</h5>
      <input class="mb-2" id="frequency" type="text" :value="this.api.now_playing_freq"><br />
      <button class="btn btn-primary">Save</button>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  // import HelloWorld from '@/components/HelloWorld.vue';

  export default {
    name: 'home',
    components: {},

    data() {
      return {

      }
    },
  };

</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Raleway:100,200,300,400,700');

  .media-cover {
    height: 200px;
    width: 200px;
    border: 3px solid white;
  }

  .media-title {
    color: white;
    font-size: 3.5rem;

  }

  .media-artist {
    color: lightgrey;
    font-weight: 100;
  }

  #frequency {
    background: transparent;
    border: none;
    font-size: 7.5rem;
    width: 100%;
    text-align: center;
    color: white;
    font-weight: 100;
  }

</style>
