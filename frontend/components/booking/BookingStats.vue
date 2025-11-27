<template>
    <v-row class="mb-4" v-if="!loading && bookings.length > 0">
        <v-col cols="12" md="4">
            <StatsCard icon="mdi-check-circle" :value="confirmedCount" label="Confirmed Bookings" color="success" />
        </v-col>
        <v-col cols="12" md="4">
            <StatsCard icon="mdi-cancel" :value="cancelledCount" label="Cancelled Bookings" color="error" />
        </v-col>
        <v-col cols="12" md="4">
            <StatsCard icon="mdi-ticket-outline" :value="totalCount" label="Total Bookings" color="primary" />
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
</script>