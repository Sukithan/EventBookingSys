<template>
    <v-row>
        <v-col v-for="n in count" :key="n" :cols="cols" :sm="sm" :md="md" :lg="lg">
            <v-skeleton-loader :type="type"></v-skeleton-loader>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    type?: string
    count?: number
    cols?: number
    sm?: number
    md?: number
    lg?: number
}

withDefaults(defineProps<Props>(), {
    type: 'article',
    count: 3,
    cols: 12
})
</script>