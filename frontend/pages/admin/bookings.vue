<template>
    <v-container>
        <PageHeader title="All Bookings" />

        <!-- Booking Stats -->
        <BookingStats :bookings="bookings" :loading="loading" />

        <!-- Search and Filters -->
        <v-card class="mb-4 pa-4">
            <SearchAndFilter v-model:search-query="searchQuery" v-model:status-filter="statusFilter"
                :status-options="statusOptions" :loading="loading" search-label="Search bookings..."
                search-placeholder="Search by name, email, username, booking ID, event name or location"
                @refresh="loadBookings" @clear-search="clearSearch">
                <template #additional-actions>
                    <v-btn v-if="bookings.length > 0" color="success" variant="outlined" class="ml-2"
                        @click="exportToCSV">
                        <v-icon start>mdi-download</v-icon>
                        Export CSV
                    </v-btn>
                </template>
            </SearchAndFilter>
        </v-card>

        <LoadingSkeleton v-if="loading" type="table" :count="1" />

        <v-row v-else-if="bookings.length > 0">
            <v-col cols="12">
                <BookingDataTable :bookings="bookings" :cancelling-booking="cancellingBooking" :search="searchQuery"
                    @cancel-booking="confirmCancelBooking" @view-details="viewBookingDetails" />
            </v-col>
        </v-row>

        <EmptyState v-else icon="mdi-ticket-outline" title="No bookings yet"
            message="Bookings will appear here once users start making reservations" />

        <!-- Cancellation Confirmation Dialog -->
        <ConfirmationDialog v-model="cancelDialog" title="Cancel Booking"
            message="Are you sure you want to cancel this booking?" :details="cancelDialogDetails" icon="mdi-alert"
            confirm-text="Cancel Booking" cancel-text="Keep Booking" :loading="!!cancellingBooking"
            @confirm="cancelBooking" />

        <!-- Booking Details Dialog -->
        <BookingDetailsDialog v-model="detailsDialog" :booking="selectedBooking" :cancelling-booking="cancellingBooking"
            @cancel-booking="confirmCancelBooking" />

        <!-- Success/Error Snackbar -->
        <NotificationSnackbar v-model="snackbar" :message="snackbarMessage" :color="snackbarColor" />
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { fetchAllBookings } = useAdmin()
const { $api } = useNuxtApp()

const loading = ref(false)
const bookings = ref<any[]>([])
const cancelDialog = ref(false)
const detailsDialog = ref(false)
const selectedBooking = ref<any>(null)
const cancellingBooking = ref<number | null>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

// Search and filter state
const searchQuery = ref('')
const statusFilter = ref('')
const searchTimeout = ref<NodeJS.Timeout | null>(null)

const statusOptions = [
    { title: 'All Status', value: '' },
    { title: 'Confirmed', value: 'confirmed' },
    { title: 'Cancelled', value: 'cancelled' }
]

const cancelDialogDetails = computed(() => {
    if (!selectedBooking.value) return ''
    return `<strong>Booking Details:</strong><br>
            User: ${selectedBooking.value.user?.full_name || 'N/A'}<br>
            Booking ID: ${selectedBooking.value.id}<br>
            Seats: ${selectedBooking.value.seats_booked}<br>
            Total: $${selectedBooking.value.total_price?.toFixed(2) || '0.00'}`
})

const loadBookings = async () => {
    loading.value = true
    console.log('Loading bookings with params:', {
        search: searchQuery.value || undefined,
        status: statusFilter.value || undefined,
        limit: 200
    })

    try {
        const result = await fetchAllBookings({
            search: searchQuery.value || undefined,
            status: statusFilter.value || undefined,
            limit: 200 // Increase limit to show more results
        })

        console.log('Bookings API result:', result)

        if (result.success) {
            bookings.value = Array.isArray(result.data) ? (result.data as any[]) : []
            console.log('Successfully loaded bookings:', bookings.value.length)
        } else {
            console.error('Failed to load bookings:', result.error)
            snackbarMessage.value = result.error || 'Failed to load bookings'
            snackbarColor.value = 'error'
            snackbar.value = true
            bookings.value = []
        }
    } catch (error: any) {
        console.error('Error loading bookings:', error)
        snackbarMessage.value = error.message || 'Failed to load bookings'
        snackbarColor.value = 'error'
        snackbar.value = true
        bookings.value = []
    } finally {
        loading.value = false
    }
}

const confirmCancelBooking = (booking: any) => {
    console.log('=== Confirm cancel booking called ===')
    console.log('Booking data:', booking)
    console.log('Booking ID:', booking?.id)
    selectedBooking.value = booking
    console.log('Selected booking set:', selectedBooking.value)
    cancelDialog.value = true
    console.log('Cancel dialog value:', cancelDialog.value)
}

const viewBookingDetails = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = true
}

const cancelBooking = async () => {
    if (!selectedBooking.value) {
        console.log('No booking selected')
        return
    }

    console.log('Cancelling booking:', selectedBooking.value.id)
    cancellingBooking.value = selectedBooking.value.id

    try {
        console.log('Making DELETE request to:', `/api/admin/bookings/${selectedBooking.value.id}`)
        const response = await $api(`/api/admin/bookings/${selectedBooking.value.id}`, {
            method: 'DELETE'
        })

        console.log('Booking cancelled successfully:', response)
        snackbarMessage.value = `Booking #${selectedBooking.value.id} cancelled successfully`
        snackbarColor.value = 'success'
        snackbar.value = true

        // Close dialogs first
        cancelDialog.value = false
        detailsDialog.value = false

        // Refresh bookings list
        await loadBookings()

    } catch (error: any) {
        console.error('Error cancelling booking:', error)
        console.error('Error details:', error.data)
        snackbarMessage.value = error.data?.detail || error.message || 'Failed to cancel booking'
        snackbarColor.value = 'error'
        snackbar.value = true

        // Close dialog even on error
        cancelDialog.value = false
    } finally {
        cancellingBooking.value = null
        console.log('Cancel operation completed')
    }
}

const debouncedSearch = () => {
    if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
    }
    searchTimeout.value = setTimeout(() => {
        loadBookings()
    }, 500)
}

const clearSearch = () => {
    searchQuery.value = ''
    loadBookings()
}

const exportToCSV = () => {
    try {
        // Prepare CSV headers
        const headers = ['Booking ID', 'User Name', 'Email', 'Username', 'Event ID', 'Seats Booked', 'Total Price', 'Status', 'Booking Date']

        // Prepare CSV rows
        const rows = bookings.value.map(booking => [
            booking.id,
            booking.user.full_name,
            booking.user.email,
            booking.user.username,
            booking.event_id,
            booking.seats_booked,
            booking.total_price.toFixed(2),
            booking.status,
            new Date(booking.booking_date).toLocaleString()
        ])

        // Create CSV content
        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
        ].join('\n')

        // Create blob and download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)

        link.setAttribute('href', url)
        link.setAttribute('download', `bookings_export_${new Date().toISOString().split('T')[0]}.csv`)
        link.style.visibility = 'hidden'

        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        snackbarMessage.value = 'Bookings exported successfully'
        snackbarColor.value = 'success'
        snackbar.value = true
    } catch (error) {
        console.error('Error exporting bookings:', error)
        snackbarMessage.value = 'Failed to export bookings'
        snackbarColor.value = 'error'
        snackbar.value = true
    }
}

// Watch for search query changes
watch(searchQuery, () => {
    debouncedSearch()
})

// Watch for status filter changes
watch(statusFilter, () => {
    loadBookings()
})

onMounted(async () => {
    // Only run on client side to avoid SSR issues
    if (!process.client) return

    console.log('Admin bookings page mounted')

    // Check authentication status
    const { isAuthenticated, isAdmin, user, initializeAuth } = useAuth()
    await initializeAuth()

    console.log('Auth status:', {
        isAuthenticated: isAuthenticated.value,
        isAdmin: isAdmin.value,
        user: user.value
    })

    if (!isAuthenticated.value || !isAdmin.value) {
        console.warn('User not authenticated or not admin, redirecting to login')
        await navigateTo('/login')
        return
    }

    loadBookings()
})
</script>

<style scoped>
:deep(.cancelled-row) {
    opacity: 0.7;
    background-color: rgba(244, 67, 54, 0.05) !important;
}

:deep(.cancelled-row:hover) {
    background-color: rgba(244, 67, 54, 0.1) !important;
}
</style>
