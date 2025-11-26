export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig()

    const api = $fetch.create({
        baseURL: config.public.apiBase as string,
        onRequest({ options }) {
            // Prefer cookie token; fall back to localStorage token on client
            let token: string | null | undefined = useCookie('auth_token').value
            if (process.client && (!token || typeof token !== 'string' || token.length <= 10)) {
                try {
                    const ls = localStorage.getItem('auth_token')
                    if (ls) token = ls
                } catch (err) {
                    // ignore localStorage errors
                }
            }

            if (!options.headers) {
                options.headers = new Headers()
            }
            if (token && typeof token === 'string' && token.length > 10) {
                (options.headers as Headers).set('Authorization', `Bearer ${token}`)
            }
        },
        onResponseError({ response }) {
            if (response.status === 401) {
                console.warn('API 401 error - token may be expired')
                // Clear auth and redirect to login only if on client side
                if (process.client) {
                    // Add a small delay to prevent race conditions
                    setTimeout(() => {
                        const { clearAuth } = useAuth()
                        clearAuth()

                        // Only redirect if not already on login page
                        const route = useRoute()
                        if (route.path !== '/login' && route.path !== '/signup') {
                            navigateTo('/login')
                        }
                    }, 100)
                }
            } else {
                console.error('API Error:', response.status, response.statusText)
            }
        }
    })

    return {
        provide: {
            api
        }
    }
})
