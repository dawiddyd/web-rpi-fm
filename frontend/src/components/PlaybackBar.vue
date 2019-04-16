<template>
  <div class="bar">
    <div class="bar d-flex align-items-center justify-content-around">
      <div class="media-progress-bar">
      </div>
      <!-- <span v-if="api.status.running == true">{{ api.status.name }}</span>
        <span v-else>Nothing playing</span> -->
      <div>
        <img src="../assets/back.svg" height="40px" class="hover-scale ml-2 mr-2">
        <img v-if="!api.status.name" src="../assets/play-button.svg" class="hover-scale ml-2 mr-2"
          height="40px">
        <img v-else @click="stopPlaying()" src="../assets/pause.svg" class="hover-scale ml-2 mr-2"
          height="40px">
        <img src="../assets/next.svg" height="40px" class="hover-scale ml-2 mr-2">
      </div>
      <!-- <img src="../assets/playlist.svg" height="40px" class="hover-scale ml-2 mr-2"> -->
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
          window.clearInterval(this.timer);
          await this.api.stopPlaying();
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

<style scoped lang="scss">
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
