# Event Booking System - Frontend

Nuxt.js 3 frontend with Vuetify for the Event Booking System.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure API URL
The API base URL is configured in `nuxt.config.ts`:
```typescript
runtimeConfig: {
  public: {
    apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
  }
}
```

### 3. Start Development Server
```bash
npm run dev
```

Application will start at: http://localhost:3000

## Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run generate     # Generate static site
npm run preview      # Preview production build
```

## Project Structure

```
frontend/
├── pages/                 # Application pages
│   ├── index.vue         # Home page with events
│   ├── login.vue         # User login
│   ├── signup.vue        # User registration
│   ├── my-bookings.vue   # User bookings
│   ├── events/
│   │   └── [id].vue      # Event details & booking
│   └── admin/
│       ├── login.vue     # Admin login
│       ├── register.vue  # Admin registration
│       ├── dashboard.vue # Admin dashboard
│       ├── events/
│       │   ├── index.vue # Event list
│       │   └── create.vue # Create event
│       └── bookings.vue  # All bookings
├── composables/          # Reusable composition functions
│   ├── useAuth.ts       # Authentication logic
│   ├── useEvents.ts     # Event operations
│   ├── useBookings.ts   # Booking operations
│   └── useAdmin.ts      # Admin operations
├── middleware/           # Route protection
│   ├── auth.ts          # User authentication
│   └── admin.ts         # Admin authorization
├── layouts/
│   └── default.vue      # Main layout with navigation
└── plugins/
    ├── api.ts           # API client configuration
    └── vuetify.ts       # Vuetify configuration
```

## User Features

### Public Access (No Login Required)
- Browse upcoming events
- Search and filter events
- View event details
- View available seats

### Authenticated Users
- Book events
- View booking history
- Cancel bookings
- Manage profile

### Admin Portal
- Create/edit/delete events
- View all bookings
- See booking details (who booked what and when)
- Dashboard with statistics

## Routes

### Public Routes
- `/` - Home page with events
- `/events/:id` - Event details
- `/login` - User login
- `/signup` - User registration

### Protected Routes (Auth Required)
- `/my-bookings` - User's bookings

### Admin Routes (Admin Only)
- `/admin/login` - Admin login
- `/admin/register` - Admin registration
- `/admin/dashboard` - Admin dashboard
- `/admin/events` - Event management
- `/admin/events/create` - Create event
- `/admin/bookings` - All bookings

## Composables

### useAuth()
```typescript
const { 
  user,              // Current user
  isAuthenticated,   // Auth status
  isAdmin,          // Admin status
  login,            // Login function
  register,         // Register function
  registerAdmin,    // Admin registration
  logout            // Logout function
} = useAuth()
```

### useEvents()
```typescript
const {
  events,              // Events list
  currentEvent,        // Selected event
  fetchEvents,         // Fetch all events
  fetchUpcomingEvents, // Fetch upcoming
  fetchEventById,      // Fetch single event
  createEvent,         // Create event (admin)
  updateEvent,         // Update event (admin)
  deleteEvent          // Delete event (admin)
} = useEvents()
```

### useBookings()
```typescript
const {
  bookings,         // User's bookings
  createBooking,    // Create booking
  fetchMyBookings,  // Fetch user bookings
  cancelBooking     // Cancel booking
} = useBookings()
```

### useAdmin()
```typescript
const {
  fetchAllEvents,      // All events (admin)
  fetchEventBookings,  // Event bookings
  fetchAllBookings,    // All bookings
  fetchDashboardStats  // Dashboard data
} = useAdmin()
```

## Middleware

### auth.ts
Protects routes requiring user authentication. Redirects to `/login` if not authenticated.

```vue
definePageMeta({
  middleware: 'auth'
})
```

### admin.ts
Protects routes requiring admin privileges. Redirects to `/admin/login` if not authenticated or not admin.

```vue
definePageMeta({
  middleware: 'admin'
})
```

## Styling

The application uses:
- **Vuetify 3** - Material Design components
- **Tailwind CSS** - Utility-first CSS (optional)
- **Material Design Icons** - Icon library

## API Integration

API calls are made using the `$api` plugin which automatically:
- Adds authentication token to requests
- Handles 401 errors (redirects to login)
- Provides base URL configuration

## Authentication Flow

1. User logs in via `/login` or `/signup`
2. Token received from backend
3. Token stored in cookie
4. Token sent with subsequent API requests
5. Middleware protects authenticated routes

## Development Tips

### Add New Page
1. Create file in `pages/` directory
2. Add navigation link in `layouts/default.vue`
3. Add middleware if protection needed

### Add New API Call
1. Create composable or add to existing
2. Use `$api` for requests
3. Handle loading and error states

### Customize Theme
Edit `plugins/vuetify.ts`:
```typescript
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          // ... add more colors
        }
      }
    }
  }
})
```

## Troubleshooting

**API connection failed:**
- Check backend is running on port 8000
- Verify API_BASE_URL in nuxt.config.ts

**Authentication issues:**
- Clear cookies and local storage
- Check token expiration
- Verify backend JWT configuration

**Module not found:**
```bash
rm -rf node_modules .nuxt
npm install
```

**Port already in use:**
```bash
lsof -ti:3000 | xargs kill -9
npm run dev
```

## Build for Production

```bash
npm run build
npm run preview
```

## Technologies Used

- Nuxt.js 3
- Vue 3 Composition API
- Vuetify 3
- TypeScript
- Vite
