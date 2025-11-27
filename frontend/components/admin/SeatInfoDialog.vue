<template>
    <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="700"
        :fullscreen="$vuetify.display.xs">
        <v-card v-if="seatInfo" elevation="24">
            <v-card-title class="text-h5 bg-gradient-info text-white d-flex align-center pa-5">
                <v-icon start size="large">mdi-information</v-icon>
                <div>
                    <div>Seat Information</div>
                    <div class="text-subtitle-2 font-weight-regular">{{ seatInfo.seat.row_number }}-{{
                        seatInfo.seat.seat_number }}</div>
                </div>
            </v-card-title>

            <v-divider></v-divider>

            <v-card-text class="pa-6">
                <v-row>
                    <v-col cols="12">
                        <v-card variant="tonal" color="info" class="mb-4">
                            <v-card-text>
                                <div class="text-h6 mb-2">Seat Details</div>
                                <v-row dense>
                                    <v-col cols="6" sm="4">
                                        <div class="text-caption text-grey-darken-1">Row</div>
                                        <div class="text-body-1 font-weight-medium">{{ seatInfo.seat.row_number }}</div>
                                    </v-col>
                                    <v-col cols="6" sm="4">
                                        <div class="text-caption text-grey-darken-1">Seat Number</div>
                                        <div class="text-body-1 font-weight-medium">{{ seatInfo.seat.seat_number }}
                                        </div>
                                    </v-col>
                                    <v-col cols="12" sm="4">
                                        <div class="text-caption text-grey-darken-1">Status</div>
                                        <v-chip :color="seatInfo.seat.is_available ? 'success' : 'error'" size="small">
                                            {{ seatInfo.seat.is_available ? 'Available' : 'Booked' }}
                                        </v-chip>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>

                    <v-col cols="12">
                        <v-card variant="outlined">
                            <v-card-text>
                                <div class="text-h6 mb-3">Booking Information</div>
                                <v-row dense>
                                    <v-col cols="12" sm="6">
                                        <div class="mb-3">
                                            <div class="text-caption text-grey-darken-1">Booking ID</div>
                                            <div class="text-body-1 font-weight-medium">#{{ seatInfo.booking.id }}</div>
                                        </div>
                                        <div class="mb-3">
                                            <div class="text-caption text-grey-darken-1">Customer Name</div>
                                            <div class="text-body-1">{{ seatInfo.booking.user?.full_name ||
                                                seatInfo.booking.user?.username || 'N/A' }}</div>
                                        </div>
                                        <div>
                                            <div class="text-caption text-grey-darken-1">Email</div>
                                            <div class="text-body-1">{{ seatInfo.booking.user?.email || 'N/A' }}</div>
                                        </div>
                                    </v-col>
                                    <v-col cols="12" sm="6">
                                        <div class="mb-3">
                                            <div class="text-caption text-grey-darken-1">Total Seats</div>
                                            <div class="text-body-1 font-weight-medium">{{
                                                seatInfo.booking.seats_booked }}</div>
                                        </div>
                                        <div class="mb-3">
                                            <div class="text-caption text-grey-darken-1">Total Price</div>
                                            <div class="text-body-1 font-weight-medium text-success">${{
                                                seatInfo.booking.total_price?.toFixed(2) }}</div>
                                        </div>
                                        <div>
                                            <div class="text-caption text-grey-darken-1">Status</div>
                                            <v-chip :color="getStatusColor(seatInfo.booking.status)" size="small">
                                                {{ seatInfo.booking.status }}
                                            </v-chip>
                                        </div>
                                    </v-col>
                                    <v-col cols="12">
                                        <div>
                                            <div class="text-caption text-grey-darken-1">Booking Date</div>
                                            <div class="text-body-1">{{ formatDate(seatInfo.booking.booking_date) }}
                                            </div>
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="pa-5 bg-grey-lighten-4 flex-column flex-sm-row gap-2">
                <v-spacer></v-spacer>
                <v-btn variant="text" size="large" @click="$emit('update:modelValue', false)">
                    Close
                </v-btn>
                <v-btn color="primary" size="large" variant="elevated" @click="$emit('view-booking', seatInfo.booking)">
                    <v-icon start>mdi-eye</v-icon>
                    View Full Booking
                </v-btn>
                <v-btn v-if="seatInfo.booking.status !== 'cancelled'" color="error" size="large" variant="elevated"
                    @click="$emit('cancel-seat', seatInfo.seat)">
                    <v-icon start>mdi-close-circle</v-icon>
                    Remove This Seat
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
interface Props {
    modelValue: boolean
    seatInfo: any
}

defineProps<Props>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    'view-booking': [booking: any]
    'cancel-seat': [seat: any]
}>()

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
</script>

<style scoped>
.bg-gradient-info {
    background: linear-gradient(135deg, #0288D1 0%, #0277BD 100%);
}
</style>
