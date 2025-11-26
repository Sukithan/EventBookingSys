export default defineNuxtRouteMiddleware(async (to, from) => {
    const { isAuthenticated, initializeAuth, user } = useAuth()

    // Only run on client side to avoid SSR issues
    if (process.server) {
        return
    }

    // Initialize auth state from cookies if not already done
    await initializeAuth()

    // Wait a tick to ensure reactivity has updated
    await nextTick()

    // Add a small delay to ensure auth state is properly set
    await new Promise(resolve => setTimeout(resolve, 100))

    // If not authenticated, redirect to login
    if (!isAuthenticated.value) {
        console.log('Auth middleware: User not authenticated, redirecting to login')
        return navigateTo('/login')
    }

    console.log('Auth middleware: User authenticated, allowing access for:', user.value?.username, 'isAdmin:', user.value?.is_admin)
})
