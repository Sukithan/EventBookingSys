<template>
    <v-container>
        <v-row>
            <v-col cols="12" md="8" offset-md="2">
                <v-card>
                    <v-card-title class="text-h5 pa-6 bg-primary text-white">
                        Create New Event
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-form ref="form" v-model="valid" @submit.prevent="handleCreate">
                            <v-text-field v-model="eventData.name" label="Event Name *" :rules="[rules.required]"
                                variant="outlined" class="mb-4"></v-text-field>

                            <v-textarea v-model="eventData.description" label="Description" variant="outlined" rows="4"
                                class="mb-4"></v-textarea>

                            <v-text-field v-model="eventData.event_date" label="Event Date & Time *"
                                type="datetime-local" :rules="[rules.required]" variant="outlined"
                                class="mb-4"></v-text-field>

                            <v-text-field v-model="eventData.location" label="Location *" :rules="[rules.required]"
                                variant="outlined" class="mb-4"></v-text-field>

                            <v-row>
                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.rows" label="Number of Rows *" type="number"
                                        :rules="[rules.required, rules.positive]" variant="outlined"
                                        @input="calculateTotalSeats"></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.seats_per_row" label="Seats per Row *"
                                        type="number" :rules="[rules.required, rules.positive]" variant="outlined"
                                        @input="calculateTotalSeats"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.total_seats" label="Total Seats"
                                        type="number" variant="outlined" readonly
                                        hint="Automatically calculated from rows × seats per row"
                                        persistent-hint></v-text-field>
                                </v-col>
                                <v-col cols="12" sm="6">
                                    <v-text-field v-model.number="eventData.price" label="Price *" type="number"
                                        step="0.01" prefix="$" :rules="[rules.required, rules.nonNegative]"
                                        variant="outlined"></v-text-field>
                                </v-col>
                            </v-row>

                            <v-text-field v-model="eventData.image_url" label="Image URL (Optional)" variant="outlined"
                                class="mb-4"></v-text-field>

                            <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

                            <div class="d-flex gap-2">
                                <v-btn color="primary" type="submit" :loading="loading" :disabled="!valid" size="large">
                                    <v-icon start>mdi-plus</v-icon>
                                    Create Event
                                </v-btn>
                                <v-btn color="grey" to="/admin/events" size="large" variant="outlined">
                                    Cancel
                                </v-btn>
                            </div>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const { createEvent } = useEvents()
const router = useRouter()

const valid = ref(false)
const loading = ref(false)
const error = ref('')

const eventData = reactive({
    name: '',
    description: '',
    event_date: '',
    location: '',
    rows: 10,
    seats_per_row: 10,
    total_seats: 100,
    price: 0,
    image_url: ''
})

// Watch for changes in rows and seats_per_row to automatically calculate total_seats
watch([() => eventData.rows, () => eventData.seats_per_row], () => {
    calculateTotalSeats()
})

// Initialize total seats on component mount
onMounted(() => {
    calculateTotalSeats()
})

const rules = {
    required: (v: any) => !!v || 'This field is required',
    positive: (v: number) => v > 0 || 'Must be greater than 0',
    nonNegative: (v: number) => v >= 0 || 'Must be 0 or greater'
}

const calculateTotalSeats = () => {
    if (eventData.rows > 0 && eventData.seats_per_row > 0) {
        eventData.total_seats = eventData.rows * eventData.seats_per_row
    }
}

const handleCreate = async () => {
    if (!valid.value) return

    loading.value = true
    error.value = ''

    // Convert datetime-local to ISO format
    const eventDataToSend = {
        ...eventData,
        event_date: new Date(eventData.event_date).toISOString()
    }

    const result = await createEvent(eventDataToSend)
    loading.value = false

    if (result.success) {
        router.push('/admin/events')
    } else {
        error.value = result.error
    }
}
</script>
