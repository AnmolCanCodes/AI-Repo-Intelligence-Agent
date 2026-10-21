# Repo Intelligence Frontend

A modern, developer-focused React + TypeScript frontend for the AI Repo Intelligence Agent.

## Design Philosophy

This frontend follows an anti-AI-slop design approach, prioritizing:

- Clean, minimal aesthetics inspired by developer tools like GitHub and Linear
- Neutral color palette with warm off-white backgrounds
- Monospace typography for technical content
- Subtle borders instead of excessive card containers
- Fast, predictable interactions
- Functional MVP design without generic AI chatbot aesthetics

## Technology Stack

- **React 19** - UI library
- **TypeScript** - Type safety (strict mode)
- **Vite** - Build tool and dev server
- **Tailwind CSS v4** - Utility-first CSS framework
- **Lucide React** - Icon library
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering with syntax highlighting
- **Remark GFM** - GitHub Flavored Markdown support

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ChatInput.tsx    # Chat input with send functionality
│   │   ├── ChatMessage.tsx  # Individual message display with markdown
│   │   ├── ChatWorkspace.tsx # Main chat container
│   │   ├── LoadingState.tsx # Loading indicator
│   │   ├── RepositoryConnect.tsx # Repository connection form
│   │   └── RepositoryHeader.tsx # Header with repo info
│   ├── services/
│   │   └── api.ts           # API service layer
│   ├── types/
│   │   └── index.ts         # TypeScript type definitions
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles and Tailwind
├── .env.example             # Environment variables template
├── package.json             # Dependencies
├── tsconfig.json            # TypeScript configuration
└── vite.config.ts           # Vite configuration
```

## Installation

```bash
cd frontend
npm install
```

## Configuration

Copy `.env.example` to `.env` and configure the backend URL:

```bash
cp .env.example .env
```

Edit `.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Development

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## API Integration

The frontend integrates with the FastAPI backend using three main endpoints:

### Health Check
`GET /` - Checks backend connection status

### Upload Repository
`POST /api/v1/upload-repo` - Clones and indexes a GitHub repository

### Chat
`POST /api/v1/chat` - Sends questions and receives AI responses

All API calls are centralized in `src/services/api.ts` with proper TypeScript typing.

## Features

- **Repository Connection**: Clean form to connect GitHub repositories
- **Real-time Status**: Backend connection indicator
- **Chat Interface**: Developer-focused chat with markdown support
- **Code Highlighting**: Syntax-highlighted code blocks with copy functionality
- **Referenced Files**: Display of files used in AI responses
- **Multi-turn Conversations**: Maintains chat history for context
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Error Handling**: Graceful error states and user feedback

## Design Decisions

- No authentication system (as per MVP scope)
- No streaming responses (backend doesn't support it)
- Minimal animations (prioritizing performance)
- Neutral color palette (avoiding generic AI aesthetics)
- Monospace typography for technical content
- Subtle borders instead of heavy shadows
- Clean typography hierarchy using system fonts

## Browser Support

Modern browsers that support:
- ES6+ JavaScript
- CSS Grid and Flexbox
- CSS Custom Properties (CSS Variables)

## Linting

```bash
npm run lint
```
