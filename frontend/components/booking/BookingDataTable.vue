<template>
    <v-card>
        <v-card-text>
            <v-data-table :headers="headers" :items="bookings" :items-per-page="itemsPerPage" class="elevation-0"
                :row-class="getRowClass" :loading="loading" :items-per-page-options="[10, 25, 50, 100]" show-expand>
                <template v-slot:item.booking_date="{ item }">
                    {{ formatDate(item.booking_date) }}
                </template>

                <template v-slot:item.user="{ item }">
                    <div>
                        <div class="font-weight-medium">{{ item.user.full_name }}</div>
                        <div class="text-caption text-grey">{{ item.user.email }}</div>
                        <div class="text-caption text-grey">ID: {{ item.user.id }} | @{{ item.user.username }}</div>
                    </div>
                </template>

                <template v-slot:item.total_price="{ item }">
                    ${{ item.total_price.toFixed(2) }}
                </template>

                <template v-slot:item.event="{ item }">
                    <div>
                        <div class="font-weight-medium">{{ item.event?.name || `Event #${item.event_id}` }}</div>
                        <div class="text-caption text-grey">{{ item.event?.location || 'N/A' }}</div>
                        <div class="text-caption text-grey">{{ item.event?.event_date ?
                            formatDate(item.event.event_date) : 'N/A' }}</div>
                    </div>
                </template>

                <template v-slot:item.seats="{ item }">
                    <div>
                        <div class="font-weight-medium mb-1">{{ item.seats_booked }} seat(s)</div>
                        <div v-if="item.seat_details && item.seat_details.length > 0" class="d-flex flex-wrap gap-1">
                            <v-chip v-for="seat in item.seat_details.slice(0, 3)" :key="seat.id" size="x-small"
                                :color="item.status === 'confirmed' ? 'primary' : 'grey'">
                                R{{ seat.row_number }}S{{ seat.seat_number }}
                            </v-chip>
                            <v-chip v-if="item.seat_details.length > 3" size="x-small" color="grey">
                                +{{ item.seat_details.length - 3 }}
                            </v-chip>
                        </div>
                        <div v-else class="text-caption text-grey">
                            No seat details
                        </div>
                    </div>
                </template>

                <template v-slot:item.status="{ item }">
                    <div>
                        <v-chip :color="getStatusColor(item.status)" size="small">
                            {{ item.status.toUpperCase() }}
                        </v-chip>
                        <div v-if="item.status === 'cancelled'" class="text-caption text-grey mt-1">
                            Cancelled booking
                        </div>
                    </div>
                </template>

                <template v-slot:item.actions="{ item }">
                    <div class="d-flex flex-wrap gap-1">
                        <v-btn v-if="item.status === 'confirmed'" color="error" size="small" variant="tonal"
                            :loading="cancellingBooking === item.id" @click.stop="() => handleCancelBooking(item)">
                            <v-icon start size="small">mdi-cancel</v-icon>
                            Cancel
                        </v-btn>
                        <v-chip v-else-if="item.status === 'cancelled'" color="grey" size="small" variant="flat">
                            Cancelled
                        </v-chip>
                        <v-btn color="primary" size="small" variant="outlined"
                            @click.stop="() => handleViewDetails(item)">
                            <v-icon start size="small">mdi-information</v-icon>
                            Details
                        </v-btn>
                    </div>
                </template>

                <template v-slot:expanded-row="{ item }">
                    <tr>
                        <td :colspan="headers.length + 1" class="pa-4 bg-grey-lighten-5">
                            <v-row>
                                <v-col cols="12" md="6">
                                    <h4 class="text-subtitle-1 mb-2">
                                        <v-icon size="small" color="primary">mdi-account</v-icon>
                                        Complete User Information
                                    </h4>
                                    <div class="mb-1"><strong>Full Name:</strong> {{ item.user.full_name }}</div>
                                    <div class="mb-1"><strong>Email:</strong> {{ item.user.email }}</div>
                                    <div class="mb-1"><strong>Username:</strong> @{{ item.user.username }}</div>
                                    <div class="mb-1"><strong>User ID:</strong> {{ item.user.id }}</div>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <h4 class="text-subtitle-1 mb-2">
                                        <v-icon size="small" color="primary">mdi-ticket</v-icon>
                                        Complete Booking Information
                                    </h4>
                                    <div class="mb-1"><strong>Booking ID:</strong> {{ item.id }}</div>
                                    <div class="mb-1"><strong>Event ID:</strong> {{ item.event_id }}</div>
                                    <div class="mb-1"><strong>Seats Booked:</strong> {{ item.seats_booked }}</div>
                                    <div class="mb-1"><strong>Total Price:</strong> ${{ item.total_price.toFixed(2) }}
                                    </div>
                                    <div class="mb-1"><strong>Booking Date:</strong> {{ formatDate(item.booking_date) }}
                                    </div>
                                    <div class="mb-1">
                                        <strong>Status:</strong>
                                        <v-chip :color="getStatusColor(item.status)" size="small" class="ml-2">
                                            {{ item.status.toUpperCase() }}
                                        </v-chip>
                                    </div>
                                </v-col>
                                <v-col cols="12" v-if="item.seat_details && item.seat_details.length > 0">
                                    <h4 class="text-subtitle-1 mb-2">
                                        <v-icon size="small" color="primary">mdi-seat</v-icon>
                                        All Booked Seats
                                    </h4>
                                    <div class="d-flex flex-wrap gap-2">
                                        <v-chip v-for="seat in item.seat_details" :key="seat.id" size="small"
                                            :color="item.status === 'confirmed' ? 'primary' : 'grey'">
                                            <v-icon start size="small">mdi-seat</v-icon>
                                            Row {{ seat.row_number }}, Seat {{ seat.seat_number }}
                                        </v-chip>
                                    </div>
                                </v-col>
                                <v-col cols="12" v-if="item.event">
                                    <h4 class="text-subtitle-1 mb-2">
                                        <v-icon size="small" color="primary">mdi-calendar-star</v-icon>
                                        Event Details
                                    </h4>
                                    <div class="mb-1"><strong>Event Name:</strong> {{ item.event.name }}</div>
                                    <div class="mb-1"><strong>Location:</strong> {{ item.event.location }}</div>
                                    <div class="mb-1"><strong>Event Date:</strong> {{ formatDate(item.event.event_date)
                                        }}</div>
                                    <div class="mb-1"><strong>Price per Seat:</strong> ${{ item.event.price?.toFixed(2)
                                        }}</div>
                                </v-col>
                            </v-row>
                        </td>
                    </tr>
                </template>

                <template v-slot:no-data>
                    <div class="text-center pa-4">
                        <v-icon size="64" color="grey-lighten-1">mdi-magnify</v-icon>
                        <p class="text-h6 mt-2">No bookings found</p>
                        <p class="text-body-2 text-grey">Try adjusting your search or filters</p>
                    </div>
                </template>
            </v-data-table>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    bookings: any[]
    loading?: boolean
    itemsPerPage?: number
    cancellingBooking?: number | null
    search?: string
}

interface Emits {
    'cancel-booking': [booking: any]
    'view-details': [booking: any]
}

const props = withDefaults(defineProps<Props>(), {
    itemsPerPage: 10,
    search: ''
})

const emit = defineEmits<Emits>()

const handleCancelBooking = (booking: any) => {
    console.log('=== BookingDataTable: Cancel button clicked ===')
    console.log('Booking object:', booking)
    console.log('Booking ID:', booking?.id)
    console.log('Booking status:', booking?.status)
    console.log('Emitting cancel-booking event with booking:', booking)
    emit('cancel-booking', booking)
    console.log('Event emitted successfully')
}

const handleViewDetails = (booking: any) => {
    console.log('BookingDataTable: View details clicked:', booking)
    emit('view-details', booking)
}

const headers = [
    { title: 'ID', value: 'id', key: 'id', width: 80 },
    { title: 'User Details', value: 'user', key: 'user', width: 220 },
    { title: 'Event Details', value: 'event', key: 'event', width: 250 },
    { title: 'Seats Booked', value: 'seats', key: 'seats', width: 180 },
    { title: 'Total', value: 'total_price', key: 'total_price', width: 100 },
    { title: 'Status', value: 'status', key: 'status', width: 130 },
    { title: 'Booked On', value: 'booking_date', key: 'booking_date', width: 170 },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false, width: 200 }
]

const { formatDate, getStatusColor } = useFormatters()

const getRowClass = (item: any) => {
    return item.status === 'cancelled' ? 'cancelled-row' : ''
}
</script>

<style scoped>
:deep(.cancelled-row) {
    opacity: 0.7;
    background-color: rgba(244, 67, 54, 0.05) !important;
}

:deep(.cancelled-row:hover) {
    background-color: rgba(244, 67, 54, 0.1) !important;
}
</style>