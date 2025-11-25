<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h4 font-weight-bold mb-6">Admin Dashboard</h1>
            </v-col>
        </v-row>

        <!-- Statistics Cards -->
        <v-row v-if="!loading">
            <v-col cols="12" sm="6" md="4" v-for="stat in stats" :key="stat.title">
                <v-card :color="stat.color" dark>
                    <v-card-text>
                        <div class="d-flex justify-space-between align-center">
                            <div>
                                <div class="text-h3 font-weight-bold">{{ stat.value }}</div>
                                <div class="text-body-1 mt-1">{{ stat.title }}</div>
                            </div>
                            <v-icon size="60" class="opacity-50">{{ stat.icon }}</v-icon>
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
                <h2 class="text-h5 font-weight-bold mb-4">Quick Actions</h2>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="primary" block size="large" to="/admin/events">
                    <v-icon start>mdi-calendar</v-icon>
                    Manage Events
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="secondary" block size="large" to="/admin/bookings">
                    <v-icon start>mdi-ticket</v-icon>
                    View Bookings
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="success" block size="large" to="/admin/events/create">
                    <v-icon start>mdi-plus</v-icon>
                    Create Event
                </v-btn>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-btn color="info" block size="large" to="/">
                    <v-icon start>mdi-home</v-icon>
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

const { fetchDashboardStats } = useAdmin()

const loading = ref(false)
const stats = ref([
    { title: 'Total Events', value: 0, icon: 'mdi-calendar-multiple', color: 'primary' },
    { title: 'Active Events', value: 0, icon: 'mdi-calendar-check', color: 'success' },
    { title: 'Upcoming Events', value: 0, icon: 'mdi-calendar-clock', color: 'info' },
    { title: 'Total Bookings', value: 0, icon: 'mdi-ticket', color: 'secondary' },
    { title: 'Cancelled Bookings', value: 0, icon: 'mdi-ticket-cancel', color: 'warning' },
    { title: 'Total Users', value: 0, icon: 'mdi-account-group', color: 'purple' }
])

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

onMounted(() => {
    loadStats()
})
</script>
