<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex justify-space-between align-center mb-6">
                    <div>
                        <h1 class="text-h4 font-weight-bold">Admin Dashboard</h1>
                        <div class="text-subtitle-1 opacity-70">Overview of events, bookings and users</div>
                    </div>
                    <div class="d-flex">
                        <v-btn color="primary" class="mr-3" to="/admin/events/create">
                            <v-icon left>mdi-plus</v-icon>
                            New Event
                        </v-btn>
                        <v-btn outlined to="/admin/bookings">
                            <v-icon left>mdi-ticket</v-icon>
                            Manage Bookings
                        </v-btn>
                    </div>
                </div>
            </v-col>
        </v-row>

        <!-- Hero Summary -->
        <v-row>
            <v-col cols="12">
                <v-card class="pa-6 mb-6" elevation="2">
                    <div class="d-flex justify-space-between align-center flex-wrap">
                        <div>
                            <div class="text-h5 font-weight-medium">Welcome back, Administrator</div>
                            <div class="text-body-1 mt-2 opacity-70">Quick stats and recent activity at a glance.</div>
                        </div>
                        <div class="d-flex mt-4 mt-sm-0">
                            <v-btn text to="/admin/events" class="mr-3">View Events</v-btn>
                            <v-btn text to="/admin/bookings">View All Bookings</v-btn>
                        </div>
                    </div>
                </v-card>
            </v-col>
        </v-row>

        <!-- Statistics Cards -->
        <v-row v-if="!loading">
            <v-col cols="12" sm="6" md="4" v-for="stat in stats" :key="stat.title">
                <v-card class="pa-4" elevation="1">
                    <v-card-text>
                        <div class="d-flex justify-space-between align-center">
                            <div>
                                <div class="text-h4 font-weight-bold">{{ stat.value }}</div>
                                <div class="text-subtitle-2 mt-1">{{ stat.title }}</div>
                            </div>
                            <v-avatar size="56" class="elevation-0" :color="stat.color">
                                <v-icon dark size="28">{{ stat.icon }}</v-icon>
                            </v-avatar>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col v-for="n in 6" :key="n" cols="12" sm="6" md="4">
                <v-skeleton-loader type="card"></v-skeleton-loader>
            </v-col>
        </v-row>

        <!-- Quick Actions -->
        <v-row class="mt-6">
            <v-col cols="12">
                <h2 class="text-h6 font-weight-bold mb-4">Quick Actions</h2>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="primary" block size="large" to="/admin/events">
                    <v-icon left>mdi-calendar</v-icon>
                    Manage Events
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="secondary" block size="large" to="/admin/bookings">
                    <v-icon left>mdi-ticket</v-icon>
                    View Bookings
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="success" block size="large" to="/admin/events/create">
                    <v-icon left>mdi-plus</v-icon>
                    Create Event
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="info" block size="large" to="/">
                    <v-icon left>mdi-home</v-icon>
                    View Site
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { fetchDashboardStats, fetchAllBookings, cancelBooking } = useAdmin()

const loading = ref(false)
const stats = ref([
    { title: 'Total Events', value: 0, icon: 'mdi-calendar-multiple', color: 'primary' },
    { title: 'Active Events', value: 0, icon: 'mdi-calendar-check', color: 'success' },
    { title: 'Upcoming Events', value: 0, icon: 'mdi-calendar-clock', color: 'info' },
    { title: 'Total Bookings', value: 0, icon: 'mdi-ticket', color: 'secondary' },
    { title: 'Cancelled Bookings', value: 0, icon: 'mdi-ticket-cancel', color: 'warning' },
    { title: 'Total Users', value: 0, icon: 'mdi-account-group', color: 'purple' }
])

const bookings = ref<any[]>([])
const bookingsLoading = ref(false)

const bookingHeaders = [
    { text: 'ID', value: 'id', width: '80' },
    { text: 'Event', value: 'event' },
    { text: 'User', value: 'user' },
    { text: 'Seats', value: 'seats', width: '80' },
    { text: 'Status', value: 'status', width: '120' },
    { text: 'Date', value: 'date' },
    { text: 'Actions', value: 'actions', sortable: false, width: '120' }
]

type DashboardData = {
    total_events: number
    active_events: number
    upcoming_events: number
    total_bookings: number
    cancelled_bookings: number
    total_users: number
}

type DashboardResult = {
    success: boolean
    data: DashboardData
}

const loadStats = async () => {
    loading.value = true
    const result = await fetchDashboardStats() as DashboardResult
    loading.value = false

    if (result && result.success && result.data) {
        stats.value[0].value = result.data.total_events
        stats.value[1].value = result.data.active_events
        stats.value[2].value = result.data.upcoming_events
        stats.value[3].value = result.data.total_bookings
        stats.value[4].value = result.data.cancelled_bookings
        stats.value[5].value = result.data.total_users
    }
}

const loadRecentBookings = async () => {
    bookingsLoading.value = true
    const res = await fetchAllBookings({ limit: 5 }) as { success?: boolean; data?: any }
    bookingsLoading.value = false

    if (res && res.success && res.data) {
        // Ensure we have an array
        bookings.value = Array.isArray(res.data)
            ? res.data
            : (Array.isArray(res.data?.bookings) ? res.data.bookings : [])
    } else {
        bookings.value = []
    }
}

const cancel = async (item: any) => {
    if (!item || !item.id) return
    // quick confirm
    // eslint-disable-next-line no-restricted-globals
    if (!confirm(`Cancel booking #${item.id}?`)) return
    const res = await cancelBooking(item.id)
    if (res && res.success) {
        await loadRecentBookings()
        await loadStats()
    } else {
        alert(res?.error || 'Failed to cancel booking')
    }
}

onMounted(() => {
    loadStats()
    loadRecentBookings()
})
</script>
