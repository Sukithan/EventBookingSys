<template>
    <v-row>
        <v-col cols="12" class="text-center py-12">
            <v-icon :size="iconSize" :color="iconColor">{{ icon }}</v-icon>
            <h2 :class="titleClass">{{ title }}</h2>
            <p v-if="message" :class="messageClass">{{ message }}</p>
            <v-btn v-if="actionText && actionTo" :color="actionColor" :to="actionTo" :variant="actionVariant"
                class="mt-4">
                <v-icon v-if="actionIcon" start>{{ actionIcon }}</v-icon>
                {{ actionText }}
            </v-btn>
            <slot name="action"></slot>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    icon: string
    title: string
    message?: string
    iconSize?: string | number
    iconColor?: string
    titleClass?: string
    messageClass?: string
    actionText?: string
    actionTo?: string
    actionIcon?: string
    actionColor?: string
    actionVariant?: 'text' | 'flat' | 'elevated' | 'outlined' | 'plain' | 'tonal'
}

withDefaults(defineProps<Props>(), {
    iconSize: 80,
    iconColor: 'grey-lighten-1',
    titleClass: 'text-h6 text-grey mt-4',
    messageClass: 'text-body-1 text-grey mb-4',
    actionColor: 'primary',
    actionVariant: 'elevated'
})
</script>