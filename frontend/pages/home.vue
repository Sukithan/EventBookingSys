<template>
    <v-container fluid class="pa-0">
        <!-- Hero Section -->
        <v-row no-gutters>
            <v-col cols="12">
                <v-card class="rounded-0" color="primary" dark>
                    <v-card-text class="py-8 py-md-12">
                        <v-container>
                            <v-row justify="center" align="center">
                                <v-col cols="12" md="8" class="text-center px-4">
                                    <h1 class="text-h4 text-md-h2 font-weight-bold mb-4">Welcome to Event Booking</h1>
                                    <p class="text-body-1 text-md-h6 mb-6">Discover and book amazing events happening
                                        near you</p>
                                    <v-text-field v-model="searchQuery" label="Search events..."
                                        prepend-inner-icon="mdi-magnify" variant="outlined" bg-color="white"
                                        hide-details @input="handleSearch" @click:clear="clearSearch" clearable
                                        class="mx-auto" style="max-width: 600px;"></v-text-field>
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

            <LoadingSkeleton v-if="loading" type="card" :count="6" :cols="12" :sm="6" :md="4" />

            <EventGrid v-if="displayEvents.length > 0" :events="displayEvents"
                :image-height="$vuetify.display.xs ? '150' : '200'" @view-event="viewEvent" />

            <EmptyState v-else icon="mdi-calendar-blank"
                :title="searchQuery ? 'No matching events found' : 'No events found'"
                :message="searchQuery ? `No events match '${searchQuery}'. Try a different search term.` : 'Check back later for upcoming events'" />
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

// Debounced search function
let searchTimeout: NodeJS.Timeout | null = null
const handleSearch = () => {
    // Clear existing timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout)
    }

    // Set new timeout for debounced search
    searchTimeout = setTimeout(async () => {
        loading.value = true
        if (searchQuery.value.trim()) {
            await fetchEvents(searchQuery.value.trim())
        } else {
            await fetchUpcomingEvents()
        }
        loading.value = false
    }, 500) // 500ms debounce
}

const clearSearch = async () => {
    searchQuery.value = ''
    loading.value = true
    await fetchUpcomingEvents()
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



onMounted(() => {
    loadEvents()
})
</script>
