<template>
  <v-layout column>
    <v-flex md6 offset-md3 xs12>
      <div class="white elevation-0">
        <div class="pl-4 pr-4 pt-1 pb-2">
          <div>
            <br>
            <h3 class="headline mb-0">{{ this.$store.state.user }}</h3>
            <div>Checkout your current Stats in this Screen
            </div>
          </div>
          Level: {{this.currentLevel}} <br>
          <template>
            <v-progress-linear v-model="currentExperiencePercent"></v-progress-linear>
          </template>
          <br>
          Experience: {{currentExperience}} out of {{currentLevelXPTotal}} required for next Level<br>
          <br>
          Koins: {{currentKoins}} <br>
          <br>
          Towers: {{currentTowers}} <br>
          <br>
          Landmarks: {{currentLandmarks}} <br>
          <br> <br>
          Sight Range: {{currentSightRange}} meters<br>
          Tower Range: {{currentTowerRange}} meters<br>
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
      currentLandmarks: 0,

      currentExperiencePercent: 0,
      currentLevel: 1,
      currentLevelXPTotal: 50,
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
    this.currentLandmarks = myAttributes.landmarks

    this.currentSightRange = myAttributes.sight_range
    this.currentTowerRange = myAttributes.tower_range

    // Calculate percent progress of current level
    if (this.currentExperience < 50 ) {
      this.currentExperiencePercent = 100 / 50 * this.currentExperience
      this.currentLevel = 1
      this.currentLevelXPTotal = 50
    } else if (this.currentExperience < 550 ) {
      this.currentExperiencePercent = 100 / (550 - 50) * (this.currentExperience - 50)
      this.currentLevel = 2
      this.currentLevelXPTotal = 550
    } else if (this.currentExperience < 2330 ) {
      this.currentExperiencePercent = 100 / (2330 - 600) * (this.currentExperience - 600)
      this.currentLevel = 3
      this.currentLevelXPTotal = 2330 
    } else {
      // Default "maxed"
      this.currentExperiencePercent = 100
      this.currentLevel = 99
    }
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
