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

    const fetchAllBookings = async (params?: {
        eventId?: number
        search?: string
        status?: string
        skip?: number
        limit?: number
    }) => {
        try {
            const queryParams: any = {}
            if (params?.eventId) queryParams.event_id = params.eventId
            if (params?.search) queryParams.search = params.search
            if (params?.status) queryParams.status = params.status
            if (params?.skip) queryParams.skip = params.skip
            if (params?.limit) queryParams.limit = params.limit

            console.log('Fetching bookings with params:', queryParams)

            const response = await $api('/api/admin/bookings', { params: queryParams })

            console.log('Bookings API response:', response)

            return { success: true, data: response }
        } catch (error: any) {
            console.error('Bookings API error:', error)
            return {
                success: false,
                error: error.data?.detail || error.message || 'Failed to fetch bookings'
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
                is_available: !seat.is_booked, // Convert is_booked to is_available
                is_booked: seat.is_booked,
                is_locked: false, // Admin can see all seats, no locks for admin
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

    const createAdminBooking = async (eventId: number, seatIds: number[], usernameOrEmail?: string) => {
        try {
            const response = await $api('/api/admin/bookings', {
                method: 'POST',
                body: {
                    event_id: eventId,
                    seat_ids: seatIds,
                    username_or_email: usernameOrEmail || ''
                }
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to create admin booking'
            }
        }
    }

    const deactivateExpiredEvents = async () => {
        try {
            const response = await $api('/api/admin/events/deactivate-expired', {
                method: 'POST'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to deactivate expired events'
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
        syncEventSeats,
        createAdminBooking,
        deactivateExpiredEvents
    }
}
