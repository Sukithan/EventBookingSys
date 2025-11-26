<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex align-center mb-6">
                    <v-btn icon="mdi-arrow-left" variant="text" @click="$router.go(-1)" class="mr-3"></v-btn>
                    <div>
                        <h1 class="text-h4 font-weight-bold">Seat Management</h1>
                        <p v-if="event" class="text-subtitle-1 text-grey">{{ event.name }}</p>
                    </div>
                    <v-spacer></v-spacer>
                    <v-btn color="secondary" variant="outlined" @click="syncSeats" :loading="syncing" class="mr-2">
                        <v-icon start>mdi-sync</v-icon>
                        Sync Seats
                    </v-btn>
                    <v-btn color="primary" variant="outlined" @click="loadSeats">
                        <v-icon start>mdi-refresh</v-icon>
                        Refresh
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12">
                <v-card class="mb-4">
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" sm="3">
                                <v-card variant="outlined">
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ event?.total_seats || 0 }}</div>
                                        <div class="text-caption">Total Seats</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" sm="3">
                                <v-card variant="outlined" color="success">
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ event?.available_seats || 0 }}</div>
                                        <div class="text-caption">Available</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" sm="3">
                                <v-card variant="outlined" color="error">
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ bookedSeatsCount }}</div>
                                        <div class="text-caption">Booked</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                            <v-col cols="12" sm="3">
                                <v-card variant="outlined" color="info">
                                    <v-card-text class="text-center">
                                        <div class="text-h4">{{ event?.rows || 0 }}x{{ event?.seats_per_row || 0 }}
                                        </div>
                                        <div class="text-caption">Layout</div>
                                    </v-card-text>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>

                <v-card>
                    <v-card-title>Seat Layout</v-card-title>
                    <v-card-text>
                        <div class="legend mb-4 d-flex gap-4">
                            <div class="d-flex align-center gap-1">
                                <div class="legend-box available"></div>
                                <span class="text-caption">Available</span>
                            </div>
                            <div class="d-flex align-center gap-1">
                                <div class="legend-box booked"></div>
                                <span class="text-caption">Booked</span>
                            </div>
                        </div>

                        <div v-if="groupedSeats && Object.keys(groupedSeats).length > 0" class="seat-layout">
                            <div v-for="row in Object.keys(groupedSeats).sort((a, b) => parseInt(a) - parseInt(b))"
                                :key="row" class="seat-row mb-3">
                                <div class="row-label">Row {{ row }}</div>
                                <div class="seats-container">
                                    <v-btn v-for="seat in groupedSeats[parseInt(row)]" :key="seat.id"
                                        :class="['seat-btn', seat.is_booked ? 'booked' : 'available']"
                                        :color="seat.is_booked ? 'error' : 'success'" variant="outlined" size="small"
                                        @click="handleSeatClick(seat)">
                                        {{ seat.seat_number }}
                                    </v-btn>
                                </div>
                            </div>
                        </div>
                        <div v-else class="text-center py-8">
                            <v-icon size="60" color="grey">mdi-seat-outline</v-icon>
                            <p class="text-grey mt-2">No seats configured</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Seat Booking Details Dialog -->
        <v-dialog v-model="detailsDialog" max-width="600">
            <v-card v-if="selectedSeat">
                <v-card-title class="text-h5">
                    Seat Details: Row {{ selectedSeat.row_number }}, Seat {{ selectedSeat.seat_number }}
                </v-card-title>
                <v-card-text>
                    <div v-if="selectedSeat.is_booked && selectedSeat.booking_info">
                        <v-alert type="error" variant="tonal" class="mb-4">
                            This seat is currently booked
                        </v-alert>

                        <h6 class="text-h6 mb-3">Booking Information</h6>
                        <v-row>
                            <v-col cols="12">
                                <div class="mb-2"><strong>Booking ID:</strong> #{{ selectedSeat.booking_info.booking_id
                                }}</div>
                                <div class="mb-2"><strong>Customer Name:</strong> {{
                                    selectedSeat.booking_info.full_name }}</div>
                                <div class="mb-2"><strong>Email:</strong> {{ selectedSeat.booking_info.email }}</div>
                                <div class="mb-2"><strong>Username:</strong> @{{ selectedSeat.booking_info.username }}
                                </div>
                                <div class="mb-2"><strong>Booked On:</strong> {{
                                    formatDate(selectedSeat.booking_info.booking_date) }}</div>
                                <div class="mb-2"><strong>Status:</strong>
                                    <v-chip
                                        :color="selectedSeat.booking_info.booking_status === 'confirmed' ? 'success' : 'error'"
                                        size="small">
                                        {{ selectedSeat.booking_info.booking_status }}
                                    </v-chip>
                                </div>
                            </v-col>
                        </v-row>
                    </div>
                    <div v-else>
                        <v-alert type="success" variant="tonal">
                            This seat is available for booking
                        </v-alert>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="detailsDialog = false">Close</v-btn>
                    <v-btn v-if="selectedSeat.is_booked && selectedSeat.booking_info" color="error"
                        :loading="cancelling" @click="cancelSeatBooking">
                        Cancel This Seat
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-snackbar v-model="snackbar" :color="snackbarColor">
            {{ snackbarMessage }}
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const route = useRoute()
const { fetchEventById } = useEvents()
const { getEventSeatsAdmin, deleteSeatBooking, syncEventSeats, recalculateEventStats } = useAdmin()

const loading = ref(false)
const syncing = ref(false)
const cancelling = ref(false)
const event = ref<any>(null)
const seats = ref<any[]>([])
const selectedSeat = ref<any>(null)
const detailsDialog = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const bookedSeatsCount = computed(() => {
    return seats.value.filter(seat => seat.is_booked).length
})

const groupedSeats = computed(() => {
    const grouped: { [key: number]: any[] } = {}
    seats.value.forEach(seat => {
        if (!grouped[seat.row_number]) {
            grouped[seat.row_number] = []
        }
        grouped[seat.row_number].push(seat)
    })

    // Sort seats within each row
    Object.keys(grouped).forEach(row => {
        grouped[parseInt(row)].sort((a, b) => a.seat_number - b.seat_number)
    })

    return grouped
})

const loadSeats = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)

    const [eventResult, seatsResult] = await Promise.all([
        fetchEventById(eventId),
        getEventSeatsAdmin(eventId)
    ])

    if (eventResult.success) {
        event.value = eventResult.data
    }

    if (seatsResult.success) {
        const data = seatsResult.data as any
        seats.value = data.seats || []
        if (data.event) {
            event.value = { ...event.value, ...data.event }
        }
    }

    loading.value = false
}

const syncSeats = async () => {
    syncing.value = true
    const eventId = parseInt(route.params.id as string)

    const result = await syncEventSeats(eventId)
    syncing.value = false

    if (result.success) {
        snackbarMessage.value = 'Seats synchronized successfully'
        snackbarColor.value = 'success'
        await loadSeats() // Reload data
    } else {
        snackbarMessage.value = result.error || 'Failed to sync seats'
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const handleSeatClick = (seat: any) => {
    selectedSeat.value = seat
    detailsDialog.value = true
}

const cancelSeatBooking = async () => {
    if (!selectedSeat.value) return

    cancelling.value = true
    const result = await deleteSeatBooking(selectedSeat.value.id)
    cancelling.value = false

    if (result.success) {
        snackbarMessage.value = 'Seat booking cancelled successfully'
        snackbarColor.value = 'success'
        detailsDialog.value = false
        await loadSeats() // Reload data
    } else {
        snackbarMessage.value = result.error || 'Failed to cancel seat booking'
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

onMounted(() => {
    loadSeats()
})
</script>

<style scoped>
.seat-layout {
    padding: 20px;
}

.seat-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.row-label {
    min-width: 60px;
    font-weight: bold;
    text-align: right;
}

.seats-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.seat-btn {
    min-width: 45px !important;
    height: 45px !important;
    font-weight: bold;
}

.seat-btn.available {
    cursor: pointer;
}

.seat-btn.booked {
    cursor: pointer;
}

.legend-box {
    width: 20px;
    height: 20px;
    border: 2px solid;
    border-radius: 4px;
}

.legend-box.available {
    border-color: rgb(var(--v-theme-success));
    background-color: rgba(var(--v-theme-success), 0.1);
}

.legend-box.booked {
    border-color: rgb(var(--v-theme-error));
    background-color: rgba(var(--v-theme-error), 0.1);
}
</style>
