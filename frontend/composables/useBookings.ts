export const useBookings = () => {
    const { $api } = useNuxtApp()

    const bookings = useState<any[]>('bookings', () => [])

    const createBooking = async (eventId: number, seatIds: number[]) => {
        try {
            const response = await $api('/api/bookings', {
                method: 'POST',
                body: { event_id: eventId, seat_ids: seatIds }
            })
            return { success: true, data: response }
        } catch (error: any) {
            let errorMessage = 'Failed to create booking'

            if (error.data?.detail) {
                errorMessage = error.data.detail
            } else if (error.statusCode === 400) {
                errorMessage = 'Invalid booking request. Please check your selected seats and try again.'
            } else if (error.statusCode === 401) {
                errorMessage = 'Please login to book tickets.'
            } else if (error.statusCode === 404) {
                errorMessage = 'Event or seats not found.'
            } else if (error.statusCode >= 500) {
                errorMessage = 'Server error. Please try again later.'
            }

            return {
                success: false,
                error: errorMessage
            }
        }
    }

    const fetchMyBookings = async () => {
        try {
            const response = await $api('/api/bookings')
            bookings.value = response as any[]
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch bookings'
            }
        }
    }

    const cancelBooking = async (bookingId: number) => {
        try {
            const response = await $api(`/api/bookings/${bookingId}`, {
                method: 'DELETE'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to cancel booking'
            }
        }
    }

    const cancelPartialSeats = async (bookingId: number, seatIds: number[]) => {
        try {
            const response = await $api(`/api/bookings/${bookingId}/cancel-seats`, {
                method: 'POST',
                body: { seat_ids: seatIds }
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to cancel seats'
            }
        }
    }

    return {
        bookings,
        createBooking,
        fetchMyBookings,
        cancelBooking,
        cancelPartialSeats
    }
}
