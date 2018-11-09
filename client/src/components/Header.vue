<template>
  <v-toolbar fixed class="light-blue" dark>
    <v-toolbar-title class=mr-4>
    <span
      class="home"
      @click="navigateTo({name: 'root'})">
      Proof of Kort-cept
      </span>
    </v-toolbar-title>

    <v-spacer></v-spacer>

      <v-toolbar-items>
        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'missions'})"
          >
          <v-icon left dark>explore</v-icon>
          Missions
        </v-btn>
        
        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'market'})"
          >
          <v-icon left dark>shopping_cart</v-icon>
          Market
        </v-btn>

        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'stats'})"
          >
          <v-icon left dark>trending_up</v-icon>
          Stats
        </v-btn>

      <v-btn 
          v-if="!$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'login'})">
          Login
        </v-btn>

        <v-btn 
          v-if="!$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'register'})">
          Sign Up
        </v-btn>
        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="logout">
          LogOut
        </v-btn>

        <div class="text-xs-center">
          <v-chip
          color="orange"
          text-color="white"
          
          v-if="$store.state.isUserLoggedIn"
          >
          <v-icon left>account_circle</v-icon>
          {{ this.$store.state.user }}
          </v-chip>
        </div>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
export default {
  methods: {
    navigateTo (route) {
      this.$router.push(route)
    },
    logout() {
      this.$store.dispatch('setToken', null)
      this.$store.dispatch('setUser', null)
      localStorage.removeItem("jwt")
      this.$router.push({
        name:'login'
      })
    },
  }
}
</script>

<style scoped>
.home{
  cursor: pointer;
}
.home:hover {
  color: #EEEEEE;
}

.header-chip{
  margin-top: 8px;
}
</style>
