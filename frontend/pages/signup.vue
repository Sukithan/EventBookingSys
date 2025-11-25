<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6" lg="5">
                <v-card elevation="8">
                    <v-card-title class="text-h4 text-center py-6 bg-primary">
                        <span class="text-white">Sign Up</span>
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-alert v-if="error" type="error" variant="tonal" closable class="mb-4"
                            @click:close="error = ''">
                            {{ error }}
                        </v-alert>

                        <v-form ref="form" v-model="valid" @submit.prevent="handleSignup">
                            <v-text-field v-model="userData.full_name" label="Full Name"
                                prepend-inner-icon="mdi-account-circle" :rules="[rules.required]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-text-field v-model="userData.email" label="Email" prepend-inner-icon="mdi-email"
                                :rules="[rules.required, rules.email]" variant="outlined" class="mb-2"></v-text-field>

                            <v-text-field v-model="userData.username" label="Username" prepend-inner-icon="mdi-account"
                                :rules="[rules.required, rules.minLength]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-text-field v-model="userData.password" label="Password" prepend-inner-icon="mdi-lock"
                                :type="showPassword ? 'text' : 'password'"
                                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append-inner="showPassword = !showPassword"
                                :rules="[rules.required, rules.passwordLength]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-text-field v-model="confirmPassword" label="Confirm Password"
                                prepend-inner-icon="mdi-lock-check" :type="showConfirmPassword ? 'text' : 'password'"
                                :append-inner-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append-inner="showConfirmPassword = !showConfirmPassword"
                                :rules="[rules.required, rules.passwordMatch]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-btn type="submit" color="primary" block size="large" :loading="loading"
                                :disabled="!valid" class="mt-4">
                                Sign Up
                            </v-btn>
                        </v-form>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions class="pa-4 justify-center">
                        <p class="text-body-2">
                            Already have an account?
                            <NuxtLink to="/login" class="text-primary font-weight-bold">Login</NuxtLink>
                        </p>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'default'
})

const { register } = useAuth()
const router = useRouter()

const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const error = ref('')
const confirmPassword = ref('')

const userData = reactive({
    full_name: '',
    email: '',
    username: '',
    password: ''
})

const rules = {
    required: (value: string) => !!value || 'This field is required',
    email: (value: string) => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return pattern.test(value) || 'Invalid email address'
    },
    minLength: (value: string) => value.length >= 3 || 'Minimum 3 characters required',
    passwordLength: (value: string) => value.length >= 6 || 'Password must be at least 6 characters',
    passwordMatch: (value: string) => value === userData.password || 'Passwords do not match'
}

const handleSignup = async () => {
    if (!valid.value) return

    loading.value = true
    error.value = ''

    const result = await register(
        userData.email,
        userData.username,
        userData.full_name,
        userData.password
    )

    loading.value = false

    if (result.success) {
        router.push('/my-bookings')
    } else {
        error.value = result.error
    }
}
</script>
