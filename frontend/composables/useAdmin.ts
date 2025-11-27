export const useAdmin = () => {
    const { $api } = useNuxtApp()

    const fetchAllEvents = async () => {
        try {
            const response = await $api('/api/admin/events')
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch events'
            }
        }
    }

    const fetchEventBookings = async (eventId: number) => {
        try {
            const response = await $api(`/api/admin/events/${eventId}/bookings`)
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch event bookings'
            }
        }
    }

    const fetchAllBookings = async (eventId?: number) => {
        try {
            const params = eventId ? { event_id: eventId } : {}
            const response = await $api('/api/admin/bookings', { params })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch bookings'
            }
        }
    }

    const fetchDashboardStats = async () => {
        try {
            const response = await $api('/api/admin/dashboard/stats')
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch dashboard stats'
            }
        }
    }

    const cancelBooking = async (bookingId: number) => {
        try {
            const response = await $api(`/api/admin/bookings/${bookingId}`, {
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

    const getEventSeatsAdmin = async (eventId: number) => {
        try {
            const response: any = await $api(`/api/admin/seats/event/${eventId}`)
            // Transform the response to match frontend expectations
            const seats = response.seats.map((seat: any) => ({
                id: seat.id,
                row_number: seat.row_number,
                seat_number: seat.seat_number,
                is_available: !seat.is_booked,
                is_locked: false, // Admin can see all seats
                booking_info: seat.booking_info
            }))
            return { success: true, data: seats }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch event seats'
            }
        }
    }

    const deleteSeat = async (seatId: number) => {
        try {
            const response = await $api(`/api/admin/seats/${seatId}`, {
                method: 'DELETE'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to delete seat'
            }
        }
    }

    const deleteSeatBooking = async (seatId: number) => {
        try {
            const response = await $api(`/api/admin/seats/${seatId}/booking`, {
                method: 'DELETE'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to delete seat booking'
            }
        }
    }

    const updateEventImage = async (eventId: number, imageUrl: string) => {
        try {
            const response = await $api(`/api/events/${eventId}/image`, {
                method: 'PUT',
                body: { image_url: imageUrl }
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to update event image'
            }
        }
    }

    const recalculateEventStats = async (eventId: number) => {
        try {
            const response = await $api(`/api/events/${eventId}/recalculate-stats`, {
                method: 'POST'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to recalculate event statistics'
            }
        }
    }

    const syncEventSeats = async (eventId: number) => {
        try {
            const response = await $api(`/api/admin/events/${eventId}/sync-seats`, {
                method: 'POST'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to synchronize event seats'
            }
        }
    }

    return {
        fetchAllEvents,
        fetchEventBookings,
        fetchAllBookings,
        fetchDashboardStats,
        cancelBooking,
        getEventSeatsAdmin,
        deleteSeat,
        deleteSeatBooking,
        updateEventImage,
        recalculateEventStats,
        syncEventSeats
    }
}
