<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="10" md="6" lg="4">
                <v-card elevation="8">
                    <v-card-title class="text-h4 text-center py-6 bg-primary">
                        <span class="text-white">Login</span>
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-alert v-if="error" type="error" variant="tonal" closable class="mb-4"
                            @click:close="error = ''">
                            {{ error }}
                        </v-alert>

                        <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
                            <v-text-field v-model="credentials.username" label="Username"
                                prepend-inner-icon="mdi-account" :rules="[rules.required]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-text-field v-model="credentials.password" label="Password" prepend-inner-icon="mdi-lock"
                                :type="showPassword ? 'text' : 'password'"
                                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append-inner="showPassword = !showPassword" :rules="[rules.required]"
                                variant="outlined" class="mb-2"></v-text-field>

                            <v-btn type="submit" color="primary" block size="large" :loading="loading"
                                :disabled="!valid" class="mt-4">
                                Login
                            </v-btn>
                        </v-form>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions class="pa-4 justify-center">
                        <p class="text-body-2">
                            Don't have an account?
                            <NuxtLink to="/signup" class="text-primary font-weight-bold">Sign up</NuxtLink>
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

const { login } = useAuth()
const router = useRouter()

const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const error = ref('')

const credentials = reactive({
    username: '',
    password: ''
})

const rules = {
    required: (value: string) => !!value || 'This field is required'
}

const handleLogin = async () => {
    if (!valid.value) return

    loading.value = true
    error.value = ''

    const result = await login(credentials.username, credentials.password)

    loading.value = false

    if (result.success) {
        if (result.user.is_admin) {
            router.push('/admin/dashboard')
        } else {
            router.push('/')
        }
    } else {
        error.value = result.error
    }
}
</script>
