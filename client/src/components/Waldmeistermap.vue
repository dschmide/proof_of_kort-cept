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
import Vegetation from '@/components/data/vegetationskarte_minimal.json'

const startPoint = [47.233498, 8.736205];
const attributionForMap = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &vert; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &vert; <a href="https://maps.zh.ch">maps.zh.ch</a>'
const tileLayerURL = 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}'

const PolygonButtonTextIdle = 'Add'
const PolygonButtonTextEditing = 'Edit'
const ToggleVegetationButtonLabel= 'Veg'
const ToggleUserAreasLabel = "UAs"

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
      vegetation: Vegetation,
      title: 'WaldmeisterMap',
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

  // This code is executed when the Waldmeistermap.vue is mounted on the page
  async mounted() {
    //Show my location on map
    //todo setinterval
    var CircleGroup = L.layerGroup();
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

      // determine if in vegetation polygon
      //var SuccessPolygon = (await getInPolygon(47.21490162751083, 8.691289296839386));
      //var SuccessPolygon = (await getInPolygon(47.255682388507054, 8.732877597212793));
      var SuccessPolygon = (await getInPolygon(crd.latitude, crd.longitude));


      if (SuccessPolygon != 0) {
        console.log("you're in: " + SuccessPolygon);

      }else{
        console.log("you're not in a forest");
      }

      console.log(DisplayForestLink);
      if (DisplayForestLink) {
        DisplayForestLink.innerHTML = SuccessPolygon;        
      }

      setTimeout(function(){ navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError, geolocationOptions); }, 5000);

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
