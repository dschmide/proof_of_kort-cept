<template>
  <div id="app">
    <v-layout row justify-center>
      <v-dialog v-model="saveDialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Create new Userarea</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <v-text-field label="Label" type="text" v-model="userAreaLabel"></v-text-field>
            Public Area:
            <input type="checkbox" id="checkbox" v-model="checked">
            <label for="checkbox"> {{ checked }}</label>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="saveDialog=false">Close</v-btn>
            <v-btn color="primary" dark class="light-green" flat @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="updateDialogBox" max-width="500px">
        <v-card>
          <v-card-title>
            <span>Update existing Userarea</span>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-card-text>
            <v-text-field label="Label" type="text" v-model="userAreaLabel"></v-text-field>
            Public Area:
            <input type="checkbox" id="checkbox" v-model="checked">
            <label for="checkbox"> {{ checked }}</label>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" flat @click.stop="updateDialogBox=false">Close</v-btn>
            <v-btn color="primary" dark class="light-green" flat @click="update">Update</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
    <div id='map'>
    </div>
  </div>
</template>
<script>
import AreaService from '@/services/AreaService'

const startPoint = [47.233498, 8.736205];
const attributionForMap = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &vert; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &vert; <a href="https://maps.zh.ch">maps.zh.ch</a>'
const tileLayerURL = 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}'


var geolocationOptions = {
  enableHighAccuracy: false,
  timeout: 60000,
  maximumAge: 5000
};

var myGeoJsonPoly = [];
var myCoords
var PolyCoordinates
var currentIdOfPolygon

var AllUserAreas = []

var DisplayForestLink



export default {
  data() {
    return {
      checked: false,
      userAreaLabel: "",
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
    // This Function sends a drawn polygon to the server and closes the save dialog
    save() {
      var theArea = {
        "label": this.userAreaLabel,
        "public": !!this.checked,
        "polygon": {
          "type": "MultiPolygon",
          "coordinates": [
            [myGeoJsonPoly]
          ]
        }
      }
      var self = this;
      AreaService.postArea(theArea)
      .then( (response) => {
        this.saveDialog = false;
        self.$emit("redrawMap");
      });
      myGeoJsonPoly = [];
    },
  },

  // This code is executed when the Missions.vue is mounted on the page
  async mounted() {
    //Show my location on map
    //todo setinterval
    var currentLatitude
    var currentLongitude

    var CircleGroup = L.layerGroup();
    var RestaurantGroup = L.layerGroup();
    var currentLocationGroup = L.layerGroup();
    navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions);
    
    async function geoLocationSuccess(pos) {
      var crd = pos.coords;
      console.log('Your current position is:');
      console.log(`Latitude : ${crd.latitude}`);
      console.log(`Longitude: ${crd.longitude}`);
      console.log(`More or less ${crd.accuracy} meters.`);

      //Draws the circle
      CircleGroup.clearLayers();
      L.circle([crd.latitude, crd.longitude], crd.accuracy, {color:'white',opacity:0,fillColor: 'blue',fillOpacity:.15}).addTo(CircleGroup);
      L.circle([crd.latitude, crd.longitude], 10, {color:'white',opacity:1,fillColor: 'blue',fillOpacity:.7}).addTo(CircleGroup);
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
    
    async function getNearbyMissions() {
      console.log("making Missions request for current proximity")
      console.log(currentLatitude)
      console.log(currentLongitude)

      self.$http.get('https://kort.dev.ifs.hsr.ch/v1.0/missions?user_id=-1&lat='+currentLatitude+'&lon='+currentLongitude+'&radius=5000&limit=100&lang=en', {foo: 'bar'}).then(response => {

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
          console.log(k.error_type)
          console.log(k.annotationCoordinate[0])
          console.log(k.annotationCoordinate[1])  
          
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

          L.circle([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 10, color:strokecolor, k}).addTo(currentLocationGroup).on('mousedown', clickedMission);
          console.log("drawn nearby mission")
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
      console.log(this.options.k.osmId)
    }

    //Get missions of example Tower (fixed location)
    this.$http.get('https://kort.dev.ifs.hsr.ch/v1.0/missions?user_id=-1&lat=47.223410&lon=8.818158&radius=5000&limit=100&lang=en', {foo: 'bar'}).then(response => {

      // get status
      response.status;

      // get status text
      response.statusText;

      // get 'Expires' header
      response.headers.get('Expires');

      // get body data
      this.someData = response.body;
      console.log(this.someData)

      //Draw all Restaurants from response
      RestaurantGroup.clearLayers();
      this.someData.forEach(k => {
        if (k.error_type /*== 'missing_cuisine'*/) {
          console.log(k.error_type)
          console.log(k.annotationCoordinate[0])
          console.log(k.annotationCoordinate[1])  
          
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

          L.circle([k.annotationCoordinate[0], k.annotationCoordinate[1]], {radius: 10, color:strokecolor}).addTo(RestaurantGroup);
          console.log("drawn mission")
        }
      });
      RestaurantGroup.addTo(map)

    }, response => {
      console.log("getting missions failed")
    });
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
