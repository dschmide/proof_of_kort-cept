<template>
  <v-layout column>
    <v-dialog v-model="confirmDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span>Confirm Selection</span>
          <v-spacer></v-spacer>
        </v-card-title>
        <v-card-text>
          <span>Are you sure about your choice?</span> <br> <br>
          <b> Vision Range: </b> {{currentSightRange}} m<br>
          <b> Tower Range: </b> {{currentTowerRange}} m<br>
          <b> Extra Towers: </b> {{currentTowers}} <br>
          <v-spacer></v-spacer>
        </v-card-text>
        <v-card-actions>
          <v-btn color="red" flat @click.stop="confirmDialog=false">Wait...</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" class="light-green" flat @click="confirm">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="spendPointsDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span>Confirm Selection</span>
          <v-spacer></v-spacer>
        </v-card-title>
        <v-card-text>
          <span>You still have unspent choices: {{choicesRemaining}}. Please use all your choices before continuing.</span> <br> <br>
          <v-spacer></v-spacer>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click.stop="spendPointsDialog=false">ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <v-flex md6 offset-md3 xs12>
      <h2> Thanks for signing up to Proof of Kort-cept! </h2> <br>
      In this webapp, you can solve Missions to create a free map of the world! <br>
      You may now choose your <b>starting bonus</b>. May they help you on your journey. <br> <br>

      Choices remaining: <b> {{choicesRemaining}} </b> <br> <br>
      
      <div id='SightRange' class="white elevation-1 pl-4 pr-4 pt-3 pb-2">
        <h3> Sight Range </h3> <br>
        <b>Sight Range</b> determines how far away you can see and solve Missions from your <b>current position</b> <br>

        <v-btn icon @click.stop="decreaseSightRange" large>
          <v-icon large>remove_circle</v-icon>
        </v-btn>
        {{currentSightRange}} m
        <v-btn icon @click.stop="increaseSightRange" large>
          <v-icon large>add_circle</v-icon>
        </v-btn> 

        <br>
      </div>

      <br>

      <div id='TowerRange' class="white elevation-1 pl-4 pr-4 pt-3 pb-2">
        <h3> Tower Range </h3> <br>
        <b>Tower Range</b> determines how much vision your <b>Towers</b> provide <br>

        <v-btn icon @click.stop="decreaseTowerRange" large>
          <v-icon large>remove_circle</v-icon>
        </v-btn>
        {{currentTowerRange}} m
        <v-btn icon @click.stop="increaseTowerRange" large>
          <v-icon large>add_circle</v-icon>
        </v-btn> 
        <br>
      </div>

      <br>

      <div id='Towers' class="white elevation-1 pl-4 pr-4 pt-3 pb-2">
        <h3> 2 Towers </h3> <br>
        Alternatively, you can chose to start with <b>free Towers</b> that you can place anywhere on the map and discover Missions in this area.<br>

        <v-btn icon @click.stop="decreaseTowers" large>
          <v-icon large>remove_circle</v-icon>
        </v-btn>
        {{currentTowers}}
        <v-btn icon @click.stop="increaseTowers" large>
          <v-icon large>add_circle</v-icon>
        </v-btn> 

        <br>
      </div>
      
      <br>
      Want more info? Read this short guide on the <a href="https://github.com/dschmide/proof_of_kort-cept/wiki" target="_blank">Wiki</a>
      <br>
      <v-btn
        dark
        class="light-blue"
        @click="openConfirmDialog">
        Continue
          <v-icon right>arrow_forward</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import UserAttributesService from '@/services/UserAttributesService'

export default {
  data () {
    return {
      // Choices
      choicesRemaining: 5,

      // Mission Dialog Boxes
      confirmDialog: false,
      spendPointsDialog: false,

      myAttributes: '',

      currentExperience: 0,
      currentTowers: 0,
      currentSightRange: 2000,
      currentTowerRange: 2000,

      currentExperiencePercent: 0,
      currentLevel: 1,
      currentLevelXPTotal: 50,
    }
  },
  methods: {
    async confirm(){
      UserAttributesService.updateUserAttributes(
        {
        'koins': 0,
        'towers': this.currentTowers,
        'sight_range': this.currentSightRange,
        'tower_range': this.currentTowerRange,
        },
        this.myAttributes.id,
      )
      this.$router.push({
        name: 'missions'
      })
    },
    async openConfirmDialog() {
      console.log("opening confirm dialog, refreshing attributes")
      this.myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
      if (this.choicesRemaining == 0) {
        this.confirmDialog = true
      } else {
        this.spendPointsDialog = true
      }
      console.log(this.choicesRemaining)
    },
    async decreaseSightRange() {
      if (this.currentSightRange > 2000) {
        this.currentSightRange = this.currentSightRange - 1000
        this.choicesRemaining += 1
      }
    },
    async increaseSightRange() {
      if (this.choicesRemaining >= 1) {
        this.currentSightRange = this.currentSightRange + 1000
        this.choicesRemaining -= 1
      }
    },
    async decreaseTowerRange() {
      if (this.currentTowerRange > 2000) {
        this.currentTowerRange -= 1000
        this.choicesRemaining += 1
      }
    },
    async increaseTowerRange() {
      if (this.choicesRemaining >= 1) {
        this.currentTowerRange += 1000
        this.choicesRemaining -= 1
      }
    },
    async decreaseTowers() {
      if (this.currentTowers > 0) {
        this.currentTowers -= 2
        this.choicesRemaining += 1
      }
    },
    async increaseTowers() {
      if (this.choicesRemaining >= 1) {
        this.currentTowers += 2
        this.choicesRemaining -= 1
      }
    },
  },

  async created() {
    //this.myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
    console.log('created Welcome')
    console.log(this.myAttributes)
  },

  // This Code is executed when the Stats component is mounted
  async mounted() {
    this.myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
    console.log('Getting Profile Data...')
    console.log(this.myAttributes)
    if (parseInt(this.myAttributes.koins) == -1) {
      console.log('mounted Welcome')      
    } else {
      this.$router.push({
        name: 'stats' 
      })
    }

    this.currentExperience = this.myAttributes.experience
    this.currentKoins = this.myAttributes.koins
    this.currentTowers = parseInt(this.myAttributes.towers)
    this.currentLandmarks = this.myAttributes.landmarks

    this.currentSightRange = parseInt(this.myAttributes.sight_range)
    this.currentTowerRange = parseInt(this.myAttributes.tower_range)
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
