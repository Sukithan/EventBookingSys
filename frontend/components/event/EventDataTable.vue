<template>
    <v-card>
        <v-card-text>
            <v-data-table :headers="headers" :items="events" :items-per-page="itemsPerPage" class="elevation-0"
                :loading="loading">
                <template v-slot:item.event_date="{ item }">
                    <div class="d-flex align-center">
                        <span>{{ formatDate(item.event_date) }}</span>
                        <v-chip v-if="isExpired(item.event_date)" color="warning" size="x-small" class="ml-2">
                            Expired
                        </v-chip>
                    </div>
                </template>

                <template v-slot:item.available_seats="{ item }">
                    {{ item.available_seats }} / {{ item.total_seats }}
                </template>

                <template v-slot:item.price="{ item }">
                    {{ formatPrice(item.price) }}
                </template>

                <template v-slot:item.is_active="{ item }">
                    <div class="d-flex flex-column gap-1">
                        <v-chip :color="getStatusColor(item)" size="small">
                            {{ getStatusText(item) }}
                        </v-chip>
                        <v-chip v-if="isExpired(item.event_date) && item.is_active" color="warning" size="x-small"
                            variant="outlined">
                            Should be inactive
                        </v-chip>
                    </div>
                </template>

                <template v-slot:item.actions="{ item }">
                    <v-btn icon="mdi-ticket" size="small" variant="text" color="primary"
                        @click="$emit('view-bookings', item.id)" title="View Details & Bookings"></v-btn>
                    <v-btn icon="mdi-pencil" size="small" variant="text" @click="$emit('edit-event', item.id)"
                        title="Edit"></v-btn>
                    <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                        @click="$emit('delete-event', item)" title="Delete"></v-btn>
                </template>

                <template v-slot:item="{ item }">
                    <tr :class="{ 'expired-row': isExpired(item.event_date) && item.is_active }">
                        <td>{{ item.name }}</td>
                        <td>
                            <div class="d-flex align-center">
                                <span>{{ formatDate(item.event_date) }}</span>
                                <v-chip v-if="isExpired(item.event_date)" color="warning" size="x-small" class="ml-2">
                                    Expired
                                </v-chip>
                            </div>
                        </td>
                        <td>{{ item.location }}</td>
                        <td>{{ item.available_seats }} / {{ item.total_seats }}</td>
                        <td>{{ formatPrice(item.price) }}</td>
                        <td>
                            <div class="d-flex flex-column gap-1">
                                <v-chip :color="getStatusColor(item)" size="small">
                                    {{ getStatusText(item) }}
                                </v-chip>
                                <v-chip v-if="isExpired(item.event_date) && item.is_active" color="warning"
                                    size="x-small" variant="outlined">
                                    Should be inactive
                                </v-chip>
                            </div>
                        </td>
                        <td>
                            <v-btn icon="mdi-ticket" size="small" variant="text" color="primary"
                                @click="$emit('view-bookings', item.id)" title="View Details & Bookings"></v-btn>
                            <v-btn icon="mdi-pencil" size="small" variant="text" @click="$emit('edit-event', item.id)"
                                title="Edit"></v-btn>
                            <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                                @click="$emit('delete-event', item)" title="Delete"></v-btn>
                        </td>
                    </tr>
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

const isExpired = (eventDate: string): boolean => {
    const now = new Date()
    const eventDateTime = new Date(eventDate)
    return eventDateTime < now
}

const getStatusColor = (item: any): string => {
    if (isExpired(item.event_date)) {
        return item.is_active ? 'warning' : 'error'
    }
    return item.is_active ? 'success' : 'error'
}

const getStatusText = (item: any): string => {
    if (isExpired(item.event_date)) {
        return item.is_active ? 'Expired (Active)' : 'Expired'
    }
    return item.is_active ? 'Active' : 'Inactive'
}

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

<style scoped>
:deep(.expired-row) {
    background-color: rgba(255, 193, 7, 0.1) !important;
    opacity: 0.8;
}

:deep(.expired-row:hover) {
    background-color: rgba(255, 193, 7, 0.2) !important;
}
</style>