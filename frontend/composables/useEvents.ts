export const useEvents = () => {
    const { $api } = useNuxtApp()

    const events = useState('events', () => [])
    const currentEvent = useState('currentEvent', () => null)

    const fetchEvents = async (search: string = '', activeOnly: boolean = true) => {
        try {
            const response = (await $api('/api/events', {
                params: { search, active_only: activeOnly }
            })) as any[]
            events.value = response
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch events'
            }
        }
    }

    const fetchUpcomingEvents = async () => {
        try {
            const response = (await $api('/api/events/upcoming')) as any[]
            events.value = response
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch upcoming events'
            }
        }
    }

    const fetchEventById = async (id: number) => {
        try {
            const response = await $api(`/api/events/${id}`)
            currentEvent.value = response
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to fetch event details'
            }
        }
    }

    const createEvent = async (eventData: any) => {
        try {
            const response = await $api('/api/events', {
                method: 'POST',
                body: eventData
            })
            return { success: true, data: response }
        } catch (error: any) {
            console.error('Create event error:', error)
            let errorMessage = 'Failed to create event'

            if (error.data?.detail) {
                errorMessage = error.data.detail
            } else if (error.statusText) {
                errorMessage = `${error.status}: ${error.statusText}`
            } else if (error.message) {
                errorMessage = error.message
            }

            return {
                success: false,
                error: errorMessage
            }
        }
    }

    const updateEvent = async (id: number, eventData: any) => {
        try {
            const response = await $api(`/api/events/${id}`, {
                method: 'PUT',
                body: eventData
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to update event'
            }
        }
    }

    const deleteEvent = async (id: number) => {
        try {
            const response = await $api(`/api/events/${id}`, {
                method: 'DELETE'
            })
            return { success: true, data: response }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Failed to delete event'
            }
        }
    }

    return {
        events,
        currentEvent,
        fetchEvents,
        fetchUpcomingEvents,
        fetchEventById,
        createEvent,
        updateEvent,
        deleteEvent
    }
}
