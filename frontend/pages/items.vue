<template>
    <div>
        <h1 class="text-4xl font-bold mb-6">Items Management</h1>

        <!-- Add Item Form -->
        <v-card class="mb-6" elevation="2">
            <v-card-title>Add New Item</v-card-title>
            <v-card-text>
                <v-form @submit.prevent="addItem">
                    <v-row>
                        <v-col cols="12" md="4">
                            <v-text-field v-model="newItem.name" label="Name" required
                                variant="outlined"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field v-model="newItem.description" label="Description"
                                variant="outlined"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="3">
                            <v-text-field v-model.number="newItem.price" label="Price" type="number" step="0.01"
                                required variant="outlined"></v-text-field>
                        </v-col>
                        <v-col cols="12" md="1" class="d-flex align-center">
                            <v-btn type="submit" color="primary" block>
                                Add
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>

        <!-- Items List -->
        <v-card elevation="2">
            <v-card-title>Items List</v-card-title>
            <v-card-text>
                <div v-if="loading" class="text-center py-4">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </div>

                <v-row v-else>
                    <v-col cols="12" md="4" sm="6" v-for="item in items" :key="item.id">
                        <v-card hover class="h-full">
                            <v-card-title>{{ item.name }}</v-card-title>
                            <v-card-subtitle>{{ item.description }}</v-card-subtitle>
                            <v-card-text>
                                <div class="text-h6 text-primary">
                                    ${{ item.price.toFixed(2) }}
                                </div>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn color="error" variant="text" @click="deleteItem(item.id!)">
                                    Delete
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>

                <div v-if="!loading && items.length === 0" class="text-center py-8">
                    <p class="text-gray-500 text-xl">No items yet. Add your first item above!</p>
                </div>
            </v-card-text>
        </v-card>

        <!-- Snackbar for notifications -->
        <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
            {{ snackbar.message }}
        </v-snackbar>
    </div>
</template>

<script setup lang="ts">
interface Item {
    id?: number
    name: string
    description?: string
    price: number
}

const { $api } = useNuxtApp()

const items = ref<Item[]>([])
const loading = ref(true)
const newItem = ref<Item>({
    name: '',
    description: '',
    price: 0
})

const snackbar = ref({
    show: false,
    message: '',
    color: 'success'
})

const showMessage = (message: string, color: string = 'success') => {
    snackbar.value = { show: true, message, color }
}

const fetchItems = async () => {
    loading.value = true
    try {
        const data = await $api('/api/items') as Item[]
        items.value = data
    } catch (error) {
        console.error('Failed to fetch items:', error)
        showMessage('Failed to fetch items', 'error')
    } finally {
        loading.value = false
    }
}

const addItem = async () => {
    if (!newItem.value.name || newItem.value.price <= 0) {
        showMessage('Please fill in all required fields', 'warning')
        return
    }

    try {
        await $api('/api/items', {
            method: 'POST',
            body: newItem.value
        })
        showMessage('Item added successfully')
        newItem.value = { name: '', description: '', price: 0 }
        await fetchItems()
    } catch (error) {
        console.error('Failed to add item:', error)
        showMessage('Failed to add item', 'error')
    }
}

const deleteItem = async (id: number) => {
    try {
        await $api(`/api/items/${id}`, {
            method: 'DELETE'
        })
        showMessage('Item deleted successfully')
        await fetchItems()
    } catch (error) {
        console.error('Failed to delete item:', error)
        showMessage('Failed to delete item', 'error')
    }
}

onMounted(() => {
    fetchItems()
})
</script>
