<template>
    <v-card>
        <v-card-text>
            <v-data-table :headers="headers" :items="bookings" :items-per-page="itemsPerPage" class="elevation-0"
                :row-class="getRowClass" :loading="loading" :items-per-page-options="[10, 25, 50, 100]">
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

                <template v-slot:item.status="{ item }">
                    <v-chip :color="getStatusColor(item.status)" size="small">
                        {{ item.status.toUpperCase() }}
                    </v-chip>
                </template>

                <template v-slot:item.actions="{ item }">
                    <div class="d-flex gap-2">
                        <v-btn v-if="item.status === 'confirmed'" color="error" size="small" variant="outlined"
                            :loading="cancellingBooking === item.id" @click.stop="handleCancelBooking(item)">
                            Cancel
                        </v-btn>
                        <v-btn v-else-if="item.status === 'cancelled'" color="grey" size="small" variant="outlined"
                            disabled>
                            Cancelled
                        </v-btn>
                        <v-btn color="info" size="small" variant="outlined" @click.stop="handleViewDetails(item)">
                            Details
                        </v-btn>
                    </div>
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
    console.log('Emitting cancel-booking event')
    emit('cancel-booking', booking)
    console.log('Event emitted')
}

const handleViewDetails = (booking: any) => {
    console.log('BookingDataTable: View details clicked:', booking)
    emit('view-details', booking)
}

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