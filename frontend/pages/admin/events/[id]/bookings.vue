<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <div class="d-flex flex-column flex-sm-row align-start align-sm-center mb-4 gap-3">
                    <div class="d-flex align-center flex-grow-1">
                        <v-btn icon="mdi-arrow-left" variant="text" @click="$router.push('/admin/events')" class="mr-2"
                            size="small"></v-btn>
                        <h1 class="text-h5 text-sm-h4 font-weight-bold">{{ event?.name || 'Event' }} - Admin</h1>
                    </div>
                    <div class="d-flex gap-2 flex-wrap">
                        <v-btn color="secondary" variant="outlined" @click="recalculateStats" size="small"
                            :loading="recalculatingStats">
                            <v-icon start size="small">mdi-calculator</v-icon>
                            <span class="d-none d-sm-inline">Recalculate</span>
                        </v-btn>
                        <v-btn color="primary" variant="outlined" @click="exportBookings" size="small">
                            <v-icon start size="small">mdi-download</v-icon>
                            <span class="d-none d-sm-inline">Export</span>
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
            <v-col cols="12" md="4">
                <v-card>
                    <v-img :src="event.image_url || 'https://via.placeholder.com/800x400?text=Event'" height="250"
                        cover></v-img>

                    <v-card-title class="text-h5 py-3">{{ event.name }}</v-card-title>

                    <v-card-text>
                        <v-row class="mb-3">
                            <v-col cols="12">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="primary" size="small">mdi-calendar</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Date & Time</div>
                                        <div class="text-body-2 font-weight-medium">{{ formatDate(event.event_date) }}
                                        </div>
                                    </div>
                                </div>
                            </v-col>

                            <v-col cols="12">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="primary" size="small">mdi-map-marker</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Location</div>
                                        <div class="text-body-2 font-weight-medium">{{ event.location }}</div>
                                    </div>
                                </div>
                            </v-col>

                            <v-col cols="12">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="primary" size="small">mdi-cash</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Price per Seat</div>
                                        <div class="text-body-2 font-weight-medium">${{ event.price.toFixed(2) }}</div>
                                    </div>
                                </div>
                            </v-col>

                            <v-col cols="12">
                                <div class="d-flex align-center mb-2">
                                    <v-icon class="mr-2" color="success" size="small">mdi-seat</v-icon>
                                    <div>
                                        <div class="text-caption text-grey">Available Seats</div>
                                        <div class="text-body-2 font-weight-medium">{{ event.available_seats }} / {{
                                            event.total_seats }}</div>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>

                        <v-divider class="my-3"></v-divider>

                        <h4 class="text-h6 mb-2">About This Event</h4>
                        <p class="text-body-2" v-if="event.description">{{ event.description }}</p>
                        <p class="text-body-2 text-grey" v-else>No description available</p>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Seat Map -->
            <v-col cols="12" md="8">
                <v-card>
                    <v-card-title class="d-flex align-center justify-space-between">
                        <div class="d-flex align-center gap-2">
                            <span>Seat Map & Booking</span>
                            <v-chip color="orange" size="small">Admin Mode</v-chip>
                        </div>
                        <v-chip color="primary" v-if="selectedSeats.length > 0">
                            {{ selectedSeats.length }} selected
                        </v-chip>
                    </v-card-title>

                    <v-card-text>
                        <!-- Theatre Screen -->
                        <div class="text-center mb-4">
                            <div class="screen-indicator">
                                <v-chip color="grey-darken-1" size="large">SCREEN</v-chip>
                            </div>
                        </div>

                        <!-- Seat Map -->
                        <div class="seat-map" v-if="!seatsLoading">
                            <div v-for="(rowSeats, rowNumber) in groupSeatsByRow" :key="rowNumber"
                                class="seat-row mb-2">
                                <div class="row-label">{{ rowNumber }}</div>
                                <div class="seats-container">
                                    <v-tooltip v-for="seat in rowSeats" :key="seat.id" location="top">
                                        <template v-slot:activator="{ props }">
                                            <div class="seat-wrapper">
                                                <v-btn :class="getSeatClass(seat)" @click="toggleSeat(seat)"
                                                    size="small" variant="flat" :loading="seatActionLoading === seat.id"
                                                    v-bind="props">
                                                    {{ seat.seat_number }}
                                                </v-btn>
                                            </div>
                                        </template>
                                        <span v-if="getSeatBookingInfo(seat)">
                                            <strong>Booked by:</strong> {{ getSeatBookingInfo(seat)?.user_name }}<br>
                                            <strong>Email:</strong> {{ getSeatBookingInfo(seat)?.user_email }}
                                        </span>
                                        <span v-else-if="seat.is_locked && !selectedSeats.includes(seat.id)">
                                            Temporarily locked by another user
                                        </span>
                                        <span v-else-if="selectedSeats.includes(seat.id)">
                                            Selected - Row {{ rowNumber }}, Seat {{ seat.seat_number }}
                                        </span>
                                        <span v-else>
                                            Available - Row {{ rowNumber }}, Seat {{ seat.seat_number }}
                                        </span>
                                    </v-tooltip>
                                </div>
                                <div class="row-label">{{ rowNumber }}</div>
                            </div>
                        </div>

                        <v-skeleton-loader v-else type="paragraph, paragraph, paragraph"></v-skeleton-loader>

                        <!-- Legend -->
                        <v-row class="mt-4">
                            <v-col cols="12">
                                <div class="d-flex flex-wrap gap-2 gap-sm-4 justify-center">
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="success" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Available</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="primary" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Selected</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="orange" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Locked</span>
                                    </div>
                                    <div class="d-flex align-center">
                                        <v-btn size="x-small" color="error" class="mr-2" disabled></v-btn>
                                        <span class="text-caption">Booked (Click to view)</span>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>

                        <!-- Admin Booking Section -->
                        <v-card v-if="selectedSeats.length > 0" elevation="4" color="primary" class="mt-4">
                            <v-card-text class="pa-3 pa-sm-4">
                                <v-row align="center">
                                    <v-col cols="6" sm="4" class="py-2">
                                        <div class="text-body-1 text-sm-h6 text-white">${{ event.price.toFixed(2) }} per
                                            seat</div>
                                        <div class="text-caption text-sm-body-2 text-white opacity-80">{{
                                            selectedSeats.length }} selected</div>
                                    </v-col>
                                    <v-col cols="6" sm="4" class="py-2 text-right text-sm-left">
                                        <div class="text-h6 text-sm-h4 font-weight-bold text-white">
                                            ${{ (event.price * selectedSeats.length).toFixed(2) }}
                                        </div>
                                        <div class="text-caption text-white opacity-80">Total</div>
                                    </v-col>
                                    <v-col cols="12" sm="4" class="d-flex flex-column flex-sm-row gap-2 py-2">
                                        <v-btn color="white" variant="elevated" :loading="bookingLoading"
                                            @click="showBookingDialog = true" block class="flex-sm-grow-1">
                                            <v-icon start size="small">mdi-ticket</v-icon>
                                            Book
                                        </v-btn>
                                        <v-btn variant="outlined" color="white" @click="clearSelection" block
                                            class="flex-sm-grow-0">
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
                <v-card>
                    <v-card-title class="d-flex align-center justify-space-between">
                        <span>Event Bookings</span>
                        <v-chip color="primary">{{ bookings.length }} Total Bookings</v-chip>
                    </v-card-title>

                    <v-card-text class="pa-2 pa-sm-4">
                        <v-row class="mb-4">
                            <v-col cols="12" sm="6" md="4">
                                <v-text-field v-model="search" label="Search by user name or email..."
                                    prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details
                                    clearable></v-text-field>
                            </v-col>
                            <v-col cols="12" sm="6" md="4">
                                <v-select v-model="statusFilter" :items="statusOptions" label="Filter by status"
                                    variant="outlined" density="compact" hide-details clearable></v-select>
                            </v-col>
                            <v-col cols="12" md="4" class="d-flex align-center">
                                <v-chip v-if="filteredBookings.length !== bookings.length" color="primary"
                                    variant="outlined">
                                    Showing {{ filteredBookings.length }} of {{ bookings.length }}
                                </v-chip>
                            </v-col>
                        </v-row>

                        <v-data-table v-if="filteredBookings.length > 0" :headers="headers" :items="filteredBookings"
                            :items-per-page="15" :search="search" class="elevation-0" :mobile-breakpoint="600">
                            <template v-slot:item.user="{ item }">
                                <div>
                                    <div class="font-weight-medium">{{ item.user?.full_name || item.user?.username }}
                                    </div>
                                    <div class="text-caption text-grey">{{ item.user?.email }}</div>
                                </div>
                            </template>

                            <template v-slot:item.booking_date="{ item }">
                                {{ formatDate(item.booking_date) }}
                            </template>

                            <template v-slot:item.seats_booked="{ item }">
                                <v-chip size="small" color="info">{{ item.seats_booked }} seats</v-chip>
                            </template>

                            <template v-slot:item.total_price="{ item }">
                                <span class="font-weight-bold">${{ item.total_price.toFixed(2) }}</span>
                            </template>

                            <template v-slot:item.status="{ item }">
                                <v-chip :color="getStatusColor(item.status)" size="small">
                                    {{ item.status }}
                                </v-chip>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <div class="d-flex gap-1">
                                    <v-btn icon="mdi-eye" size="small" variant="text" @click="viewBookingDetails(item)"
                                        title="View Details"></v-btn>
                                    <v-btn icon="mdi-seat" size="small" variant="text" color="primary"
                                        @click="manageSeatBookings(item)" title="Manage Seats"></v-btn>
                                    <v-btn icon="mdi-cancel" size="small" variant="text" color="error"
                                        @click="cancelBookingConfirm(item)" :disabled="item.status === 'cancelled'"
                                        title="Cancel Booking"></v-btn>
                                </div>
                            </template>
                        </v-data-table>

                        <div v-else class="text-center py-12">
                            <v-icon size="80" color="grey-lighten-1">mdi-ticket-outline</v-icon>
                            <p class="text-h6 text-grey mt-4">No bookings found</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Admin Booking Dialog -->
        <v-dialog v-model="showBookingDialog" max-width="600" :fullscreen="$vuetify.display.xs">
            <v-card>
                <v-card-title class="text-h5 bg-primary text-white d-flex align-center">
                    <v-icon start>mdi-ticket-confirmation</v-icon>
                    <span class="text-h6 text-sm-h5">Create Booking</span>
                </v-card-title>
                <v-card-text class="pa-4 pa-sm-6">
                    <v-text-field v-model="bookingUsername" label="Username or Email (Optional)"
                        prepend-inner-icon="mdi-account-search" variant="outlined"
                        hint="Leave empty to book for yourself as admin, or enter username/email for another user"
                        persistent-hint clearable class="mb-4"></v-text-field>

                    <v-alert type="info" variant="tonal" class="mb-4">
                        <div class="d-flex justify-space-between align-center mb-1">
                            <span><strong>Seats selected:</strong></span>
                            <span>{{ selectedSeats.length }}</span>
                        </div>
                        <div class="d-flex justify-space-between align-center">
                            <span><strong>Total price:</strong></span>
                            <span class="text-h6">${{ event ? (event.price * selectedSeats.length).toFixed(2) : '0.00'
                            }}</span>
                        </div>
                    </v-alert>

                    <v-alert v-if="bookingError" type="error" variant="tonal" dismissible class="mb-4">
                        {{ bookingError }}
                    </v-alert>
                </v-card-text>
                <v-card-actions class="pa-4">
                    <v-spacer></v-spacer>
                    <v-btn variant="text" @click="showBookingDialog = false">Cancel</v-btn>
                    <v-btn color="primary" :loading="bookingLoading" @click="handleAdminBooking">
                        <v-icon start size="small">mdi-check</v-icon>
                        Create Booking
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
                                        color="primary">
                                        Row {{ seat.row_number }} - Seat {{ seat.seat_number }}
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
        <v-dialog v-model="seatManagementDialog" max-width="800" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedBooking">
                <v-card-title class="text-h6 text-sm-h5 bg-info text-white d-flex align-center">
                    <v-icon start>mdi-seat</v-icon>
                    <span>Manage Seat Bookings</span>
                </v-card-title>
                <v-card-subtitle class="py-3 bg-grey-lighten-4">
                    <div class="mb-1"><strong>Customer:</strong> {{ selectedBooking.user?.full_name ||
                        selectedBooking.user?.username }}</div>
                    <div><strong>Email:</strong> {{ selectedBooking.user?.email }}</div>
                    <div class="mt-2">
                        <v-chip size="small" color="success" class="mr-2">{{ seatDetails.length }} seats</v-chip>
                        <v-chip size="small" color="primary">${{ selectedBooking.total_price?.toFixed(2) || '0.00'
                        }}</v-chip>
                    </div>
                </v-card-subtitle>
                <v-card-text class="pa-4 pa-sm-6">
                    <div v-if="seatDetails.length > 0">
                        <div class="d-flex justify-space-between align-center mb-3">
                            <h6 class="text-subtitle-1 text-sm-h6 font-weight-bold">Booked Seats</h6>
                            <v-chip size="small" variant="tonal">{{ seatDetails.length }}</v-chip>
                        </div>
                        <div class="seat-chips-grid mb-4">
                            <v-chip v-for="seat in seatDetails" :key="seat.id" color="primary" closable
                                @click:close="confirmDeleteSeat(seat)" class="ma-1">
                                <v-icon start size="small">mdi-seat</v-icon>
                                R{{ seat.row_number }}-S{{ seat.seat_number }}
                            </v-chip>
                        </div>
                        <v-alert type="warning" variant="tonal" density="compact">
                            <div class="text-body-2">
                                <strong>Admin Action:</strong> Click the <v-icon size="x-small">mdi-close</v-icon> on
                                any seat
                                to remove it from this booking.
                                This will update the total price and make the seat available.
                            </div>
                        </v-alert>
                    </div>
                    <div v-else class="text-center py-8 py-sm-12">
                        <v-icon size="64" color="grey-lighten-1">mdi-seat-outline</v-icon>
                        <p class="text-body-1 text-sm-h6 text-grey mt-4">No seat details available</p>
                    </div>
                </v-card-text>
                <v-card-actions class="pa-4">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="seatManagementDialog = false">Close</v-btn>
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
                            <v-chip size="small" color="primary" class="mr-2">
                                <v-icon start size="small">mdi-seat</v-icon>
                                Row {{ selectedSeat.row_number }} - Seat {{ selectedSeat.seat_number }}
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
        <v-dialog v-model="seatInfoDialog" max-width="600" :fullscreen="$vuetify.display.xs">
            <v-card v-if="selectedSeatInfo">
                <v-card-title class="text-h6 text-sm-h5 bg-info text-white d-flex align-center">
                    <v-icon start>mdi-seat</v-icon>
                    <span>Seat Information</span>
                </v-card-title>
                <v-card-text class="pa-4 pa-sm-6">
                    <!-- Seat Details -->
                    <div class="mb-4">
                        <h3 class="text-h6 mb-3">Seat Details</h3>
                        <v-chip color="error" size="large" class="mb-2">
                            <v-icon start>mdi-seat</v-icon>
                            Row {{ selectedSeatInfo.seat.row_number }} - Seat {{ selectedSeatInfo.seat.seat_number }}
                        </v-chip>
                        <div class="text-body-2 text-grey mt-2">This seat is currently booked</div>
                    </div>

                    <v-divider class="my-4"></v-divider>

                    <!-- User Details -->
                    <div class="mb-4">
                        <h3 class="text-h6 mb-3">Booked By</h3>
                        <v-card variant="outlined" class="pa-3 bg-grey-lighten-5">
                            <div class="mb-2">
                                <strong>Name:</strong> {{ selectedSeatInfo.user_name }}
                            </div>
                            <div class="mb-2">
                                <strong>Email:</strong> {{ selectedSeatInfo.user_email }}
                            </div>
                            <div class="mb-2">
                                <strong>Booking ID:</strong> #{{ selectedSeatInfo.booking.id }}
                            </div>
                            <div class="mb-2">
                                <strong>Total Seats in Booking:</strong> {{ selectedSeatInfo.booking.seats_booked }}
                            </div>
                            <div>
                                <strong>Total Price:</strong> ${{ selectedSeatInfo.booking.total_price?.toFixed(2) }}
                            </div>
                        </v-card>
                    </div>

                    <!-- Quick Actions -->
                    <v-alert type="info" variant="tonal" density="compact" class="mb-2">
                        <div class="text-body-2">
                            <strong>Admin Actions:</strong> You can view all seats in this booking or cancel just this
                            seat.
                        </div>
                    </v-alert>
                </v-card-text>
                <v-card-actions class="pa-4 flex-column flex-sm-row gap-2">
                    <v-btn @click="seatInfoDialog = false" block variant="outlined">Close</v-btn>
                    <v-btn color="primary" @click="viewFullBooking(selectedSeatInfo.booking)" block>
                        <v-icon start size="small">mdi-eye</v-icon>
                        View Full Booking
                    </v-btn>
                    <v-btn color="error" @click="cancelSingleSeat(selectedSeatInfo.seat)" block>
                        <v-icon start size="small">mdi-cancel</v-icon>
                        Cancel This Seat
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
    if (!seat.is_available && !seat.is_locked && Array.isArray(bookings.value)) {
        // Find booking that contains this seat
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
            // Find the full booking details
            const booking = bookings.value.find((b: any) => b.id === bookingInfo.booking_id)
            if (booking) {
                selectedSeatInfo.value = {
                    seat: seat,
                    booking: booking,
                    user_name: bookingInfo.user_name,
                    user_email: bookingInfo.user_email
                }
                seatInfoDialog.value = true
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

const handleAdminBooking = async () => {
    if (!event.value || selectedSeats.value.length === 0) return

    bookingError.value = ''
    bookingLoading.value = true

    try {
        // If no username provided, use current admin's username
        const usernameOrEmail = bookingUsername.value.trim() || user.value?.username

        if (!usernameOrEmail) {
            bookingError.value = 'Unable to determine user for booking'
            return
        }

        const response = await $api('/api/admin/bookings', {
            method: 'POST',
            body: {
                event_id: event.value.id,
                seat_ids: selectedSeats.value,
                username_or_email: usernameOrEmail
            }
        })

        const bookingFor = bookingUsername.value.trim() ? bookingUsername.value : 'yourself'
        snackbarMessage.value = `Booking created successfully for ${bookingFor}`
        snackbarColor.value = 'success'
        snackbar.value = true

        showBookingDialog.value = false
        clearSelection()
        await loadData() // Reload all data
    } catch (error: any) {
        bookingError.value = error.data?.detail || 'Failed to create booking'
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
        await loadData() // Reload data
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
    selectedSeat.value = seat
    deleteSeatDialog.value = true
}

const manageSeatBookings = async (booking: any) => {
    selectedBooking.value = booking

    // Load seat details for this booking
    if (booking.seat_details && booking.seat_details.length > 0) {
        seatDetails.value = booking.seat_details.map((seat: any) => ({
            ...seat,
            seat_id: seat.seat_id || seat.id
        }))
    } else {
        // If seat details are not available, we need to fetch them
        seatDetails.value = []
    }

    seatManagementDialog.value = true
}

const confirmDeleteSeat = (seat: any) => {
    selectedSeat.value = seat
    deleteSeatDialog.value = true
}

const confirmDeleteSeatBooking = async () => {
    if (!selectedSeat.value) return

    deletingSeat.value = true
    const { deleteSeatBooking } = useAdmin()
    const result = await deleteSeatBooking(selectedSeat.value.seat_id)
    deletingSeat.value = false

    if (result.success) {
        snackbarMessage.value = 'Seat booking removed successfully'
        snackbarColor.value = 'success'
        deleteSeatDialog.value = false
        seatManagementDialog.value = false
        await loadData() // Reload data
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
        await loadData() // Reload data to show updated stats
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

onMounted(() => {
    loadData()
})

onUnmounted(() => {
    clearSelection()
})
</script>

<style scoped>
.screen-indicator {
    margin-bottom: 2rem;
    background: linear-gradient(90deg, transparent 0%, #424242 20%, #424242 80%, transparent 100%);
    height: 4px;
    border-radius: 2px;
    position: relative;
}

.screen-indicator::after {
    content: '';
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 20px;
    background: linear-gradient(180deg, #424242 0%, transparent 100%);
    border-radius: 10px 10px 0 0;
}

.seat-map {
    max-width: 100%;
    overflow-x: auto;
    padding: 1rem 0;
}

.seat-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.row-label {
    width: 35px;
    text-align: center;
    font-weight: bold;
    color: #333;
    font-size: 1rem;
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 4px;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.seats-container {
    display: flex;
    gap: 0.25rem;
    flex-wrap: nowrap;
}

.seat-wrapper {
    position: relative;
}

.seat-available {
    background-color: #4CAF50 !important;
    color: white !important;
}

.seat-selected {
    background-color: #2196F3 !important;
    color: white !important;
    box-shadow: 0 0 0 2px #1976D2 !important;
}

.seat-locked {
    background-color: #FF9800 !important;
    color: white !important;
}

.seat-booked {
    background-color: #F44336 !important;
    color: white !important;
    cursor: pointer !important;
}

.seat-available:hover {
    background-color: #45A049 !important;
    transform: scale(1.05);
    transition: all 0.2s ease;
}

.seat-selected:hover {
    background-color: #1976D2 !important;
}

.seat-booked:hover {
    background-color: #D32F2F !important;
}

.v-btn.seat-available,
.v-btn.seat-selected,
.v-btn.seat-locked,
.v-btn.seat-booked {
    min-width: 36px !important;
    height: 36px !important;
    border-radius: 8px !important;
    font-size: 0.75rem !important;
    font-weight: bold !important;
}

@media (max-width: 960px) {
    .seat-map {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
}

@media (max-width: 768px) {
    .seat-row {
        gap: 0.25rem;
    }

    .row-label {
        width: 28px;
        font-size: 0.85rem;
        min-height: 28px;
        padding: 2px;
    }

    .v-btn.seat-available,
    .v-btn.seat-selected,
    .v-btn.seat-locked,
    .v-btn.seat-booked {
        min-width: 28px !important;
        height: 28px !important;
        font-size: 0.7rem !important;
    }

    .seats-container {
        gap: 0.125rem;
    }
}

/* Seat chips grid for better mobile display */
.seat-chips-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
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