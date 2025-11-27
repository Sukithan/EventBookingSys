<template>
  <v-container fluid class="pa-0">
    <!-- Hero Section -->
    <v-row no-gutters>
      <v-col cols="12">
        <v-card class="rounded-0" color="primary" dark>
          <v-card-text class="py-12">
            <v-container>
              <v-row justify="center" align="center">
                <v-col cols="12" md="8" class="text-center">
                  <h1 class="text-h2 font-weight-bold mb-4">Welcome to Event Booking</h1>
                  <p class="text-h6 mb-6">Discover and book amazing events happening near you</p>
                  <v-text-field v-model="searchQuery" label="Search events..." prepend-inner-icon="mdi-magnify"
                    variant="outlined" bg-color="white" hide-details @input="handleSearch" class="mx-auto"
                    style="max-width: 600px;"></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Events Section -->
    <v-container class="py-8">
      <v-row>
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold mb-6">
            {{ searchQuery ? 'Search Results' : 'Upcoming Events' }}
          </h2>
        </v-col>
      </v-row>

      <v-row v-if="loading">
        <v-col v-for="n in 6" :key="n" cols="12" sm="6" md="4">
          <v-skeleton-loader type="card"></v-skeleton-loader>
        </v-col>
      </v-row>

      <v-row v-else-if="displayEvents.length > 0">
        <v-col v-for="event in displayEvents" :key="event.id" cols="12" sm="6" md="4">
          <v-card hover @click="viewEvent(event.id)" class="h-100">
            <v-img :src="event.image_url || 'https://via.placeholder.com/400x250?text=Event'" height="200" cover>
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-row>
              </template>
            </v-img>

            <v-card-title class="text-h6">{{ event.name }}</v-card-title>

            <v-card-text>
              <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-calendar</v-icon>
                {{ formatDate(event.event_date) }}
              </div>
              <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
                {{ event.location }}
              </div>
              <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-seat</v-icon>
                {{ event.available_seats }} / {{ event.total_seats }} seats available
              </div>
              <div class="text-h6 primary--text mt-2">
                ${{ event.price.toFixed(2) }}
              </div>
            </v-card-text>

            <v-card-actions>
              <v-chip :color="event.available_seats > 0 ? 'success' : 'error'" size="small" variant="flat">
                {{ event.available_seats > 0 ? 'Available' : 'Sold Out' }}
              </v-chip>
              <v-spacer></v-spacer>
              <v-btn color="primary" variant="text">
                View Details
                <v-icon end>mdi-arrow-right</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col cols="12" class="text-center py-12">
          <v-icon size="80" color="grey-lighten-1">mdi-calendar-blank</v-icon>
          <p class="text-h6 text-grey mt-4">No events found</p>
          <p class="text-body-1 text-grey">Check back later for upcoming events</p>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
const { fetchUpcomingEvents, fetchEvents, events } = useEvents()
const router = useRouter()

const searchQuery = ref('')
const loading = ref(false)
const displayEvents = computed(() => events.value || [])

const loadEvents = async () => {
  loading.value = true
  await fetchUpcomingEvents()
  loading.value = false
}

const handleSearch = async () => {
  loading.value = true
  await fetchEvents(searchQuery.value)
  loading.value = false
}

const { isAdmin } = useAuth()

const viewEvent = (id: number) => {
  // Redirect admin to admin bookings page
  if (isAdmin.value) {
    router.push(`/admin/events/${id}/bookings`)
  } else {
    router.push(`/events/${id}`)
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadEvents()
})
</script>
