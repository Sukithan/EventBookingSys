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

    return {
        fetchAllEvents,
        fetchEventBookings,
        fetchAllBookings,
        fetchDashboardStats
    }
}
