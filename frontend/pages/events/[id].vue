<template>
    <v-container>
        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article, actions"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="event">
            <!-- Event Details -->
            <v-col cols="12" md="5">
                <v-card>
                    <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="300"
                        cover></v-img>

                    <v-card-title class="text-h5 py-3">{{ event.name }}</v-card-title>

                    <v-card-text>
                        <v-row class="mb-3">
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="primary" size="small">mdi-calendar</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Date & Time</div>
                                        <div class="text-body-2 font-weight-medium">{{ formatDate(event.event_date) }}
                                        </div>
                                    </div>
                                </div>
                            </v-col>

                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="primary" size="small">mdi-map-marker</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Location</div>
                                        <div class="text-body-2 font-weight-medium">{{ event.location }}</div>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>

                        <v-divider class="my-3"></v-divider>

                        <h4 class="text-h6 mb-2">About This Event</h4>
                        <p class="text-body-2" v-if="event.description">{{ event.description }}</p>
                        <p class="text-body-2 text-grey" v-else>No description available</p>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Seat Selection -->
            <v-col cols="12" md="7">
                <v-card>
                    <v-card-title class="d-flex align-center justify-space-between">
                        <div class="d-flex align-center gap-2">
                            <span>Select Your Seats</span>
                            <v-chip color="orange" size="small" v-if="isAdmin">Admin</v-chip>
                        </div>
                        <v-chip color="primary" v-if="selectedSeats.length > 0">
                            {{ selectedSeats.length }} selected
                        </v-chip>
                    </v-card-title>

                    <v-card-text>
                        <!-- Theatre Screen -->
                        <div class="text-center mb-6">
                            <div class="screen-indicator">
                                <v-chip color="grey-darken-1" size="large"> </v-chip>
                            </div>
                        </div>

                        <!-- Seat Map -->
                        <div class="seat-map" v-if="!seatsLoading">
                            <div v-for="(rowSeats, rowNumber) in groupSeatsByRow" :key="rowNumber"
                                class="seat-row mb-2">
                                <div class="row-label">{{ rowNumber }}</div>
                                <div class="seats-container">
                                    <div v-for="seat in rowSeats" :key="seat.id" class="seat-wrapper">
                                        <v-btn :class="getSeatClass(seat)"
                                            :disabled="!isAuthenticated || (!seat.is_available && !selectedSeats.includes(seat.id))"
                                            @click="toggleSeat(seat)" size="small" variant="flat"
                                            :loading="seatActionLoading === seat.id">
                                            {{ seat.seat_number }}
                                        </v-btn>
                                    </div>
                                </div>
                                <div class="row-label">{{ rowNumber }}</div>
                            </div>
                        </div>

                        <v-skeleton-loader v-else type="paragraph, paragraph, paragraph"></v-skeleton-loader>

                        <!-- Legend -->
                        <v-row class="mt-4">
                            <v-col cols="12">
                                <div class="d-flex flex-wrap gap-4 justify-center">
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="success" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Available</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="primary" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Selected</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="orange" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Locked</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="error" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Booked</span>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Booking Summary -->
            <v-col cols="12">
                <v-card v-if="selectedSeats.length > 0" elevation="8" color="primary" dark>
                    <v-card-text>
                        <v-row align="center">
                            <v-col cols="12" sm="4">
                                <div class="text-h6">${{ event.price.toFixed(2) }} per seat</div>
                                <div class="text-body-2 opacity-80">{{ selectedSeats.length }} seat(s) selected</div>
                            </v-col>
                            <v-col cols="12" sm="4">
                                <div class="text-h4 font-weight-bold">
                                    Total: ${{ (event.price * selectedSeats.length).toFixed(2) }}
                                </div>
                            </v-col>
                            <v-col cols="12" sm="4" class="text-center text-sm-right">
                                <v-btn color="white" variant="elevated" size="large" :loading="bookingLoading"
                                    @click="handleBooking" class="mb-2 mb-sm-0 mr-sm-2">
                                    <v-icon start>mdi-ticket</v-icon>
                                    Book Now
                                </v-btn>
                                <v-btn variant="outlined" color="white" @click="clearSelection">
                                    Clear
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>

                <v-alert v-else-if="!isAuthenticated" type="info" variant="tonal" class="mt-4">
                    Please <NuxtLink to="/login" class="font-weight-bold">login</NuxtLink> to book this event
                </v-alert>

                <v-alert v-else-if="existingBooking && !isAdmin" type="info" variant="tonal" class="mt-4">
                    <div class="d-flex align-center">
                        <div>
                            <div class="font-weight-bold">Previous Booking Found</div>
                            <div class="text-body-2">You have existing bookings for this event. You can make additional
                                reservations if needed. Check your <NuxtLink to="/my-bookings" class="font-weight-bold">
                                    My Bookings</NuxtLink> page to manage them.</div>
                        </div>
                    </div>
                </v-alert>

                <v-alert v-else-if="isAdmin && isAuthenticated" type="info" variant="tonal" class="mt-4">
                    <div class="d-flex align-center">
                        <v-icon start>mdi-shield-crown</v-icon>
                        <div>
                            <div class="font-weight-bold">Admin Access</div>
                            <div class="text-body-2">You can make multiple bookings and manage seat reservations</div>
                        </div>
                    </div>
                </v-alert>
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
                        Seats: <strong>{{ bookedSeatsCount }}</strong><br>
                        Total: <strong>${{ event ? (event.price * bookedSeatsCount).toFixed(2) : '0.00' }}</strong>
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
const { createBooking, fetchMyBookings, bookings } = useBookings()
const { isAuthenticated, isAdmin } = useAuth()
const {
    seats,
    selectedSeats,
    loading: seatsLoading,
    fetchEventSeats,
    toggleSeatSelection,
    clearSelection,
    groupSeatsByRow
} = useSeats()

const event = computed(() => currentEvent.value)
const loading = ref(false)
const bookingLoading = ref(false)
const successDialog = ref(false)
const errorSnackbar = ref(false)
const errorMessage = ref('')
const seatActionLoading = ref<number | null>(null)
const bookedSeatsCount = ref(0)
const existingBooking = computed(() => {
    if (!event.value || !bookings.value || !isAuthenticated.value) return null
    return bookings.value.find(booking =>
        booking.event_id === event.value.id &&
        booking.status === 'confirmed'
    )
})

const loadEvent = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)
    await fetchEventById(eventId)
    loading.value = false
}

const loadSeats = async (silent = false) => {
    const eventId = parseInt(route.params.id as string)
    await fetchEventSeats(eventId, silent)
}

const toggleSeat = async (seat: any) => {
    // Check if user is authenticated
    if (!isAuthenticated.value) {
        errorMessage.value = 'Please login to select seats'
        errorSnackbar.value = true
        return
    }

    if (!seat.is_available && !selectedSeats.value.includes(seat.id)) return

    seatActionLoading.value = seat.id
    const result = await toggleSeatSelection(seat.id)
    seatActionLoading.value = null

    if (!result?.success && result?.error) {
        errorMessage.value = result.error
        errorSnackbar.value = true
    }

    // Refresh seats to get updated status (silent to prevent UI flashing)
    await loadSeats(true)
}

const getSeatClass = (seat: any) => {
    if (selectedSeats.value.includes(seat.id)) {
        return 'seat-selected'
    } else if (!seat.is_available) {
        return seat.is_locked ? 'seat-locked' : 'seat-booked'
    } else {
        return 'seat-available'
    }
}

const handleBooking = async () => {
    if (!event.value || !isAuthenticated.value || selectedSeats.value.length === 0) return

    // Users can now book multiple times for the same event

    bookingLoading.value = true
    const result = await createBooking(event.value.id, selectedSeats.value)
    bookingLoading.value = false

    if (result.success) {
        bookedSeatsCount.value = selectedSeats.value.length
        clearSelection() // This will clear selectedSeats and unlock them
        successDialog.value = true
        // Reload event and seats to get updated counts
        await loadEvent()
        await loadSeats()
        // Refresh bookings to update existing booking status
        if (isAuthenticated.value) {
            await fetchMyBookings()
        }
    } else {
        errorMessage.value = result.error
        errorSnackbar.value = true
        // Refresh seats to get updated status in case of partial failures
        await loadSeats(true)
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

onMounted(async () => {
    await loadEvent()
    await loadSeats()
    // Load user's bookings to check for existing bookings
    if (isAuthenticated.value) {
        await fetchMyBookings()
    }
})

watch(() => route.params.id, async () => {
    if (route.params.id) {
        await loadEvent()
        await loadSeats()
    }
})

// Auto-refresh seats every 60 seconds to show real-time updates (reduced frequency)
let refreshInterval: NodeJS.Timeout
onMounted(() => {
    refreshInterval = setInterval(() => {
        // Only refresh if user is not currently selecting seats to prevent UI disruption
        if (selectedSeats.value.length === 0) {
            loadSeats(true) // Silent refresh
        }
    }, 60000)
})

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval)
    }
    // Clear selection when leaving page
    clearSelection()
})
</script>

<style scoped>
.screen-indicator {
    margin-bottom: 2rem;
    background: linear-gradient(90deg, transparent 0%, #424242 20%, #424242 80%, transparent 100%);
    height: 4px;
    border-radius: 2px;
    position: relative;
}

.screen-indicator::after {
    content: '';
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 20px;
    background: linear-gradient(180deg, #424242 0%, transparent 100%);
    border-radius: 10px 10px 0 0;
}

.seat-map {
    max-width: 100%;
    overflow-x: auto;
    padding: 1rem 0;
}

.seat-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.row-label {
    width: 35px;
    text-align: center;
    font-weight: bold;
    color: #333;
    font-size: 1rem;
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 4px;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.seats-container {
    display: flex;
    gap: 0.25rem;
    flex-wrap: nowrap;
}

.seat-wrapper {
    position: relative;
}

.seat-available {
    background-color: #4CAF50 !important;
    color: white !important;
}

.seat-selected {
    background-color: #2196F3 !important;
    color: white !important;
    box-shadow: 0 0 0 2px #1976D2 !important;
}

.seat-locked {
    background-color: #FF9800 !important;
    color: white !important;
}

.seat-booked {
    background-color: #F44336 !important;
    color: white !important;
}

.seat-available:hover {
    background-color: #45A049 !important;
    transform: scale(1.05);
    transition: all 0.2s ease;
}

.seat-selected:hover {
    background-color: #1976D2 !important;
}

.v-btn.seat-available,
.v-btn.seat-selected,
.v-btn.seat-locked,
.v-btn.seat-booked {
    min-width: 36px !important;
    height: 36px !important;
    border-radius: 8px !important;
    font-size: 0.75rem !important;
    font-weight: bold !important;
}

@media (max-width: 960px) {
    .seat-map {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}

@media (max-width: 768px) {
    .seat-row {
        gap: 0.25rem;
    }

    .row-label {
        width: 28px;
        font-size: 0.85rem;
        min-height: 28px;
        padding: 2px;
    }

    .v-btn.seat-available,
    .v-btn.seat-selected,
    .v-btn.seat-locked,
    .v-btn.seat-booked {
        min-width: 28px !important;
        height: 28px !important;
        font-size: 0.7rem !important;
    }

    .seats-container {
        gap: 0.125rem;
    }
}
</style>
