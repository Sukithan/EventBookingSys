<template>
    <v-card class="h-100 elevation-2">
        <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="220" cover>
            <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
                </v-row>
            </template>
        </v-img>

        <v-card-title class="text-h6 py-4">{{ event.name }}</v-card-title>

        <v-card-text>
            <v-list dense>
                <v-list-item>
                    <template #prepend>
                        <v-icon>mdi-map-marker</v-icon>
                    </template>
                    <v-list-item-title>{{ event.location }}</v-list-item-title>
                </v-list-item>

                <v-list-item>
                    <template #prepend>
                        <v-icon>mdi-calendar</v-icon>
                    </template>
                    <v-list-item-title>{{ formatDate(event.date) }}</v-list-item-title>
                </v-list-item>

                <v-list-item>
                    <template #prepend>
                        <v-icon>mdi-cash</v-icon>
                    </template>
                    <v-list-item-title>${{ event.ticket_price?.toFixed(2) }} per seat</v-list-item-title>
                </v-list-item>

                <v-divider class="my-3"></v-divider>

                <v-list-item>
                    <template #prepend>
                        <v-icon>mdi-seat</v-icon>
                    </template>
                    <v-list-item-title>
                        <div class="d-flex justify-space-between">
                            <span>Total Seats</span>
                            <span class="font-weight-bold">{{ event.total_seats }}</span>
                        </div>
                    </v-list-item-title>
                </v-list-item>

                <v-list-item>
                    <template #prepend>
                        <v-icon color="success">mdi-check-circle</v-icon>
                    </template>
                    <v-list-item-title>
                        <div class="d-flex justify-space-between">
                            <span>Available</span>
                            <span class="font-weight-bold text-success">{{ event.available_seats }}</span>
                        </div>
                    </v-list-item-title>
                </v-list-item>

                <v-list-item>
                    <template #prepend>
                        <v-icon color="error">mdi-close-circle</v-icon>
                    </template>
                    <v-list-item-title>
                        <div class="d-flex justify-space-between">
                            <span>Booked</span>
                            <span class="font-weight-bold text-error">{{ event.total_seats - event.available_seats
                            }}</span>
                        </div>
                    </v-list-item-title>
                </v-list-item>

                <v-divider class="my-3"></v-divider>

                <v-list-item>
                    <v-progress-linear :model-value="occupancyPercentage"
                        :color="getOccupancyColor(occupancyPercentage)" height="20" rounded>
                        <template v-slot:default>
                            <strong class="text-white">{{ occupancyPercentage.toFixed(1) }}% Full</strong>
                        </template>
                    </v-progress-linear>
                </v-list-item>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    event: any
}

const props = defineProps<Props>()

const occupancyPercentage = computed(() => {
    if (!props.event.total_seats) return 0
    return ((props.event.total_seats - props.event.available_seats) / props.event.total_seats) * 100
})

const getOccupancyColor = (percentage: number) => {
    if (percentage < 50) return 'success'
    if (percentage < 80) return 'warning'
    return 'error'
}

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}
</script>
