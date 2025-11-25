<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex justify-space-between align-center mb-6">
                    <h1 class="text-h4 font-weight-bold">My Bookings</h1>
                    <v-btn color="primary" to="/" variant="outlined">
                        <v-icon start>mdi-calendar-search</v-icon>
                        Browse Events
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col v-for="n in 3" :key="n" cols="12">
                <v-skeleton-loader type="article"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="displayBookings.length > 0">
            <v-col v-for="booking in displayBookings" :key="booking.id" cols="12">
                <v-card class="mb-4">
                    <v-row no-gutters>
                        <v-col cols="12" md="8">
                            <v-card-title class="text-h6">{{ booking.event.name }}</v-card-title>
                            <v-card-text>
                                <v-row>
                                    <v-col cols="12" sm="6">
                                        <div class="mb-2">
                                            <v-icon size="small" class="mr-2">mdi-calendar</v-icon>
                                            <span class="text-body-2">{{ formatDate(booking.event.event_date) }}</span>
                                        </div>
                                        <div class="mb-2">
                                            <v-icon size="small" class="mr-2">mdi-map-marker</v-icon>
                                            <span class="text-body-2">{{ booking.event.location }}</span>
                                        </div>
                                    </v-col>
                                    <v-col cols="12" sm="6">
                                        <div class="mb-2">
                                            <v-icon size="small" class="mr-2">mdi-seat</v-icon>
                                            <span class="text-body-2">{{ booking.seats_booked }} seat(s)</span>
                                        </div>
                                        <div class="mb-2">
                                            <v-icon size="small" class="mr-2">mdi-clock</v-icon>
                                            <span class="text-body-2">Booked: {{ formatDate(booking.booking_date)
                                                }}</span>
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-col>

                        <v-col cols="12" md="4"
                            class="d-flex flex-column justify-center align-center pa-4 bg-grey-lighten-4">
                            <div class="text-h5 primary--text mb-2">${{ booking.total_price.toFixed(2) }}</div>
                            <v-chip :color="booking.status === 'confirmed' ? 'success' : 'error'" class="mb-4">
                                {{ booking.status.toUpperCase() }}
                            </v-chip>

                            <v-btn v-if="booking.status === 'confirmed'" color="error" variant="outlined" size="small"
                                @click="openCancelDialog(booking)">
                                <v-icon start>mdi-cancel</v-icon>
                                Cancel Booking
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                <p class="text-h6 text-grey mt-4">No bookings yet</p>
                <p class="text-body-1 text-grey mb-4">Start by booking an event</p>
                <v-btn color="primary" to="/">
                    Browse Events
                </v-btn>
            </v-col>
        </v-row>

        <!-- Cancel Confirmation Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h6">Cancel Booking</v-card-title>
                <v-card-text>
                    <p>Are you sure you want to cancel this booking?</p>
                    <p class="font-weight-bold mt-2">{{ selectedBooking?.event.name }}</p>
                    <p class="text-body-2">This action cannot be undone.</p>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn variant="text" @click="cancelDialog = false">No, Keep It</v-btn>
                    <v-btn color="error" :loading="cancelling" @click="confirmCancel">Yes, Cancel</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Snackbar -->
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
            {{ snackbarMessage }}
            <template v-slot:actions>
                <v-btn variant="text" @click="snackbar = false">Close</v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'auth'
})

const { fetchMyBookings, cancelBooking, bookings } = useBookings()

const loading = ref(false)
const cancelling = ref(false)
const cancelDialog = ref(false)
const selectedBooking = ref<any>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const displayBookings = computed(() => bookings.value || [])

const loadBookings = async () => {
    loading.value = true
    await fetchMyBookings()
    loading.value = false
}

const openCancelDialog = (booking: any) => {
    selectedBooking.value = booking
    cancelDialog.value = true
}

const confirmCancel = async () => {
    if (!selectedBooking.value) return

    cancelling.value = true
    const result = await cancelBooking(selectedBooking.value.id)
    cancelling.value = false

    if (result.success) {
        snackbarMessage.value = 'Booking cancelled successfully'
        snackbarColor.value = 'success'
        snackbar.value = true
        cancelDialog.value = false
        await loadBookings()
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
        snackbar.value = true
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
    loadBookings()
})
</script>
