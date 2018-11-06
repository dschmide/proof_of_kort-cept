<template>
  <v-layout column>
    <v-flex md6 offset-md3 xs12>
      <div class="white elevation-2">
        <v-toolbar flar dense class="light-blue" dark>
        <v-toolbar-title>Stats</v-toolbar-title>
        </v-toolbar>
        <div class="pl-4 pr-4 pt-2 pb-2">
          <div>
            <br>
            <h3 class="headline mb-0">{{ this.$store.state.user }}</h3>
            <div>Checkout your current Stats in this Screen
            </div>
          </div>
          Experience:
          <template>
            <v-progress-linear v-model="currentExperience"></v-progress-linear>
          </template>
          Koins: {{currentKoins}} <br>
          Towers: {{currentTowers}} <br>
          <br> <br>
          Sight Range: {{currentSightRange}} <br>
          Tower Range: {{currentTowerRange}} <br>
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import UserAttributesService from '@/services/UserAttributesService'

export default {
  data () {
    return {
      // Mission Dialog Boxes
      currentExperience: 0,
      currentKoins: 0,
      currentTowers: 0,
      currentSightRange: 0,
      currentTowerRange: 0,
    }
  },
  methods: {
    
  },

  // This Code is executed when the Stats component is mounted
  async mounted() {
    var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
    console.log('Getting Profile Data...')
    console.log(myAttributes)
    this.currentExperience = myAttributes.experience
    this.currentKoins = myAttributes.koins
    this.currentTowers = myAttributes.towers

    this.currentSightRange = myAttributes.sight_range
    this.currentTowerRange = myAttributes.tower_range
  }
}
</script>

<style scoped>

.card__media__background {
  background-size: auto 100%;
}

.error{
   color:red;
 }

</style>
