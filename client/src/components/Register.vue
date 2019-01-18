<template>
  <v-layout column>
    <v-flex md6 offset-md3 xs12>
      <div class="white elevation-2">
      <div class="pl-4 pr-4 pt-2 pb-2">
        <v-text-field
              label="Displayname"
              v-model="displayname"
              @keyup.enter="register" 
        ></v-text-field>
        
        <br>
        <v-text-field
              label="Password"
              type="password"
              v-model="password"
              @keyup.enter="register" 
        ></v-text-field>
        <br>
        <v-text-field
              label="Email (optional)"
              v-model="email"
              @keyup.enter="register" 
        ></v-text-field>
        <div class="error" v-if="error">
          <ul>
            <li v-if="error.data.username">Displayname: {{ error.data.username[0] }}</li>
            <li v-if="error.data.password">Password: {{ error.data.password[0] }}</li>
            <li v-if="error.data.email">Email: {{ error.data.email[0] }}</li>
            <li v-if="error.data">{{ error.data[0] }}</li>
          </ul>
        </div><br>
        <v-btn
          dark
          class="light-green"
          @click="register"> 
          Register
        </v-btn>
      </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import AuthenticationSevice from '@/services/AuthenticationService'
import UserAttributesService from '@/services/UserAttributesService'

export default {
  data () {
    return {
      email:'',
      password:'',
      displayname:'',
      error: null
    }
  },
  methods: {
    async register(){
        AuthenticationSevice.register({
          email: this.email,
          password: this.password,
          username: this.displayname
        })
        .then( () => {
          const Response = AuthenticationSevice.login({ 
            username: this.displayname, 
            password: this.password
          })
          .then( (response) => {
            this.$store.dispatch('setToken', response.data.token)
            this.$store.dispatch('setUser', this.displayname)

            console.log(response.data)

            // Create fresh Profile
            UserAttributesService.newUser(
            {
              "koins": -1,
              "experience": 0,
              "towers": 0,
              "tower_range": 2000,
              "sight_range": 2000,
            })
            console.log('fresh profile created')            
          })
          .then(() => {
            this.$router.push({
              name: 'welcome' 
            })
          })
        })
        .catch((error) => {
          // Catches & displays the error messages if necessary
          this.error = error.response;
        })
      }
    }
  }
</script>

<style scoped>

.error {
  color: white;
  list-style:  none;
  text-align: left;
}

</style>
