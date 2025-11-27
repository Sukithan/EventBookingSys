<template>
    <div class="seat-map-container">
        <!-- Screen indicator -->
        <div class="screen-indicator"></div>

        <div class="seat-map">
            <div v-for="(seatsInRow, rowNumber) in groupedSeats" :key="rowNumber" class="seat-row">
                <!-- Row label -->
                <div class="row-label">
                    {{ rowNumber }}
                </div>

                <!-- Seats in row -->
                <div class="seats-container">
                    <v-btn v-for="seat in seatsInRow" :key="seat.id" :class="getSeatClass(seat)"
                        :disabled="getSeatDisabled(seat)" :loading="seatActionLoading === seat.id"
                        @click="toggleSeat(seat)" min-width="44" height="44" variant="elevated" size="small">
                        {{ seat.seat_number }}
                    </v-btn>
                </div>
            </div>
        </div>

        <!-- Legend -->
        <v-row class="mt-4 px-2">
            <v-col cols="6" sm="3">
                <div class="d-flex align-center gap-2">
                    <div class="legend-seat seat-available"></div>
                    <span class="text-caption">Available</span>
                </div>
            </v-col>
            <v-col cols="6" sm="3">
                <div class="d-flex align-center gap-2">
                    <div class="legend-seat seat-selected"></div>
                    <span class="text-caption">Selected</span>
                </div>
            </v-col>
            <v-col cols="6" sm="3">
                <div class="d-flex align-center gap-2">
                    <div class="legend-seat seat-booked"></div>
                    <span class="text-caption">Booked</span>
                </div>
            </v-col>
            <v-col cols="6" sm="3">
                <div class="d-flex align-center gap-2">
                    <div class="legend-seat seat-locked"></div>
                    <span class="text-caption">Locked</span>
                </div>
            </v-col>
        </v-row>
    </div>
</template>

<script setup lang="ts">
interface Props {
    seats: any[]
    selectedSeats: number[]
    seatActionLoading?: number | null
    isAdmin?: boolean
}

interface Emits {
    'toggle-seat': [seat: any]
    'seat-click': [seat: any]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const groupedSeats = computed(() => {
    const grouped: { [key: number]: any[] } = {}

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

const getSeatClass = (seat: any) => {
    if (props.selectedSeats.includes(seat.id)) {
        return 'seat-selected'
    } else if (!seat.is_available) {
        return seat.is_locked ? 'seat-locked' : 'seat-booked'
    } else {
        return 'seat-available'
    }
}

const getSeatDisabled = (seat: any) => {
    // For regular users, disable booked/locked seats
    if (!props.isAdmin) {
        return !seat.is_available
    }

    // For admin, allow interaction with all seats
    return false
}

const toggleSeat = (seat: any) => {
    emit('toggle-seat', seat)
    emit('seat-click', seat)
}
</script>

<style scoped>
.seat-map-container {
    max-width: 100%;
    overflow-x: auto;
    padding: 1rem;
    background: linear-gradient(to bottom, #f5f5f5 0%, #fafafa 100%);
    border-radius: 12px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
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

:deep(.v-btn.seat-available),
:deep(.v-btn.seat-selected),
:deep(.v-btn.seat-locked),
:deep(.v-btn.seat-booked) {
    min-width: 44px !important;
    height: 44px !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.legend-seat {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    display: inline-block;
}

@media (max-width: 960px) {
    .seat-map {
        padding: 0.5rem 0;
    }
}

@media (max-width: 768px) {
    .seat-row {
        gap: 0.5rem;
    }

    .row-label {
        width: 36px;
        font-size: 0.9rem;
        min-height: 36px;
        padding: 6px 2px;
    }

    :deep(.v-btn.seat-available),
    :deep(.v-btn.seat-selected),
    :deep(.v-btn.seat-locked),
    :deep(.v-btn.seat-booked) {
        min-width: 40px !important;
        height: 40px !important;
        font-size: 0.75rem !important;
    }

    .seats-container {
        gap: 0.25rem;
    }

    .seat-map-container {
        padding: 0.5rem;
    }
}
</style>