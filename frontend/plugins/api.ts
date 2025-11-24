export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig()

    const api = $fetch.create({
        baseURL: config.public.apiBase as string,
        onRequest({ options }) {
            // Add any default headers here
            if (!options.headers) {
                options.headers = new Headers()
            }
        },
        onResponseError({ response }) {
            // Handle API errors globally
            console.error('API Error:', response.status, response.statusText)
        }
    })

    return {
        provide: {
            api
        }
    }
})
