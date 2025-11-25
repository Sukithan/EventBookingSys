<template>
    <v-container>
        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article, actions"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="event">
            <v-col cols="12" md="8">
                <v-card>
                    <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="400"
                        cover></v-img>

                    <v-card-title class="text-h4 py-4">{{ event.name }}</v-card-title>

                    <v-card-text>
                        <v-row class="mb-4">
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-2" color="primary">mdi-calendar</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Date & Time</div>
                                        <div class="font-weight-medium">{{ formatDate(event.event_date) }}</div>
                                    </div>
                                </div>
                            </v-col>

                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-2" color="primary">mdi-map-marker</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Location</div>
                                        <div class="font-weight-medium">{{ event.location }}</div>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>

                        <v-divider class="my-4"></v-divider>

                        <h3 class="text-h6 mb-2">About This Event</h3>
                        <p class="text-body-1" v-if="event.description">{{ event.description }}</p>
                        <p class="text-body-1 text-grey" v-else>No description available</p>
                    </v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card class="sticky-top" style="top: 20px;">
                    <v-card-text>
                        <div class="text-h4 primary--text mb-4">${{ event.price.toFixed(2) }}</div>

                        <v-list>
                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon>mdi-seat</v-icon>
                                </template>
                                <v-list-item-title>Available Seats</v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ event.available_seats }} / {{ event.total_seats }}
                                </v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon>mdi-ticket</v-icon>
                                </template>
                                <v-list-item-title>Status</v-list-item-title>
                                <v-list-item-subtitle>
                                    <v-chip :color="event.available_seats > 0 ? 'success' : 'error'" size="small">
                                        {{ event.available_seats > 0 ? 'Available' : 'Sold Out' }}
                                    </v-chip>
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>

                        <v-text-field v-model.number="seatsToBook" label="Number of Seats" type="number" :min="1"
                            :max="event.available_seats" variant="outlined" class="mt-4"
                            :disabled="!event.available_seats"></v-text-field>

                        <div class="text-body-1 mb-4">
                            Total: <span class="font-weight-bold">${{ (event.price * seatsToBook).toFixed(2) }}</span>
                        </div>

                        <v-btn color="primary" block size="large" :disabled="!event.available_seats || !isAuthenticated"
                            :loading="bookingLoading" @click="handleBooking">
                            <v-icon start>mdi-ticket</v-icon>
                            Book Now
                        </v-btn>

                        <v-alert v-if="!isAuthenticated" type="info" variant="tonal" class="mt-4">
                            Please <NuxtLink to="/login" class="font-weight-bold">login</NuxtLink> to book this event
                        </v-alert>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-alert-circle</v-icon>
                <p class="text-h6 text-grey mt-4">Event not found</p>
            </v-col>
        </v-row>

        <!-- Success Dialog -->
        <v-dialog v-model="successDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5 bg-success text-white">
                    <v-icon start>mdi-check-circle</v-icon>
                    Booking Successful!
                </v-card-title>
                <v-card-text class="pa-6">
                    <p class="text-body-1">Your booking has been confirmed!</p>
                    <p class="text-body-2 mt-2">
                        Event: <strong>{{ event?.name }}</strong><br>
                        Seats: <strong>{{ seatsToBook }}</strong><br>
                        Total: <strong>${{ event ? (event.price * seatsToBook).toFixed(2) : '0.00' }}</strong>
                    </p>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="goToMyBookings">View My Bookings</v-btn>
                    <v-btn variant="text" @click="successDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Error Snackbar -->
        <v-snackbar v-model="errorSnackbar" color="error" :timeout="5000">
            {{ errorMessage }}
            <template v-slot:actions>
                <v-btn variant="text" @click="errorSnackbar = false">Close</v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { fetchEventById, currentEvent } = useEvents()
const { createBooking } = useBookings()
const { isAuthenticated } = useAuth()

const event = computed(() => currentEvent.value)
const loading = ref(false)
const bookingLoading = ref(false)
const seatsToBook = ref(1)
const successDialog = ref(false)
const errorSnackbar = ref(false)
const errorMessage = ref('')

const loadEvent = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)
    await fetchEventById(eventId)
    loading.value = false
}

const handleBooking = async () => {
    if (!event.value || !isAuthenticated.value) return

    bookingLoading.value = true
    const result = await createBooking(event.value.id, seatsToBook.value)
    bookingLoading.value = false

    if (result.success) {
        successDialog.value = true
        // Reload event to get updated seat count
        await loadEvent()
    } else {
        errorMessage.value = result.error
        errorSnackbar.value = true
    }
}

const goToMyBookings = () => {
    successDialog.value = false
    router.push('/my-bookings')
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
    loadEvent()
})

watch(() => route.params.id, () => {
    if (route.params.id) {
        loadEvent()
    }
})
</script>
