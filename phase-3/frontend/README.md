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

### AI Task Assistant (New!)
- **Natural Language Interface**: Manage tasks through conversational AI
- **Real-time Chat**: Send messages and receive instant AI responses
- **Tool Call Visualization**: See which actions the AI performs (add, list, update, complete, delete)
- **Conversation History**: View and resume previous conversations
- **Smart Context**: AI remembers conversation context (last 20 messages)
- **Error Recovery**: Graceful handling of API failures with helpful suggestions
- **Rate Limited**: 60 requests per minute for optimal performance

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
- `POST /api/{user_id}/chat` - Send message to AI chatbot
- `GET /api/{user_id}/conversations` - List all conversations
- `GET /api/{user_id}/conversations/{id}` - Get conversation details
- `DELETE /api/{user_id}/conversations/{id}` - Delete conversation

## Using the AI Task Assistant

### Accessing the Chat

1. Sign in to your account at `/signin`
2. Navigate to `/chat` or click "AI Assistant" from the dashboard
3. Start chatting with the AI to manage your tasks

### Example Commands

**Adding Tasks:**
- "Add a task to buy groceries"
- "Create a task: finish the project report by Friday"
- "Add three tasks: call mom, pay bills, and schedule dentist appointment"

**Listing Tasks:**
- "Show me my tasks"
- "List my active tasks"
- "What tasks do I have?"
- "Show completed tasks"

**Completing Tasks:**
- "Mark the grocery task as complete"
- "Complete the first task"
- "Mark task [task-id] as done"

**Updating Tasks:**
- "Update the grocery task title to 'Buy organic groceries'"
- "Change the description of task [task-id] to 'Buy milk and eggs'"
- "Set due date for task [task-id] to 2024-03-15"

**Deleting Tasks:**
- "Delete the grocery task"
- "Remove task [task-id]"
- "Delete all completed tasks" (AI will ask for confirmation)

### Understanding AI Responses

The AI assistant will:
- **Confirm actions**: "I've added the task 'buy groceries' to your list."
- **Show tool calls**: Visual indicators showing which operations were performed
- **Ask for clarification**: If your request is ambiguous, the AI will ask questions
- **Provide alternatives**: If an operation fails, the AI suggests what to do next

### Tool Call Indicators

When the AI performs an action, you'll see tool call cards showing:
- **Tool name**: The operation performed (e.g., add_task, list_tasks)
- **Status**: Success (green) or Error (red)
- **Message**: Confirmation or error details

### Conversation History

- Click "History" to view past conversations
- Click any conversation to resume it
- Click "New Chat" to start fresh
- Conversations persist across sessions

### Tips for Best Results

**Be Specific:**
- ❌ "Add a task"
- ✅ "Add a task to buy groceries"

**Use Natural Language:**
- ✅ "Show me what I need to do today"
- ✅ "Mark the grocery shopping as done"

**Provide Context:**
- Reference task titles: "Complete the grocery task"
- Use task IDs if you have them: "Update task abc-123"

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
