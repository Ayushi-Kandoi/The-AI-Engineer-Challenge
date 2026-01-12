# Frontend - Next.js Application

A modern, responsive Next.js frontend for the FastAPI mental coach backend.

## Features

- ✅ Homepage with chat interface
- ✅ Real-time backend health checking
- ✅ Loading states and error handling
- ✅ Environment variable configuration for API URL
- ✅ Modern, responsive design matching the project theme
- ✅ TypeScript for type safety

## Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)
- FastAPI backend running at `http://127.0.0.1:8000` (see `../api/README.md` for backend setup)

### Installing Node.js

If you don't have Node.js installed, you can install it using one of these methods:

**Option 1: Using Homebrew (macOS/Linux)**
```bash
brew install node
```

**Option 2: Using nvm (Node Version Manager) - Recommended**
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart your terminal or run:
source ~/.zshrc  # or ~/.bashrc

# Install Node.js LTS version
nvm install --lts
nvm use --lts
```

**Option 3: Download from Official Website**
Visit [nodejs.org](https://nodejs.org/) and download the LTS version installer for your operating system.

After installation, verify it works:
```bash
node --version
npm --version
```

## Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Configure environment variables:**

Create a `.env.local` file in the `frontend` directory:

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

**Note:** For production deployment on Vercel, update this to your production API URL.

## Running the Application

### Development Mode

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

The dev server includes:
- Hot module replacement (HMR)
- Automatic page reloading
- Error overlay in the browser

### Production Build

Build the application for production:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with Inter font
│   ├── page.tsx            # Homepage with chat interface
│   ├── page.module.css     # Homepage styles
│   └── globals.css         # Global styles and theme variables
├── lib/
│   └── api.ts              # API utility functions
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── next.config.js          # Next.js configuration
```

## Theme

The application follows the theme defined in `.cursor/rules/frontend-rule.mdc`:

- **Primary Color:** `#4F46E5` (Indigo)
- **Secondary Color:** `#F43F5E` (Rose)
- **Font Family:** Inter, sans-serif
- **Border Radius:** 8px
- **Button Style:** Rounded

## API Integration

The frontend communicates with the FastAPI backend through:

- **Health Check:** `GET /` - Verifies backend connectivity
- **Chat Endpoint:** `POST /api/chat` - Sends messages and receives AI responses

All API calls are handled in `lib/api.ts` with proper error handling and TypeScript types.

## Error Handling

The application includes comprehensive error handling:

- Backend connection errors
- API request failures
- Network issues
- User input validation

Errors are displayed in user-friendly error messages with clear instructions.

## Loading States

The UI provides visual feedback during:

- Backend health check on page load
- Message sending and response waiting
- All async operations

## Deployment

This frontend is designed to work with Vercel. To deploy:

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set environment variables in Vercel Dashboard:**
   - Go to your project settings on Vercel
   - Navigate to "Environment Variables"
   - Add: `NEXT_PUBLIC_API_URL` with your backend URL (e.g., `https://your-backend.vercel.app` or `http://127.0.0.1:8000` for local testing)

5. **Redeploy after setting environment variables:**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. **Push your code to a Git repository** (GitHub, GitLab, or Bitbucket)

2. **Import the project in Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your Git repository
   - **Important:** Set the root directory to `frontend` (not the project root)

3. **Configure environment variables:**
   - In project settings, go to "Environment Variables"
   - Add: `NEXT_PUBLIC_API_URL` = your backend API URL

4. **Deploy:**
   - Vercel will automatically detect Next.js and deploy

### Important Notes:

- **Root Directory:** Make sure to set the root directory to `frontend` in Vercel project settings
- **Environment Variables:** `NEXT_PUBLIC_API_URL` must be set in Vercel dashboard for the frontend to connect to your backend
- **Backend URL:** If your backend is also on Vercel, use the Vercel URL. For local development, use `http://127.0.0.1:8000`

## Testing Locally

1. Start the FastAPI backend (see `../api/README.md`):
   ```bash
   uv run uvicorn api.index:app --reload
   ```

2. Start the Next.js frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

4. Test the chat interface by sending a message

## Troubleshooting

### Node.js/npm Not Found

If you see `zsh: command not found: npm` or similar errors:

1. **Verify Node.js is installed:**
   ```bash
   node --version
   npm --version
   ```

2. **If not installed, see the "Installing Node.js" section above**

3. **If installed but not in PATH:**
   - Restart your terminal
   - Check your shell configuration file (`~/.zshrc` or `~/.bashrc`)
   - Ensure Node.js binary location is in your PATH

### Backend Connection Error

If you see "Failed to connect to backend":
- Ensure the FastAPI server is running at `http://127.0.0.1:8000`
- Check that CORS is properly configured in the backend
- Verify the `NEXT_PUBLIC_API_URL` in `.env.local`

### Port Already in Use

If port 3000 is already in use:
- Next.js will automatically try the next available port
- Or specify a different port: `npm run dev -- -p 3001`

### Build Errors

If you encounter TypeScript errors:
- Run `npm install` to ensure all dependencies are installed
- Check that all files are saved
- Clear `.next` directory and rebuild: `rm -rf .next && npm run build`
