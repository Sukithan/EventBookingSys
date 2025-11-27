<template>
    <v-row class="mb-4">
        <v-col cols="12" :md="searchColWidth">
            <v-text-field :model-value="searchQuery" :label="searchLabel" :placeholder="searchPlaceholder"
                prepend-inner-icon="mdi-magnify" clearable variant="outlined" @update:model-value="updateSearch"
                @click:clear="clearSearch" />
        </v-col>
        <v-col v-if="showStatusFilter" cols="12" :md="filterColWidth">
            <v-select :model-value="statusFilter" label="Status Filter" :items="statusOptions" variant="outlined"
                clearable @update:model-value="updateStatusFilter" />
        </v-col>
        <v-col cols="12" :md="actionColWidth" class="d-flex align-center">
            <v-btn color="primary" @click="refreshData" :loading="loading">
                <v-icon start>mdi-refresh</v-icon>
                Refresh
            </v-btn>
            <slot name="additional-actions"></slot>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
interface Props {
    searchQuery: string
    searchLabel?: string
    searchPlaceholder?: string
    statusFilter?: string
    statusOptions?: Array<{ title: string; value: string }>
    loading?: boolean
    showStatusFilter?: boolean
    searchColWidth?: number
    filterColWidth?: number
    actionColWidth?: number
}

interface Emits {
    'update:searchQuery': [value: string]
    'update:statusFilter': [value: string]
    'refresh': []
    'clear-search': []
}

withDefaults(defineProps<Props>(), {
    searchLabel: 'Search...',
    searchPlaceholder: 'Enter search term',
    showStatusFilter: true,
    searchColWidth: 6,
    filterColWidth: 3,
    actionColWidth: 3
})

const emit = defineEmits<Emits>()

const updateSearch = (value: string) => {
    emit('update:searchQuery', value)
}

const updateStatusFilter = (value: string) => {
    emit('update:statusFilter', value)
}

const refreshData = () => {
    emit('refresh')
}

const clearSearch = () => {
    emit('clear-search')
}
</script>