export interface Seat {
    id: number
    row_number: number
    seat_number: number
    is_available: boolean
    is_locked: boolean
    locked_by_current_user: boolean
}

export interface SeatLock {
    seat_id: number
    locked_until: string
}

export interface BookingRequest {
    event_id: number
    seat_ids: number[]
}

export const useSeats = () => {
    const { $api } = useNuxtApp()

    const seats = ref<Seat[]>([])
    const selectedSeats = ref<number[]>([])
    const lockedSeats = ref<number[]>([])
    const loading = ref(false)

    const fetchEventSeats = async (eventId: number, silent = false) => {
        if (!silent) loading.value = true
        try {
            const response = await $api(`/api/seats/event/${eventId}`)
            seats.value = response as Seat[]
            return { success: true, data: response }
        } catch (error: any) {
            console.error('Error fetching seats:', error)
            return { success: false, error: error.data?.detail || 'Failed to fetch seats' }
        } finally {
            if (!silent) loading.value = false
        }
    }

    const lockSeats = async (seatIds: number[]) => {
        try {
            const response = await $api('/api/seats/lock', {
                method: 'POST',
                body: { seat_ids: seatIds }
            })
            lockedSeats.value = seatIds
            return { success: true, data: response }
        } catch (error: any) {
            console.error('Error locking seats:', error)
            let errorMessage = 'Failed to select seats'

            if (error.data?.detail) {
                errorMessage = error.data.detail
            } else if (error.statusCode === 400) {
                errorMessage = 'These seats are currently unavailable. Please try different seats.'
            } else if (error.statusCode === 401) {
                errorMessage = 'Please login to select seats.'
            } else if (error.statusCode === 404) {
                errorMessage = 'Seats not found.'
            }

            return { success: false, error: errorMessage }
        }
    }

    const unlockSeats = async (seatIds: number[]) => {
        try {
            await $api('/api/seats/unlock', {
                method: 'DELETE',
                body: seatIds
            })
            lockedSeats.value = lockedSeats.value.filter(id => !seatIds.includes(id))
            return { success: true }
        } catch (error: any) {
            console.error('Error unlocking seats:', error)
            return { success: false, error: error.data?.detail || 'Failed to unlock seats' }
        }
    }

    const toggleSeatSelection = async (seatId: number) => {
        if (selectedSeats.value.includes(seatId)) {
            // Deselect seat
            selectedSeats.value = selectedSeats.value.filter(id => id !== seatId)
            await unlockSeats([seatId])
        } else {
            // Select seat
            const lockResult = await lockSeats([seatId])
            if (lockResult.success) {
                selectedSeats.value.push(seatId)
            }
            return lockResult
        }
    }

    const clearSelection = async () => {
        if (selectedSeats.value.length > 0) {
            await unlockSeats(selectedSeats.value)
            selectedSeats.value = []
        }
    }

    const groupSeatsByRow = computed(() => {
        const grouped: { [key: number]: Seat[] } = {}
        seats.value.forEach(seat => {
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

    const totalSelectedPrice = computed(() => {
        return selectedSeats.value.length
    })

    return {
        seats,
        selectedSeats,
        lockedSeats,
        loading,
        fetchEventSeats,
        lockSeats,
        unlockSeats,
        toggleSeatSelection,
        clearSelection,
        groupSeatsByRow,
        totalSelectedPrice
    }
}