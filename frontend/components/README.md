# Components Library

This directory contains reusable Vue components following best coding practices to reduce code duplication and improve maintainability.

## Structure

```
components/
├── common/           # Common reusable components
├── booking/          # Booking-related components  
└── event/           # Event-related components
```

## Common Components

### StatsCard.vue
Displays statistical information in a card format with icon, value, and label.

**Props:**
- `icon` (string): Material Design icon
- `value` (string|number): The main value to display
- `label` (string): Description text
- `color?` (string): Card color theme
- `iconSize?` (string|number): Icon size
- `valueClass?` (string): CSS classes for value
- `labelClass?` (string): CSS classes for label

**Usage:**
```vue
<StatsCard
  icon="mdi-check-circle"
  :value="42"
  label="Confirmed Bookings"
  color="success"
/>
```

### SearchAndFilter.vue
Provides search input and status filter controls with refresh functionality.

**Props:**
- `searchQuery` (string): Current search term
- `statusFilter?` (string): Current status filter
- `statusOptions?` (Array): Available status options
- `loading?` (boolean): Loading state
- `showStatusFilter?` (boolean): Show/hide status filter

**Events:**
- `@update:searchQuery`: Search query changed
- `@update:statusFilter`: Status filter changed  
- `@refresh`: Refresh button clicked
- `@clear-search`: Clear search clicked

### ConfirmationDialog.vue
Reusable confirmation dialog for destructive actions.

**Props:**
- `modelValue` (boolean): Dialog visibility
- `title` (string): Dialog title
- `message` (string): Confirmation message
- `details?` (string): Additional HTML details
- `loading?` (boolean): Loading state
- `confirmText?` (string): Confirm button text
- `cancelText?` (string): Cancel button text

**Events:**
- `@confirm`: User confirmed action
- `@cancel`: User cancelled action

### LoadingSkeleton.vue
Displays skeleton loading placeholders in grid format.

**Props:**
- `type?` (string): Skeleton type ('article', 'card', 'table', etc.)
- `count?` (number): Number of skeletons
- `cols?` (number): Grid columns
- `sm?`, `md?`, `lg?` (number): Responsive breakpoints

### NotificationSnackbar.vue
Displays toast notifications with customizable styling.

**Props:**
- `modelValue` (boolean): Snackbar visibility
- `message` (string): Notification message
- `color?` (string): Color theme
- `timeout?` (number): Auto-hide timeout
- `actionText?` (string): Action button text

### EmptyState.vue
Shows empty state with icon, message, and optional action button.

**Props:**
- `icon` (string): Display icon
- `title` (string): Main message
- `message?` (string): Additional description
- `actionText?` (string): Action button text
- `actionTo?` (string): Navigation route

### PageHeader.vue
Standardized page header with title and action buttons.

**Props:**
- `title` (string): Page title
- `subtitle?` (string): Optional subtitle
- `actionText?` (string): Action button text
- `actionTo?` (string): Action navigation route
- `actionIcon?` (string): Action button icon

## Booking Components

### BookingDataTable.vue
Data table for displaying booking information with actions.

**Props:**
- `bookings` (Array): Booking data
- `loading?` (boolean): Loading state
- `cancellingBooking?` (number): ID of booking being cancelled

**Events:**
- `@cancel-booking`: Cancel booking requested
- `@view-details`: View booking details requested

### BookingDetailsDialog.vue
Modal dialog showing detailed booking information.

**Props:**
- `modelValue` (boolean): Dialog visibility
- `booking` (Object): Booking data
- `cancellingBooking?` (number): Cancellation loading state

### BookingStats.vue
Statistical overview cards for booking metrics.

**Props:**
- `bookings` (Array): Booking data for calculations
- `loading` (boolean): Loading state

### MyBookingCard.vue
User booking display card with cancellation options.

**Props:**
- `booking` (Object): Booking information

**Events:**
- `@cancel-booking`: Full cancellation requested
- `@partial-cancel`: Partial cancellation requested

## Event Components

### EventCard.vue
Card display for individual events with details and actions.

**Props:**
- `event` (Object): Event data
- `clickable?` (boolean): Enable click interactions
- `imageHeight?` (string|number): Image container height
- `actionText?` (string): Action button text

**Events:**
- `@view-event`: Event click/view requested

### EventGrid.vue
Grid layout for displaying multiple event cards.

**Props:**
- `events` (Array): Events data
- `cols?`, `sm?`, `md?`, `lg?` (number): Responsive grid settings
- `imageHeight?` (string|number): Card image height

### EventDataTable.vue
Admin data table for event management with actions.

**Props:**
- `events` (Array): Events data
- `loading?` (boolean): Loading state
- `itemsPerPage?` (number): Pagination setting

**Events:**
- `@view-bookings`: View event bookings
- `@edit-event`: Edit event requested
- `@delete-event`: Delete event requested

## Composables Integration

### useFormatters.ts
Utility functions for consistent data formatting across components.

**Available Functions:**
- `formatDate(dateString)`: Short date format
- `formatLongDate(dateString)`: Long date format
- `formatPrice(price)`: Currency formatting
- `getStatusColor(status)`: Status color mapping
- `formatSeatLabel(row, seat)`: Seat label formatting
- `truncateText(text, length)`: Text truncation

## Usage Benefits

1. **Code Reusability**: Components can be used across multiple pages
2. **Consistency**: Uniform UI patterns and behavior
3. **Maintainability**: Changes in one component affect all usages
4. **Type Safety**: TypeScript interfaces for props and events
5. **Accessibility**: Built-in Vuetify accessibility features
6. **Responsiveness**: Mobile-first responsive design
7. **Performance**: Smaller bundle sizes through tree-shaking

## Best Practices Implemented

- **Single Responsibility**: Each component has one clear purpose
- **Props Interface**: Strongly typed props with defaults
- **Event Emission**: Clear event contracts between parent/child
- **Slot Support**: Flexible content injection where needed
- **Composable Integration**: Shared logic through composables
- **Consistent Naming**: Clear, descriptive component names
- **Documentation**: Comprehensive prop and event documentation