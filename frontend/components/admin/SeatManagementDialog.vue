<template>
    <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="900"
        :fullscreen="$vuetify.display.xs">
        <v-card v-if="booking" elevation="24">
            <v-card-title class="text-h5 bg-gradient-info text-white d-flex align-center pa-5">
                <v-icon start size="large">mdi-seat-recline-extra</v-icon>
                <div>
                    <div>Manage Seats</div>
                    <div class="text-subtitle-2 font-weight-regular">Booking #{{ booking.id }}</div>
                </div>
            </v-card-title>

            <v-divider></v-divider>

            <v-card variant="flat" color="blue-lighten-5" class="ma-0">
                <v-card-text class="py-4 px-5">
                    <v-row dense>
                        <v-col cols="12" sm="6" md="3">
                            <div class="text-caption text-grey-darken-2">Customer</div>
                            <div class="text-body-1 font-weight-medium">
                                {{ booking.user?.full_name || booking.user?.username || 'N/A' }}
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6" md="3">
                            <div class="text-caption text-grey-darken-2">Total Seats</div>
                            <div class="text-body-1 font-weight-medium">
                                {{ seatDetails.length }} seat{{ seatDetails.length !== 1 ? 's' : '' }}
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6" md="3">
                            <div class="text-caption text-grey-darken-2">Total Price</div>
                            <div class="text-body-1 font-weight-medium text-success">
                                ${{ booking.total_price?.toFixed(2) }}
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6" md="3">
                            <div class="text-caption text-grey-darken-2">Status</div>
                            <v-chip :color="getStatusColor(booking.status)" size="small" class="mt-1">
                                {{ booking.status }}
                            </v-chip>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>

            <v-card-text class="pa-6">
                <div v-if="seatDetails.length > 0">
                    <div class="text-h6 mb-4">Booked Seats</div>
                    <v-row>
                        <v-col v-for="seat in seatDetails" :key="seat.id" cols="12" sm="6" md="4">
                            <v-card variant="outlined" class="pa-3">
                                <div class="d-flex justify-space-between align-center mb-2">
                                    <div>
                                        <v-chip color="primary" size="small" class="mb-1">
                                            Row {{ seat.row_number }} - Seat {{ seat.seat_number }}
                                        </v-chip>
                                    </div>
                                    <v-btn icon size="small" color="error" variant="text"
                                        @click="$emit('delete-seat', seat)" :disabled="deletingSeat">
                                        <v-icon>mdi-delete</v-icon>
                                    </v-btn>
                                </div>
                                <div class="text-caption text-grey-darken-1">
                                    Seat ID: {{ seat.id }}
                                </div>
                            </v-card>
                        </v-col>
                    </v-row>
                </div>
                <v-card v-else variant="outlined" class="text-center py-12">
                    <v-icon size="64" color="grey-lighten-1">mdi-seat-outline</v-icon>
                    <div class="text-h6 text-grey mt-2">No seats found for this booking</div>
                </v-card>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="pa-5 bg-grey-lighten-4">
                <v-spacer></v-spacer>
                <v-btn color="primary" size="large" variant="elevated" @click="$emit('close')">
                    <v-icon start>mdi-check</v-icon>
                    Done
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
interface Props {
    modelValue: boolean
    booking: any
    seatDetails: any[]
    deletingSeat?: boolean
}

withDefaults(defineProps<Props>(), {
    deletingSeat: false
})

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    'delete-seat': [seat: any]
    'close': []
}>()

const getStatusColor = (status: string) => {
    switch (status) {
        case 'confirmed': return 'success'
        case 'cancelled': return 'error'
        case 'pending': return 'warning'
        default: return 'grey'
    }
}
</script>

<style scoped>
.bg-gradient-info {
    background: linear-gradient(135deg, #0288D1 0%, #0277BD 100%);
}
</style>
