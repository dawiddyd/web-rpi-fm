<template>
  <div class="home">
    <div class="container-fluid">
      <img v-if="api.status.img" :src="api.baseurl + '/static/img/' + api.status.img"
        class="media-cover">
      <img v-else class="media-cover" src="../assets/default-cover.png">
      <h1 v-if="api.status.name" class="media-title">{{ api.status.name }}</h1>
      <h1 v-else class="media-title">Nothing playing</h1>
      <h5 v-if="api.status.name" class="media-artist">{{ api.status.author }}</h5>
      <h5 v-else class="media-artist">Play music in the My Music page</h5>
      <form @submit.prevent="changeFreq" class="mb-2">
        <input class="mb-2" id="frequency" type="text" :value="this.api.now_playing_freq"><br />
        <button type="submit" class="btn btn-primary">Save</button>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'home',
    components: {},

    data() {
      return {

      }
    },

    async created() {
      console.log(this.api.status);
    },

    methods: {
      async changeFreq(freq) {
        try {
          await this.api.changeFreq(freq);
        } catch (e) {
          this.api.processException(e);
        }
      },
    }
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
