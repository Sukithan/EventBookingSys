<template>
    <v-card>
        <v-card-text>
            <v-data-table :headers="headers" :items="events" :items-per-page="itemsPerPage" class="elevation-0"
                :loading="loading">
                <template v-slot:item.event_date="{ item }">
                    {{ formatDate(item.event_date) }}
                </template>

                <template v-slot:item.available_seats="{ item }">
                    {{ item.available_seats }} / {{ item.total_seats }}
                </template>

                <template v-slot:item.price="{ item }">
                    {{ formatPrice(item.price) }}
                </template>

                <template v-slot:item.is_active="{ item }">
                    <v-chip :color="item.is_active ? 'success' : 'error'" size="small">
                        {{ item.is_active ? 'Active' : 'Inactive' }}
                    </v-chip>
                </template>

                <template v-slot:item.actions="{ item }">
                    <v-btn icon="mdi-ticket" size="small" variant="text" color="primary"
                        @click="$emit('view-bookings', item.id)" title="View Details & Bookings"></v-btn>
                    <v-btn icon="mdi-pencil" size="small" variant="text" @click="$emit('edit-event', item.id)"
                        title="Edit"></v-btn>
                    <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                        @click="$emit('delete-event', item)" title="Delete"></v-btn>
                </template>
            </v-data-table>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    events: any[]
    loading?: boolean
    itemsPerPage?: number
}

interface Emits {
    'view-bookings': [eventId: number]
    'edit-event': [eventId: number]
    'delete-event': [event: any]
}

withDefaults(defineProps<Props>(), {
    itemsPerPage: 10
})

defineEmits<Emits>()

const { formatDate, formatPrice } = useFormatters()

const headers = [
    { title: 'Event Name', value: 'name', key: 'name' },
    { title: 'Date', value: 'event_date', key: 'event_date' },
    { title: 'Location', value: 'location', key: 'location' },
    { title: 'Seats', value: 'available_seats', key: 'available_seats' },
    { title: 'Price', value: 'price', key: 'price' },
    { title: 'Status', value: 'is_active', key: 'is_active' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]
</script>