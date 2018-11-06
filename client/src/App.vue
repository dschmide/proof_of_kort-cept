<template>
  <div id="app">
    <v-app>
      <page-header />
        <main>
          <v-container fluid>
            <router-view>
            </router-view>
          </v-container>
        </main>
    </v-app>
  </div>
</template>

<script>
import PageHeader from '@/components/Header.vue'
import Missions from '@/components/Missions.vue'

export default {
  name: 'app',
  components: {
    PageHeader, Missions
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

div.container {
  margin-top: 56px;
}

@import './assets/leaflet.css'
</style>
