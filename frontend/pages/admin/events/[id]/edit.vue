<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex align-center mb-6">
                    <v-btn icon="mdi-arrow-left" variant="text" @click="$router.go(-1)" class="mr-3"></v-btn>
                    <h1 class="text-h4 font-weight-bold">Edit Event</h1>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article, actions"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="event">
            <v-col cols="12" md="8">
                <v-card>
                    <v-card-title>Event Details</v-card-title>
                    <v-card-text>
                        <v-form ref="form" v-model="valid" @submit.prevent="saveEvent">
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="eventData.name" label="Event Name" :rules="[rules.required]"
                                        variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12">
                                    <v-textarea v-model="eventData.description" label="Description" variant="outlined"
                                        rows="3"></v-textarea>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model="eventData.location" label="Location"
                                        :rules="[rules.required]" variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model="eventData.price" label="Price" type="number" step="0.01"
                                        min="0" :rules="[rules.required]" variant="outlined" prefix="$"></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model="eventData.event_date" label="Event Date & Time"
                                        type="datetime-local" :rules="[rules.required]"
                                        variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model="eventData.image_url" label="Image URL"
                                        variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.rows" label="Number of Rows" type="number"
                                        min="1" :rules="[rules.required]" variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.seats_per_row" label="Seats per Row"
                                        type="number" min="1" :rules="[rules.required]"
                                        variant="outlined"></v-text-field>
                                </v-col>

                                <v-col cols="12">
                                    <v-switch v-model="eventData.is_active" label="Event Active" color="primary"
                                        hide-details></v-switch>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="$router.go(-1)">Cancel</v-btn>
                        <v-btn color="primary" :loading="saving" :disabled="!valid" @click="saveEvent">
                            Save Changes
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>

            <v-col cols="12" md="4">
                <v-card class="mb-4">
                    <v-card-title>Quick Actions</v-card-title>
                    <v-card-text>
                        <div class="d-flex flex-column gap-2">
                            <v-btn color="orange" variant="outlined" @click="viewBookings">
                                <v-icon start>mdi-ticket</v-icon>
                                View Bookings
                            </v-btn>
                            <v-btn color="error" variant="outlined" @click="cancelAllBookings">
                                <v-icon start>mdi-cancel</v-icon>
                                Cancel All Bookings
                            </v-btn>
                        </div>
                    </v-card-text>
                </v-card>

                <v-card>
                    <v-card-title>Event Statistics</v-card-title>
                    <v-card-text>
                        <div class="mb-3" v-if="calculatedTotalSeats !== event.total_seats">
                            <div class="text-caption text-grey">Total Seats </div>
                            <div class="text-h6 text-warning">{{ calculatedTotalSeats }}</div>
                        </div>
                        <v-divider class="my-3"></v-divider>
                        <v-row>
                            <v-col cols="6">
                                <div class="text-center">
                                    <div class="text-h4 text-primary">{{ bookedSeats }}
                                    </div>
                                    <div class="text-caption">Booked</div>
                                </div>
                            </v-col>
                            <v-col cols="6">
                                <div class="text-center">
                                    <div class="text-h4 text-success">{{ calculatedAvailableSeats }}</div>
                                    <div class="text-caption">Available (after save)</div>
                                </div>
                            </v-col>
                        </v-row>
                        <v-progress-linear :model-value="bookingPercentage" color="primary" height="8" rounded
                            class="mt-3"></v-progress-linear>
                        <div class="text-center mt-2 text-caption">
                            {{ Math.round(bookingPercentage) }}% Full
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row v-else>
            <v-col cols="12" class="text-center py-12">
                <v-icon size="80" color="grey-lighten-1">mdi-alert-circle</v-icon>
                <p class="text-h6 text-grey mt-4">Event not found</p>
            </v-col>
        </v-row>

        <!-- Cancel All Bookings Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5">Cancel All Bookings</v-card-title>
                <v-card-text>
                    <p>Are you sure you want to cancel all bookings for this event?</p>
                    <p class="text-body-2 text-grey mt-2">
                        This will cancel {{ event?.total_seats - event?.available_seats }} booking(s) and free up all
                        seats.
                    </p>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="cancelDialog = false">Cancel</v-btn>
                    <v-btn color="error" :loading="cancelling" @click="confirmCancelAllBookings">
                        Cancel All Bookings
                    </v-btn>
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

const route = useRoute()
const router = useRouter()
const { fetchEventById, updateEvent } = useEvents()
const { cancelBooking } = useAdmin()

const loading = ref(false)
const saving = ref(false)
const cancelling = ref(false)
const valid = ref(false)
const event = ref<any>(null)
const cancelDialog = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const eventData = reactive({
    name: '',
    description: '',
    location: '',
    price: 0,
    event_date: '',
    image_url: '',
    rows: 10,
    seats_per_row: 10,
    is_active: true
})

const calculatedTotalSeats = computed(() => {
    return (eventData.rows || 0) * (eventData.seats_per_row || 0)
})

const bookedSeats = computed(() => {
    if (!event.value) return 0
    return event.value.total_seats - event.value.available_seats
})

const calculatedAvailableSeats = computed(() => {
    if (!event.value) return 0
    const seatsDiff = calculatedTotalSeats.value - event.value.total_seats
    return event.value.available_seats + seatsDiff
})

const bookingPercentage = computed(() => {
    if (calculatedTotalSeats.value === 0) return 0
    return (bookedSeats.value / calculatedTotalSeats.value) * 100
})

const rules = {
    required: (value: any) => !!value || 'This field is required'
}

const loadEvent = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)
    const result = await fetchEventById(eventId)

    if (result.success) {
        event.value = result.data
        // Populate form data
        Object.assign(eventData, {
            name: event.value.name,
            description: event.value.description || '',
            location: event.value.location,
            price: event.value.price,
            event_date: formatDateTimeForInput(event.value.event_date),
            image_url: event.value.image_url || '',
            rows: event.value.rows || 10,
            seats_per_row: event.value.seats_per_row || 10,
            is_active: event.value.is_active
        })
    }
    loading.value = false
}

const saveEvent = async () => {
    if (!valid.value) return

    saving.value = true
    const eventId = parseInt(route.params.id as string)
    const result = await updateEvent(eventId, eventData)
    saving.value = false

    if (result.success) {
        snackbarMessage.value = 'Event updated successfully'
        snackbarColor.value = 'success'
        await loadEvent() // Reload event data
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}


const viewBookings = () => {
    router.push(`/admin/events/${route.params.id}/bookings`)
}

const cancelAllBookings = () => {
    cancelDialog.value = true
}

const confirmCancelAllBookings = async () => {
    cancelling.value = true
    // TODO: Implement cancel all bookings API call
    await new Promise(resolve => setTimeout(resolve, 1000)) // Placeholder
    cancelling.value = false
    cancelDialog.value = false

    snackbarMessage.value = 'All bookings cancelled successfully'
    snackbarColor.value = 'success'
    snackbar.value = true

    await loadEvent() // Reload to update statistics
}

const formatDateTimeForInput = (dateString: string) => {
    const date = new Date(dateString)
    return date.toISOString().slice(0, 16)
}

onMounted(() => {
    loadEvent()
})
</script>