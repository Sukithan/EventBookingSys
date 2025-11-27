<template>
    <v-card class="elevation-2">
        <v-card-title class="d-flex align-center justify-space-between">
            <div class="d-flex align-center">
                <v-icon class="mr-2">mdi-seat-outline</v-icon>
                <span>Seat Map</span>
            </div>
            <v-btn v-if="selectedSeats.length > 0" color="primary" @click="$emit('create-booking')" :disabled="loading">
                <v-icon start>mdi-ticket-confirmation</v-icon>
                Book {{ selectedSeats.length }} Seat{{ selectedSeats.length > 1 ? 's' : '' }}
            </v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-4">
            <!-- Legend -->
            <v-row class="mb-4">
                <v-col cols="12" sm="6" md="3" v-for="legend in legendItems" :key="legend.class">
                    <div class="d-flex align-center">
                        <div :class="['legend-box', legend.class]"></div>
                        <span class="ml-2 text-caption">{{ legend.label }}</span>
                    </div>
                </v-col>
            </v-row>

            <!-- Selected Seats Summary -->
            <v-expand-transition>
                <v-card v-if="selectedSeats.length > 0" variant="tonal" color="primary" class="mb-4">
                    <v-card-text class="pa-4">
                        <div class="d-flex justify-space-between align-center flex-wrap gap-2">
                            <div>
                                <div class="text-subtitle-2 mb-1">Selected Seats</div>
                                <div class="d-flex flex-wrap gap-1">
                                    <v-chip v-for="seatId in selectedSeats" :key="seatId" closable size="small"
                                        @click:close="removeSeatFromSelection(seatId)">
                                        {{ getSeatLabel(seatId) }}
                                    </v-chip>
                                </div>
                            </div>
                            <v-btn variant="text" color="error" size="small" @click="$emit('clear-selection')">
                                Clear Selection
                            </v-btn>
                        </div>
                    </v-card-text>
                </v-card>
            </v-expand-transition>

            <!-- Loading State -->
            <v-skeleton-loader v-if="loading" type="image"></v-skeleton-loader>

            <!-- Seat Map -->
            <div v-else class="seat-map-container">
                <div class="screen-indicator mb-8">
                    <div class="text-center text-caption text-grey-darken-2 mt-2">SCREEN</div>
                </div>

                <div class="seat-map">
                    <div v-for="(rowSeats, rowNumber) in groupedSeats" :key="rowNumber" class="seat-row">
                        <div class="row-label">{{ rowNumber }}</div>
                        <div class="seats-container">
                            <div v-for="seat in rowSeats" :key="seat.id" class="seat-wrapper">
                                <v-btn :class="getSeatClass(seat)" size="small" elevation="2" @click="toggleSeat(seat)"
                                    :loading="seatActionLoading === seat.id" :disabled="loading">
                                    {{ seat.seat_number }}
                                </v-btn>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Seat {
    id: number
    row_number: number
    seat_number: number
    is_available: boolean
    is_locked: boolean
    booking_info?: any
}

interface Props {
    seats: Seat[]
    selectedSeats: number[]
    loading?: boolean
    seatActionLoading?: number | null
}

const props = withDefaults(defineProps<Props>(), {
    loading: false,
    seatActionLoading: null
})

const emit = defineEmits<{
    'toggle-seat': [seat: Seat]
    'clear-selection': []
    'remove-seat': [seatId: number]
    'create-booking': []
}>()

const legendItems = [
    { class: 'seat-available', label: 'Available' },
    { class: 'seat-selected', label: 'Selected' },
    { class: 'seat-booked', label: 'Booked (Click for info)' },
    { class: 'seat-locked', label: 'Locked' }
]

const groupedSeats = computed(() => {
    const grouped: { [key: number]: Seat[] } = {}

    if (!Array.isArray(props.seats)) {
        return grouped
    }

    props.seats.forEach(seat => {
        if (!grouped[seat.row_number]) {
            grouped[seat.row_number] = []
        }
        grouped[seat.row_number].push(seat)
    })

    // Sort seats within each row
    Object.keys(grouped).forEach(row => {
        grouped[parseInt(row)].sort((a, b) => a.seat_number - b.seat_number)
    })

    return grouped
})

const getSeatClass = (seat: Seat) => {
    if (props.selectedSeats.includes(seat.id)) {
        return 'seat-selected'
    } else if (!seat.is_available) {
        return seat.is_locked ? 'seat-locked' : 'seat-booked'
    } else {
        return 'seat-available'
    }
}

const getSeatLabel = (seatId: number) => {
    const seat = props.seats.find(s => s.id === seatId)
    if (seat) {
        return `${seat.row_number}-${seat.seat_number}`
    }
    return `Seat ${seatId}`
}

const toggleSeat = (seat: Seat) => {
    emit('toggle-seat', seat)
}

const removeSeatFromSelection = (seatId: number) => {
    emit('remove-seat', seatId)
}
</script>

<style scoped>
.legend-box {
    width: 24px;
    height: 24px;
    border-radius: 4px;
    border: 2px solid;
}

.seat-available.legend-box {
    background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%);
    border-color: #43A047;
}

.seat-selected.legend-box {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    border-color: #1565C0;
}

.seat-booked.legend-box {
    background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
    border-color: #C62828;
}

.seat-locked.legend-box {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
    border-color: #EF6C00;
}

.screen-indicator {
    margin-bottom: 3rem;
    background: linear-gradient(90deg, transparent 0%, #424242 15%, #616161 50%, #424242 85%, transparent 100%);
    height: 6px;
    border-radius: 3px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.screen-indicator::after {
    content: '';
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 280px;
    height: 25px;
    background: linear-gradient(180deg, rgba(66, 66, 66, 0.8) 0%, transparent 100%);
    border-radius: 15px 15px 0 0;
}

.seat-map-container {
    max-width: 100%;
    overflow-x: auto;
    padding: 1rem;
    background: linear-gradient(to bottom, #f5f5f5 0%, #fafafa 100%);
    border-radius: 12px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
}

.seat-map {
    max-width: 100%;
    padding: 1rem 0;
}

.seat-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}

.row-label {
    width: 42px;
    text-align: center;
    font-weight: 700;
    color: #424242;
    font-size: 1.05rem;
    background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
    border-radius: 8px;
    padding: 8px 4px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
}

.seats-container {
    display: flex;
    gap: 0.35rem;
    flex-wrap: nowrap;
}

.seat-wrapper {
    position: relative;
}

.seat-available {
    background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%) !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3) !important;
    border: 2px solid #43A047 !important;
}

.seat-selected {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.5) !important;
    border: 2px solid #1565C0 !important;
    transform: scale(1.05);
}

.seat-locked {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%) !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(255, 152, 0, 0.3) !important;
    border: 2px solid #EF6C00 !important;
}

.seat-booked {
    background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%) !important;
    color: white !important;
    cursor: pointer !important;
    box-shadow: 0 2px 6px rgba(244, 67, 54, 0.3) !important;
    border: 2px solid #C62828 !important;
}

.seat-available:hover {
    background: linear-gradient(135deg, #45A049 0%, #388E3C 100%) !important;
    transform: scale(1.1);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.5) !important;
}

.seat-selected:hover {
    background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%) !important;
    transform: scale(1.08);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.seat-booked:hover {
    background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%) !important;
    transform: scale(1.1);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.5) !important;
}

.seat-locked:hover {
    transform: scale(1.05);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-btn.seat-available,
.v-btn.seat-selected,
.v-btn.seat-locked,
.v-btn.seat-booked {
    min-width: 44px !important;
    height: 44px !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

@media (max-width: 768px) {
    .seat-row {
        gap: 0.4rem;
    }

    .row-label {
        width: 32px;
        font-size: 0.9rem;
        min-height: 32px;
        padding: 4px 2px;
    }

    .v-btn.seat-available,
    .v-btn.seat-selected,
    .v-btn.seat-locked,
    .v-btn.seat-booked {
        min-width: 36px !important;
        height: 36px !important;
        font-size: 0.75rem !important;
    }

    .seats-container {
        gap: 0.25rem;
    }

    .seat-map-container {
        padding: 0.75rem;
    }
}
</style>
