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
                            <strong>Current Seats:</strong>
                            <div class="d-flex flex-wrap gap-1 mt-1">
                                <v-chip v-for="seat in booking.seat_details" :key="seat.id" size="small"
                                    :color="booking.status === 'confirmed' ? 'primary' : 'grey'"
                                    :closable="booking.status === 'confirmed'" @click:close="deleteSeat(seat.seat_id)">
                                    <v-icon start size="small">mdi-seat</v-icon>
                                    R{{ seat.row_number }}S{{ seat.seat_number }}
                                </v-chip>
                            </div>
                            <div v-if="booking.status === 'confirmed'" class="text-caption text-grey mt-2">
                                <v-icon size="small">mdi-information</v-icon>
                                Click the X on a seat to remove it from this booking
                            </div>
                            <div v-if="booking.status === 'confirmed' && booking.seat_details.length !== booking.seats_booked"
                                class="text-caption text-warning mt-1">
                                Note: Some seats may have been removed from this booking
                            </div>
                        </div>
                        <div v-else-if="booking.status === 'cancelled'" class="mb-2">
                            <v-alert type="info" variant="tonal" density="compact">
                                All seats have been cancelled for this booking
                            </v-alert>
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

                <!-- Event Details Section -->
                <v-divider class="my-4"></v-divider>
                <v-row v-if="booking.event">
                    <v-col cols="12">
                        <h3 class="text-h6 mb-3">Event Information</h3>
                    </v-col>
                    <v-col cols="12" md="6">
                        <div class="mb-2"><strong>Event Name:</strong> {{ booking.event.name }}</div>
                        <div class="mb-2"><strong>Location:</strong> {{ booking.event.location }}</div>
                        <div class="mb-2"><strong>Event Date:</strong> {{ formatDate(booking.event.event_date) }}</div>
                    </v-col>
                    <v-col cols="12" md="6">
                        <div class="mb-2"><strong>Price per Seat:</strong> ${{ booking.event.price?.toFixed(2) }}</div>
                        <div class="mb-2"><strong>Total Seats:</strong> {{ booking.event.total_seats }}</div>
                        <div class="mb-2"><strong>Available Seats:</strong> {{ booking.event.available_seats }}</div>
                    </v-col>
                </v-row>
                <v-row v-else>
                    <v-col cols="12">
                        <v-alert type="info" variant="tonal">
                            Event details not available
                        </v-alert>
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
const { deleteSeatBooking } = useAdmin()

interface Props {
    modelValue: boolean
    booking: any
    cancellingBooking?: number | null
}

interface Emits {
    'update:modelValue': [value: boolean]
    'cancel-booking': [booking: any]
    'seat-deleted': []
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const deletingSeatId = ref<number | null>(null)

const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const { formatDate, getStatusColor } = useFormatters()

const deleteSeat = async (seatId: number) => {
    if (!confirm('Are you sure you want to remove this seat from the booking? This action cannot be undone.')) {
        return
    }

    deletingSeatId.value = seatId

    try {
        const result = await deleteSeatBooking(seatId)
        if (result.success) {
            // Notify parent to refresh the booking list
            emit('seat-deleted')

            // Update local booking data
            if (props.booking.seat_details) {
                const index = props.booking.seat_details.findIndex((s: any) => s.seat_id === seatId)
                if (index > -1) {
                    props.booking.seat_details.splice(index, 1)
                }

                // If no seats left, close the dialog
                if (props.booking.seat_details.length === 0) {
                    show.value = false
                }
            }
        } else {
            alert(result.error || 'Failed to delete seat')
        }
    } catch (error: any) {
        alert(error.message || 'Failed to delete seat')
    } finally {
        deletingSeatId.value = null
    }
}
</script>