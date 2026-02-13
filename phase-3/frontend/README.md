# Todo Application - Frontend

A modern, full-stack todo application built with Next.js 16+ (App Router), TypeScript, and Tailwind CSS. This frontend integrates with a FastAPI backend using JWT authentication.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **API Client**: Axios 1.6+
- **Validation**: Zod 3.22+
- **Testing**: Vitest, React Testing Library, Playwright
- **Authentication**: Custom JWT (Bearer tokens)

## Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000 (see ../backend/README.md)

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set the backend API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Run tests
npm run test

# Run end-to-end tests
npm run test:e2e
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   ├── signup/            # Signup page
│   ├── signin/            # Signin page
│   └── dashboard/         # Protected dashboard
├── src/
│   ├── components/        # React components
│   │   ├── ui/           # Base UI components
│   │   ├── auth/         # Authentication components
│   │   ├── tasks/        # Task management components
│   │   └── layout/       # Layout components
│   ├── lib/              # Utilities and libraries
│   │   ├── api/          # API client and endpoints
│   │   ├── hooks/        # Custom React hooks
│   │   └── utils/        # Utility functions
│   └── types/            # TypeScript type definitions
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## Features

### Authentication
- User signup with email and password
- User signin with JWT token generation
- Secure logout with session cleanup
- Protected routes requiring authentication
- Automatic token refresh on API calls

### Task Management
- Create tasks with title and description
- View all personal tasks
- Edit task details
- Mark tasks as complete/incomplete
- Delete tasks with confirmation
- User isolation (users only see their own tasks)

### UI/UX
- Responsive design (mobile, tablet, desktop)
- Loading states for all async operations
- Error handling with user-friendly messages
- Accessible interface (WCAG AA compliant)
- Dark mode support

## API Integration

The frontend communicates with the FastAPI backend using Bearer token authentication:

**Base URL**: `http://localhost:8000`

**Authentication Flow**:
1. User signs up/signs in → Backend returns JWT token
2. Frontend stores token in localStorage
3. All API requests include `Authorization: Bearer <token>` header
4. Backend verifies token and returns user-specific data

**Endpoints**:
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/signin` - Sign in and get token
- `POST /api/auth/logout` - Sign out
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

## Testing

### Unit Tests
```bash
npm run test
```

### End-to-End Tests
```bash
npm run test:e2e
```

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

1. Push code to GitHub repository
2. Import project in Vercel dashboard
3. Configure environment variables
4. Deploy

See [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Troubleshooting

### Backend Connection Issues
- Ensure backend is running on http://localhost:8000
- Check CORS configuration in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Authentication Issues
- Clear localStorage and try signing in again
- Check browser console for token errors
- Verify backend JWT secret is configured

### Build Errors
- Delete `.next` folder and rebuild
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## License

MIT
