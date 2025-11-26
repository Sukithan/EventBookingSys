<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex justify-space-between align-center mb-6">
                    <h1 class="text-h4 font-weight-bold">Manage Events</h1>
                    <v-btn color="primary" to="/admin/events/create">
                        <v-icon start>mdi-plus</v-icon>
                        Create Event
                    </v-btn>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col v-for="n in 4" :key="n" cols="12">
                <v-skeleton-loader type="article"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="events.length > 0">
            <v-col cols="12">
                <v-card>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="events" :items-per-page="10" class="elevation-0">
                            <template v-slot:item.event_date="{ item }">
                                {{ formatDate(item.event_date) }}
                            </template>

                            <template v-slot:item.available_seats="{ item }">
                                {{ item.available_seats }} / {{ item.total_seats }}
                            </template>

                            <template v-slot:item.price="{ item }">
                                ${{ item.price.toFixed(2) }}
                            </template>

                            <template v-slot:item.is_active="{ item }">
                                <v-chip :color="item.is_active ? 'success' : 'error'" size="small">
                                    {{ item.is_active ? 'Active' : 'Inactive' }}
                                </v-chip>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <v-btn icon="mdi-information" size="small" variant="text" @click="viewDetails(item.id)"
                                    title="View Details"></v-btn>
                                <v-btn icon="mdi-ticket" size="small" variant="text" @click="viewBookings(item.id)"
                                    title="View Bookings"></v-btn>
                                <v-btn icon="mdi-pencil" size="small" variant="text" @click="editEvent(item.id)"
                                    title="Edit"></v-btn>
                                <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                                    @click="deleteEventConfirm(item)" title="Delete"></v-btn>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-calendar-blank</v-icon>
                <p class="text-h6 text-grey mt-4">No events created yet</p>
                <v-btn color="primary" to="/admin/events/create" class="mt-4">
                    Create First Event
                </v-btn>
            </v-col>
        </v-row>

        <!-- Delete Confirmation Dialog -->
        <v-dialog v-model="deleteDialog" max-width="500">
            <v-card>
                <v-card-title>Delete Event</v-card-title>
                <v-card-text>
                    Are you sure you want to delete <strong>{{ selectedEvent?.name }}</strong>?
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="deleteDialog = false">Cancel</v-btn>
                    <v-btn color="error" :loading="deleting" @click="confirmDelete">Delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-snackbar v-model="snackbar" :color="snackbarColor">
            {{ snackbarMessage }}
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { fetchAllEvents } = useAdmin()
const { deleteEvent } = useEvents()
const router = useRouter()

const loading = ref(false)
const deleting = ref(false)
const events = ref<any[]>([])
const deleteDialog = ref(false)
const selectedEvent = ref<any>(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const headers = [
    { title: 'Event Name', value: 'name', key: 'name' },
    { title: 'Date', value: 'event_date', key: 'event_date' },
    { title: 'Location', value: 'location', key: 'location' },
    { title: 'Seats', value: 'available_seats', key: 'available_seats' },
    { title: 'Price', value: 'price', key: 'price' },
    { title: 'Status', value: 'is_active', key: 'is_active' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]

const loadEvents = async () => {
    loading.value = true
    const result = await fetchAllEvents()
    if (result.success) {
        events.value = result.data as any[]
    }
    loading.value = false
}

const viewDetails = (id: number) => {
    router.push(`/events/${id}`)
}

const viewBookings = (id: number) => {
    router.push(`/admin/events/${id}/bookings`)
}

const editEvent = (id: number) => {
    router.push(`/admin/events/${id}/edit`)
}

const deleteEventConfirm = (event: any) => {
    selectedEvent.value = event
    deleteDialog.value = true
}

const confirmDelete = async () => {
    if (!selectedEvent.value) return

    deleting.value = true
    const result = await deleteEvent(selectedEvent.value.id)
    deleting.value = false

    if (result.success) {
        snackbarMessage.value = 'Event deleted successfully'
        snackbarColor.value = 'success'
        deleteDialog.value = false
        await loadEvents()
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
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
    loadEvents()
})
</script>
