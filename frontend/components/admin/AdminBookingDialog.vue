<template>
    <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="650"
        :fullscreen="$vuetify.display.xs" persistent>
        <v-card elevation="24">
            <v-card-title class="text-h5 bg-gradient-primary text-white d-flex align-center pa-5">
                <v-icon start size="large">mdi-ticket-confirmation</v-icon>
                <div>
                    <div>Create Admin Booking</div>
                    <div class="text-subtitle-2 font-weight-regular">{{ eventName }}</div>
                </div>
            </v-card-title>

            <v-divider></v-divider>

            <v-card-text class="pa-6">
                <!-- Username Input -->
                <v-card variant="outlined" class="mb-4 pa-4 bg-blue-lighten-5">
                    <div class="text-subtitle-2 mb-2 font-weight-bold">Customer Information (Optional)</div>
                    <v-text-field v-model="localUsername" label="Username or Email"
                        placeholder="Leave empty to book as admin" variant="outlined" density="comfortable"
                        hide-details="auto" hint="Enter customer username/email or leave empty for admin booking">
                        <template #prepend-inner>
                            <v-icon>mdi-account</v-icon>
                        </template>
                    </v-text-field>
                    <div class="text-caption text-grey-darken-1 mt-2">
                        <v-icon size="small">mdi-information</v-icon>
                        If left empty, the booking will be created under your admin account
                    </div>
                </v-card>

                <!-- Booking Summary -->
                <v-card variant="tonal" color="primary" class="mb-4">
                    <v-card-text>
                        <div class="text-h6 mb-3">Booking Summary</div>
                        <v-row dense>
                            <v-col cols="6">
                                <div class="text-caption">Selected Seats</div>
                                <div class="text-h6">{{ selectedSeats.length }}</div>
                            </v-col>
                            <v-col cols="6">
                                <div class="text-caption">Total Price</div>
                                <div class="text-h6 text-success">${{ totalPrice.toFixed(2) }}</div>
                            </v-col>
                            <v-col cols="12">
                                <div class="text-caption mb-1">Seats:</div>
                                <div class="d-flex flex-wrap gap-1">
                                    <v-chip v-for="seatId in selectedSeats" :key="seatId" size="small" color="primary">
                                        {{ getSeatLabel(seatId) }}
                                    </v-chip>
                                </div>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>

                <!-- Error Alert -->
                <v-alert v-if="error" type="error" variant="tonal" dismissible class="mb-4"
                    @click:close="$emit('clear-error')">
                    {{ error }}
                </v-alert>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="pa-5 bg-grey-lighten-4">
                <v-spacer></v-spacer>
                <v-btn variant="text" size="large" @click="handleCancel" :disabled="loading">
                    Cancel
                </v-btn>
                <v-btn color="primary" size="large" variant="elevated" :loading="loading"
                    @click="$emit('confirm', localUsername)" :disabled="selectedSeats.length === 0">
                    <v-icon start>mdi-check</v-icon>
                    Confirm Booking
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
interface Props {
    modelValue: boolean
    eventName: string
    selectedSeats: number[]
    ticketPrice: number
    username?: string
    loading?: boolean
    error?: string
    seats: any[]
}

const props = withDefaults(defineProps<Props>(), {
    username: '',
    loading: false,
    error: ''
})

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    'confirm': [username: string]
    'clear-error': []
}>()

const localUsername = ref(props.username)

watch(() => props.username, (newVal) => {
    localUsername.value = newVal
})

const totalPrice = computed(() => {
    return props.selectedSeats.length * props.ticketPrice
})

const getSeatLabel = (seatId: number) => {
    const seat = props.seats.find(s => s.id === seatId)
    if (seat) {
        return `${seat.row_number}-${seat.seat_number}`
    }
    return `Seat ${seatId}`
}

const handleCancel = () => {
    localUsername.value = ''
    emit('update:modelValue', false)
}
</script>

<style scoped>
.bg-gradient-primary {
    background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
}
</style>
