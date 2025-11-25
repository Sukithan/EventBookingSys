export const useBookings = () => {
    const { $api } = useNuxtApp()

    const bookings = useState<any[]>('bookings', () => [])

    const createBooking = async (eventId: number, seatsBooked: number = 1) => {
        try {
            const response = await $api('/api/bookings', {
                method: 'POST',
                body: { event_id: eventId, seats_booked: seatsBooked }
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to create booking'
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

    return {
        bookings,
        createBooking,
        fetchMyBookings,
        cancelBooking
    }
}
