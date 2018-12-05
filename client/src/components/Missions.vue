<template>
  <div id="missions">
    <v-layout row justify-center>
      <v-dialog v-model="buildLandmarkDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Confirm Placement</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <span>Are you sure you want to permanently place a Landmark here?</span> <br> <br>
            {{newLandmarkLat}}, {{newLandmarkLng}}
            <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="red" flat @click.stop="buildLandmarkDialog=false">Cancel</v-btn>
            <v-btn color="primary" class="light-green" flat @click="placeLandmark">Confirm</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="buildTowerDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Confirm Placement</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <span>Are you sure you want to permanently place a Tower here?</span> <br> <br>
            {{newTowerLat}}, {{newTowerLng}}
            <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="red" flat @click.stop="buildTowerDialog=false">Cancel</v-btn>
            <v-btn color="primary" class="light-green" flat @click="placeTower">Confirm</v-btn>
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
            <span>You selected the following Mission: </span> <br>
            <strong> {{missionType}} </strong> <br> <br>
            <span>This Mission is {{missionDifficulty}} </span>
            <v-spacer></v-spacer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="missionBriefing=false">Not now</v-btn>
            <v-spacer></v-spacer>
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
            <div v-if="missionPossibleAnswers == 0">
              <v-text-field label="Your answer" outline v-model="missionAnswer"></v-text-field>
            </div>
            <div v-if="missionPossibleAnswers.length > 0">
              <v-select
                :items="missionPossibleAnswers"
                label="Choose from..."
                v-model="missionAnswer"
              ></v-select>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="submitMissionDialog=false">Close</v-btn>
            <v-spacer></v-spacer>
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
            <v-spacer></v-spacer>
            <v-btn color="primary" dark class="light-green" flat @click="closeReward">Ok</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
    <div id='map'>
      
    </div>
    <v-alert class="errorClass"
        v-model="LocationError"
        type="error"
        dismissible
      >
        Error getting location. Please allow location service.
      </v-alert>
      <v-alert class="errorClass"
        v-model="LoginError"
        type="error"
        dismissible
      >
        Error getting Account Data. Please Login or Sign up first
      </v-alert>
  </div>
</template>

<script>
import UserAttributesService from '@/services/UserAttributesService'
import MissionService from '@/services/MissionService'
import TowerService from '@/services/TowerService'
import LandmarkService from '@/services/LandmarkService'

const startPoint = [47.233498, 8.736205];
const attributionForMap = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &vert; <a href="https://github.com/CartoDB/CartoDB-basemaps/blob/master/LICENSE.txt">Map CC-BY</a> &vert; <a href="https://opendatacommons.org/licenses/odbl/">Data ODbL </a> &vert; v1'
const tileLayerURL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"


var geolocationOptions = {
  enableHighAccuracy: false,
  timeout: 5000,
  maximumAge: 0
};

// Mission Briefing and solving Mission
var currentMissionDetails = ''
var newTower
var newLandmark
var myAttributes

export default {
  data() {
    return {
      // Leaflet map images
      towerImage: require('@/assets/tower.png'),
      landmarkImage: require('@/assets/landmark.png'),

      // Location Error
      LocationError: false,
      // Login Error
      LoginError: false,

      // Mission Dialog Boxes
      submitMissionDialog: false,
      missionBriefing: false,
      missionRewardDialog: false,
      buildTowerDialog: false,
      buildLandmarkDialog: false,

      newTowerLat: 0,
      newTowerLng: 0,

      newLandmarkLat: 0,
      newLandmarkLng: 0,
      
      missionQuestion: '',
      missionType: '',
      missionPossibleAnswers: '',
      missionOsmID: '',
      missionDifficulty: '',

      missionKoinReward: 20,
      missionExperienceReward: 10,

      missionAnswer: "",
      title: 'KortMissionMap',
      zoom: 13,
      center: [51.505, -0.09],

      saveDialog: false,
      updateDialogBox: false,
      notifications: false,
      sound: true,
      widgets: false,
    }
  },
  methods: {
    // This Function sends a created Landmark to the backend, updates the UserAttributes and redraws all Landmarks
    async placeLandmark() {
      myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
      
      // Create the tower on the backend
      LandmarkService.newLandmark(newLandmark)

      // Update the UserAttributes
      myAttributes.landmarks = parseInt(myAttributes.landmarks) - 1
      UserAttributesService.updateUserAttributes(
        {
        'landmarks': myAttributes.landmarks,
        },
        myAttributes.id,
      )
      this.buildLandmarkDialog = false
      var self = this
      self.$emit("reloadLandmarks");
    },
    // This Function sends a created tower to the backend, updates the UserAttributes and redraws all missions from all towers
    async placeTower() {
      
      myAttributes = (await UserAttributesService.getUserAttributes()).data[0]

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
      var self = this
      self.$emit("reloadTowers");
    },
    // This Function closes the Mission Briefing and opens the Mission Dialog
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
        self.$emit("updateSolvedMissions");
        this.missionRewardDialog = true;
        self.$emit("reloadTowers");
        self.$emit("reloadNearbyMissions");
      });
    },
    // This Function closes the reward dialog box that opens after solving a mission
    async closeReward() {
      var self = this;
      this.missionRewardDialog = false
      this.missionOsmID = ''
      this.missionAnswer = ''
      
      //get current Attributes from profile
      myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
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
    var mySolvedMissions
    // make closure of "this"
    var self = this;
    
    console.log('get Attributes if logged in...')
    if (this.$store.state.isUserLoggedIn) {
      console.log('Player is logged in')
      myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
      console.log(myAttributes)
    } else {
      console.log('Player is not logged in')
      self.LoginError=true
    }

    //Show my location on map
    var currentLatitude
    var currentLongitude

    var CircleGroup = L.layerGroup();
    var currentLocationGroup = L.layerGroup();
    var TowerMissionGroup = L.layerGroup();
    var LeafletTowersIconsGroup = L.layerGroup();
    var LeafletLandmarksIconsGroup = L.layerGroup();

    navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions);
    
    async function geoLocationSuccess(pos) {
      var crd = pos.coords;

      //Draws the circle
      CircleGroup.clearLayers();
      L.circleMarker([crd.latitude, crd.longitude], crd.accuracy, {color:'white',opacity:0,fillColor: 'blue',fillOpacity:.15}).addTo(CircleGroup);
      L.circleMarker([crd.latitude, crd.longitude], 10, {color:'white',opacity:1,fillColor: 'blue',fillOpacity:.7}).addTo(CircleGroup);
      CircleGroup.addTo(map)

      currentLatitude = crd.latitude
      currentLongitude = crd.longitude

      setTimeout(function(){ navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions); }, 10000);
      getNearbyMissions()
    }  

    function geoLocationError(err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
      setTimeout(function(){ navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions); }, 10000);
      console.log("gettingLocationError");
      self.LocationError = true
    }

    // init the map object
    var map = L.map('map', {attributionControl: false}).setView(startPoint, 15),
      tilelayer = L.tileLayer(tileLayerURL, {
        attribution: attributionForMap,
        minZoom: 8,
        maxZoom: 18,
        ext: 'png',
      }).addTo(map);

    // remove the "Leaflet" attribution prefix
    var myAttribution = L.control.attribution({prefix: '', position: 'bottomright'}).addTo(map);

    // test draw landmark
    /*
    placeLandmarkIconOnMap(47.2499721, 8.699938399999999, test)
    */

    // This function draws a Landmark on the LeafletLandmarksIconsGroup
    async function placeLandmarkIconOnMap(inLat, inLon, inLabel) {
      var landmarkLat = inLat
      var landmarkLon = inLon
      var landmarkLabel = inLabel
      var landmarkIcon = L.icon({
          iconUrl:      self.landmarkImage,
          iconSize:     [38, 42], // size of the icon
          iconAnchor:   [19, 21], // point of the icon which will correspond to marker's location
          shadowAnchor: [4, 62],  // the same for the shadow
          popupAnchor:  [19, -20] // point from which the popup should open relative to the iconAnchor
      });
      //L.marker([towerLat, towerLon], {icon: landmarkIcon}).addTo(LeafletLandmarksIconsGroup);
      L.marker([landmarkLat, landmarkLon], {icon: landmarkIcon, name:landmarkLabel}).addTo(map).on('click', clickedLandmark).bindTooltip(landmarkLabel, {direction:'top', permanent:true, offset:[0,-20] }).openTooltip();
    }

    // This function draws a tower on the LeafletTowersIconsGroup
    async function placeTowerIconOnMap(inLat, inLon) {
      var towerLat = inLat
      var towerLon = inLon
      var towerIcon = L.icon({
          iconUrl:      self.towerImage,
          iconSize:     [18, 30], // size of the icon
          iconAnchor:   [9, 15], // point of the icon which will correspond to marker's location
          shadowAnchor: [4, 62],  // the same for the shadow
          popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
      });
      L.marker([towerLat, towerLon], {icon: towerIcon}).addTo(LeafletTowersIconsGroup);
    }

    // Geolocation and Marker 
    // Here the browser attempts to return a geolocation and asks the user for permission
    map.locate({setView: true, maxZoom: 15, enableHighAccuracy:false, timeout:5000, maximumAge:0});

    // Get all my previously solved Missions
    mySolvedMissions = await getMySolvedMissions()

    // This function updates the List of solved Missions via the eventhub
    this.$on("updateSolvedMissions", async function(){
      mySolvedMissions = await getMySolvedMissions()
    })
    
    // This function retrieves the list of all previously solved Missions by this User from the backend Server
    async function getMySolvedMissions() {
      let myMissions = await MissionService.getSolvedMissions()
      return myMissions.data
    }

    // This function adds all nearby Missions to the map via the eventhub
    this.$on("reloadNearbyMissions", async function(){
      getNearbyMissions()
    })
    
    // Add Missions from current location
    async function getNearbyMissions() {
      var range = 5000
      if (self.$store.state.isUserLoggedIn) {
        //myAttributes = (await UserAttributesService.getUserAttributes()).data[0]
        console.log(myAttributes)
        range = parseInt(myAttributes.sight_range)
      }
      self.$http.get('/api_kort/v1.0/missions?user_id=-1&lat='+currentLatitude+'&lon='+currentLongitude+'&radius='+range+'&limit=100&lang=en', {foo: 'bar'}).then(response => {

      // get status
      response.status;

      // get status text
      response.statusText;

      // get 'Expires' header
      response.headers.get('Expires');

      // get body data
      self.someData = response.body;

      // Draw all nearby Missions from response
      currentLocationGroup.clearLayers();
      self.someData.forEach(k => {
        if (k.error_type  && !checkMissionSolvedStatus(mySolvedMissions, k.osmId)) {
          // Default color blue (unrecognized mission type)
          // Mission Mapping (Difficulty)
          let difficulty = 'medium'
          let strokecolor =  'blue'
          if (k.error_type == "missing_track_type") {
            strokecolor = 'yellow'
            difficulty = 'medium'
          }
          if (k.error_type == "missing_maxspeed") {
            strokecolor = 'orange'
            difficulty = 'medium'
          }
          if (k.error_type == "poi_name") {
            strokecolor = 'OrangeRed'
            difficulty = 'hard'
          }
          if (k.error_type == "language_unknown") {
            strokecolor = 'green'
            difficulty = 'easy'
          }
          if (k.error_type == "religion") {
            strokecolor = 'Chartreuse'
            difficulty = 'easy'
          }

          L.circleMarker([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 6, color:strokecolor, k, difficulty}).addTo(currentLocationGroup).on('click', clickedMission);
        }
      });
      currentLocationGroup.addTo(map)

    }, response => {
      console.log("getting missions failed")
    });

    }

    // This function is triggered when a Player has clicked a Landmark
    function clickedLandmark(e) {
      console.log('you clicked landmark of: ' + this.options.name)
    }

    // This function is triggered when a Player has clicked a mission
    function clickedMission(e) { 
      if (!self.$store.state.isUserLoggedIn) {
        self.LoginError=true
      } else {
        self.submitMissionDialog = false
        self.missionBriefing = true

        currentMissionDetails = this.options.k
        self.missionType = currentMissionDetails.title
        self.missionQuestion = currentMissionDetails.question
        self.missionPossibleAnswers = currentMissionDetails.inputType.options
        self.missionOsmID = currentMissionDetails.osmId
        
        self.missionDifficulty = this.options.difficulty

        // Todo:
        // mission reward adjustements for difficulty and current level here
        // get Player Level, make adjustements
      }
    }

    // Show "place tower" button on map if any towers are available and user is logged in
    if (self.$store.state.isUserLoggedIn) {
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
                  container.style.display = 'none';
                }
              });
            container.style.display = 'block';
            return container;
          }
        });
        map.addControl(new L.NewPolygonControl());
      }
    }
    // Show "place landmark" button on map if any landmarks are available and user is logged in
    if (self.$store.state.isUserLoggedIn) {
      if (myAttributes.landmarks >= 1) {
        L.NewPolygonControl = L.Control.extend({
          options: {
            position: 'bottomleft'
          },
          onAdd: function(map) {
            var container = L.DomUtil.create('div', 'leaflet-control leaflet-bar'),
              link = L.DomUtil.create('a', '', container);
            link.href = '#';
            link.title = 'Place Landmark';
            link.innerHTML = 'LMK';
            L.DomEvent.on(link, 'click', L.DomEvent.stop)
              .on(link, 'click', function() {
                if (myAttributes.landmarks >= 1) {
                  console.log('placing landmark now...')
                  console.log(map.getCenter())
                  newLandmark = {
                    'location': [map.getCenter().lat, map.getCenter().lng],
                    'label': self.$store.state.user,
                    'owner': self.$store.state.user,
                  }
                  // open the Dialogbox before placeing a new tower
                  self.newLandmarkLat = map.getCenter().lat
                  self.newLandmarkLng = map.getCenter().lng
                  self.buildLandmarkDialog = true
                } else {
                  console.log('no towers available...')
                  container.style.display = 'none';
                }
              });
            container.style.display = 'block';
            return container;
          }
        });
        map.addControl(new L.NewPolygonControl());
      }
    }

    // initially draw all available towers
    getAllTowers()

    // This function is called when the eventhub emits the reloadTowers event
    this.$on("reloadTowers", function(){
      getAllTowers();
    })
    
    // This Function retrieves and adds all Missions from all Towers to the map
    async function getAllTowers() {
      var allTowers = await TowerService.getMyTowers()

      TowerMissionGroup.clearLayers();
      LeafletTowersIconsGroup.clearLayers()
      allTowers.data.forEach(t=> {
        if (t.location.length > 0) {
          getMissionsFromTower(t.location[0], t.location[1])
          placeTowerIconOnMap(t.location[0], t.location[1])
        }
      })
      TowerMissionGroup.addTo(map)
      LeafletTowersIconsGroup.addTo(map)
    }

    // initially draw all available landmarks
    getAllLandmarks()

    // This function is called when the eventhub emits the reloadLandmarks event
    this.$on("reloadLandmarks", function(){
      getAllLandmarks();
    })
    
    // This Function retrieves and adds all Missions from all Towers to the map
    async function getAllLandmarks() {
      var allLandmarks = await LandmarkService.getAllLandmarks()

      LeafletLandmarksIconsGroup.clearLayers()
      allLandmarks.data.forEach(t=> {
        if (t.location.length > 0) {
          placeLandmarkIconOnMap(t.location[0], t.location[1], t.label)
        }
      })
      LeafletLandmarksIconsGroup.addTo(map)
    }

    // helper function to check if a mission (osmID) is already solved
    function checkMissionSolvedStatus(arr, val) {
      return arr.some(function(arrVal) {
        return val.toString() === arrVal.osmID;
      });
    }

    // Add Missions from a Tower
    async function getMissionsFromTower(towerLat, towerLng) {
      var range = parseInt(myAttributes.tower_range)
      self.$http.get('/api_kort/v1.0/missions?user_id=-1&lat='+towerLat+'&lon='+towerLng+'&radius='+range+'&limit=100&lang=en', {foo: 'bar'}).then(response => {

      // get status
      response.status;
      // get status text
      response.statusText;
      // get 'Expires' header
      response.headers.get('Expires');
      // get body data
      self.someData = response.body;

      //Add all Missions from response to layerGroup TowerMissionGroup
      self.someData.forEach(k => {
        if (k.error_type && !checkMissionSolvedStatus(mySolvedMissions, k.osmId)) {
          //Default color blue
          //Mission Mapping (Difficulty)
          let difficulty = 'medium'
          let strokecolor =  'blue'
          if (k.error_type == "missing_track_type") {
            strokecolor = 'yellow'
            difficulty = 'medium'
          }
          if (k.error_type == "missing_maxspeed") {
            strokecolor = 'orange'
            difficulty = 'medium'
          }
          if (k.error_type == "poi_name") {
            strokecolor = 'OrangeRed'
            difficulty = 'hard'
          }
          if (k.error_type == "language_unknown") {
            strokecolor = 'green'
            difficulty = 'easy'
          }
          if (k.error_type == "religion") {
            strokecolor = 'Chartreuse'
            difficulty = 'easy'
          }
          L.circleMarker([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 6, color:strokecolor, k, difficulty}).addTo(TowerMissionGroup).on('click', clickedMission);
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
  top: 66px;
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

div.overlay--active {
  z-index: 1000 !important
}

div.dialog__content__active {
  z-index: 1000 !important
}

div.errorClass {
  z-index: 2000 !important
}

</style>
