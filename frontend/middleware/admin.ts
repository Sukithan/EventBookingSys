export default defineNuxtRouteMiddleware(async (to, from) => {
    const { isAuthenticated, isAdmin, user, initializeAuth } = useAuth()

    // Only run on client side to avoid SSR issues
    if (process.server) {
        return
    }

    // Ensure auth is initialized
    await initializeAuth()
    await nextTick()

    console.log('Admin middleware check:', {
        isAuthenticated: isAuthenticated.value,
        isAdmin: isAdmin.value,
        username: user.value?.username,
        userIsAdmin: user.value?.is_admin
    })

    if (!isAuthenticated.value) {
        console.log('Admin middleware: Not authenticated, redirecting to login')
        return navigateTo('/login')
    }

    if (!isAdmin.value) {
        console.log('Admin middleware: Not admin, redirecting to home')
        return navigateTo('/')
    }

    console.log('Admin middleware: Access granted for admin user:', user.value?.username)
})
