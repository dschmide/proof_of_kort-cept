<template>
  <div id="app">
    <v-layout row justify-center>
      <v-dialog v-model="buildTowerDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Confirm Placement</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <span>Are you sure you want to place a tower here?</span>
            {{newTowerLat}}, {{newTowerLng}}
            <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="red" flat @click.stop="buildTowerDialog=false">Cancel</v-btn>
            <v-btn color="primary" class="light-green" @click="placeTower">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="missionBriefing" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Mission Briefing</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <span>You selected the following Mission: </span>
            {{missionType}}
            <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="missionBriefing=false">Not now</v-btn>
            <v-btn color="primary" dark class="light-green" flat @click.stop="openMission">Solve!</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="submitMissionDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Solve this Mission</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            {{missionQuestion}}
            <v-text-field label="Your answer" outline v-model="missionAnswer"></v-text-field>
            {{missionDescription}}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="submitMissionDialog=false">Close</v-btn>
            <v-btn color="primary" dark class="light-green" flat @click="submitMission">Submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="missionRewardDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Mission Reward</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            Thank you for solving this mission!
            You have been rewarded with: <br> <br>
            + {{missionKoinReward}} Koins <br>
            + {{missionExperienceReward}} Experience <br>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" dark class="light-green" flat @click="closeReward">Ok</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
    <div id='map'>
    </div>
  </div>
</template>
<script>
import UserAttributesService from '@/services/UserAttributesService'
import MissionService from '@/services/MissionService'
import TowerService from '@/services/TowerService'


const startPoint = [47.233498, 8.736205];
const attributionForMap = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
const tileLayerURL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"


var geolocationOptions = {
  enableHighAccuracy: false,
  timeout: 60000,
  maximumAge: 5000
};

// Mission Briefing and solving Mission
var currentMissionDetails = ''
var newTower


export default {
  data() {
    return {
      // Mission Dialog Boxes
      submitMissionDialog: false,
      missionBriefing: false,
      missionRewardDialog: false,
      buildTowerDialog: false,

      newTowerLat: 0,
      newTowerLng: 0,
      
      missionQuestion: '',
      missionType: '',
      missionDescription: '',
      missionOsmID: '',

      missionKoinReward: 20,
      missionExperienceReward: 10,

      missionAnswer: "",
      title: 'KortMissionMap',
      zoom: 13,
      center: [51.505, -0.09],
      url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",

      saveDialog: false,
      updateDialogBox: false,
      notifications: false,
      sound: true,
      widgets: false,
    }
  },
  methods: {
    // This Function sends a created tower to the backend and updates the UserAttributes
    async placeTower() {
      var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]

      console.log('method placeTower')
      // Create the tower on the backend
      TowerService.newTower(newTower)

      // Update the UserAttributes
      myAttributes.towers = parseInt(myAttributes.towers) - 1
      UserAttributesService.updateUserAttributes(
        {
        'towers': myAttributes.towers,
        },
        myAttributes.id,
      )
      this.buildTowerDialog = false 
    },
    // This Function submits a solved Mission to the server and closes the Mission dialog
    openMission() {
      this.missionBriefing = false
      this.submitMissionDialog = true
    },
    // This Function submits a solved Mission to the server and closes the Mission dialog
    submitMission() {
      var solvedMission = {
        "answer": this.missionAnswer,
        "osmID": this.missionOsmID,
        "solved_by": this.$store.state.user,
        "timestamp": Math.floor(new Date().getTime() / 1000)
      }
      var self = this;
      MissionService.postMission(solvedMission)
      .then( (response) => {
        this.submitMissionDialog = false;
        self.$emit("redrawMap");
        this.missionRewardDialog = true;
      });
    },
    // This Function closes the reward dialog box that opens after solving a mission
    async closeReward() {
      var self = this;
      this.missionRewardDialog = false
      this.missionOsmID = ''
      this.missionAnswer = ''

      //get current Attributes from profile
      var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
      myAttributes.experience = parseInt(myAttributes.experience) + parseInt(this.missionExperienceReward)
      myAttributes.koins = parseInt(myAttributes.koins) + parseInt(this.missionKoinReward)

      UserAttributesService.updateUserAttributes(
        {
        'koins': myAttributes.koins,
        'experience': myAttributes.experience,
        'towers': myAttributes.towers,
        },
        myAttributes.id,
      )
    },
  },

  // This code is executed when the Missions.vue is mounted on the page
  async mounted() {
    //Show my location on map
    var currentLatitude
    var currentLongitude

    var CircleGroup = L.layerGroup();
    var RestaurantGroup = L.layerGroup();
    var currentLocationGroup = L.layerGroup();
    var TowerMissionGroup = L.layerGroup();

    navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions);
    
    async function geoLocationSuccess(pos) {
      var crd = pos.coords;
      console.log('Your current position is:');
      console.log(`Latitude : ${crd.latitude}`);
      console.log(`Longitude: ${crd.longitude}`);
      console.log(`More or less ${crd.accuracy} meters.`);
      console.log('map center is:')
      console.log(map.getCenter())

      //Draws the circle
      CircleGroup.clearLayers();
      L.circleMarker([crd.latitude, crd.longitude], crd.accuracy, {color:'white',opacity:0,fillColor: 'blue',fillOpacity:.15}).addTo(CircleGroup);
      L.circleMarker([crd.latitude, crd.longitude], 10, {color:'white',opacity:1,fillColor: 'blue',fillOpacity:.7}).addTo(CircleGroup);
      CircleGroup.addTo(map)

      currentLatitude = crd.latitude
      currentLongitude = crd.longitude

      setTimeout(function(){ navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions); }, 5000);
      getNearbyMissions()
    }  

    function geoLocationError(err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
      setTimeout(function(){ navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions); }, 5000);
      console.log("gettingLocationError");
    }


    // init the map object
    var map = L.map('map', { editable: true }).setView(startPoint, 15),
      tilelayer = L.tileLayer(tileLayerURL, {
        attribution: attributionForMap,
        subdomains: 'abcd',
        minZoom: 0,
        maxZoom: 18,
        ext: 'png'
      }).addTo(map);

    //Geolocation and Marker 
    //Here the browser attempts to return a geolocation and asks the user for permission
    map.locate({setView: true, maxZoom: 15, enableHighAccuracy:false, timeout:60000, maximumAge:Infinity});

    // make closure of "this"
    var self = this;
    
    // Add Missions from current location
    async function getNearbyMissions() {
      self.$http.get('/api_kort/v1.0/missions?user_id=-1&lat='+currentLatitude+'&lon='+currentLongitude+'&radius=5000&limit=100&lang=en', {foo: 'bar'}).then(response => {

      // get status
      response.status;

      // get status text
      response.statusText;

      // get 'Expires' header
      response.headers.get('Expires');

      // get body data
      self.someData = response.body;
      console.log(self.someData)

      //Draw all nearby Missions from response
      currentLocationGroup.clearLayers();
      self.someData.forEach(k => {
        if (k.error_type /*== 'missing_cuisine'*/) {

          //Default color blue
          //Sample missions
          let strokecolor =  'blue'
          if (k.error_type == "missing_track_type") {
            strokecolor = 'yellow'
          }
          if (k.error_type == "missing_maxspeed") {
            strokecolor = 'red'
          }
          if (k.error_type == "poi_name") {
            strokecolor = 'green'
          }
          if (k.error_type == "language_unknown") {
            strokecolor = 'orange'
          }

          L.circleMarker([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 6, color:strokecolor, k}).addTo(currentLocationGroup).on('click', clickedMission);
        }
      });
      currentLocationGroup.addTo(map)

    }, response => {
      console.log("getting missions failed")
    });

    }

    function clickedMission(e)
    {
      console.log("hi. you clicked the mission at" + this.getLatLng());
      console.log(this.options.k)
      self.submitMissionDialog = false
      self.missionBriefing = true
      console.log(self.missionBriefing, self.submitMissionDialog)

      currentMissionDetails = this.options.k
      self.missionType = currentMissionDetails.title
      self.missionQuestion = currentMissionDetails.question
      self.missionDescription = currentMissionDetails.inputType.options
      self.missionOsmID = currentMissionDetails.osmId
    }

    //Show "place tower" button on map if any towers are available
    var myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
    if (myAttributes.towers >= 1) {
      L.NewPolygonControl = L.Control.extend({
        options: {
          position: 'bottomleft'
        },
        onAdd: function(map) {
          var container = L.DomUtil.create('div', 'leaflet-control leaflet-bar'),
            link = L.DomUtil.create('a', '', container);
          link.href = '#';
          link.title = 'Place Tower';
          link.innerHTML = 'Tower';
          L.DomEvent.on(link, 'click', L.DomEvent.stop)
            .on(link, 'click', function() {
              if (myAttributes.towers >= 1) {
                console.log('placing tower now...')
                console.log(map.getCenter())
                newTower = {
                  'location': [map.getCenter().lat, map.getCenter().lng]
                }
                // open the Dialogbox before placeing a new tower
                self.newTowerLat = map.getCenter().lat
                self.newTowerLng = map.getCenter().lng
                self.buildTowerDialog = true
              } else {
                console.log('no towers available...')
              }
            });
          container.style.display = 'block';
          return container;
        }
      });
      map.addControl(new L.NewPolygonControl());
    }

    getAllTowers()

    async function getAllTowers() {
      var allTowers = await TowerService.getMyTowers()
      console.log('logging all towers')
      console.log(allTowers.data)

      TowerMissionGroup.clearLayers();
      allTowers.data.forEach(t=> {
        if (t.location.length > 0) {
          console.log(t.location)
          getMissionsFromTower(t.location[0], t.location[1])
        }
      })
      TowerMissionGroup.addTo(map)
    }

    // Add Missions from a Tower
    async function getMissionsFromTower(towerLat, towerLng) {
      self.$http.get('/api_kort/v1.0/missions?user_id=-1&lat='+towerLat+'&lon='+towerLng+'&radius=5000&limit=100&lang=en', {foo: 'bar'}).then(response => {

      // get status
      response.status;

      // get status text
      response.statusText;

      // get 'Expires' header
      response.headers.get('Expires');

      // get body data
      self.someData = response.body;
      console.log(self.someData)

      //Add all Missions from response to layerGroup
      self.someData.forEach(k => {
        if (k.error_type /*== 'missing_cuisine'*/) {

          //Default color blue
          //Sample missions
          let strokecolor =  'blue'
          if (k.error_type == "missing_track_type") {
            strokecolor = 'yellow'
          }
          if (k.error_type == "missing_maxspeed") {
            strokecolor = 'red'
          }
          if (k.error_type == "poi_name") {
            strokecolor = 'green'
          }
          if (k.error_type == "language_unknown") {
            strokecolor = 'orange'
          }

          L.circleMarker([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 6, color:strokecolor, k}).addTo(TowerMissionGroup).on('click', clickedMission);
        }
      });
    }, response => {
      console.log("getting missions failed")
    });

    }
    
  }

}

</script>
<style type='text/css'>
body {
  margin: 0;
  padding: 0;
}

#map {
  position: absolute;
  top: 56px;
  bottom: 0;
  right: 0;
  left: 0;
  width: 100%;
}

.leaflet-sidebar>.leaflet-control {
  overflow-y: hidden;
}

.propertyLabel {
  color: white;
  text-shadow: 2px 2px 2px black;
  opacity: 1;
}

.cssPolygon{
  color:green;
}
.AreaLabelPublic {
  color: green;
  text-shadow: 2px 2px 2px black;
  opacity: 1;
}

.AreaLabelPrivate {
  color: yellow;
  text-shadow: 2px 2px 2px black;
  opacity: 1;
}

div.overlay--active {
  z-index: 1000 !important
}

div.dialog__content__active {
  z-index: 1000 !important
}

</style>
