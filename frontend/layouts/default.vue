<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>
        <NuxtLink to="/" class="text-white no-underline">
          Project Demo
        </NuxtLink>
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn to="/" text>Home</v-btn>
      <v-btn to="/items" text>Items</v-btn>
      <v-btn to="/about" text>About</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <NuxtPage />
      </v-container>
    </v-main>

    <v-footer app color="primary" dark>
      <v-container>
        <div class="text-center">
          © 2025 FastAPI + Nuxt.js + Vuetify + Tailwind CSS
        </div>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
// Layout setup
</script>

<style scoped>
.no-underline {
  text-decoration: none;
}
</style>
