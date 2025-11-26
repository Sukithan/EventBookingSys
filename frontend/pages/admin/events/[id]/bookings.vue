<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex align-center mb-6">
                    <v-btn icon="mdi-arrow-left" variant="text" @click="$router.go(-1)" class="mr-3"></v-btn>
                    <h1 class="text-h4 font-weight-bold">Event Bookings</h1>
                    <v-spacer></v-spacer>
                    <v-btn color="secondary" variant="outlined" @click="recalculateStats" class="mr-2"
                        :loading="recalculatingStats">
                        <v-icon start>mdi-calculator</v-icon>
                        Recalculate Stats
                    </v-btn>
                    <v-btn color="primary" variant="outlined" @click="exportBookings">
                        <v-icon start>mdi-download</v-icon>
                        Export CSV
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="table"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12">
                <v-card>
                    <v-card-title class="d-flex align-center justify-space-between">
                        <span>{{ event?.name || 'Event' }} - Bookings</span>
                        <v-chip color="primary">{{ bookings.length }} Total Bookings</v-chip>
                    </v-card-title>

                    <v-card-text>
                        <v-row class="mb-4">
                            <v-col cols="12" sm="4">
                                <v-text-field v-model="search" label="Search users..." prepend-inner-icon="mdi-magnify"
                                    variant="outlined" hide-details clearable></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="4">
                                <v-select v-model="statusFilter" :items="statusOptions" label="Filter by status"
                                    variant="outlined" hide-details clearable></v-select>
                            </v-col>
                        </v-row>

                        <v-data-table v-if="filteredBookings.length > 0" :headers="headers" :items="filteredBookings"
                            :items-per-page="15" :search="search" class="elevation-0">
                            <template v-slot:item.user="{ item }">
                                <div>
                                    <div class="font-weight-medium">{{ item.user?.full_name || item.user?.username }}
                                    </div>
                                    <div class="text-caption text-grey">{{ item.user?.email }}</div>
                                </div>
                            </template>

                            <template v-slot:item.booking_date="{ item }">
                                {{ formatDate(item.booking_date) }}
                            </template>

                            <template v-slot:item.seats_booked="{ item }">
                                <v-chip size="small" color="info">{{ item.seats_booked }} seats</v-chip>
                            </template>

                            <template v-slot:item.total_price="{ item }">
                                <span class="font-weight-bold">${{ item.total_price.toFixed(2) }}</span>
                            </template>

                            <template v-slot:item.status="{ item }">
                                <v-chip :color="getStatusColor(item.status)" size="small">
                                    {{ item.status }}
                                </v-chip>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <v-btn icon="mdi-eye" size="small" variant="text" @click="viewBookingDetails(item)"
                                    title="View Details"></v-btn>
                                <v-btn icon="mdi-seat" size="small" variant="text" color="primary"
                                    @click="manageSeatBookings(item)" title="Manage Seats"></v-btn>
                                <v-btn icon="mdi-cancel" size="small" variant="text" color="error"
                                    @click="cancelBookingConfirm(item)" :disabled="item.status === 'cancelled'"
                                    title="Cancel Booking"></v-btn>
                            </template>
                        </v-data-table>

                        <div v-else class="text-center py-12">
                            <v-icon size="80" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                            <p class="text-h6 text-grey mt-4">No bookings found</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Booking Details Dialog -->
        <v-dialog v-model="detailsDialog" max-width="600">
            <v-card v-if="selectedBooking">
                <v-card-title class="text-h5">Booking Details</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Booking ID</div>
                                <div class="text-body-1">#{{ selectedBooking.id }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Status</div>
                                <v-chip :color="getStatusColor(selectedBooking.status)" size="small">
                                    {{ selectedBooking.status }}
                                </v-chip>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Customer</div>
                                <div class="text-body-1">{{ selectedBooking.user?.full_name ||
                                    selectedBooking.user?.username }}
                                </div>
                                <div class="text-caption">{{ selectedBooking.user?.email }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Booking Date</div>
                                <div class="text-body-1">{{ formatDate(selectedBooking.booking_date) }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Seats Booked</div>
                                <div class="text-body-1">{{ selectedBooking.seats_booked }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Total Price</div>
                                <div class="text-h6 text-primary">${{ selectedBooking.total_price.toFixed(2) }}</div>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="detailsDialog = false">Close</v-btn>
                    <v-btn color="error" v-if="selectedBooking.status !== 'cancelled'"
                        @click="cancelBookingFromDetails">
                        Cancel Booking
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Seat Management Dialog -->
        <v-dialog v-model="seatManagementDialog" max-width="800">
            <v-card v-if="selectedBooking">
                <v-card-title class="text-h5">Manage Seat Bookings</v-card-title>
                <v-card-subtitle>
                    {{ selectedBooking.user?.full_name || selectedBooking.user?.username }} -
                    {{ selectedBooking.user?.email }}
                </v-card-subtitle>
                <v-card-text>
                    <div v-if="seatDetails.length > 0">
                        <h6 class="text-h6 mb-3">Booked Seats</h6>
                        <div class="d-flex flex-wrap gap-2 mb-4">
                            <v-chip v-for="seat in seatDetails" :key="seat.id" color="primary" closable
                                @click:close="confirmDeleteSeat(seat)">
                                Row {{ String.fromCharCode(64 + seat.row_number) }} - Seat {{ seat.seat_number }}
                            </v-chip>
                        </div>
                        <v-alert type="info" variant="tonal">
                            Click the X on any seat chip to remove that specific seat from this booking.
                        </v-alert>
                    </div>
                    <div v-else class="text-center py-4">
                        <v-icon size="60" color="grey">mdi-seat-outline</v-icon>
                        <p class="text-grey mt-2">No seat details available</p>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="seatManagementDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Delete Seat Confirmation Dialog -->
        <v-dialog v-model="deleteSeatDialog" max-width="500">
            <v-card v-if="selectedSeat">
                <v-card-title class="text-h5">Remove Seat</v-card-title>
                <v-card-text>
                    <p>Are you sure you want to remove this seat from the booking?</p>
                    <div class="mt-3 pa-3 bg-grey-lighten-4 rounded">
                        <p><strong>Seat:</strong> Row {{ String.fromCharCode(64 + selectedSeat.row_number) }} - Seat {{
                            selectedSeat.seat_number }}</p>
                        <p><strong>User:</strong> {{ selectedBooking?.user?.full_name || selectedBooking?.user?.username
                        }}</p>
                    </div>
                    <v-alert type="warning" variant="tonal" class="mt-3">
                        This will make the seat available for booking again and update the booking total.
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="deleteSeatDialog = false">Cancel</v-btn>
                    <v-btn color="error" :loading="deletingSeat" @click="confirmDeleteSeatBooking">
                        Remove Seat
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Cancel Booking Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5">Cancel Booking</v-card-title>
                <v-card-text>
                    <p>Are you sure you want to cancel this booking?</p>
                    <div v-if="selectedBooking" class="mt-3 pa-3 bg-grey-lighten-4 rounded">
                        <p><strong>User:</strong> {{ selectedBooking.user?.full_name || selectedBooking.user?.username
                            }}</p>
                        <p><strong>Seats:</strong> {{ selectedBooking.seats_booked }}</p>
                        <p><strong>Total:</strong> ${{ selectedBooking.total_price.toFixed(2) }}</p>
                    </div>
                    <v-alert type="warning" variant="tonal" class="mt-3">
                        This action cannot be undone. The seats will be made available for booking again.
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="cancelDialog = false">Cancel</v-btn>
                    <v-btn color="error" :loading="cancelling" @click="confirmCancelBooking">
                        Cancel Booking
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
const router = useRouter()
const { fetchEventById } = useEvents()
const { fetchEventBookings, cancelBooking } = useAdmin()

const loading = ref(false)
const cancelling = ref(false)
const deletingSeat = ref(false)
const recalculatingStats = ref(false)
const event = ref<any>(null)
const bookings = ref<any[]>([])
const search = ref('')
const statusFilter = ref('')
const detailsDialog = ref(false)
const cancelDialog = ref(false)
const seatManagementDialog = ref(false)
const deleteSeatDialog = ref(false)
const selectedBooking = ref<any>(null)
const selectedSeat = ref<any>(null)
const seatDetails = ref<any[]>([])
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const statusOptions = [
    { title: 'All', value: '' },
    { title: 'Confirmed', value: 'confirmed' },
    { title: 'Cancelled', value: 'cancelled' },
    { title: 'Pending', value: 'pending' }
]

const headers = [
    { title: 'Customer', value: 'user', key: 'user' },
    { title: 'Booking Date', value: 'booking_date', key: 'booking_date' },
    { title: 'Seats', value: 'seats_booked', key: 'seats_booked' },
    { title: 'Total', value: 'total_price', key: 'total_price' },
    { title: 'Status', value: 'status', key: 'status' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]

const filteredBookings = computed(() => {
    let filtered = bookings.value

    if (statusFilter.value) {
        filtered = filtered.filter(booking => booking.status === statusFilter.value)
    }

    return filtered
})

const loadData = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)

    const [eventResult, bookingsResult] = await Promise.all([
        fetchEventById(eventId),
        fetchEventBookings(eventId)
    ])

    if (eventResult.success) {
        event.value = eventResult.data
    }

    if (bookingsResult.success) {
        bookings.value = bookingsResult.data as any[]
    }

    loading.value = false
}

const viewBookingDetails = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = true
}

const cancelBookingConfirm = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = false
    cancelDialog.value = true
}

const cancelBookingFromDetails = () => {
    detailsDialog.value = false
    cancelDialog.value = true
}

const confirmCancelBooking = async () => {
    if (!selectedBooking.value) return

    cancelling.value = true
    const result = await cancelBooking(selectedBooking.value.id)
    cancelling.value = false

    if (result.success) {
        snackbarMessage.value = 'Booking cancelled successfully'
        snackbarColor.value = 'success'
        cancelDialog.value = false
        await loadData() // Reload data
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const manageSeatBookings = async (booking: any) => {
    selectedBooking.value = booking

    // Load seat details for this booking
    if (booking.seat_details && booking.seat_details.length > 0) {
        seatDetails.value = booking.seat_details.map((seat: any) => ({
            ...seat,
            seat_id: seat.seat_id || seat.id
        }))
    } else {
        // If seat details are not available, we need to fetch them
        seatDetails.value = []
    }

    seatManagementDialog.value = true
}

const confirmDeleteSeat = (seat: any) => {
    selectedSeat.value = seat
    deleteSeatDialog.value = true
}

const confirmDeleteSeatBooking = async () => {
    if (!selectedSeat.value) return

    deletingSeat.value = true
    const { deleteSeatBooking } = useAdmin()
    const result = await deleteSeatBooking(selectedSeat.value.seat_id)
    deletingSeat.value = false

    if (result.success) {
        snackbarMessage.value = 'Seat booking removed successfully'
        snackbarColor.value = 'success'
        deleteSeatDialog.value = false
        seatManagementDialog.value = false
        await loadData() // Reload data
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const recalculateStats = async () => {
    const eventId = parseInt(route.params.id as string)
    recalculatingStats.value = true

    const { recalculateEventStats } = useAdmin()
    const result = await recalculateEventStats(eventId)
    recalculatingStats.value = false

    if (result.success) {
        snackbarMessage.value = 'Event statistics recalculated successfully'
        snackbarColor.value = 'success'
        await loadData() // Reload data to show updated stats
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const exportBookings = () => {
    // Create CSV content
    const csvContent = [
        ['Booking ID', 'Customer Name', 'Email', 'Booking Date', 'Seats', 'Total', 'Status'],
        ...filteredBookings.value.map(booking => [
            booking.id,
            booking.user?.full_name || booking.user?.username || 'N/A',
            booking.user?.email || 'N/A',
            formatDate(booking.booking_date),
            booking.seats_booked,
            booking.total_price.toFixed(2),
            booking.status
        ])
    ].map(row => row.join(',')).join('\n')

    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${event.value?.name || 'event'}-bookings-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)

    snackbarMessage.value = 'Bookings exported successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'confirmed': return 'success'
        case 'cancelled': return 'error'
        case 'pending': return 'warning'
        default: return 'grey'
    }
}

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

onMounted(() => {
    loadData()
})
</script>