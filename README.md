# FastAPI + Nuxt.js + Vuetify + Tailwind CSS Project

A full-stack web application with FastAPI backend and Nuxt.js 3 frontend featuring Vuetify 3 and Tailwind CSS.

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for Python

### Frontend
- **Nuxt.js 3** - Vue.js framework with SSR
- **Vue 3** - Progressive JavaScript framework
- **Vuetify 3** - Material Design component framework
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript

## 📁 Project Structure

```
Project_1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── .gitignore
│
└── frontend/
    ├── pages/              # Nuxt pages (auto-routing)
    ├── layouts/            # Layout components
    ├── plugins/            # Nuxt plugins (Vuetify, API)
    ├── assets/             # CSS and static assets
    ├── package.json        # Node dependencies
    ├── nuxt.config.ts      # Nuxt configuration
    ├── tailwind.config.js  # Tailwind configuration
    └── .gitignore
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## 🎯 Features

### Backend (FastAPI)
- ✅ RESTful API endpoints
- ✅ Automatic API documentation (Swagger/OpenAPI)
- ✅ CORS middleware configured
- ✅ Pydantic models for data validation
- ✅ CRUD operations for items
- ✅ Health check endpoint

### Frontend (Nuxt.js)
- ✅ Server-side rendering (SSR)
- ✅ File-based routing
- ✅ Auto-imports for components and composables
- ✅ Vuetify 3 Material Design components
- ✅ Tailwind CSS utility classes
- ✅ TypeScript support
- ✅ API integration plugin
- ✅ Responsive layouts

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/api/health` | Health check |
| GET | `/api/items` | Get all items |
| GET | `/api/items/{id}` | Get single item |
| POST | `/api/items` | Create new item |
| PUT | `/api/items/{id}` | Update item |
| DELETE | `/api/items/{id}` | Delete item |

## 🎨 Using Vuetify and Tailwind Together

This project demonstrates how to use both Vuetify and Tailwind CSS together:

- **Vuetify** is used for complex UI components (cards, buttons, forms, navigation)
- **Tailwind CSS** is used for utility styling (margins, padding, colors, gradients)

Example:
```vue
<!-- Vuetify Card with Tailwind utilities -->
<v-card class="mx-auto max-w-lg shadow-xl">
  <v-card-title class="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
    Title
  </v-card-title>
</v-card>
```

## 🔧 Configuration

### Backend Configuration (.env)
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
FRONTEND_URL=http://localhost:3000
```

### Frontend Configuration (.env)
```env
API_BASE_URL=http://localhost:8000
```

## 📦 Available Scripts

### Backend
```bash
python main.py          # Run development server with hot reload
```

### Frontend
```bash
npm run dev            # Start development server
npm run build          # Build for production
npm run generate       # Generate static site
npm run preview        # Preview production build
```

## 🚀 Production Deployment

### Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
npm run build
npm run preview
```

## 🔒 CORS Configuration

CORS is configured in `backend/main.py` to allow requests from the frontend:
```python
allow_origins=["http://localhost:3000"]
```

Update this for production with your actual frontend URL.

## 📚 Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nuxt.js Documentation](https://nuxt.com/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Learning Resources

- **FastAPI**: Check the auto-generated docs at `/docs` after starting the backend
- **Nuxt.js**: File-based routing in the `pages/` directory
- **Vuetify**: Browse components at [vuetifyjs.com/components](https://vuetifyjs.com/components/)
- **Tailwind**: Reference utilities at [tailwindcss.com/docs](https://tailwindcss.com/docs)

## 💡 Tips

1. The frontend will auto-reload on file changes
2. The backend uses `reload=True` for hot reloading during development
3. Check browser console and terminal for any errors
4. API documentation is automatically generated at `/docs`
5. Use Vuetify for components, Tailwind for quick styling adjustments

---

Happy coding! 
