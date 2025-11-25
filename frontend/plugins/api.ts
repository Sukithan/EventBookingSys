export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig()

    const api = $fetch.create({
        baseURL: config.public.apiBase as string,
        onRequest({ options }) {
            const token = useCookie('auth_token').value
            if (!options.headers) {
                options.headers = new Headers()
            }
            if (token) {
                (options.headers as Headers).set('Authorization', `Bearer ${token}`)
            }
        },
        onResponseError({ response }) {
            if (response.status === 401) {
                // Clear auth and redirect to login
                const authToken = useCookie('auth_token')
                const authUser = useCookie('auth_user')
                authToken.value = null
                authUser.value = null

                if (process.client) {
                    navigateTo('/login')
                }
            }
            console.error('API Error:', response.status, response.statusText)
        }
    })

    return {
        provide: {
            api
        }
    }
})
