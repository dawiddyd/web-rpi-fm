<template>
  <div class="mymusic">
    <div class="container-fluid">
      <div class="container">
        <h1>My music</h1>
        <div class="row mt-4">
          <table class="table text-white">
            <thead>
              <tr>
                <th scope="col"></th>
                <th scope="col">Name</th>
                <th scope="col">Author</th>
                <th scope="col">Length</th>
                <th scope="col"></th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="api.songs == undefined">
                <td colspan="4">
                  <h4 style="opacity: 0.4">Your playlist is currently empty</h4>
                </td>
              </tr>
              <tr v-for="(song, index) in api.songs" :key="song.name">
                <td>
                  <img v-if="song.img" :src="'http://192.168.0.107:9000/static/img/' + song.img"
                    width="40">
                  <img v-else src="../assets/default-cover.png" width="40">
                </td>
                <td>
                  <span v-if="song.name">{{song.name}}</span>
                  <span v-else>Unknown name</span>
                </td>
                <td>
                  <span v-if="song.author">{{song.author}}</span>
                  <span v-else>Unknown author</span>
                </td>
                <td>
                  <span v-if="song.length">{{song.length / 60}} min</span>
                  <span v-else>Unknown length</span>
                </td>
                <td>
                  <img v-if="api.status.name != song.name"
                    @click="startPlaying(song.filename, api.now_playing_freq, 'web-rpi-fm')"
                    src="../assets/play-button.svg" class="ml-2 mr-2" height="30px">
                  <img v-else @click="stopPlaying()" src="../assets/pause.svg" class="ml-2 mr-2"
                    height="30px">
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'mymusic',
    components: {},

    data() {
      return {

      }
    },

    async created() {
      this.api.songs = await this.api.getLs();
      console.log(this.api.songs);
    },

    methods: {
      async startPlaying(file_name, freq, radio_text) {
        try {
          await this.api.startPlaying(file_name, freq, radio_text);
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

<style scoped>
  .table {
    font-weight: 200;
  }

  th {
    border-bottom: 1px solid white !important;
    border-top: 0px;
    font-weight: 200;
  }

  td {
    border: 0px;
  }

</style>
