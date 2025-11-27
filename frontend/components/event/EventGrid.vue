<template>
    <v-row>
        <v-col v-for="event in events" :key="event.id" :cols="cols" :sm="sm" :md="md" :lg="lg">
            <EventCard :event="event" :image-height="imageHeight" @view-event="handleViewEvent" />
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    events: any[]
    cols?: number
    sm?: number
    md?: number
    lg?: number
    imageHeight?: string | number
}

interface Emits {
    'view-event': [eventId: number]
}

withDefaults(defineProps<Props>(), {
    cols: 12,
    sm: 6,
    md: 4,
    lg: 4,
    imageHeight: 200
})

const emit = defineEmits<Emits>()

const handleViewEvent = (eventId: number) => {
    emit('view-event', eventId)
}
</script>