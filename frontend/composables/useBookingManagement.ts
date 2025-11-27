export const useBookingManagement = () => {
    const { $api } = useNuxtApp()
    const { fetchAllBookings, fetchEventBookings, cancelBooking: adminCancelBooking, createAdminBooking, deleteSeatBooking, recalculateEventStats } = useAdmin()

    const state = reactive({
        loading: false,
        cancelling: false,
        deletingSeat: false,
        recalculatingStats: false,
        bookingLoading: false,
        seatsLoading: false,
        seatActionLoading: null as number | null,
        bookings: [] as any[],
        selectedBooking: null as any,
        selectedSeat: null as any,
        selectedSeatInfo: null as any,
        seatDetails: [] as any[],
        snackbar: false,
        snackbarMessage: '',
        snackbarColor: 'success'
    })

    const showSnackbar = (message: string, color: 'success' | 'error' | 'warning' | 'info' = 'success') => {
        state.snackbarMessage = message
        state.snackbarColor = color
        state.snackbar = true
    }

    const loadAllBookings = async (params?: { search?: string; status?: string; limit?: number }) => {
        state.loading = true
        try {
            const result = await fetchAllBookings(params)
            if (result.success) {
                state.bookings = Array.isArray(result.data) ? result.data : []
                return { success: true, data: state.bookings }
            } else {
                showSnackbar(result.error || 'Failed to load bookings', 'error')
                state.bookings = []
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to load bookings', 'error')
            state.bookings = []
            return { success: false, error: error.message }
        } finally {
            state.loading = false
        }
    }

    const loadEventBookings = async (eventId: number) => {
        state.loading = true
        try {
            const result = await fetchEventBookings(eventId)
            if (result.success) {
                const data = result.data as any
                state.bookings = Array.isArray(data) ? data : (data.bookings || [])
                return { success: true, data: state.bookings }
            } else {
                showSnackbar(result.error || 'Failed to load bookings', 'error')
                state.bookings = []
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to load bookings', 'error')
            state.bookings = []
            return { success: false, error: error.message }
        } finally {
            state.loading = false
        }
    }

    const handleCancelBooking = async (bookingId: number) => {
        state.cancelling = true
        try {
            const result = await adminCancelBooking(bookingId)
            if (result.success) {
                showSnackbar('Booking cancelled successfully', 'success')
                return { success: true }
            } else {
                showSnackbar(result.error || 'Failed to cancel booking', 'error')
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to cancel booking', 'error')
            return { success: false, error: error.message }
        } finally {
            state.cancelling = false
        }
    }

    const handleDeleteSeat = async (seatId: number) => {
        state.deletingSeat = true
        try {
            const result = await deleteSeatBooking(seatId)
            if (result.success) {
                showSnackbar('Seat booking removed successfully', 'success')
                return { success: true }
            } else {
                showSnackbar(result.error || 'Failed to remove seat', 'error')
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to remove seat', 'error')
            return { success: false, error: error.message }
        } finally {
            state.deletingSeat = false
        }
    }

    const handleCreateAdminBooking = async (eventId: number, seatIds: number[], username: string) => {
        state.bookingLoading = true
        try {
            const result = await createAdminBooking(eventId, seatIds, username)
            if (result.success) {
                const bookingFor = username.trim() ? username : 'yourself (admin)'
                showSnackbar(`Booking created successfully for ${bookingFor}`, 'success')
                return { success: true, data: result.data }
            } else {
                showSnackbar(result.error || 'Failed to create booking', 'error')
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to create booking', 'error')
            return { success: false, error: error.message }
        } finally {
            state.bookingLoading = false
        }
    }

    const handleRecalculateStats = async (eventId: number) => {
        state.recalculatingStats = true
        try {
            const result = await recalculateEventStats(eventId)
            if (result.success) {
                showSnackbar('Event statistics recalculated successfully', 'success')
                return { success: true }
            } else {
                showSnackbar(result.error || 'Failed to recalculate stats', 'error')
                return { success: false, error: result.error }
            }
        } catch (error: any) {
            showSnackbar(error.message || 'Failed to recalculate stats', 'error')
            return { success: false, error: error.message }
        } finally {
            state.recalculatingStats = false
        }
    }

    const exportBookingsToCSV = (bookings: any[], eventName?: string) => {
        try {
            const headers = ['Booking ID', 'Customer Name', 'Email', 'Username', 'Booking Date', 'Seats', 'Total', 'Status']
            const rows = bookings.map(booking => [
                booking.id,
                booking.user?.full_name || 'N/A',
                booking.user?.email || 'N/A',
                booking.user?.username || 'N/A',
                new Date(booking.booking_date).toLocaleString(),
                booking.seats_booked,
                booking.total_price?.toFixed(2) || '0.00',
                booking.status
            ])

            const csvContent = [
                headers.join(','),
                ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
            ].join('\n')

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
            const link = document.createElement('a')
            const url = URL.createObjectURL(blob)

            const fileName = eventName
                ? `${eventName.replace(/\s+/g, '-')}-bookings-${new Date().toISOString().split('T')[0]}.csv`
                : `bookings-export-${new Date().toISOString().split('T')[0]}.csv`

            link.setAttribute('href', url)
            link.setAttribute('download', fileName)
            link.style.visibility = 'hidden'

            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)

            showSnackbar('Bookings exported successfully', 'success')
            return { success: true }
        } catch (error: any) {
            showSnackbar('Failed to export bookings', 'error')
            return { success: false, error: error.message }
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

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'confirmed': return 'success'
            case 'cancelled': return 'error'
            case 'pending': return 'warning'
            default: return 'grey'
        }
    }

    return {
        state,
        loadAllBookings,
        loadEventBookings,
        handleCancelBooking,
        handleDeleteSeat,
        handleCreateAdminBooking,
        handleRecalculateStats,
        exportBookingsToCSV,
        showSnackbar,
        formatDate,
        getStatusColor
    }
}
