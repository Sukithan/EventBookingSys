export const useAuth = () => {
    const { $api } = useNuxtApp()
    const authToken = useCookie('auth_token', { maxAge: 60 * 60 * 24 * 7 }) // 7 days
    const authUser = useCookie('auth_user', { maxAge: 60 * 60 * 24 * 7 })

    const user = useState('user', () => {
        if (!authUser.value) return null
        try {
            // Check if the value is a valid JSON string
            const userValue = authUser.value as string
            if (userValue === '[object Object]' || userValue.trim() === '') {
                // Clear invalid data
                authUser.value = null
                return null
            }
            return JSON.parse(userValue)
        } catch (error) {
            // Clear invalid JSON data
            authUser.value = null
            return null
        }
    })
    const isAuthenticated = computed(() => !!user.value && !!authToken.value)
    const isAdmin = computed(() => user.value?.is_admin || false)

    const login = async (username: string, password: string) => {
        try {
            const response = await $api('/api/auth/login', {
                method: 'POST',
                body: { username, password }
            })
            const data = response as { access_token?: string; user?: any }

            authToken.value = data.access_token ?? null
            authUser.value = data.user ? JSON.stringify(data.user) : null
            user.value = data.user ?? null

            return { success: true, user: data.user ?? null }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Login failed. Please check your credentials.'
            }
        }
    }

    const register = async (email: string, username: string, full_name: string, password: string) => {
        try {
            const response = await $api('/api/auth/register', {
                method: 'POST',
                body: { email, username, full_name, password }
            })

            const data = response as { access_token?: string; user?: any }

            authToken.value = data.access_token ?? null
            authUser.value = data.user ? JSON.stringify(data.user) : null
            user.value = data.user ?? null

            return { success: true, user: data.user ?? null }
        } catch (error: any) {
            return {
                success: false,
                error: error.data?.detail || 'Registration failed. Please try again.'
            }
        }
    }



    const logout = () => {
        authToken.value = null
        authUser.value = null
        user.value = null
        navigateTo('/login')
    }

    return {
        user,
        isAuthenticated,
        isAdmin,
        login,
        register,
        logout
    }
}
