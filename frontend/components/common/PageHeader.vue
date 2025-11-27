<template>
    <v-row class="mb-6">
        <v-col cols="12">
            <div :class="containerClass">
                <div>
                    <h1 :class="titleClass">{{ title }}</h1>
                    <p v-if="subtitle" :class="subtitleClass">{{ subtitle }}</p>
                </div>
                <div v-if="$slots.actions || actionText" :class="actionsClass">
                    <slot name="actions">
                        <v-btn v-if="actionText" :color="actionColor" :variant="actionVariant" :to="actionTo"
                            :@click="actionClick">
                            <v-icon v-if="actionIcon" start>{{ actionIcon }}</v-icon>
                            {{ actionText }}
                        </v-btn>
                    </slot>
                </div>
            </div>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    title: string
    subtitle?: string
    titleClass?: string
    subtitleClass?: string
    containerClass?: string
    actionsClass?: string
    actionText?: string
    actionTo?: string
    actionIcon?: string
    actionColor?: string
    actionVariant?: "text" | "flat" | "elevated" | "outlined" | "plain" | "tonal"
    actionClick?: () => void
}

withDefaults(defineProps<Props>(), {
    titleClass: 'text-h4 font-weight-bold',
    subtitleClass: 'text-body-1 text-grey mt-2',
    containerClass: 'd-flex justify-space-between align-center flex-wrap gap-3',
    actionsClass: 'd-flex gap-2 align-center flex-wrap',
    actionColor: 'primary',
    actionVariant: 'elevated'
})
</script>