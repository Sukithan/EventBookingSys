<template>
  <v-container>
    <v-card max-width="800" class="mx-auto" elevation="3">
      <v-card-title class="text-h5 text-sm-h4 text-center bg-primary text-white py-4 py-sm-6">
        About This Project
      </v-card-title>

      <v-card-text class="pa-4 pa-sm-8">
        <div class="mb-6">
          <h2 class="text-2xl font-bold mb-4">Technology Stack</h2>

          <div class="space-y-4">
            <div class="border-l-4 border-green-500 pl-4">
              <h3 class="text-xl font-semibold mb-2">Backend: FastAPI</h3>
              <p class="text-gray-700">
                High-performance Python web framework with automatic API documentation,
                data validation using Pydantic, and async support.
              </p>
            </div>

            <div class="border-l-4 border-green-500 pl-4">
              <h3 class="text-xl font-semibold mb-2">Frontend: Nuxt.js 3</h3>
              <p class="text-gray-700">
                Vue.js framework with server-side rendering, file-based routing,
                and powerful auto-imports for an amazing developer experience.
              </p>
            </div>

            <div class="border-l-4 border-blue-500 pl-4">
              <h3 class="text-xl font-semibold mb-2">UI: Vuetify 3</h3>
              <p class="text-gray-700">
                Material Design component library providing beautiful, responsive
                UI components that work seamlessly with Vue 3.
              </p>
            </div>

            <div class="border-l-4 border-cyan-500 pl-4">
              <h3 class="text-xl font-semibold mb-2">Styling: Tailwind CSS</h3>
              <p class="text-gray-700">
                Utility-first CSS framework for rapidly building custom designs
                with flexible, composable utility classes.
              </p>
            </div>
          </div>
        </div>

        <v-divider class="my-6"></v-divider>

        <div>
          <h2 class="text-2xl font-bold mb-4">Features</h2>
          <v-list>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="success">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>Full-stack RESTful API</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="success">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>CRUD operations with FastAPI</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="success">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>Responsive UI with Vuetify & Tailwind</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="success">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>Type-safe with TypeScript</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="success">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>CORS configured for local development</v-list-item-title>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
// About page
</script>

<style scoped>
.space-y-4>*+* {
  margin-top: 1rem;
}
</style>
