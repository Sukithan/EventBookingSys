<template>
    <v-card hover @click="viewEvent" class="h-100" :class="{ 'cursor-pointer': clickable }">
        <v-img :src="event.image_url || defaultImage" :height="imageHeight" cover>
            <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-row>
            </template>
        </v-img>

        <v-card-title class="text-h6">{{ event.name }}</v-card-title>

        <v-card-text>
            <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-calendar</v-icon>
                {{ formatDate(event.event_date) }}
            </div>
            <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
                {{ event.location }}
            </div>
            <div class="text-body-2 mb-2">
                <v-icon size="small" class="mr-1">mdi-seat</v-icon>
                {{ event.available_seats }} / {{ event.total_seats }} seats available
            </div>
            <div class="text-h6 primary--text mt-2">
                ${{ event.price.toFixed(2) }}
            </div>
        </v-card-text>

        <v-card-actions>
            <v-chip :color="event.available_seats > 0 ? 'success' : 'error'" size="small" variant="flat">
                {{ event.available_seats > 0 ? 'Available' : 'Sold Out' }}
            </v-chip>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" @click.stop="viewEvent">
                {{ actionText }}
                <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    event: any
    clickable?: boolean
    imageHeight?: string | number
    defaultImage?: string
    actionText?: string
}

interface Emits {
    'view-event': [eventId: number]
}

const props = withDefaults(defineProps<Props>(), {
    clickable: true,
    imageHeight: 200,
    defaultImage: 'https://via.placeholder.com/400x250?text=Event',
    actionText: 'View Details'
})

const emit = defineEmits<Emits>()

const viewEvent = () => {
    if (props.clickable) {
        emit('view-event', props.event.id)
    }
}

const { formatLongDate: formatDate } = useFormatters()
</script>

<style scoped>
.cursor-pointer {
    cursor: pointer;
}
</style>