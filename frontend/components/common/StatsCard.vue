<template>
    <v-card variant="outlined" :color="color" class="h-100">
        <v-card-text class="text-center">
            <v-icon :size="iconSize" :color="color">{{ icon }}</v-icon>
            <div :class="valueClass">{{ value }}</div>
            <div :class="labelClass">{{ label }}</div>
        </v-card-text>
    </v-card>
</template>

<script setup lang="ts">
interface Props {
    icon: string
    value: string | number
    label: string
    color?: string
    iconSize?: string | number
    valueClass?: string
    labelClass?: string
}

withDefaults(defineProps<Props>(), {
    color: 'primary',
    iconSize: 30,
    valueClass: 'text-h6 font-weight-bold',
    labelClass: 'text-caption'
})
</script>