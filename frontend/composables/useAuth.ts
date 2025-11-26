export const useAuth = () => {
    const { $api } = useNuxtApp()
    const config = useRuntimeConfig()

    // Use secure cookies only in production (HTTPS)
    const isProduction = process.env.NODE_ENV === 'production'

    const authToken = useCookie('auth_token', {
        maxAge: 60 * 60 * 24 * 7, // 7 days
        secure: false, // Set to false for localhost development
        sameSite: 'lax',
        httpOnly: false,
        default: () => null,
        path: '/'
    })
    const authUser = useCookie('auth_user', {
        maxAge: 60 * 60 * 24 * 7, // 7 days
        secure: false, // Set to false for localhost development
        sameSite: 'lax',
        httpOnly: false,
        default: () => null,
        path: '/'
    })

    const user = useState('user', () => {
        // Try to initialize from cookie or localStorage (client only)
        if (!process.client) return null

        // Prefer cookie values, fall back to localStorage
        let tokenVal = authToken.value
        let userVal = authUser.value

        if ((!tokenVal || !userVal) && typeof window !== 'undefined') {
            try {
                const lsToken = localStorage.getItem('auth_token')
                const lsUser = localStorage.getItem('auth_user')
                if (!tokenVal && lsToken) tokenVal = lsToken
                if (!userVal && lsUser) userVal = lsUser
            } catch (err) {
                // ignore localStorage errors
            }
        }

        if (tokenVal && userVal) {
            try {
                // If userVal is already an object, use it; else parse JSON
                const parsedUser = typeof userVal === 'string' ? JSON.parse(userVal) : userVal
                if (parsedUser && (parsedUser.id !== undefined || parsedUser.username)) {
                    console.log('User state initialized from storage:', parsedUser.username)
                    return parsedUser
                }
            } catch (error) {
                console.warn('Failed to parse user from storage:', error)
                // Clear invalid storage
                authUser.value = null
                authToken.value = null
                try { localStorage.removeItem('auth_user'); localStorage.removeItem('auth_token') } catch (e) { }
            }
        }

        return null
    })

    const isAuthenticated = computed(() => {
        // Ensure both token and user exist and are valid
        const hasValidToken = authToken.value && typeof authToken.value === 'string' && authToken.value.length > 10
        const hasValidUser = user.value?.username && (user.value?.id !== undefined)
        const result = !!(hasValidToken && hasValidUser)

        if (process.client) {
            console.log('Auth state check:', {
                hasValidToken: !!hasValidToken,
                hasValidUser: !!hasValidUser,
                user: user.value?.username,
                isAdmin: user.value?.is_admin,
                result
            })
        }

        return result
    })

    const isAdmin = computed(() => user.value?.is_admin || false)

    // Track initialization to prevent multiple calls
    let isInitializing = false
    let isInitialized = false

    // Initialize auth state from cookies on app start
    const initializeAuth = async () => {
        if (!process.client || isInitializing || isInitialized) {
            return
        }

        isInitializing = true

        try {
            console.log('Initializing auth...', {
                hasToken: !!authToken.value,
                hasUser: !!authUser.value,
                currentUser: !!user.value
            })

            // Prefer cookies but fall back to localStorage to restore auth state
            let tokenVal = authToken.value
            let userVal = authUser.value

            if ((!tokenVal || !userVal) && typeof window !== 'undefined') {
                try {
                    const lsToken = localStorage.getItem('auth_token')
                    const lsUser = localStorage.getItem('auth_user')
                    if (!tokenVal && lsToken) tokenVal = lsToken
                    if (!userVal && lsUser) userVal = lsUser
                } catch (err) {
                    // ignore localStorage read errors
                }
            }

            if (tokenVal && userVal) {
                try {
                    const parsedUser = typeof userVal === 'string' ? JSON.parse(userVal) : userVal
                    if (parsedUser?.username && (parsedUser?.id !== undefined)) {
                        user.value = parsedUser
                        // ensure cookies reflect stored values
                        authUser.value = typeof userVal === 'string' ? userVal : JSON.stringify(parsedUser)
                        authToken.value = tokenVal as any
                        console.log('Auth initialized successfully for user:', parsedUser.username, 'isAdmin:', parsedUser.is_admin)
                        isInitialized = true
                        return
                    }
                } catch (error) {
                    console.error('Failed to parse user data:', error)
                    // Clear invalid storage
                    clearAuth()
                }
            }

            isInitialized = true
        } finally {
            isInitializing = false
        }
    }

    // Clear all auth data
    const clearAuth = () => {
        console.log('Clearing auth data')
        authToken.value = null
        authUser.value = null
        user.value = null
        isInitialized = false

        // Clear any cached state
        if (process.client) {
            try {
                localStorage.removeItem('auth_token')
                localStorage.removeItem('auth_user')
                // Clear all auth-related cookies
                document.cookie = 'auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
                document.cookie = 'auth_user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
            } catch (error) {
                console.warn('Error clearing local storage:', error)
            }
        }
    }

    // Validate token with backend
    const validateToken = async () => {
        if (!authToken.value) {
            return false
        }

        try {
            // Make a simple authenticated request to validate token
            const response = await $api('/api/auth/me', {
                method: 'GET'
            })

            // Update user data from response if needed
            const userData = response as any
            if (userData && userData.id) {
                if (!user.value || user.value.id !== userData.id) {
                    user.value = userData
                    authUser.value = JSON.stringify(userData)
                    console.log('User data refreshed from server')
                }
                return true
            }

            return false
        } catch (error: any) {
            console.error('Token validation failed:', error)
            if (error.status === 401 || error.status === 403) {
                console.log('Token expired or invalid, clearing auth')
                clearAuth()
                return false
            }
            // For network errors, don't clear auth - just log the error
            console.warn('Network error during token validation, keeping current auth state')
            return true // Assume token is still valid for network errors
        }
    }

    const login = async (username: string, password: string) => {
        try {
            console.log('Attempting login for user:', username)
            const response = await $api('/api/auth/login', {
                method: 'POST',
                body: { username, password }
            })
            const data = response as { access_token?: string; user?: any }

            if (data.access_token && data.user && data.user.username) {
                console.log('Login response received:', { username: data.user.username, isAdmin: data.user.is_admin })

                // Set cookies first
                authToken.value = data.access_token
                authUser.value = JSON.stringify(data.user)

                // Then set reactive state
                user.value = data.user
                isInitialized = true

                console.log('Login successful for user:', data.user.username, 'isAdmin:', data.user.is_admin)

                // Force a small delay to ensure cookies are set
                await new Promise(resolve => setTimeout(resolve, 100))

                return { success: true, user: data.user }
            } else {
                console.error('Invalid response format:', data)
                throw new Error('Invalid response format')
            }
        } catch (error: any) {
            console.error('Login failed:', error)
            clearAuth()
            return {
                success: false,
                error: error.data?.detail || error.message || 'Login failed. Please check your credentials.'
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

            if (data.access_token && data.user && data.user.id) {
                // Set cookies first
                authToken.value = data.access_token
                authUser.value = JSON.stringify(data.user)

                // Then set reactive state
                user.value = data.user

                console.log('Registration successful for user:', data.user.username)
                return { success: true, user: data.user }
            } else {
                throw new Error('Invalid response format')
            }
        } catch (error: any) {
            console.error('Registration failed:', error)
            clearAuth()
            return {
                success: false,
                error: error.data?.detail || 'Registration failed. Please try again.'
            }
        }
    }



    const logout = () => {
        clearAuth()
        navigateTo('/login')
    }

    return {
        user,
        isAuthenticated,
        isAdmin,
        login,
        register,
        logout,
        initializeAuth,
        validateToken,
        clearAuth
    }
}
