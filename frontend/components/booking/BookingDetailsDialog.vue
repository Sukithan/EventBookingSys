<template>
    <v-dialog v-model="show" max-width="700" :fullscreen="display.xs.value">
        <v-card v-if="booking">
            <v-card-title class="text-h5 bg-primary text-white">
                <v-icon start>mdi-ticket</v-icon>
                Booking Details #{{ booking.id }}
            </v-card-title>
            <v-card-text class="pa-6">
                <v-row>
                    <v-col cols="12" md="6">
                        <h3 class="text-h6 mb-3">User Information</h3>
                        <div class="mb-2"><strong>Name:</strong> {{ booking.user?.full_name }}</div>
                        <div class="mb-2"><strong>Email:</strong> {{ booking.user?.email }}</div>
                        <div class="mb-2"><strong>Username:</strong> @{{ booking.user?.username }}</div>
                        <div class="mb-2"><strong>User ID:</strong> {{ booking.user?.id }}</div>
                    </v-col>
                    <v-col cols="12" md="6">
                        <h3 class="text-h6 mb-3">Booking Information</h3>
                        <div class="mb-2"><strong>Booking ID:</strong> {{ booking.id }}</div>
                        <div class="mb-2"><strong>Event ID:</strong> {{ booking.event_id }}</div>
                        <div class="mb-2"><strong>Seats Booked:</strong> {{ booking.seats_booked }}</div>
                        <div v-if="booking.seat_details && booking.seat_details.length > 0" class="mb-2">
                            <strong>Seat Numbers:</strong>
                            <div class="d-flex flex-wrap gap-1 mt-1">
                                <v-chip v-for="seat in booking.seat_details" :key="seat.id" size="x-small"
                                    color="primary">
                                    R{{ seat.row_number }}S{{ seat.seat_number }}
                                </v-chip>
                            </div>
                        </div>
                        <div class="mb-2"><strong>Total Price:</strong> ${{ booking.total_price?.toFixed(2) }}</div>
                        <div class="mb-2">
                            <strong>Status:</strong>
                            <v-chip :color="getStatusColor(booking.status)" size="small">
                                {{ booking.status?.toUpperCase() }}
                            </v-chip>
                        </div>
                        <div class="mb-2"><strong>Booked On:</strong> {{ formatDate(booking.booking_date) }}</div>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-if="booking.status === 'confirmed'" color="error" variant="outlined"
                    :loading="cancellingBooking === booking.id" @click="$emit('cancel-booking', booking)">
                    Cancel This Booking
                </v-btn>
                <v-chip v-else-if="booking.status === 'cancelled'" color="error" size="small">
                    Booking Cancelled
                </v-chip>
                <v-btn variant="text" @click="show = false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

const display = useDisplay()

interface Props {
    modelValue: boolean
    booking: any
    cancellingBooking?: number | null
}

interface Emits {
    'update:modelValue': [value: boolean]
    'cancel-booking': [booking: any]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const { formatDate, getStatusColor } = useFormatters()
</script>