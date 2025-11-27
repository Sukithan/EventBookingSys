<template>
    <v-container>
        <PageHeader title="Manage Events" action-text="Create Event" action-to="/admin/events/create"
            action-icon="mdi-plus" />

        <LoadingSkeleton v-if="loading" type="article" :count="4" />

        <v-row v-else-if="events.length > 0">
            <v-col cols="12">
                <EventDataTable :events="events" :loading="loading" @view-bookings="viewBookings"
                    @edit-event="editEvent" @delete-event="deleteEventConfirm" />
            </v-col>
        </v-row>

        <EmptyState v-else icon="mdi-calendar-blank" title="No events created yet" action-text="Create First Event"
            action-to="/admin/events/create" action-icon="mdi-plus" />

        <!-- Delete Confirmation Dialog -->
        <ConfirmationDialog v-model="deleteDialog" title="Delete Event"
            :message="`Are you sure you want to delete ${selectedEvent?.name}?`" icon="mdi-delete" confirm-text="Delete"
            :loading="deleting" @confirm="confirmDelete" />

        <NotificationSnackbar v-model="snackbar" :message="snackbarMessage" :color="snackbarColor" />
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



const loadEvents = async () => {
    loading.value = true
    const result = await fetchAllEvents()
    if (result.success) {
        events.value = result.data as any[]
    }
    loading.value = false
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



onMounted(() => {
    loadEvents()
})
</script>
