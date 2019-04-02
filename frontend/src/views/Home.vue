<template>
  <div class="home">
    <div class="container-fluid">
      <img :src="this.api.now_playing" class="media-cover">
      <h1 class="media-title">Szprycer</h1>
      <h5 class="media-artist">Taco Hemingway</h5>
      <input class="mb-2" id="frequency" type="text" value="90.0Hz"><br />
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
