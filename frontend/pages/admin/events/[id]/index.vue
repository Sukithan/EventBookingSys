<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex align-center mb-6">
                    <v-btn icon="mdi-arrow-left" variant="text" @click="$router.go(-1)" class="mr-3"></v-btn>
                    <h1 class="text-h4 font-weight-bold">Event Details</h1>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" :to="`/admin/events/${route.params.id}/edit`">
                        <v-icon start>mdi-pencil</v-icon>
                        Edit Event
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article, actions"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="event">
            <!-- Event Info -->
            <v-col cols="12" md="8">
                <v-card class="mb-4">
                    <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="300"
                        cover></v-img>
                    <v-card-title class="text-h4">{{ event.name }}</v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-3" color="primary">mdi-calendar</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Date & Time</div>
                                        <div class="text-body-1 font-weight-medium">{{ formatDate(event.event_date) }}
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-3" color="primary">mdi-map-marker</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Location</div>
                                        <div class="text-body-1 font-weight-medium">{{ event.location }}</div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-3" color="primary">mdi-currency-usd</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Price</div>
                                        <div class="text-body-1 font-weight-medium">${{ event.price.toFixed(2) }}</div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center mb-3">
                                    <v-icon class="mr-3" color="primary">mdi-check-circle</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Status</div>
                                        <v-chip :color="event.is_active ? 'success' : 'error'" size="small">
                                            {{ event.is_active ? 'Active' : 'Inactive' }}
                                        </v-chip>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>

                        <v-divider class="my-4"></v-divider>

                        <div>
                            <h3 class="text-h6 mb-2">Description</h3>
                            <p class="text-body-1" v-if="event.description">{{ event.description }}</p>
                            <p class="text-body-2 text-grey" v-else>No description available</p>
                        </div>
                    </v-card-text>
                </v-card>

                <!-- Bookings List -->
                <v-card>
                    <v-card-title class="d-flex align-center justify-space-between">
                        <span>Event Bookings</span>
                        <v-chip color="primary">{{ bookings.length }} Bookings</v-chip>
                    </v-card-title>
                    <v-card-text>
                        <v-data-table v-if="bookings.length > 0" :headers="bookingHeaders" :items="bookings"
                            :items-per-page="10" class="elevation-0">
                            <template v-slot:item.booking_date="{ item }">
                                {{ formatDate(item.booking_date) }}
                            </template>
                            <template v-slot:item.total_price="{ item }">
                                ${{ item.total_price.toFixed(2) }}
                            </template>
                            <template v-slot:item.status="{ item }">
                                <v-chip :color="getStatusColor(item.status)" size="small">
                                    {{ item.status }}
                                </v-chip>
                            </template>
                            <template v-slot:item.actions="{ item }">
                                <v-btn icon="mdi-cancel" size="small" variant="text" color="error"
                                    @click="cancelBookingConfirm(item)" :disabled="item.status === 'cancelled'"
                                    title="Cancel Booking"></v-btn>
                            </template>
                        </v-data-table>

                        <div v-else class="text-center py-8">
                            <v-icon size="60" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                            <p class="text-body-1 text-grey mt-2">No bookings yet</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Stats & Actions -->
            <v-col cols="12" md="4">
                <v-card class="mb-4">
                    <v-card-title>Event Statistics</v-card-title>
                    <v-card-text>
                        <div class="text-center mb-4">
                            <v-progress-circular :size="120" :width="12" :model-value="occupancyPercentage"
                                color="primary">
                                <span class="text-h5">{{ Math.round(occupancyPercentage) }}%</span>
                            </v-progress-circular>
                            <p class="text-body-2 mt-2">Occupancy Rate</p>
                        </div>

                        <v-row class="text-center">
                            <v-col cols="4">
                                <div class="text-h6 text-primary">{{ event.total_seats }}</div>
                                <div class="text-caption">Total</div>
                            </v-col>
                            <v-col cols="4">
                                <div class="text-h6 text-error">{{ event.total_seats - event.available_seats }}</div>
                                <div class="text-caption">Booked</div>
                            </v-col>
                            <v-col cols="4">
                                <div class="text-h6 text-success">{{ event.available_seats }}</div>
                                <div class="text-caption">Available</div>
                            </v-col>
                        </v-row>

                        <v-divider class="my-4"></v-divider>

                        <div class="d-flex justify-space-between align-center">
                            <span class="text-body-2">Total Revenue:</span>
                            <span class="text-h6 text-primary">${{ totalRevenue.toFixed(2) }}</span>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card class="mb-4">
                    <v-card-title>Quick Actions</v-card-title>
                    <v-card-text>
                        <div class="d-flex flex-column gap-2">
                            <v-btn color="primary" variant="outlined" :to="`/admin/events/${route.params.id}/edit`">
                                <v-icon start>mdi-pencil</v-icon>
                                Edit Event
                            </v-btn>
                            <v-btn color="info" variant="outlined" :to="`/admin/events/${route.params.id}/seats`">
                                <v-icon start>mdi-seat</v-icon>
                                Manage Seats
                            </v-btn>
                            <v-btn color="orange" variant="outlined" @click="exportBookings">
                                <v-icon start>mdi-download</v-icon>
                                Export Bookings
                            </v-btn>
                            <v-btn color="error" variant="outlined" @click="toggleEventStatus">
                                <v-icon start>{{ event.is_active ? 'mdi-pause' : 'mdi-play' }}</v-icon>
                                {{ event.is_active ? 'Deactivate' : 'Activate' }} Event
                            </v-btn>
                        </div>
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
const { fetchEventById, updateEvent } = useEvents()
const { fetchEventBookings, cancelBooking } = useAdmin()

const loading = ref(false)
const cancelling = ref(false)
const event = ref<any>(null)
const bookings = ref<any[]>([])
const cancelDialog = ref(false)
const selectedBooking = ref<any>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const bookingHeaders = [
    { title: 'User', value: 'user.full_name', key: 'user.full_name' },
    { title: 'Booking Date', value: 'booking_date', key: 'booking_date' },
    { title: 'Seats', value: 'seats_booked', key: 'seats_booked' },
    { title: 'Total', value: 'total_price', key: 'total_price' },
    { title: 'Status', value: 'status', key: 'status' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]

const occupancyPercentage = computed(() => {
    if (!event.value) return 0
    return ((event.value.total_seats - event.value.available_seats) / event.value.total_seats) * 100
})

const totalRevenue = computed(() => {
    return bookings.value
        .filter(booking => booking.status === 'confirmed')
        .reduce((sum, booking) => sum + booking.total_price, 0)
})

const loadEvent = async () => {
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

const cancelBookingConfirm = (booking: any) => {
    selectedBooking.value = booking
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
        await loadEvent() // Reload data
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const exportBookings = () => {
    // Create CSV content
    const csvContent = [
        ['User', 'Email', 'Booking Date', 'Seats', 'Total', 'Status'],
        ...bookings.value.map(booking => [
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
    a.download = `${event.value?.name || 'event'}-bookings.csv`
    a.click()
    window.URL.revokeObjectURL(url)
}

const toggleEventStatus = async () => {
    if (!event.value) return

    const eventData = {
        ...event.value,
        is_active: !event.value.is_active
    }

    const result = await updateEvent(event.value.id, eventData)

    if (result.success) {
        snackbarMessage.value = `Event ${eventData.is_active ? 'activated' : 'deactivated'} successfully`
        snackbarColor.value = 'success'
        await loadEvent()
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
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
    loadEvent()
})
</script>