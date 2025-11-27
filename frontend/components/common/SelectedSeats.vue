<template>
    <v-card v-if="selectedSeats.length > 0" class="mb-4" color="primary" variant="tonal">
        <v-card-text>
            <div class="d-flex justify-space-between align-center mb-3">
                <h3 class="text-h6">Selected Seats ({{ selectedSeats.length }})</h3>
                <v-btn v-if="showClearButton" color="error" variant="text" size="small"
                    @click="$emit('clear-selection')">
                    <v-icon start>mdi-close</v-icon>
                    Clear All
                </v-btn>
            </div>

            <div class="seat-chips-grid">
                <v-chip v-for="seatId in selectedSeats" :key="seatId" color="primary" closable
                    @click:close="$emit('remove-seat', seatId)">
                    {{ getSeatLabel(seatId) }}
                </v-chip>
            </div>

            <div v-if="showBookingForm" class="mt-4">
                <v-divider class="mb-4"></v-divider>
                <v-text-field :model-value="username" label="Username (for admin booking)"
                    placeholder="Enter username to book for" :error-messages="errorMessage"
                    @update:model-value="$emit('update:username', $event)" />

                <div class="d-flex gap-2 mt-3">
                    <v-btn color="success" :loading="bookingLoading" :disabled="!username || selectedSeats.length === 0"
                        @click="$emit('book-seats')">
                        <v-icon start>mdi-ticket-confirmation</v-icon>
                        Book {{ selectedSeats.length }} Seat{{ selectedSeats.length !== 1 ? 's' : '' }}
                    </v-btn>
                    <v-btn variant="outlined" @click="$emit('clear-selection')">
                        Cancel
                    </v-btn>
                </div>
            </div>

            <div v-else-if="showTotal" class="mt-4">
                <v-divider class="mb-3"></v-divider>
                <div class="d-flex justify-space-between align-center">
                    <span class="text-h6">Total:</span>
                    <span class="text-h5 font-weight-bold">${{ totalPrice.toFixed(2) }}</span>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    selectedSeats: number[]
    seats?: any[]
    showClearButton?: boolean
    showBookingForm?: boolean
    showTotal?: boolean
    username?: string
    errorMessage?: string
    bookingLoading?: boolean
    seatPrice?: number
}

interface Emits {
    'clear-selection': []
    'remove-seat': [seatId: number]
    'update:username': [value: string]
    'book-seats': []
}

const props = withDefaults(defineProps<Props>(), {
    showClearButton: true,
    showBookingForm: false,
    showTotal: false,
    seatPrice: 0
})

defineEmits<Emits>()

const getSeatLabel = (seatId: number) => {
    if (!props.seats) return `Seat ${seatId}`

    const seat = props.seats.find(s => s.id === seatId)
    if (seat) {
        return `R${seat.row_number}S${seat.seat_number}`
    }
    return `Seat ${seatId}`
}

const totalPrice = computed(() => {
    return props.selectedSeats.length * props.seatPrice
})
</script>

<style scoped>
.seat-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
</style>