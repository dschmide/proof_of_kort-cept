<template>
  <v-toolbar fixed height="60" class="light-blue" dark>
    <v-toolbar-title class="hidden-sm-and-down">
    <span
      class="home"
      @click="navigateTo({name: 'root'})">
      Proof of Kort-zept
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
          <v-icon dark>explore</v-icon> 
        </v-btn>
        
        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'market'})"
          >
          <v-icon dark>shopping_cart</v-icon>
        </v-btn>

        <v-btn 
          v-if="$store.state.isUserLoggedIn"
          flat 
          dark
          @click="navigateTo({name: 'stats'})"
          >
          <v-icon dark>trending_up</v-icon>
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

        <div class="text-xs-right hidden-sm-and-down">
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

.chip{
  margin-top: 12px;
}
</style>
