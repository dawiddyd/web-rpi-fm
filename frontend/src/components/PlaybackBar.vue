<template>
  <div class="bar">
    <div class="bar d-flex align-items-center justify-content-center">
      <div class="media-progress-bar">
      </div>
      <div>
        <img src="../assets/back.svg" height="40px" class="playback-nav ml-2 mr-2">
        <img v-if="!api.status.name" src="../assets/play-button.svg" class="playback-nav ml-2 mr-2"
          height="40px">
        <img v-else @click="stopPlaying()" src="../assets/pause.svg" class="playback-nav ml-2 mr-2"
          height="40px">
        <img src="../assets/next.svg" height="40px" class="playback-nav ml-2 mr-2">
      </div>
      <!-- <span>{{ api.status.name }}</span> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaybackBar',
  methods: {
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
          window.clearInterval(this.timer);
          $('.media-progress-bar').stop(true).css(
            'width', '0%'
          );
          this.api.status = await this.api.getStatus();
        } catch (e) {
          this.api.processException(e);
        }
      },
  },
};

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  .playback-nav {
    cursor: pointer;
    transition: 100ms;

    &:hover {
      transform: scale(1.1)
    }
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

</style>
