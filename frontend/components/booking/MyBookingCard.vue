<template>
    <v-card class="mb-4">
        <v-row no-gutters>
            <v-col cols="12" md="8">
                <v-card-title class="text-h6">{{ booking.event?.name || 'Event Name' }}</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <div class="mb-2">
                                <v-icon size="small" class="mr-2">mdi-calendar</v-icon>
                                <span class="text-body-2">{{ booking.event?.event_date ?
                                    formatDate(booking.event.event_date) : 'Date not available' }}</span>
                            </div>
                            <div class="mb-2">
                                <v-icon size="small" class="mr-2">mdi-map-marker</v-icon>
                                <span class="text-body-2">{{ booking.event?.location || 'Location not available'
                                    }}</span>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-2">
                                <v-icon size="small" class="mr-2">mdi-seat</v-icon>
                                <span class="text-body-2">{{ booking.seats_booked || 0 }} seat(s)</span>
                            </div>
                            <div class="mb-2" v-if="booking.seat_details && booking.seat_details.length > 0">
                                <v-icon size="small" class="mr-2">mdi-format-list-numbered</v-icon>
                                <span class="text-body-2">
                                    Seats:
                                    <v-chip v-for="seat in booking.seat_details" :key="seat.id" size="x-small"
                                        class="ma-1" color="primary" variant="outlined">
                                        {{ seat.row_number || 'N/A' }}-{{ seat.seat_number || 'N/A' }}
                                    </v-chip>
                                </span>
                            </div>
                            <div class="mb-2">
                                <v-icon size="small" class="mr-2">mdi-clock</v-icon>
                                <span class="text-body-2">Booked: {{ booking.booking_date ?
                                    formatDate(booking.booking_date) : 'Date not available' }}</span>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-col>

            <v-col cols="12" md="4" class="d-flex flex-column justify-center align-center pa-4 bg-grey-lighten-4">
                <div class="text-h5 text-primary mb-2">${{ booking.total_price?.toFixed(2) || '0.00' }}</div>
                <v-chip :color="booking.status === 'confirmed' ? 'success' : 'error'" class="mb-4">
                    {{ booking.status?.toUpperCase() || 'UNKNOWN' }}
                </v-chip>

                <div v-if="booking.status === 'confirmed'" class="d-flex flex-column gap-2 w-100">
                    <v-btn color="error" variant="outlined" size="small" @click="$emit('cancel-booking', booking)"
                        block>
                        <v-icon start>mdi-cancel</v-icon>
                        Cancel All
                    </v-btn>
                    <v-btn v-if="booking.seat_details && booking.seat_details.length > 1" color="warning"
                        variant="outlined" size="small" @click="$emit('partial-cancel', booking)" block>
                        <v-icon start>mdi-seat-outline</v-icon>
                        Cancel Seats
                    </v-btn>
                </div>
            </v-col>
        </v-row>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    booking: any
}

interface Emits {
    'cancel-booking': [booking: any]
    'partial-cancel': [booking: any]
}

defineProps<Props>()
defineEmits<Emits>()

const { formatLongDate: formatDate } = useFormatters()
</script>