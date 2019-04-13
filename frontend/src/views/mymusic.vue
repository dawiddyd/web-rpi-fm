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
              <tr v-for="song in api.songs" :key="song.filename">
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
                  <span v-if="song.length">{{Number((song.length / 60).toFixed(1))}} min</span>
                  <span v-else>Unknown length</span>
                </td>
                <td>
                  <img v-if="api.status.name != song.name"
                    @click="startPlaying(song.filename, api.now_playing_freq, song.filename, song.length)"
                    src="../assets/play-button.svg" class="playback-nav ml-2 mr-2" height="30px">
                  <img v-else @click="stopPlaying()" src="../assets/pause.svg"
                    class="playback-nav ml-2 mr-2" height="30px">
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

  async created() {
    this.api.songs = await this.api.getLs();
  },

  methods: {
    async startPlaying(file_name, freq, radio_text, length) {
      try {
        await this.api.startPlaying(file_name, freq, radio_text);
        this.api.status = await this.api.getStatus();

        $('.media-progress-bar').stop(true).css(
          'width', '0%',
        ),

        $('.media-progress-bar').animate({
          width: '100%',
        }, length * 600);
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

<style scoped lang="scss">
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

  .playback-nav {
    cursor: pointer;
    transition: 100ms;

    &:hover {
      transform: scale(1.1)
    }
  }

</style>
