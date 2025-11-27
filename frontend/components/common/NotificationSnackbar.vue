<template>
    <v-snackbar v-model="show" :color="color" :timeout="timeout" :location="location">
        {{ message }}
        <template v-slot:actions>
            <v-btn variant="text" @click="show = false">{{ actionText }}</v-btn>
        </template>
    </v-snackbar>
</template>

<script setup lang="ts">
interface Props {
    modelValue: boolean
    message: string
    color?: string
    timeout?: number
    location?: any
    actionText?: string
}

interface Emits {
    'update:modelValue': [value: boolean]
}

const props = withDefaults(defineProps<Props>(), {
    color: 'success',
    timeout: 5000,
    location: 'bottom',
    actionText: 'Close'
})

const emit = defineEmits<Emits>()

const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})
</script>