<template>
    <v-container>
        <CommonPageHeader title="My Bookings" action-text="Browse Events" action-to="/"
            action-icon="mdi-calendar-search" action-variant="outlined" />

        <!-- Search Section -->
        <v-row class="mb-4">
            <v-col cols="12" md="6">
                <v-text-field v-model="searchQuery" label="Search bookings..." prepend-inner-icon="mdi-magnify"
                    variant="outlined" clearable @input="handleSearch"
                    placeholder="Search by event name, location, or booking status"></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
                <v-select v-model="statusFilter" label="Filter by status" :items="statusOptions" variant="outlined"
                    clearable @update:model-value="handleFilter"></v-select>
            </v-col>
        </v-row>

        <CommonLoadingSkeleton v-if="loading" type="article" :count="3" />

        <v-alert v-else-if="error" type="error" class="mb-4">
            {{ error }}
            <template v-slot:append>
                <v-btn icon="mdi-refresh" variant="text" @click="loadBookings" :loading="loading"></v-btn>
            </template>
        </v-alert>

        <v-row v-else-if="displayBookings.length > 0">
            <v-col v-for="booking in displayBookings" :key="booking.id" cols="12">
                <BookingMyBookingCard :booking="booking" @cancel-booking="openCancelDialog"
                    @partial-cancel="openPartialCancelDialog" />
            </v-col>
        </v-row>

        <CommonEmptyState v-else icon="mdi-ticket-outline" title="No bookings yet" message="Start by booking an event"
            action-text="Browse Events" action-to="/" action-icon="mdi-calendar-search" />

        <!-- Cancel Confirmation Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h6">Cancel Booking</v-card-title>
                <v-card-text>
                    <p>Are you sure you want to cancel this entire booking?</p>
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

        <!-- Partial Cancel Dialog -->
        <v-dialog v-model="partialCancelDialog" max-width="600">
            <v-card>
                <v-card-title class="text-h6">Cancel Selected Seats</v-card-title>
                <v-card-text>
                    <p>Select the seats you want to cancel:</p>
                    <p class="font-weight-bold mt-2">{{ selectedBooking?.event.name }}</p>

                    <div class="mt-4">
                        <v-row v-if="selectedBooking?.seat_details">
                            <v-col v-for="seat in selectedBooking.seat_details" :key="seat.id" cols="6" sm="4">
                                <v-checkbox v-model="selectedSeatsToCancel" :value="seat.seat_id"
                                    :label="`Row ${seat.row_number}, Seat ${seat.seat_number}`"
                                    hide-details></v-checkbox>
                            </v-col>
                        </v-row>
                    </div>

                    <v-alert v-if="selectedSeatsToCancel.length === selectedBooking?.seat_details?.length" type="info"
                        class="mt-4">
                        You're cancelling all seats. This will cancel the entire booking.
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn variant="text" @click="closePartialCancelDialog">Cancel</v-btn>
                    <v-btn color="warning" :loading="cancelling" :disabled="selectedSeatsToCancel.length === 0"
                        @click="confirmPartialCancel">
                        Cancel {{ selectedSeatsToCancel.length }} Seat(s)
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Snackbar -->
        <CommonNotificationSnackbar v-model="snackbar" :message="snackbarMessage" :color="snackbarColor"
            :timeout="3000" />
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'auth'
})

const { fetchMyBookings, cancelBooking, cancelPartialSeats, bookings } = useBookings()

const loading = ref(false)
const cancelling = ref(false)
const cancelDialog = ref(false)
const partialCancelDialog = ref(false)
const selectedBooking = ref<any>(null)
const selectedSeatsToCancel = ref<number[]>([])
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const error = ref('')

// Search and filter state
const searchQuery = ref('')
const statusFilter = ref('')
const statusOptions = [
    { title: 'All Statuses', value: '' },
    { title: 'Confirmed', value: 'confirmed' },
    { title: 'Cancelled', value: 'cancelled' }
]

// Computed property for filtered and searched bookings
const displayBookings = computed(() => {
    let filtered = bookings.value || []

    // Filter by status
    if (statusFilter.value) {
        filtered = filtered.filter(booking => booking.status === statusFilter.value)
    }

    // Filter by search query
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(booking =>
            booking.event?.name?.toLowerCase().includes(query) ||
            booking.event?.location?.toLowerCase().includes(query) ||
            booking.status?.toLowerCase().includes(query)
        )
    }

    return filtered
})

const loadBookings = async () => {
    loading.value = true
    error.value = ''
    try {
        const result = await fetchMyBookings()
        if (!result.success) {
            error.value = result.error
            snackbarMessage.value = result.error
            snackbarColor.value = 'error'
            snackbar.value = true
        }
    } catch (err: any) {
        error.value = 'Failed to load bookings'
        snackbarMessage.value = 'Failed to load bookings'
        snackbarColor.value = 'error'
        snackbar.value = true
    }
    loading.value = false
}

const openCancelDialog = (booking: any) => {
    selectedBooking.value = booking
    cancelDialog.value = true
}

const openPartialCancelDialog = (booking: any) => {
    selectedBooking.value = booking
    selectedSeatsToCancel.value = []
    partialCancelDialog.value = true
}

const closePartialCancelDialog = () => {
    partialCancelDialog.value = false
    selectedSeatsToCancel.value = []
    selectedBooking.value = null
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

const confirmPartialCancel = async () => {
    if (!selectedBooking.value || selectedSeatsToCancel.value.length === 0) return

    cancelling.value = true
    const result = await cancelPartialSeats(selectedBooking.value.id, selectedSeatsToCancel.value)
    cancelling.value = false

    if (result.success) {
        snackbarMessage.value = (result.data as any)?.message || 'Seats cancelled successfully'
        snackbarColor.value = 'success'
        snackbar.value = true
        closePartialCancelDialog()
        await loadBookings()
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
        snackbar.value = true
    }
}

// Search and filter handlers
const handleSearch = () => {
    // The computed property will automatically update when searchQuery changes
    // No additional logic needed here for basic search
}

const handleFilter = () => {
    // The computed property will automatically update when statusFilter changes
    // No additional logic needed here for basic filtering
}

onMounted(() => {
    loadBookings()
})
</script>
