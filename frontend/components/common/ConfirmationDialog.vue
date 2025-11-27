<template>
    <v-dialog v-model="show" max-width="500" :fullscreen="display.xs.value">
        <v-card>
            <v-card-title :class="titleClass">
                <v-icon v-if="icon" start>{{ icon }}</v-icon>
                {{ title }}
            </v-card-title>
            <v-card-text class="pa-6">
                <p class="text-body-1">{{ message }}</p>
                <v-alert v-if="details" :type="alertType" variant="tonal" class="mt-4">
                    <div v-html="details"></div>
                </v-alert>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn variant="text" @click="cancel">{{ cancelText }}</v-btn>
                <v-btn :color="confirmColor" :loading="loading" @click="confirm">
                    {{ confirmText }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'

const display = useDisplay()

interface Props {
    modelValue: boolean
    title: string
    message: string
    details?: string
    icon?: string
    titleClass?: string
    alertType?: 'info' | 'warning' | 'error' | 'success'
    confirmText?: string
    cancelText?: string
    confirmColor?: string
    loading?: boolean
}

interface Emits {
    'update:modelValue': [value: boolean]
    'confirm': []
    'cancel': []
}

const props = withDefaults(defineProps<Props>(), {
    titleClass: 'text-h5 bg-error text-white',
    alertType: 'warning',
    confirmText: 'Confirm',
    cancelText: 'Cancel',
    confirmColor: 'error'
})

const emit = defineEmits<Emits>()

const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const confirm = () => {
    console.log('=== ConfirmationDialog: Confirm button clicked ===')
    console.log('Emitting confirm event')
    emit('confirm')
    console.log('Confirm event emitted')
    // Don't close the dialog here - let the parent handle it after the async operation completes
}

const cancel = () => {
    show.value = false
    emit('cancel')
}
</script>