export default defineNuxtPlugin(async () => {
    const { initializeAuth, isAuthenticated } = useAuth()

    // Initialize auth state from cookies on client side
    if (process.client) {
        console.log('Auth plugin initializing...')

        // Wait for DOM to be ready and hydration to complete
        await new Promise(resolve => {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', resolve)
            } else {
                resolve(null)
            }
        })

        // Add a delay to ensure hydration is complete and cookies are available
        await new Promise(resolve => setTimeout(resolve, 100))

        try {
            await initializeAuth()
            console.log('Auth plugin initialized successfully. Authenticated:', isAuthenticated.value)

            // Log current auth state for debugging
            const { user } = useAuth()
            if (user.value) {
                console.log('Current user:', user.value.username, 'isAdmin:', user.value.is_admin)
            }
        } catch (error) {
            console.error('Auth plugin initialization failed:', error)
        }
    }
})