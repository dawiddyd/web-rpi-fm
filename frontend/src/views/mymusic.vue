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
                <th scope="col"></th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="this.api.songs.length == 0">
                <td colspan="4">
                  <h4 style="opacity: 0.4">Your playlist is currently empty</h4>
                </td>
              </tr>
              <tr v-for="(song, index) in api.songs" :key="song.filename">
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
                    @click="startPlaying(index, song.filename, song.filename, song.length)"
                    src="../assets/play-button.svg" class="playback-nav ml-2 mr-2" height="35px">
                  <img v-else @click="stopPlaying()" src="../assets/pause.svg"
                    class="playback-nav ml-2 mr-2" height="35px">
                </td>
                <td>
                  <img class="playback-nav" @click="deleteFile(song.filename)"
                    src="../assets/trash-can.png" width="20">
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
  import {
    setInterval,
    setTimeout
  } from 'timers';
  export default {
    name: 'mymusic',
    data() {
      return {
        now_playing_index: '',
      };
    },
    components: {},

    async created() {
      this.api.songs = await this.api.getLs();
    },

    methods: {
      async startPlaying(index, file_name, radio_text, length) {
        this.stopPlaying();
        try {
          console.log(index);
          await this.api.startPlaying(file_name, radio_text);
          this.api.status = await this.api.getStatus();
          this.now_playing_index = index;
          $('.media-progress-bar').stop(true).css(
            'width', '0%'
          );

          this.timer = window.setInterval(async () => {
            this.api.getTimeElapsed();
            if (this.api.status.time_elapsed <= length) {
              $('.media-progress-bar').animate({
                width: '100%',
              }, length * 1000);
            } else {
              window.clearInterval(this.timer);
              await this.api.stopPlaying();
              $('.media-progress-bar').stop(true).css(
                'width', '0%'
              )
              this.api.status = await this.api.getStatus();
              this.nextSong(this.now_playing_index);
            }
          }, 500);
        } catch (e) {
          this.api.processException(e);
        }
      },

      async nextSong(index) {
        try {
          index = parseInt(index);
          let songs = this.api.songs;
          // if (((index) % songs.length) >= 1) {
          await this.startPlaying(index + 1, songs[index + 1].filename,
            songs[index + 1].filename, songs[index + 1].length);
          // }
        } catch (e) {
          this.api.processException(e);
        }
      },

      async stopPlaying() {
        try {
          await this.api.stopPlaying();
          window.clearInterval(this.timer);
          $('.media-progress-bar').stop(true).css(
            'width', '0%'
          );
          this.api.status = await this.api.getStatus();
        } catch (e) {
          this.api.processException(e);
        }
      },

      async deleteFile(filename) {
        try {
          await this.api.deleteFile(filename);
          this.api.songs = await this.api.getLs();
          // this.api.status = await this.api.getStatus();
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
