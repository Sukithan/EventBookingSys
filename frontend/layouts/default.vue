<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>
        <NuxtLink to="/" class="text-white no-underline">
          <v-icon>mdi-ticket-confirmation</v-icon>
          Event Booking
        </NuxtLink>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <template v-if="isAuthenticated">
        <v-btn v-if="isAdmin" to="/admin/dashboard" icon title="Admin">
          <v-icon>mdi-shield-account</v-icon>
        </v-btn>
        <v-btn to="/my-bookings" icon title="My Bookings">
          <v-icon>mdi-ticket</v-icon>
        </v-btn>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <v-icon>mdi-account-circle</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>{{ user?.full_name }}</v-list-item-title>
              <v-list-item-subtitle>{{ user?.email }}</v-list-item-subtitle>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item @click="handleLogout">
              <template v-slot:prepend>
                <v-icon>mdi-logout</v-icon>
              </template>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
      <template v-else>
        <v-btn to="/login" variant="text">Login</v-btn>
        <v-btn to="/signup" variant="outlined">Sign Up</v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <v-list-item prepend-icon="mdi-home" title="Home" to="/"></v-list-item>
        <template v-if="isAuthenticated">
          <v-list-item prepend-icon="mdi-ticket" title="My Bookings" to="/my-bookings"></v-list-item>
          <template v-if="isAdmin">
            <v-divider class="my-2"></v-divider>
            <v-list-subheader>Admin</v-list-subheader>
            <v-list-item prepend-icon="mdi-view-dashboard" title="Dashboard" to="/admin/dashboard"></v-list-item>
            <v-list-item prepend-icon="mdi-calendar" title="Manage Events" to="/admin/events"></v-list-item>
            <v-list-item prepend-icon="mdi-ticket-confirmation" title="All Bookings" to="/admin/bookings"></v-list-item>
          </template>
          <v-divider class="my-2"></v-divider>
          <v-list-item prepend-icon="mdi-logout" title="Logout" @click="handleLogout"></v-list-item>
        </template>
        <template v-else>
          <v-list-item prepend-icon="mdi-login" title="Login" to="/login"></v-list-item>
          <v-list-item prepend-icon="mdi-account-plus" title="Sign Up" to="/signup"></v-list-item>
          <v-divider class="my-2"></v-divider>
          <v-list-item prepend-icon="mdi-shield-lock" title="Admin Login" to="/admin/login"></v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <NuxtPage />
      </v-container>
    </v-main>

    <v-footer app color="primary" dark>
      <v-container>
        <div class="text-center">
          © 2025 Event Booking System | FastAPI + Nuxt.js + Vuetify
        </div>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
const { isAuthenticated, isAdmin, user, logout } = useAuth()
const drawer = ref(false)

const handleLogout = () => {
  drawer.value = false
  logout()
}
</script>

<style scoped>
.no-underline {
  text-decoration: none;
}
</style>
