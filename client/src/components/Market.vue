<template>
  <div id=content>
  <v-layout column>
    <v-flex md6 offset-md3 xs12>
      <div id='market' class="white elevation-0">
        <div class="pl-4 pr-4 pt-1 pb-2">
          <div>
            <h3 class="headline mb-0">Market</h3>
            <div>In the Market, players may exchange their Koins for in-game Resources or Attributes
            </div>
          </div>
        </div>
        <v-dialog v-model="showInfoBox" max-width="500px">
          <v-card>
            <v-card-title>
              <v-spacer></v-spacer>
            </v-card-title>
            <img
              :src="showInfoImage" 
              width=auto
              height=100
            >
            <v-card-text>
              
              <span>{{showInfo}}</span> <br> <br>
              <v-spacer></v-spacer>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn color="primary" class="light-green" flat @click.stop="showInfoBox=false">Ok</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        
        <v-container
          fluid
          grid-list-md
          mt-0
        >
          <v-layout row wrap>
            <v-flex
              v-for="card in cards"
              v-bind="{ [`xs${card.flex}`]: true }"
              :key="card.title"
            >
              <v-card>
                  <v-container
                    fill-height
                    fluid
                    pa-2
                    mt-1
                  >
                    <v-layout fill-height>
                      <v-flex xs12 flexbox>
                        <div :style="'height:40px'">
                          <span class="h2" v-text="card.title"></span>
                        </div>
                        <br>

                        <div class="pt-1">
                        <img
                          :src="card.imagePath" 
                          width=auto
                          height=100
                        >
                        </img>
                        </div>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  <v-btn icon @click.stop="giveInfo(card.type, card)">
                    <v-icon>info</v-icon>
                  </v-btn>
                  <v-spacer></v-spacer>
                  {{card.cost}} Koins
                  <v-btn icon @click.stop="buyItem(card.type)">
                    <v-icon>add_circle</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </div>
    </v-flex>
  </v-layout>
  <v-alert class="errorClass"
        v-model="itemBoughtSuccess"
        type="success"
        dismissible
        transition="scale-transition"
        width=400
      >
        You got a {{itemBought}}
      </v-alert>
      <v-alert class="errorClass"
        v-model="itemBoughtError"
        type="error"
        dismissible
        transition="scale-transition"
        width=400
      >
        You do not have enough Koins to get a {{itemBought}}
      </v-alert>
   </div>
</template>

<script>
import UserAttributesService from '@/services/UserAttributesService'



export default {
  data () {
    return {
      // Info Box
      showInfo: '',
      showInfoBox: false,
      showInfoImage: '',

      // alerts
      itemBought: 0,
      itemBoughtSuccess: false,
      itemBoughtError: false,

      // Mission Dialog Boxes
      currentExperience: 0,
      currentKoins: 0,
      currentTowers: 0,
      currentSightRange: 0,
      currentTowerRange: 0,

      currentExperiencePercent: 0,
      currentLevel: 1,

      cards: [
        { type: 'tower', cost: 50, title: 'Buy 1 Tower', flex: 4, imagePath: require('@/assets/tower.png'), info: "A Tower allows you to extend your vision range into territories beyond your Sight Range" },
        { type: 'landmark', cost: 500, title: 'Buy 1 Landmark', flex: 4, imagePath: require('@/assets/landmark.png'), info: "All Players can see a Landmark placed by you and bask in its glory" },
        { type: 'vrange', cost: 150, title: 'Upgrade Vision Range', flex: 4, imagePath: require('@/assets/vrange.png'), info: "Extends your Vision Range by 1000 m"},
        { type: 'trange', cost: 150, title: 'Upgrade Tower Range', flex: 4, imagePath: require('@/assets/trange.png'), info: "Extends the Range of all your Towers by 1000 m" },
      ]
    }
  },
  methods: {
    async buyItem(itemType) {
      var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]

      switch(itemType) {
      case 'tower':
        this.itemBought = itemType
        var itemPrice = 50
        if (myAttributes.koins >= itemPrice) {
          myAttributes.koins = parseInt(myAttributes.koins) - itemPrice
          myAttributes.towers = parseInt(myAttributes.towers) + 1

          UserAttributesService.updateUserAttributes(
            {
            'koins': myAttributes.koins,
            'towers': myAttributes.towers,
            },
            myAttributes.id, 
          )
          this.itemBoughtSuccess = true
        } else {
          this.itemBoughtError = true
        }
        break;

      case 'landmark':
        this.itemBought = itemType
        var itemPrice = 500
        if (myAttributes.koins >= itemPrice) {
          myAttributes.koins = parseInt(myAttributes.koins) - itemPrice
          myAttributes.landmarks = parseInt(myAttributes.landmarks) + 1

          UserAttributesService.updateUserAttributes(
            {
            'koins': myAttributes.koins,
            'landmarks': myAttributes.landmarks,
            },
            myAttributes.id,
          )
          this.itemBoughtSuccess = true
        } else {
          this.itemBoughtError = true
        }
        break;

      case 'vrange':
        this.itemBought = 'Sight Range upgrade'
        if (myAttributes.koins >= 150) {
          myAttributes.koins = parseInt(myAttributes.koins) - 150
          myAttributes.sight_range = parseInt(myAttributes.sight_range) + 1000

          UserAttributesService.updateUserAttributes(
            {
            'koins': myAttributes.koins,
            'sight_range': myAttributes.sight_range,
            },
            myAttributes.id,
          )
          this.itemBoughtSuccess = true
        } else {
          this.itemBoughtError = true
        }
        break;

      case 'trange':
          this.itemBought = 'Tower Range upgrade'
          if (myAttributes.koins >= 150) {
          myAttributes.koins = parseInt(myAttributes.koins) - 150
          myAttributes.tower_range = parseInt(myAttributes.tower_range) + 1000

          UserAttributesService.updateUserAttributes(
            {
            'koins': myAttributes.koins,
            'tower_range': myAttributes.tower_range,
            },
            myAttributes.id,
          )
          this.itemBoughtSuccess = true
        } else {
          this.itemBoughtError = true
        }
        break;

      default:
          console.log('buying something else')
      }
      setTimeout(function () {
        this.itemBoughtSuccess = false
        this.itemBoughtError = false
      }, 2000);
    },
    async giveInfo(itemType, inCard) {
      var selectedCard = inCard
      console.log('info for: ' + itemType)
      this.showInfo = selectedCard.info
      this.showInfoBox = true
      this.showInfoImage = selectedCard.imagePath
    }
  },

  // This Code is executed when the Market component is mounted
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

#market {
  position: absolute;
  top: 66px;
  bottom: 0;
  right: 0;
  left: 0;
  width: 100%;
}

.card__media__background {
  background-size: auto 100%;
}

.background{
  color: white;
}

.errorClass {
  z-index: 2000 !important;
  top: 66px;
  width: 90%;
  position: fixed;
}

</style>
