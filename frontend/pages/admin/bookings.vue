<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h4 font-weight-bold mb-6">All Bookings</h1>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="table"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="bookings.length > 0">
            <v-col cols="12">
                <v-card>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="bookings" :items-per-page="10" class="elevation-0">
                            <template v-slot:item.booking_date="{ item }">
                                {{ formatDate(item.booking_date) }}
                            </template>

                            <template v-slot:item.user="{ item }">
                                <div>
                                    <div class="font-weight-medium">{{ item.user.full_name }}</div>
                                    <div class="text-caption text-grey">{{ item.user.email }}</div>
                                    <div class="text-caption text-grey">ID: {{ item.user.id }} | @{{ item.user.username
                                    }}</div>
                                </div>
                            </template>

                            <template v-slot:item.total_price="{ item }">
                                ${{ item.total_price.toFixed(2) }}
                            </template>

                            <template v-slot:item.status="{ item }">
                                <v-chip :color="item.status === 'confirmed' ? 'success' : 'error'" size="small">
                                    {{ item.status.toUpperCase() }}
                                </v-chip>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <div class="d-flex gap-2">
                                    <v-btn v-if="item.status === 'confirmed'" color="error" size="small"
                                        variant="outlined" :loading="cancellingBooking === item.id"
                                        @click="confirmCancelBooking(item)">
                                        Cancel
                                    </v-btn>
                                    <v-btn color="info" size="small" variant="outlined"
                                        @click="viewBookingDetails(item)">
                                        Details
                                    </v-btn>
                                </div>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                <p class="text-h6 text-grey mt-4">No bookings yet</p>
            </v-col>
        </v-row>

        <!-- Cancellation Confirmation Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5 bg-error text-white">
                    <v-icon start>mdi-alert</v-icon>
                    Cancel Booking
                </v-card-title>
                <v-card-text class="pa-6">
                    <p class="text-body-1">Are you sure you want to cancel this booking?</p>
                    <v-alert type="warning" variant="tonal" class="mt-4">
                        <strong>Booking Details:</strong><br>
                        User: {{ selectedBooking?.user?.full_name }}<br>
                        Booking ID: {{ selectedBooking?.id }}<br>
                        Seats: {{ selectedBooking?.seats_booked }}<br>
                        Total: ${{ selectedBooking?.total_price?.toFixed(2) }}
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn variant="text" @click="cancelDialog = false">Keep Booking</v-btn>
                    <v-btn color="error" :loading="!!cancellingBooking" @click="cancelBooking">Cancel Booking</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Booking Details Dialog -->
        <v-dialog v-model="detailsDialog" max-width="700">
            <v-card v-if="selectedBooking">
                <v-card-title class="text-h5 bg-primary text-white">
                    <v-icon start>mdi-ticket</v-icon>
                    Booking Details #{{ selectedBooking.id }}
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-row>
                        <v-col cols="12" md="6">
                            <h3 class="text-h6 mb-3">User Information</h3>
                            <div class="mb-2"><strong>Name:</strong> {{ selectedBooking.user?.full_name }}</div>
                            <div class="mb-2"><strong>Email:</strong> {{ selectedBooking.user?.email }}</div>
                            <div class="mb-2"><strong>Username:</strong> @{{ selectedBooking.user?.username }}</div>
                            <div class="mb-2"><strong>User ID:</strong> {{ selectedBooking.user?.id }}</div>
                        </v-col>
                        <v-col cols="12" md="6">
                            <h3 class="text-h6 mb-3">Booking Information</h3>
                            <div class="mb-2"><strong>Booking ID:</strong> {{ selectedBooking.id }}</div>
                            <div class="mb-2"><strong>Event ID:</strong> {{ selectedBooking.event_id }}</div>
                            <div class="mb-2"><strong>Seats Booked:</strong> {{ selectedBooking.seats_booked }}</div>
                            <div v-if="selectedBooking.seat_details && selectedBooking.seat_details.length > 0"
                                class="mb-2">
                                <strong>Seat Numbers:</strong>
                                <div class="d-flex flex-wrap gap-1 mt-1">
                                    <v-chip v-for="seat in selectedBooking.seat_details" :key="seat.id" size="x-small"
                                        color="primary">
                                        R{{ seat.row_number }}S{{ seat.seat_number }}
                                    </v-chip>
                                </div>
                            </div>
                            <div class="mb-2"><strong>Total Price:</strong> ${{ selectedBooking.total_price?.toFixed(2)
                            }}</div>
                            <div class="mb-2"><strong>Status:</strong>
                                <v-chip :color="selectedBooking.status === 'confirmed' ? 'success' : 'error'"
                                    size="small">
                                    {{ selectedBooking.status?.toUpperCase() }}
                                </v-chip>
                            </div>
                            <div class="mb-2"><strong>Booked On:</strong> {{ formatDate(selectedBooking.booking_date) }}
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn v-if="selectedBooking.status === 'confirmed'" color="error" variant="outlined"
                        :loading="cancellingBooking === selectedBooking.id"
                        @click="confirmCancelBooking(selectedBooking)">
                        Cancel This Booking
                    </v-btn>
                    <v-btn variant="text" @click="detailsDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Success/Error Snackbar -->
        <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="5000">
            {{ snackbarMessage }}
            <template v-slot:actions>
                <v-btn variant="text" @click="snackbar = false">Close</v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { fetchAllBookings } = useAdmin()
const { $api } = useNuxtApp()

const loading = ref(false)
const bookings = ref<any[]>([])
const cancelDialog = ref(false)
const detailsDialog = ref(false)
const selectedBooking = ref<any>(null)
const cancellingBooking = ref<number | null>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const headers = [
    { title: 'Booking ID', value: 'id', key: 'id' },
    { title: 'User', value: 'user', key: 'user' },
    { title: 'Event ID', value: 'event_id', key: 'event_id' },
    { title: 'Seats', value: 'seats_booked', key: 'seats_booked' },
    { title: 'Total Price', value: 'total_price', key: 'total_price' },
    { title: 'Status', value: 'status', key: 'status' },
    { title: 'Booked On', value: 'booking_date', key: 'booking_date' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]

const loadBookings = async () => {
    loading.value = true
    const result = await fetchAllBookings()
    if (result.success) {
        bookings.value = Array.isArray(result.data) ? (result.data as any[]) : []
    }
    loading.value = false
}

const confirmCancelBooking = (booking: any) => {
    selectedBooking.value = booking
    cancelDialog.value = true
}

const viewBookingDetails = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = true
}

const cancelBooking = async () => {
    if (!selectedBooking.value) return

    cancellingBooking.value = selectedBooking.value.id

    try {
        await $api(`/api/admin/bookings/${selectedBooking.value.id}`, {
            method: 'DELETE'
        })

        snackbarMessage.value = `Booking #${selectedBooking.value.id} cancelled successfully`
        snackbarColor.value = 'success'
        snackbar.value = true

        // Refresh bookings list
        await loadBookings()

        // Close dialogs
        cancelDialog.value = false
        detailsDialog.value = false

    } catch (error: any) {
        snackbarMessage.value = error.data?.detail || 'Failed to cancel booking'
        snackbarColor.value = 'error'
        snackbar.value = true
    } finally {
        cancellingBooking.value = null
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
    loadBookings()
})
</script>
