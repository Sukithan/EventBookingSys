<template>
  <div>
    <!-- Hero Section with Tailwind -->
    <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white py-20">
      <div class="container mx-auto text-center px-4">
        <h1 class="text-5xl font-bold mb-4">Welcome to the Project</h1>
        <p class="text-xl mb-8">FastAPI + Nuxt.js + Vuetify + Tailwind CSS</p>
        <v-btn size="large" color="white" variant="elevated" to="/items">
          Get Started
        </v-btn>
      </div>
    </div>

    <!-- Features Section with Vuetify Cards -->
    <v-container class="my-12">
      <h2 class="text-4xl font-bold text-center mb-8">Tech Stack</h2>
      <v-row>
        <v-col cols="12" md="3" sm="6" v-for="(feature, index) in features" :key="index">
          <v-card class="h-full" hover elevation="2">
            <v-card-title class="text-h5 justify-center">
              <v-icon size="48" :color="feature.color" class="mb-2">
                {{ feature.icon }}
              </v-icon>
            </v-card-title>
            <v-card-title class="justify-center">
              {{ feature.title }}
            </v-card-title>
            <v-card-text class="text-center">
              {{ feature.description }}
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- API Status Section -->
    <div class="bg-gray-100 py-12">
      <v-container>
        <h2 class="text-3xl font-bold text-center mb-8">API Status</h2>
        <v-card max-width="600" class="mx-auto">
          <v-card-text>
            <div v-if="loading" class="text-center">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
            </div>
            <div v-else-if="apiStatus">
              <div class="flex items-center justify-between mb-2">
                <span class="font-semibold">Status:</span>
                <v-chip :color="apiStatus.status === 'running' ? 'success' : 'error'">
                  {{ apiStatus.status }}
                </v-chip>
              </div>
              <div class="flex items-center justify-between mb-2">
                <span class="font-semibold">Version:</span>
                <span>{{ apiStatus.version }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="font-semibold">Message:</span>
                <span>{{ apiStatus.message }}</span>
              </div>
            </div>
            <div v-else class="text-center text-red-500">
              Failed to connect to API
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const features = [
  {
    title: 'FastAPI',
    description: 'Modern, fast Python web framework for building APIs',
    icon: 'mdi-lightning-bolt',
    color: 'green'
  },
  {
    title: 'Nuxt.js 3',
    description: 'Intuitive Vue framework for web applications',
    icon: 'mdi-vuejs',
    color: 'green'
  },
  {
    title: 'Vuetify',
    description: 'Material Design component framework for Vue',
    icon: 'mdi-material-design',
    color: 'blue'
  },
  {
    title: 'Tailwind CSS',
    description: 'Utility-first CSS framework for rapid UI development',
    icon: 'mdi-tailwind',
    color: 'cyan'
  }
]

const loading = ref(true)
const apiStatus = ref<any>(null)

onMounted(async () => {
  try {
    const data = await $api('/')
    apiStatus.value = data
  } catch (error) {
    console.error('Failed to fetch API status:', error)
  } finally {
    loading.value = false
  }
})
</script>
