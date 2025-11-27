<template>
    <v-container fluid class="pa-4 pa-md-6">
        <v-row>
            <v-col cols="12">
                <div class="d-flex flex-column flex-sm-row align-start align-sm-center mb-6 gap-3">
                    <div class="d-flex align-center flex-grow-1">
                        <v-btn icon="mdi-arrow-left" variant="text" @click="$router.push('/admin/events')"
                            class="mr-2"></v-btn>
                        <div>
                            <h1 class="text-h5 text-sm-h4 font-weight-bold">{{ event?.name || 'Event' }}</h1>
                            <div class="text-caption text-grey">Admin Management Dashboard</div>
                        </div>
                    </div>
                    <div class="d-flex gap-2 flex-wrap">
                        <v-btn color="secondary" variant="tonal" @click="recalculateStats"
                            :loading="recalculatingStats">
                            <v-icon start>mdi-calculator</v-icon>
                            <span class="d-none d-sm-inline">Recalculate Stats</span>
                        </v-btn>
                        <v-btn color="primary" variant="tonal" @click="exportBookings">
                            <v-icon start>mdi-download</v-icon>
                            <span class="d-none d-sm-inline">Export CSV</span>
                        </v-btn>
                    </div>
                </div>
            </v-col>
        </v-row>

        <v-row v-if="loading">
            <v-col cols="12">
                <v-skeleton-loader type="article, table"></v-skeleton-loader>
            </v-col>
        </v-row>

        <v-row v-else-if="event">
            <!-- Event Details Card -->
            <v-col cols="12" lg="4">
                <v-card class="h-100 elevation-2">
                    <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="220"
                        cover>
                        <v-chip class="ma-3" color="primary" variant="elevated">
                            <v-icon start>mdi-shield-crown</v-icon>
                            Admin View
                        </v-chip>
                    </v-img>

                    <v-card-title class="text-h6 py-4">{{ event.name }}</v-card-title>

                    <v-card-text>
                        <v-list density="compact" class="bg-transparent">
                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon color="primary">mdi-calendar</v-icon>
                                </template>
                                <v-list-item-title class="text-caption text-grey">Date & Time</v-list-item-title>
                                <v-list-item-subtitle class="text-body-2 font-weight-medium">
                                    {{ formatDate(event.event_date) }}
                                </v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon color="primary">mdi-map-marker</v-icon>
                                </template>
                                <v-list-item-title class="text-caption text-grey">Location</v-list-item-title>
                                <v-list-item-subtitle class="text-body-2 font-weight-medium">
                                    {{ event.location }}
                                </v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon color="success">mdi-cash</v-icon>
                                </template>
                                <v-list-item-title class="text-caption text-grey">Price per Seat</v-list-item-title>
                                <v-list-item-subtitle class="text-h6 font-weight-bold text-success">
                                    ${{ event.price.toFixed(2) }}
                                </v-list-item-subtitle>
                            </v-list-item>

                            <v-list-item>
                                <template v-slot:prepend>
                                    <v-icon color="info">mdi-seat</v-icon>
                                </template>
                                <v-list-item-title class="text-caption text-grey">Seat Availability</v-list-item-title>
                                <v-list-item-subtitle class="text-body-1 font-weight-bold">
                                    {{ event.available_seats }} / {{ event.total_seats }}
                                    <v-progress-linear
                                        :model-value="((event.total_seats - event.available_seats) / event.total_seats) * 100"
                                        color="primary" height="6" rounded class="mt-2">
                                    </v-progress-linear>
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>

                        <v-divider class="my-4"></v-divider>

                        <div>
                            <h4 class="text-subtitle-1 font-weight-bold mb-2">About This Event</h4>
                            <p class="text-body-2 text-grey-darken-1" v-if="event.description">{{ event.description }}
                            </p>
                            <p class="text-body-2 text-grey-lighten-1" v-else>No description available</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Seat Map -->
            <v-col cols="12" lg="8">
                <v-card class="elevation-2">
                    <v-card-title
                        class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between gap-3 py-4">
                        <div class="d-flex align-center gap-2">
                            <v-icon color="primary">mdi-seat</v-icon>
                            <span class="text-h6">Seat Map & Booking</span>
                            <v-chip color="orange" size="small" variant="flat">
                                <v-icon start size="small">mdi-shield-star</v-icon>
                                Admin Mode
                            </v-chip>
                        </div>
                        <v-chip color="primary" size="large" v-if="selectedSeats.length > 0" variant="elevated">
                            <v-icon start>mdi-checkbox-marked-circle</v-icon>
                            {{ selectedSeats.length }} selected
                        </v-chip>
                    </v-card-title>

                    <v-divider></v-divider>

                    <v-card-text class="pa-4">
                        <!-- Theatre Screen -->
                        <div class="text-center mb-6">
                            <div class="screen-indicator">
                                <v-chip color="grey-darken-2" size="x-large" variant="elevated">
                                    <v-icon start>mdi-television</v-icon>
                                    SCREEN
                                </v-chip>
                            </div>
                        </div>

                        <!-- Seat Map -->
                        <div class="seat-map-container" v-if="!seatsLoading">
                            <div class="seat-map">
                                <div v-for="(rowSeats, rowNumber) in groupSeatsByRow" :key="rowNumber" class="seat-row">
                                    <div class="row-label">{{ rowNumber }}</div>
                                    <div class="seats-container">
                                        <v-tooltip v-for="seat in rowSeats" :key="seat.id" location="top">
                                            <template v-slot:activator="{ props }">
                                                <div class="seat-wrapper">
                                                    <v-btn :class="getSeatClass(seat)" @click="toggleSeat(seat)"
                                                        size="small" variant="flat"
                                                        :loading="seatActionLoading === seat.id" v-bind="props"
                                                        :ripple="false">
                                                        {{ seat.seat_number }}
                                                    </v-btn>
                                                </div>
                                            </template>
                                            <div class="text-center" v-if="getSeatBookingInfo(seat)">
                                                <div class="font-weight-bold mb-1">🎫 BOOKED</div>
                                                <div><strong>User:</strong> {{ getSeatBookingInfo(seat)?.user_name }}
                                                </div>
                                                <div><strong>Email:</strong> {{ getSeatBookingInfo(seat)?.user_email }}
                                                </div>
                                                <div class="text-caption mt-1 text-grey-lighten-2">Click to view/manage
                                                </div>
                                            </div>
                                            <div v-else-if="seat.is_locked && !selectedSeats.includes(seat.id)">
                                                <div class="font-weight-bold">🔒 LOCKED</div>
                                                <div class="text-caption">Being selected by another user</div>
                                            </div>
                                            <div v-else-if="selectedSeats.includes(seat.id)">
                                                <div class="font-weight-bold">✓ SELECTED</div>
                                                <div>Row {{ rowNumber }}, Seat {{ seat.seat_number }}</div>
                                                <div class="text-caption mt-1">Click to deselect</div>
                                            </div>
                                            <div v-else>
                                                <div class="font-weight-bold">✓ AVAILABLE</div>
                                                <div>Row {{ rowNumber }}, Seat {{ seat.seat_number }}</div>
                                                <div class="text-caption mt-1">Click to select</div>
                                            </div>
                                        </v-tooltip>
                                    </div>
                                    <div class="row-label">{{ rowNumber }}</div>
                                </div>
                            </div>
                        </div>

                        <v-skeleton-loader v-else type="paragraph, paragraph, paragraph"
                            class="my-4"></v-skeleton-loader>

                        <!-- Legend -->
                        <v-card variant="outlined" class="mt-6 bg-grey-lighten-5">
                            <v-card-text class="py-3">
                                <div class="d-flex flex-wrap gap-3 gap-sm-4 justify-center align-center">
                                    <div class="d-flex align-center">
                                        <v-btn size="small" color="success" class="mr-2" disabled icon>
                                            <v-icon>mdi-check</v-icon>
                                        </v-btn>
                                        <span class="text-body-2 font-weight-medium">Available</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="small" color="primary" class="mr-2" disabled icon>
                                            <v-icon>mdi-cursor-default-click</v-icon>
                                        </v-btn>
                                        <span class="text-body-2 font-weight-medium">Selected</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="small" color="orange" class="mr-2" disabled icon>
                                            <v-icon>mdi-lock</v-icon>
                                        </v-btn>
                                        <span class="text-body-2 font-weight-medium">Locked</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="small" color="error" class="mr-2" disabled icon>
                                            <v-icon>mdi-account</v-icon>
                                        </v-btn>
                                        <span class="text-body-2 font-weight-medium">Booked (Click to view)</span>
                                    </div>
                                </div>
                            </v-card-text>
                        </v-card>

                        <!-- Admin Booking Section -->
                        <v-card v-if="selectedSeats.length > 0" elevation="8" color="primary" class="mt-6" rounded="lg">
                            <v-card-text class="pa-4 pa-sm-5">
                                <v-row align="center" class="text-white">
                                    <v-col cols="12" class="py-2">
                                        <div class="text-overline opacity-80 mb-2">Selected Seats</div>
                                        <div class="d-flex flex-wrap gap-1">
                                            <v-chip v-for="seatId in selectedSeats" :key="seatId" size="small"
                                                color="white" variant="elevated" closable
                                                @click:close="removeSeatFromSelection(seatId)">
                                                {{ getSeatLabel(seatId) }}
                                            </v-chip>
                                        </div>
                                    </v-col>
                                    <v-col cols="12" sm="3" class="py-2">
                                        <div class="text-overline opacity-80">Price per Seat</div>
                                        <div class="text-h6 font-weight-bold">${{ event.price.toFixed(2) }}</div>
                                        <div class="text-caption opacity-70">{{ selectedSeats.length }} seat{{
                                            selectedSeats.length
                                                > 1 ? 's' : '' }} selected</div>
                                    </v-col>
                                    <v-col cols="12" sm="3" class="py-2">
                                        <div class="text-overline opacity-80">Total Amount</div>
                                        <div class="text-h4 font-weight-bold">
                                            ${{ (event.price * selectedSeats.length).toFixed(2) }}
                                        </div>
                                    </v-col>
                                    <v-col cols="12" sm="6" class="d-flex flex-column flex-sm-row gap-2 py-2">
                                        <v-btn color="white" variant="elevated" size="large" :loading="bookingLoading"
                                            @click="showBookingDialog = true" class="flex-sm-grow-1">
                                            <v-icon start>mdi-ticket-confirmation</v-icon>
                                            Create Booking
                                        </v-btn>
                                        <v-btn variant="outlined" color="white" size="large" @click="clearSelection">
                                            <v-icon start>mdi-close</v-icon>
                                            Clear
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Bookings Table -->
            <v-col cols="12">
                <v-card class="elevation-2">
                    <v-card-title
                        class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between gap-3 py-4">
                        <div class="d-flex align-center gap-2">
                            <v-icon color="primary" size="large">mdi-format-list-bulleted</v-icon>
                            <div>
                                <div class="text-h6 font-weight-bold">Event Bookings</div>
                                <div class="text-caption text-grey">Manage all bookings for this event</div>
                            </div>
                        </div>
                        <v-chip color="primary" size="large" variant="elevated">
                            <v-icon start>mdi-ticket-account</v-icon>
                            {{ bookings.length }} Total
                        </v-chip>
                    </v-card-title>

                    <v-divider></v-divider>

                    <v-card-text class="pa-4 pa-sm-6">
                        <v-row class="mb-4" align="center">
                            <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="search" label="Search bookings..."
                                    placeholder="Enter name or email" prepend-inner-icon="mdi-magnify"
                                    variant="outlined" density="comfortable" hide-details clearable>
                                </v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="3">
                                <v-select v-model="statusFilter" :items="statusOptions" label="Filter by status"
                                    variant="outlined" density="comfortable" hide-details clearable>
                                    <template v-slot:prepend-inner>
                                        <v-icon>mdi-filter</v-icon>
                                    </template>
                                </v-select>
                            </v-col>
                            <v-col cols="12" md="5" class="d-flex align-center justify-end gap-2">
                                <v-chip v-if="filteredBookings.length !== bookings.length" color="info" variant="tonal">
                                    <v-icon start size="small">mdi-filter-check</v-icon>
                                    {{ filteredBookings.length }} / {{ bookings.length }}
                                </v-chip>
                            </v-col>
                        </v-row>

                        <v-data-table v-if="filteredBookings.length > 0" :headers="headers" :items="filteredBookings"
                            :items-per-page="15" :search="search" class="elevation-1 rounded" :mobile-breakpoint="600">
                            <template v-slot:item.user="{ item }">
                                <div class="py-2">
                                    <div class="font-weight-bold text-body-1">
                                        <v-icon size="small" color="primary" class="mr-1">mdi-account</v-icon>
                                        {{ item.user?.full_name || item.user?.username }}
                                    </div>
                                    <div class="text-caption text-grey-darken-1">
                                        <v-icon size="x-small" class="mr-1">mdi-email</v-icon>
                                        {{ item.user?.email }}
                                    </div>
                                </div>
                            </template>

                            <template v-slot:item.booking_date="{ item }">
                                <div class="text-body-2">
                                    <v-icon size="small" class="mr-1" color="grey-darken-1">mdi-calendar-clock</v-icon>
                                    {{ formatDate(item.booking_date) }}
                                </div>
                            </template>

                            <template v-slot:item.seats_booked="{ item }">
                                <div>
                                    <v-chip size="small" color="info" variant="elevated" class="mb-1">
                                        <v-icon start size="small">mdi-seat</v-icon>
                                        {{ item.seats_booked }}
                                    </v-chip>
                                    <div class="text-caption text-grey"
                                        v-if="item.seat_details && item.seat_details.length > 0">
                                        {{item.seat_details.map(s => `${s.row_number}-${s.seat_number}`).join(', ')}}
                                    </div>
                                </div>
                            </template>

                            <template v-slot:item.total_price="{ item }">
                                <span class="text-h6 font-weight-bold text-success">
                                    ${{ item.total_price.toFixed(2) }}
                                </span>
                            </template>

                            <template v-slot:item.status="{ item }">
                                <v-chip :color="getStatusColor(item.status)" size="small" variant="flat">
                                    <v-icon start size="small">
                                        {{ item.status === 'confirmed' ? 'mdi-check-circle' : item.status ===
                                            'cancelled' ? 'mdi-cancel' : 'mdi-clock-outline' }}
                                    </v-icon>
                                    {{ item.status }}
                                </v-chip>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <div class="d-flex gap-1">
                                    <v-tooltip text="View Details" location="top">
                                        <template v-slot:activator="{ props }">
                                            <v-btn icon="mdi-eye" size="small" variant="tonal" color="primary"
                                                @click="viewBookingDetails(item)" v-bind="props">
                                            </v-btn>
                                        </template>
                                    </v-tooltip>
                                    <v-tooltip text="Manage Seats" location="top">
                                        <template v-slot:activator="{ props }">
                                            <v-btn icon="mdi-seat" size="small" variant="tonal" color="info"
                                                @click="manageSeatBookings(item)" v-bind="props">
                                            </v-btn>
                                        </template>
                                    </v-tooltip>
                                    <v-tooltip text="Cancel Booking" location="top">
                                        <template v-slot:activator="{ props }">
                                            <v-btn icon="mdi-cancel" size="small" variant="tonal" color="error"
                                                @click="cancelBookingConfirm(item)"
                                                :disabled="item.status === 'cancelled'" v-bind="props">
                                            </v-btn>
                                        </template>
                                    </v-tooltip>
                                </div>
                            </template>
                        </v-data-table>

                        <v-card v-else variant="outlined" class="text-center py-16">
                            <v-icon size="100" color="grey-lighten-2">mdi-ticket-outline</v-icon>
                            <p class="text-h5 text-grey-darken-1 mt-6 font-weight-medium">No bookings found</p>
                            <p class="text-body-2 text-grey mt-2">Try adjusting your search or filter criteria</p>
                        </v-card>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Admin Booking Dialog -->
        <v-dialog v-model="showBookingDialog" max-width="650" :fullscreen="$vuetify.display.xs" persistent>
            <v-card elevation="24">
                <v-card-title class="text-h5 bg-gradient-primary text-white d-flex align-center pa-5">
                    <v-icon start size="large">mdi-ticket-confirmation</v-icon>
                    <div>
                        <div class="text-h5 font-weight-bold">Create Booking</div>
                        <div class="text-caption opacity-80">Admin booking interface</div>
                    </div>
                </v-card-title>

                <v-divider></v-divider>

                <v-card-text class="pa-6">
                    <!-- Username Input -->
                    <v-card variant="outlined" class="mb-4 pa-4 bg-blue-lighten-5">
                        <div class="text-subtitle-2 font-weight-bold mb-3">
                            <v-icon color="primary" class="mr-2">mdi-account-search</v-icon>
                            Book for User (Optional)
                        </div>
                        <v-text-field v-model="bookingUsername" label="Enter Username or Email"
                            prepend-inner-icon="mdi-account" variant="outlined" density="comfortable"
                            hint="Leave empty to book for yourself as admin" persistent-hint clearable
                            :disabled="bookingLoading">
                        </v-text-field>
                        <v-alert type="info" variant="text" density="compact" class="mt-2">
                            <template v-slot:prepend>
                                <v-icon size="small">mdi-information</v-icon>
                            </template>
                            <div class="text-caption">
                                You can create bookings for any registered user by entering their username or email.
                                If left empty, the booking will be created under your admin account.
                            </div>
                        </v-alert>
                    </v-card>

                    <!-- Booking Summary -->
                    <v-card variant="tonal" color="primary" class="mb-4">
                        <v-card-title class="text-subtitle-1 font-weight-bold">
                            <v-icon class="mr-2">mdi-receipt-text</v-icon>
                            Booking Summary
                        </v-card-title>
                        <v-card-text>
                            <v-row dense>
                                <v-col cols="12">
                                    <div class="d-flex justify-space-between align-center py-2 border-b">
                                        <span class="font-weight-medium">Event:</span>
                                        <span class="font-weight-bold">{{ event?.name }}</span>
                                    </div>
                                </v-col>
                                <v-col cols="12">
                                    <div class="py-2 border-b">
                                        <div class="font-weight-medium mb-2">Seats Selected:</div>
                                        <div class="d-flex flex-wrap gap-1">
                                            <v-chip v-for="seatId in selectedSeats" :key="seatId" color="primary"
                                                size="small" variant="elevated">
                                                <v-icon start size="x-small">mdi-seat</v-icon>
                                                {{ getSeatLabel(seatId) }}
                                            </v-chip>
                                        </div>
                                    </div>
                                </v-col>
                                <v-col cols="12">
                                    <div class="d-flex justify-space-between align-center py-2 border-b">
                                        <span class="font-weight-medium">Price per Seat:</span>
                                        <span class="font-weight-bold">${{ event ? event.price.toFixed(2) : '0.00'
                                            }}</span>
                                    </div>
                                </v-col>
                                <v-col cols="12">
                                    <div
                                        class="d-flex justify-space-between align-center py-3 bg-primary rounded pa-3 mt-2">
                                        <span class="text-h6 font-weight-bold text-white">Total Amount:</span>
                                        <span class="text-h4 font-weight-bold text-white">
                                            ${{ event ? (event.price * selectedSeats.length).toFixed(2) : '0.00' }}
                                        </span>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-card-text>
                    </v-card>

                    <!-- Error Alert -->
                    <v-alert v-if="bookingError" type="error" variant="tonal" dismissible class="mb-4">
                        <template v-slot:prepend>
                            <v-icon>mdi-alert-circle</v-icon>
                        </template>
                        <div class="font-weight-medium">{{ bookingError }}</div>
                    </v-alert>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions class="pa-5 bg-grey-lighten-4">
                    <v-spacer></v-spacer>
                    <v-btn variant="text" size="large" @click="showBookingDialog = false" :disabled="bookingLoading">
                        <v-icon start>mdi-close</v-icon>
                        Cancel
                    </v-btn>
                    <v-btn color="primary" size="large" variant="elevated" :loading="bookingLoading"
                        @click="handleAdminBooking">
                        <v-icon start>mdi-check-circle</v-icon>
                        Confirm Booking
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Booking Details Dialog -->
        <v-dialog v-model="detailsDialog" max-width="700" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedBooking">
                <v-card-title class="text-h6 text-sm-h5 bg-primary text-white d-flex align-center">
                    <v-icon start>mdi-ticket</v-icon>
                    <span>Booking #{{ selectedBooking.id }}</span>
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-row>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Booking ID</div>
                                <div class="text-body-1">#{{ selectedBooking.id }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Status</div>
                                <v-chip :color="getStatusColor(selectedBooking.status)" size="small">
                                    {{ selectedBooking.status }}
                                </v-chip>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Customer Name</div>
                                <div class="text-body-1 font-weight-bold">{{ selectedBooking.user?.full_name ||
                                    selectedBooking.user?.username }}
                                </div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Customer Email</div>
                                <div class="text-body-1">{{ selectedBooking.user?.email }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Booking Date</div>
                                <div class="text-body-1">{{ formatDate(selectedBooking.booking_date) }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Seats Booked</div>
                                <div class="text-body-1">{{ selectedBooking.seats_booked }}</div>
                            </div>
                        </v-col>
                        <v-col cols="12">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Seat Details</div>
                                <div v-if="selectedBooking.seat_details && selectedBooking.seat_details.length > 0"
                                    class="d-flex flex-wrap gap-1 mt-1">
                                    <v-chip v-for="seat in selectedBooking.seat_details" :key="seat.id" size="small"
                                        color="primary" variant="elevated">
                                        <v-icon start size="small">mdi-seat</v-icon>
                                        {{ seat.row_number }}-{{ seat.seat_number }}
                                    </v-chip>
                                </div>
                                <div v-else class="text-grey">No seat details available</div>
                            </div>
                        </v-col>
                        <v-col cols="12">
                            <div class="mb-3">
                                <div class="text-caption text-grey">Total Price</div>
                                <div class="text-h5 text-primary font-weight-bold">${{
                                    selectedBooking.total_price.toFixed(2) }}
                                </div>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="detailsDialog = false">Close</v-btn>
                    <v-btn color="error" v-if="selectedBooking.status !== 'cancelled'"
                        @click="cancelBookingFromDetails">
                        Cancel Booking
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Seat Management Dialog -->
        <v-dialog v-model="seatManagementDialog" max-width="900" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedBooking" elevation="24">
                <v-card-title class="text-h5 bg-gradient-info text-white d-flex align-center pa-5">
                    <v-icon start size="large">mdi-seat-recline-extra</v-icon>
                    <div>
                        <div class="text-h5 font-weight-bold">Manage Seat Bookings</div>
                        <div class="text-caption opacity-80">Remove individual seats from booking</div>
                    </div>
                </v-card-title>

                <v-divider></v-divider>

                <v-card variant="flat" color="blue-lighten-5" class="ma-0">
                    <v-card-text class="py-4 px-5">
                        <v-row dense align="center">
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center gap-2 mb-2">
                                    <v-icon color="primary">mdi-account-circle</v-icon>
                                    <div>
                                        <div class="text-caption text-grey-darken-1">Customer</div>
                                        <div class="text-body-1 font-weight-bold">
                                            {{ selectedBooking.user?.full_name || selectedBooking.user?.username }}
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <div class="d-flex align-center gap-2">
                                    <v-icon color="primary">mdi-email</v-icon>
                                    <div>
                                        <div class="text-caption text-grey-darken-1">Email</div>
                                        <div class="text-body-2 font-weight-medium">{{ selectedBooking.user?.email }}
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" class="mt-2">
                                <v-divider></v-divider>
                            </v-col>
                            <v-col cols="6" sm="3">
                                <v-chip color="info" variant="elevated" class="font-weight-bold">
                                    <v-icon start size="small">mdi-seat</v-icon>
                                    {{ seatDetails.length }} Seats
                                </v-chip>
                            </v-col>
                            <v-col cols="6" sm="3">
                                <v-chip color="success" variant="elevated" class="font-weight-bold">
                                    <v-icon start size="small">mdi-cash</v-icon>
                                    ${{ selectedBooking.total_price?.toFixed(2) || '0.00' }}
                                </v-chip>
                            </v-col>
                            <v-col cols="12" sm="6" class="text-sm-right">
                                <v-chip color="primary" variant="outlined">
                                    <v-icon start size="small">mdi-ticket</v-icon>
                                    Booking #{{ selectedBooking.id }}
                                </v-chip>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>

                <v-card-text class="pa-6">
                    <div v-if="seatDetails.length > 0">
                        <div class="d-flex justify-space-between align-center mb-4">
                            <h3 class="text-h6 font-weight-bold">
                                <v-icon color="primary" class="mr-2">mdi-format-list-bulleted</v-icon>
                                Booked Seats
                            </h3>
                            <v-chip color="primary" variant="tonal">{{ seatDetails.length }} total</v-chip>
                        </div>

                        <v-card variant="outlined" class="pa-4 bg-grey-lighten-5">
                            <div class="seat-chips-grid">
                                <v-chip v-for="seat in seatDetails" :key="seat.id" color="error" variant="elevated"
                                    closable size="large" @click:close="confirmDeleteSeat(seat)"
                                    class="ma-1 font-weight-bold">
                                    <v-icon start>mdi-seat-passenger</v-icon>
                                    {{ seat.row_number }}-{{ seat.seat_number }}
                                </v-chip>
                            </div>
                        </v-card>

                        <v-alert type="warning" variant="tonal" density="comfortable" class="mt-4">
                            <template v-slot:prepend>
                                <v-icon>mdi-alert-circle</v-icon>
                            </template>
                            <div class="text-body-2">
                                <strong>Admin Action:</strong> Click the <v-icon size="small">mdi-close</v-icon> button
                                on
                                any seat chip to remove it from this booking. This will:
                                <ul class="mt-2 ml-4">
                                    <li>Update the total booking price</li>
                                    <li>Make the seat available for new bookings</li>
                                    <li>If all seats are removed, the entire booking will be cancelled</li>
                                </ul>
                            </div>
                        </v-alert>
                    </div>
                    <v-card v-else variant="outlined" class="text-center py-12">
                        <v-icon size="80" color="grey-lighten-2">mdi-seat-outline</v-icon>
                        <p class="text-h6 text-grey-darken-1 mt-4">No seat details available</p>
                        <p class="text-body-2 text-grey mt-2">This booking has no associated seats</p>
                    </v-card>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions class="pa-5 bg-grey-lighten-4">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" size="large" variant="elevated" @click="closeSeatManagement">
                        <v-icon start>mdi-check</v-icon>
                        Done
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Delete Seat Confirmation Dialog -->
        <v-dialog v-model="deleteSeatDialog" max-width="500" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedSeat">
                <v-card-title class="text-h6 text-sm-h5 bg-error text-white d-flex align-center">
                    <v-icon start>mdi-alert</v-icon>
                    <span>Remove Seat</span>
                </v-card-title>
                <v-card-text class="pa-4 pa-sm-6">
                    <p class="text-body-1 mb-4">Are you sure you want to remove this seat from the booking?</p>
                    <v-card variant="outlined" class="pa-3 bg-grey-lighten-5 mb-4">
                        <div class="mb-2">
                            <v-chip size="small" color="primary" class="mr-2" variant="elevated">
                                <v-icon start size="small">mdi-seat</v-icon>
                                {{ selectedSeat.row_number }}-{{ selectedSeat.seat_number }}
                            </v-chip>
                        </div>
                        <div class="mb-2"><strong>Customer:</strong> {{ selectedBooking?.user?.full_name ||
                            selectedBooking?.user?.username }}</div>
                        <div><strong>Email:</strong> {{ selectedBooking?.user?.email }}</div>
                    </v-card>
                    <v-alert type="warning" variant="tonal" density="compact">
                        <div class="text-body-2">This will make the seat available and update the booking total price.
                        </div>
                    </v-alert>
                </v-card-text>
                <v-card-actions class="pa-4 flex-column flex-sm-row">
                    <v-spacer></v-spacer>
                    <v-btn @click="deleteSeatDialog = false" block class="mb-2 mb-sm-0 mr-sm-2">Cancel</v-btn>
                    <v-btn color="error" :loading="deletingSeat" @click="confirmDeleteSeatBooking" block>
                        <v-icon start size="small">mdi-delete</v-icon>
                        Remove Seat
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Cancel Booking Dialog -->
        <v-dialog v-model="cancelDialog" max-width="500" :fullscreen="$vuetify.display.xs">
            <v-card>
                <v-card-title class="text-h6 text-sm-h5 bg-error text-white d-flex align-center">
                    <v-icon start>mdi-cancel</v-icon>
                    <span>Cancel Booking</span>
                </v-card-title>
                <v-card-text class="pa-4 pa-sm-6">
                    <p class="text-body-1 mb-4">Are you sure you want to cancel this booking?</p>
                    <v-card v-if="selectedBooking" variant="outlined" class="pa-3 bg-grey-lighten-5 mb-4">
                        <div class="mb-2"><strong>User:</strong> {{ selectedBooking.user?.full_name ||
                            selectedBooking.user?.username }}</div>
                        <div class="mb-2"><strong>Seats:</strong> {{ selectedBooking.seats_booked }}</div>
                        <div><strong>Total:</strong> ${{ selectedBooking.total_price.toFixed(2) }}</div>
                    </v-card>
                    <v-alert type="warning" variant="tonal" density="compact">
                        <div class="text-body-2">This action cannot be undone. The seats will be made available for
                            booking
                            again.</div>
                    </v-alert>
                </v-card-text>
                <v-card-actions class="pa-4 flex-column flex-sm-row">
                    <v-spacer></v-spacer>
                    <v-btn @click="cancelDialog = false" block class="mb-2 mb-sm-0 mr-sm-2">Keep Booking</v-btn>
                    <v-btn color="error" :loading="cancelling" @click="confirmCancelBooking" block>
                        <v-icon start size="small">mdi-cancel</v-icon>
                        Cancel Booking
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Seat Info Dialog (Click on booked seat) -->
        <v-dialog v-model="seatInfoDialog" max-width="700" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedSeatInfo" elevation="24">
                <v-card-title class="text-h5 bg-gradient-info text-white d-flex align-center pa-5">
                    <v-icon start size="large">mdi-seat-passenger</v-icon>
                    <div>
                        <div class="text-h5 font-weight-bold">Seat Information</div>
                        <div class="text-caption opacity-80">View and manage seat booking</div>
                    </div>
                </v-card-title>

                <v-divider></v-divider>

                <v-card-text class="pa-6">
                    <!-- Seat Details -->
                    <v-card variant="tonal" color="error" class="mb-4">
                        <v-card-text class="text-center py-4">
                            <v-icon size="64" color="error">mdi-seat</v-icon>
                            <div class="text-h4 font-weight-bold mt-2">
                                Row {{ selectedSeatInfo.seat.row_number }} - Seat {{ selectedSeatInfo.seat.seat_number
                                }}
                            </div>
                            <v-chip color="error" class="mt-2" variant="elevated">
                                <v-icon start>mdi-lock</v-icon>
                                BOOKED
                            </v-chip>
                        </v-card-text>
                    </v-card>

                    <!-- User Details -->
                    <v-card variant="outlined" class="mb-4">
                        <v-card-title class="bg-grey-lighten-4 font-weight-bold">
                            <v-icon class="mr-2" color="primary">mdi-account-circle</v-icon>
                            Customer Information
                        </v-card-title>
                        <v-card-text class="pa-4">
                            <v-list density="comfortable" class="bg-transparent">
                                <v-list-item>
                                    <template v-slot:prepend>
                                        <v-icon color="primary">mdi-account</v-icon>
                                    </template>
                                    <v-list-item-title class="text-caption text-grey">Full Name</v-list-item-title>
                                    <v-list-item-subtitle class="text-body-1 font-weight-bold">
                                        {{ selectedSeatInfo.user_name }}
                                    </v-list-item-subtitle>
                                </v-list-item>

                                <v-list-item>
                                    <template v-slot:prepend>
                                        <v-icon color="primary">mdi-email</v-icon>
                                    </template>
                                    <v-list-item-title class="text-caption text-grey">Email Address</v-list-item-title>
                                    <v-list-item-subtitle class="text-body-1 font-weight-medium">
                                        {{ selectedSeatInfo.user_email }}
                                    </v-list-item-subtitle>
                                </v-list-item>
                            </v-list>
                        </v-card-text>
                    </v-card>

                    <!-- Booking Details -->
                    <v-card variant="outlined">
                        <v-card-title class="bg-grey-lighten-4 font-weight-bold">
                            <v-icon class="mr-2" color="success">mdi-ticket</v-icon>
                            Booking Details
                        </v-card-title>
                        <v-card-text class="pa-4">
                            <v-row dense>
                                <v-col cols="6">
                                    <div class="text-caption text-grey">Booking ID</div>
                                    <div class="text-body-1 font-weight-bold">#{{ selectedSeatInfo.booking.id }}</div>
                                </v-col>
                                <v-col cols="6">
                                    <div class="text-caption text-grey">Total Seats</div>
                                    <div class="text-body-1 font-weight-bold">{{ selectedSeatInfo.booking.seats_booked
                                        }}</div>
                                </v-col>
                                <v-col cols="12" class="mt-2">
                                    <div class="text-caption text-grey">Total Amount</div>
                                    <div class="text-h5 font-weight-bold text-success">
                                        ${{ selectedSeatInfo.booking.total_price?.toFixed(2) }}
                                    </div>
                                </v-col>
                            </v-row>
                        </v-card-text>
                    </v-card>

                    <!-- Admin Actions Info -->
                    <v-alert type="warning" variant="tonal" density="comfortable" class="mt-4">
                        <template v-slot:prepend>
                            <v-icon>mdi-shield-star</v-icon>
                        </template>
                        <div class="text-body-2">
                            <strong>Admin Options:</strong> You can view the complete booking details or remove just
                            this seat
                            from the booking.
                        </div>
                    </v-alert>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions class="pa-5 bg-grey-lighten-4 flex-column flex-sm-row gap-2">
                    <v-btn @click="seatInfoDialog = false" block variant="outlined" size="large">
                        <v-icon start>mdi-close</v-icon>
                        Close
                    </v-btn>
                    <v-spacer class="d-none d-sm-flex"></v-spacer>
                    <v-btn color="primary" @click="viewFullBooking(selectedSeatInfo.booking)" block size="large"
                        variant="elevated">
                        <v-icon start>mdi-eye</v-icon>
                        View Full Booking
                    </v-btn>
                    <v-btn color="error" @click="cancelSingleSeat(selectedSeatInfo.seat)" block size="large"
                        variant="elevated">
                        <v-icon start>mdi-delete</v-icon>
                        Remove This Seat
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-snackbar v-model="snackbar" :color="snackbarColor">
            {{ snackbarMessage }}
        </v-snackbar>
    </v-container>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'admin'
})

const route = useRoute()
const router = useRouter()
const { fetchEventById } = useEvents()
const { fetchEventBookings, cancelBooking, getEventSeatsAdmin } = useAdmin()
const { user } = useAuth()
const { $api } = useNuxtApp()

const loading = ref(false)
const cancelling = ref(false)
const deletingSeat = ref(false)
const recalculatingStats = ref(false)
const bookingLoading = ref(false)
const seatsLoading = ref(false)
const seatActionLoading = ref<number | null>(null)
const event = ref<any>(null)
const bookings = ref<any[]>([])
const seats = ref<any[]>([])
const selectedSeats = ref<number[]>([])
const search = ref('')
const statusFilter = ref('')
const detailsDialog = ref(false)
const cancelDialog = ref(false)
const seatManagementDialog = ref(false)
const deleteSeatDialog = ref(false)
const showBookingDialog = ref(false)
const selectedBooking = ref<any>(null)
const selectedSeat = ref<any>(null)
const seatDetails = ref<any[]>([])
const bookingUsername = ref('')
const bookingError = ref('')
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')
const seatInfoDialog = ref(false)
const selectedSeatInfo = ref<any>(null)

const statusOptions = [
    { title: 'All', value: '' },
    { title: 'Confirmed', value: 'confirmed' },
    { title: 'Cancelled', value: 'cancelled' },
    { title: 'Pending', value: 'pending' }
]

const headers = [
    { title: 'Customer', value: 'user', key: 'user' },
    { title: 'Booking Date', value: 'booking_date', key: 'booking_date' },
    { title: 'Seats', value: 'seats_booked', key: 'seats_booked' },
    { title: 'Total', value: 'total_price', key: 'total_price' },
    { title: 'Status', value: 'status', key: 'status' },
    { title: 'Actions', value: 'actions', key: 'actions', sortable: false }
]

const filteredBookings = computed(() => {
    // Ensure bookings.value is an array
    if (!Array.isArray(bookings.value)) {
        return []
    }

    let filtered = bookings.value

    if (statusFilter.value) {
        filtered = filtered.filter(booking => booking.status === statusFilter.value)
    }

    if (search.value) {
        const searchLower = search.value.toLowerCase()
        filtered = filtered.filter(booking => {
            const userName = (booking.user?.full_name || booking.user?.username || '').toLowerCase()
            const userEmail = (booking.user?.email || '').toLowerCase()
            return userName.includes(searchLower) || userEmail.includes(searchLower)
        })
    }

    return filtered
})

const groupSeatsByRow = computed(() => {
    const grouped: { [key: number]: any[] } = {}

    // Ensure seats.value is an array
    if (!Array.isArray(seats.value)) {
        return grouped
    }

    seats.value.forEach(seat => {
        if (!grouped[seat.row_number]) {
            grouped[seat.row_number] = []
        }
        grouped[seat.row_number].push(seat)
    })

    // Sort seats within each row
    Object.keys(grouped).forEach(row => {
        grouped[parseInt(row)].sort((a, b) => a.seat_number - b.seat_number)
    })

    return grouped
})

const loadData = async () => {
    loading.value = true
    const eventId = parseInt(route.params.id as string)

    const [eventResult, bookingsResult, seatsResult] = await Promise.all([
        fetchEventById(eventId),
        fetchEventBookings(eventId),
        loadSeats(true)
    ])

    if (eventResult.success) {
        event.value = eventResult.data
    }

    if (bookingsResult.success) {
        // The API returns an object with a bookings property
        const data = bookingsResult.data as any
        bookings.value = Array.isArray(data) ? data : (data.bookings || [])
    }

    loading.value = false
}

const loadSeats = async (silent = false) => {
    if (!silent) seatsLoading.value = true
    const eventId = parseInt(route.params.id as string)

    try {
        const result = await getEventSeatsAdmin(eventId)
        if (result.success) {
            seats.value = result.data as any[]
        }
        return result
    } catch (error) {
        console.error('Error loading seats:', error)
        return { success: false, error: 'Failed to load seats' }
    } finally {
        if (!silent) seatsLoading.value = false
    }
}

const getSeatClass = (seat: any) => {
    if (selectedSeats.value.includes(seat.id)) {
        return 'seat-selected'
    } else if (!seat.is_available) {
        return seat.is_locked ? 'seat-locked' : 'seat-booked'
    } else {
        return 'seat-available'
    }
}

const getSeatBookingInfo = (seat: any) => {
    // First try to get booking info directly from seat (from admin seats API)
    if (seat.booking_info) {
        return {
            user_name: seat.booking_info.full_name || seat.booking_info.username,
            user_email: seat.booking_info.email,
            booking_id: seat.booking_info.booking_id
        }
    }

    // Fallback: search through bookings if booking_info is not available
    if (!seat.is_available && !seat.is_locked && Array.isArray(bookings.value)) {
        for (const booking of bookings.value) {
            if (booking.seat_details && booking.seat_details.some((s: any) => s.seat_id === seat.id || s.id === seat.id)) {
                return {
                    user_name: booking.user?.full_name || booking.user?.username,
                    user_email: booking.user?.email,
                    booking_id: booking.id
                }
            }
        }
    }
    return null
}

const toggleSeat = async (seat: any) => {
    if (!seat.is_available && !selectedSeats.value.includes(seat.id)) {
        // Show detailed booking info dialog for booked seats
        const bookingInfo = getSeatBookingInfo(seat)
        if (bookingInfo) {
            // Refresh bookings data to ensure we have the latest information
            const eventId = parseInt(route.params.id as string)
            const { fetchEventBookings } = useAdmin()
            const bookingsResult = await fetchEventBookings(eventId)

            let booking = null
            if (bookingsResult.success) {
                const data = bookingsResult.data as any
                const refreshedBookings = Array.isArray(data) ? data : (data.bookings || [])
                booking = refreshedBookings.find((b: any) => b.id === bookingInfo.booking_id)

                // Update the bookings array with fresh data
                bookings.value = refreshedBookings
            } else {
                // Fallback to existing booking data
                booking = bookings.value.find((b: any) => b.id === bookingInfo.booking_id)
            }

            if (booking) {
                selectedSeatInfo.value = {
                    seat: seat,
                    booking: booking,
                    user_name: bookingInfo.user_name,
                    user_email: bookingInfo.user_email
                }
                seatInfoDialog.value = true
            } else {
                // Booking might have been cancelled, refresh all data
                snackbarMessage.value = 'Seat booking information has changed. Refreshing...'
                snackbarColor.value = 'info'
                snackbar.value = true
                await loadData()
                await loadSeats(true)
            }
        }
        return
    }

    seatActionLoading.value = seat.id

    if (selectedSeats.value.includes(seat.id)) {
        // Deselect
        selectedSeats.value = selectedSeats.value.filter(id => id !== seat.id)
    } else {
        // Select
        selectedSeats.value.push(seat.id)
    }

    seatActionLoading.value = null
}

const clearSelection = () => {
    selectedSeats.value = []
    bookingUsername.value = ''
    bookingError.value = ''
}

const getSeatLabel = (seatId: number) => {
    const seat = seats.value.find(s => s.id === seatId)
    if (seat) {
        return `${seat.row_number}-${seat.seat_number}`
    }
    return `Seat ${seatId}`
}

const removeSeatFromSelection = (seatId: number) => {
    selectedSeats.value = selectedSeats.value.filter(id => id !== seatId)
}

const handleAdminBooking = async () => {
    if (!event.value || selectedSeats.value.length === 0) return

    bookingError.value = ''
    bookingLoading.value = true

    try {
        // If no username provided, use current admin's username or leave empty
        const usernameOrEmail = bookingUsername.value.trim() || ''

        const { createAdminBooking } = useAdmin()
        const result = await createAdminBooking(event.value.id, selectedSeats.value, usernameOrEmail)

        if (result.success) {
            const bookingFor = bookingUsername.value.trim() ? bookingUsername.value : 'yourself (admin)'
            snackbarMessage.value = `Booking created successfully for ${bookingFor}`
            snackbarColor.value = 'success'
            snackbar.value = true

            showBookingDialog.value = false
            clearSelection()

            // Comprehensive data reload to ensure all UI components are updated
            await Promise.all([
                loadData(), // Reload bookings and event data
                loadSeats(true) // Reload seat map data
            ])
        } else {
            bookingError.value = result.error
            snackbarMessage.value = result.error
            snackbarColor.value = 'error'
            snackbar.value = true
        }
    } catch (error: any) {
        bookingError.value = error.message || 'Failed to create booking'
        snackbarMessage.value = bookingError.value
        snackbarColor.value = 'error'
        snackbar.value = true
    } finally {
        bookingLoading.value = false
    }
}

const viewBookingDetails = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = true
}

const cancelBookingConfirm = (booking: any) => {
    selectedBooking.value = booking
    detailsDialog.value = false
    cancelDialog.value = true
}

const cancelBookingFromDetails = () => {
    detailsDialog.value = false
    cancelDialog.value = true
}

const confirmCancelBooking = async () => {
    if (!selectedBooking.value) return

    cancelling.value = true
    const result = await cancelBooking(selectedBooking.value.id)
    cancelling.value = false

    if (result.success) {
        snackbarMessage.value = 'Booking cancelled successfully'
        snackbarColor.value = 'success'
        cancelDialog.value = false

        // Comprehensive data reload to ensure all UI components are updated
        await Promise.all([
            loadData(), // Reload bookings and event data
            loadSeats(true) // Reload seat map data
        ])

        // Clear any cached booking info
        selectedBooking.value = null
        selectedSeatInfo.value = null
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const viewFullBooking = (booking: any) => {
    seatInfoDialog.value = false
    selectedBooking.value = booking
    detailsDialog.value = true
}

const cancelSingleSeat = async (seat: any) => {
    seatInfoDialog.value = false
    // Ensure we have the correct seat_id for the API call
    selectedSeat.value = {
        ...seat,
        seat_id: seat.seat_id || seat.id
    }
    deleteSeatDialog.value = true
}

const manageSeatBookings = async (booking: any) => {
    selectedBooking.value = booking

    // Refresh booking data to get latest seat details
    const eventId = parseInt(route.params.id as string)
    const { fetchEventBookings } = useAdmin()
    const bookingsResult = await fetchEventBookings(eventId)

    if (bookingsResult.success) {
        const data = bookingsResult.data as any
        const allBookings = Array.isArray(data) ? data : (data.bookings || [])
        const refreshedBooking = allBookings.find((b: any) => b.id === booking.id)

        if (refreshedBooking) {
            selectedBooking.value = refreshedBooking
            // Load seat details for this booking
            if (refreshedBooking.seat_details && refreshedBooking.seat_details.length > 0) {
                seatDetails.value = refreshedBooking.seat_details.map((seat: any) => ({
                    ...seat,
                    id: seat.id,
                    seat_id: seat.seat_id || seat.id // Ensure seat_id is available
                }))
            } else {
                seatDetails.value = []
            }
        } else {
            // Booking might have been cancelled or deleted
            snackbarMessage.value = 'Booking not found or has been cancelled'
            snackbarColor.value = 'warning'
            snackbar.value = true
            return
        }
    } else {
        // Fallback to original booking data
        if (booking.seat_details && booking.seat_details.length > 0) {
            seatDetails.value = booking.seat_details.map((seat: any) => ({
                ...seat,
                id: seat.id,
                seat_id: seat.seat_id || seat.id
            }))
        } else {
            seatDetails.value = []
        }
    }

    seatManagementDialog.value = true
}

const confirmDeleteSeat = (seat: any) => {
    // Ensure we have the correct seat_id for the API call
    selectedSeat.value = {
        ...seat,
        seat_id: seat.seat_id || seat.id
    }
    deleteSeatDialog.value = true
}

const closeSeatManagement = async () => {
    seatManagementDialog.value = false

    // Refresh main booking data to reflect any changes made in seat management
    await loadData()
}

const confirmDeleteSeatBooking = async () => {
    if (!selectedSeat.value) return

    deletingSeat.value = true
    const { deleteSeatBooking } = useAdmin()
    // Use seat_id if available, otherwise fall back to id
    const seatIdToDelete = selectedSeat.value.seat_id || selectedSeat.value.id

    if (!seatIdToDelete) {
        snackbarMessage.value = 'Error: Unable to identify seat ID'
        snackbarColor.value = 'error'
        snackbar.value = true
        deletingSeat.value = false
        return
    }

    const result = await deleteSeatBooking(seatIdToDelete)
    deletingSeat.value = false

    if (result.success) {
        snackbarMessage.value = 'Seat booking removed successfully'
        snackbarColor.value = 'success'
        deleteSeatDialog.value = false
        seatManagementDialog.value = false

        // Comprehensive data reload to ensure all UI components are updated
        await Promise.all([
            loadData(), // Reload bookings and event data
            loadSeats(true) // Reload seat map data
        ])

        // Clear any cached seat info
        selectedSeatInfo.value = null
        selectedBooking.value = null
        selectedSeat.value = null
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const recalculateStats = async () => {
    const eventId = parseInt(route.params.id as string)
    recalculatingStats.value = true

    const { recalculateEventStats } = useAdmin()
    const result = await recalculateEventStats(eventId)
    recalculatingStats.value = false

    if (result.success) {
        snackbarMessage.value = 'Event statistics recalculated successfully'
        snackbarColor.value = 'success'

        // Comprehensive reload to ensure all data is synchronized
        await Promise.all([
            loadData(), // Reload bookings and event data
            loadSeats(true) // Reload seat map data
        ])
    } else {
        snackbarMessage.value = result.error
        snackbarColor.value = 'error'
    }
    snackbar.value = true
}

const exportBookings = () => {
    // Create CSV content
    const csvContent = [
        ['Booking ID', 'Customer Name', 'Email', 'Booking Date', 'Seats', 'Total', 'Status'],
        ...filteredBookings.value.map(booking => [
            booking.id,
            booking.user?.full_name || booking.user?.username || 'N/A',
            booking.user?.email || 'N/A',
            formatDate(booking.booking_date),
            booking.seats_booked,
            booking.total_price.toFixed(2),
            booking.status
        ])
    ].map(row => row.join(',')).join('\n')

    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${event.value?.name || 'event'}-bookings-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)

    snackbarMessage.value = 'Bookings exported successfully'
    snackbarColor.value = 'success'
    snackbar.value = true
}

const getStatusColor = (status: string) => {
    switch (status) {
        case 'confirmed': return 'success'
        case 'cancelled': return 'error'
        case 'pending': return 'warning'
        default: return 'grey'
    }
}

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

// Auto-refresh interval (optional - can be removed if not needed)
let refreshInterval: NodeJS.Timeout | null = null

onMounted(() => {
    loadData()

    // Optional: Set up auto-refresh every 30 seconds for admin interface
    // This ensures seat availability stays current when multiple admins are working
    refreshInterval = setInterval(async () => {
        // Only refresh if no dialogs are open to avoid disrupting user interactions
        if (!showBookingDialog.value && !detailsDialog.value && !seatManagementDialog.value &&
            !deleteSeatDialog.value && !cancelDialog.value && !seatInfoDialog.value) {
            await loadSeats(true) // Silent refresh of seat data
        }
    }, 30000) // 30 seconds
})

onUnmounted(() => {
    clearSelection()
    if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
    }
})
</script>

<style scoped>
.bg-gradient-primary {
    background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
}

.bg-gradient-info {
    background: linear-gradient(135deg, #0288D1 0%, #0277BD 100%);
}

.screen-indicator {
    margin-bottom: 3rem;
    background: linear-gradient(90deg, transparent 0%, #424242 15%, #616161 50%, #424242 85%, transparent 100%);
    height: 6px;
    border-radius: 3px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.screen-indicator::after {
    content: '';
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 280px;
    height: 25px;
    background: linear-gradient(180deg, rgba(66, 66, 66, 0.8) 0%, transparent 100%);
    border-radius: 15px 15px 0 0;
}

.seat-map-container {
    max-width: 100%;
    overflow-x: auto;
    padding: 1rem;
    background: linear-gradient(to bottom, #f5f5f5 0%, #fafafa 100%);
    border-radius: 12px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
}

.seat-map {
    max-width: 100%;
    padding: 1rem 0;
}

.seat-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}

.row-label {
    width: 42px;
    text-align: center;
    font-weight: 700;
    color: #424242;
    font-size: 1.05rem;
    background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
    border-radius: 8px;
    padding: 8px 4px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
}

.seats-container {
    display: flex;
    gap: 0.35rem;
    flex-wrap: nowrap;
}

.seat-wrapper {
    position: relative;
}

.seat-available {
    background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%) !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3) !important;
    border: 2px solid #43A047 !important;
}

.seat-selected {
    background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(33, 150, 243, 0.5) !important;
    border: 2px solid #1565C0 !important;
    transform: scale(1.05);
}

.seat-locked {
    background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%) !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(255, 152, 0, 0.3) !important;
    border: 2px solid #EF6C00 !important;
}

.seat-booked {
    background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%) !important;
    color: white !important;
    cursor: pointer !important;
    box-shadow: 0 2px 6px rgba(244, 67, 54, 0.3) !important;
    border: 2px solid #C62828 !important;
}

.seat-available:hover {
    background: linear-gradient(135deg, #45A049 0%, #388E3C 100%) !important;
    transform: scale(1.1);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.5) !important;
}

.seat-selected:hover {
    background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%) !important;
    transform: scale(1.08);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.seat-booked:hover {
    background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%) !important;
    transform: scale(1.1);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.5) !important;
}

.seat-locked:hover {
    transform: scale(1.05);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-btn.seat-available,
.v-btn.seat-selected,
.v-btn.seat-locked,
.v-btn.seat-booked {
    min-width: 44px !important;
    height: 44px !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

@media (max-width: 960px) {
    .seat-map {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}

@media (max-width: 768px) {
    .seat-row {
        gap: 0.4rem;
    }

    .row-label {
        width: 32px;
        font-size: 0.9rem;
        min-height: 32px;
        padding: 4px 2px;
    }

    .v-btn.seat-available,
    .v-btn.seat-selected,
    .v-btn.seat-locked,
    .v-btn.seat-booked {
        min-width: 36px !important;
        height: 36px !important;
        font-size: 0.75rem !important;
    }

    .seats-container {
        gap: 0.25rem;
    }

    .seat-map-container {
        padding: 0.75rem;
    }
}

/* Seat chips grid for better mobile display */
.seat-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.border-b {
    border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

/* Responsive spacing utilities */
@media (max-width: 600px) {
    .v-card-text {
        padding: 12px !important;
    }

    .gap-3 {
        gap: 0.75rem !important;
    }
}

/* Ensure buttons stack properly on mobile */
@media (max-width: 600px) {
    .d-flex.gap-2 {
        flex-direction: column;
        align-items: stretch;
    }

    .d-flex.gap-2 .v-btn {
        width: 100%;
    }
}
</style>