<template>
  <v-layout column>
    <v-flex md6 offset-md3 xs12>
      <div class="white elevation-2">
        <v-toolbar flar dense class="light-blue" dark>
        <v-toolbar-title>Market</v-toolbar-title>
        </v-toolbar>
        <div class="pl-4 pr-4 pt-2 pb-2">
          <div>
            <h3 class="headline mb-0">Market</h3>
            <div>In the Market, players may exchange their Koins for in-game Resources or Attributes
            </div>
          </div>
        </div>
      
      <v-card>
        <v-container
          fluid
          grid-list-md
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
                  >
                    <v-layout fill-height>
                      <v-flex xs12 align-end flexbox>
                        <span class="headline black--text" v-text="card.title"></span>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  {{card.cost}} Koins
                  <v-spacer></v-spacer>
                  <v-btn icon @click.stop="buyItem(card.type)">
                    <v-icon>add_circle</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
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

      currentExperiencePercent: 0,
      currentLevel: 1,

      cards: [
        { type: 'tower', cost: 50, title: 'Tower', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
        { type: 'arc', cost: 500, title: 'Arc', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
        { type: 'vrange', cost: 150, title: 'Vision Range upgrade', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
        { type: 'trange', cost: 150, title: 'Tower Range upgrade', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
      ]
    }
  },
  methods: {
    async buyItem(itemType) {
      var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]

      switch(itemType) {
      case 'tower':
          console.log('buying a tower...')
          if (myAttributes.koins >= 50) {
            myAttributes.koins = parseInt(myAttributes.koins) - 50
            myAttributes.towers = parseInt(myAttributes.towers) + 1

            UserAttributesService.updateUserAttributes(
              {
              'koins': myAttributes.koins,
              'towers': myAttributes.towers,
              },
              myAttributes.id,
            )
          } else {
            console.log("warning, you can't afford this item")
          }
          break;

      case 'arc':
          console.log('buying arc...')
          break;

      default:
          console.log('buying something else')
      }
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

.card__media__background {
  background-size: auto 100%;
}

.error{
   color:red;
 }

</style>
