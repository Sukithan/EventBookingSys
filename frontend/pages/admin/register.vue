<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="6" lg="4">
                <v-card elevation="8">
                    <v-card-title class="text-h4 text-center py-6 bg-error">
                        <span class="text-white">Admin Registration Disabled</span>
                    </v-card-title>

                    <v-card-text class="pa-6 text-center">
                        <v-icon size="80" color="error" class="mb-4">mdi-shield-lock</v-icon>

                        <h3 class="text-h6 mb-3">Admin Registration Not Available</h3>

                        <p class="text-body-1 mb-4">
                            Admin registration has been disabled for security reasons.
                            Please contact your system administrator for admin access.
                        </p>

                        <v-alert type="warning" variant="tonal" class="mb-4">
                            <div class="text-center">
                                <strong>Contact System Administrator</strong><br>
                                <span>Please contact your system administrator for admin access credentials.</span>
                            </div>
                        </v-alert>

                        <v-btn color="error" size="large" to="/admin/login" class="mt-4">
                            <v-icon start>mdi-shield-account</v-icon>
                            Go to Admin Login
                        </v-btn>
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
</script>
