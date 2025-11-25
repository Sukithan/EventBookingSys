<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6" lg="4">
                <v-card elevation="8">
                    <v-card-title class="text-h4 text-center py-6 bg-error">
                        <span class="text-white">Admin Login</span>
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-alert v-if="error" type="error" variant="tonal" closable class="mb-4"
                            @click:close="error = ''">
                            {{ error }}
                        </v-alert>

                        <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
                            <v-text-field v-model="credentials.username" label="Admin Username"
                                prepend-inner-icon="mdi-shield-account" :rules="[rules.required]" variant="outlined"
                                class="mb-2"></v-text-field>

                            <v-text-field v-model="credentials.password" label="Password" prepend-inner-icon="mdi-lock"
                                :type="showPassword ? 'text' : 'password'"
                                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                @click:append-inner="showPassword = !showPassword" :rules="[rules.required]"
                                variant="outlined" class="mb-2"></v-text-field>

                            <v-btn type="submit" color="error" block size="large" :loading="loading" :disabled="!valid"
                                class="mt-4">
                                <v-icon start>mdi-shield-lock</v-icon>
                                Admin Login
                            </v-btn>
                        </v-form>
                    </v-card-text>


                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'default'
})

const { login, user } = useAuth()
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
            error.value = 'Access denied. Admin privileges required.'
        }
    } else {
        error.value = result.error
    }
}
</script>
