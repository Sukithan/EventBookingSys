<template>
    <v-row class="mb-4" v-if="!loading && bookings.length > 0">
        <v-col cols="12" md="3">
            <StatsCard icon="mdi-check-circle" :value="confirmedCount" label="Confirmed Bookings" color="success">
                <template #subtitle>
                    {{ confirmedSeatsCount }} seats
                </template>
            </StatsCard>
        </v-col>
        <v-col cols="12" md="3">
            <StatsCard icon="mdi-cancel" :value="cancelledCount" label="Cancelled Bookings" color="error">
                <template #subtitle>
                    {{ cancelledSeatsCount }} seats
                </template>
            </StatsCard>
        </v-col>
        <v-col cols="12" md="3">
            <StatsCard icon="mdi-ticket-outline" :value="totalCount" label="Total Bookings" color="primary">
                <template #subtitle>
                    {{ totalSeatsCount }} total seats
                </template>
            </StatsCard>
        </v-col>
        <v-col cols="12" md="3">
            <StatsCard icon="mdi-cash" :value="`$${totalRevenue.toFixed(2)}`" label="Total Revenue" color="info">
                <template #subtitle>
                    From confirmed bookings
                </template>
            </StatsCard>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    bookings: any[]
    loading: boolean
}

const props = defineProps<Props>()

const confirmedCount = computed(() => {
    return props.bookings.filter(booking => booking.status === 'confirmed').length
})

const cancelledCount = computed(() => {
    return props.bookings.filter(booking => booking.status === 'cancelled').length
})

const totalCount = computed(() => {
    return props.bookings.length
})

const confirmedSeatsCount = computed(() => {
    return props.bookings
        .filter(booking => booking.status === 'confirmed')
        .reduce((sum, booking) => sum + (booking.seats_booked || 0), 0)
})

const cancelledSeatsCount = computed(() => {
    return props.bookings
        .filter(booking => booking.status === 'cancelled')
        .reduce((sum, booking) => sum + (booking.seats_booked || 0), 0)
})

const totalSeatsCount = computed(() => {
    return props.bookings.reduce((sum, booking) => sum + (booking.seats_booked || 0), 0)
})

const totalRevenue = computed(() => {
    return props.bookings
        .filter(booking => booking.status === 'confirmed')
        .reduce((sum, booking) => sum + (booking.total_price || 0), 0)
})
</script>