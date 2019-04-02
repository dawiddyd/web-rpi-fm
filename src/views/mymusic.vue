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
              </tr>
            </thead>
            <tbody>
              <tr v-for="(song, index) in api.songs" :key="song.name">
                <!-- <td>
                  {{ index }}
                </td> -->
                <td>
                  <img v-if="song.img" :src="'http://localhost:9000/static/img/' + song.img"
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
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  // import HelloWorld from '@/components/HelloWorld.vue';

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
