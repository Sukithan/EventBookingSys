<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <h1 class="text-h4 font-weight-bold mb-6">All Bookings</h1>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="table"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="bookings.length > 0">
            <v-col cols="12">
                <v-card>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="bookings" :items-per-page="10" class="elevation-0">
                            <template v-slot:item.booking_date="{ item }">
                                {{ formatDate(item.booking_date) }}
                            </template>

                            <template v-slot:item.user="{ item }">
                                <div>
                                    <div class="font-weight-medium">{{ item.user.full_name }}</div>
                                    <div class="text-caption text-grey">{{ item.user.email }}</div>
                                </div>
                            </template>

                            <template v-slot:item.total_price="{ item }">
                                ${{ item.total_price.toFixed(2) }}
                            </template>

                            <template v-slot:item.status="{ item }">
                                <v-chip :color="item.status === 'confirmed' ? 'success' : 'error'" size="small">
                                    {{ item.status.toUpperCase() }}
                                </v-chip>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                <p class="text-h6 text-grey mt-4">No bookings yet</p>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { fetchAllBookings } = useAdmin()

const loading = ref(false)
const bookings = ref<any[]>([])

const headers = [
    { title: 'Booking ID', value: 'id', key: 'id' },
    { title: 'User', value: 'user', key: 'user' },
    { title: 'Event ID', value: 'event_id', key: 'event_id' },
    { title: 'Seats', value: 'seats_booked', key: 'seats_booked' },
    { title: 'Total Price', value: 'total_price', key: 'total_price' },
    { title: 'Status', value: 'status', key: 'status' },
    { title: 'Booked On', value: 'booking_date', key: 'booking_date' }
]

const loadBookings = async () => {
    loading.value = true
    const result = await fetchAllBookings()
    if (result.success) {
        bookings.value = Array.isArray(result.data) ? (result.data as any[]) : []
    }
    loading.value = false
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

onMounted(() => {
    loadBookings()
})
</script>
