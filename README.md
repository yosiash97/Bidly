# Bidly - Full Stack Application

A full-stack bidding application with NestJS backend and React frontend, ready for deployment on Replit.

## Project Structure

```
bidly/
├── bidly-backend/          # NestJS backend API
│   ├── src/                # Source files
│   ├── prisma/             # Database schema and migrations
│   └── package.json        # Backend dependencies
├── bidly-frontend/         # React frontend
│   ├── src/                # Source files
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── package.json            # Root package with scripts
├── .replit                 # Replit configuration
└── README.md               # This file
```

## Technology Stack

### Backend
- **Framework**: NestJS
- **Database**: PostgreSQL with Prisma ORM
- **Language**: TypeScript

### Frontend
- **Framework**: React
- **UI Library**: Material-UI (MUI)
- **Language**: JavaScript/JSX

## Prerequisites

- Node.js >= 18.0.0
- PostgreSQL database (for production)

## Local Development

### Install Dependencies

```bash
npm run install:all
```

This will install dependencies for both backend and frontend.

### Environment Variables

#### Backend (.env in bidly-backend/)
Create a `.env` file in the `bidly-backend` directory:

```env
DATABASE_URL="your_postgresql_connection_string"
PORT=3000
```

#### Frontend (.env in bidly-frontend/)
Create a `.env` file in the `bidly-frontend` directory:

```env
REACT_APP_API_URL=http://localhost:3000
```

### Run in Development Mode

```bash
npm run dev
```

This will start both the backend (port 3000) and frontend (port 3001) concurrently.

### Run Individually

Backend only:
```bash
npm run dev:backend
```

Frontend only:
```bash
npm run dev:frontend
```

## Building for Production

```bash
npm run build
```

This builds both the backend and frontend for production.

## Deploying to Replit

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial commit - combined repos"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Import to Replit

1. Go to [Replit](https://replit.com)
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste your GitHub repository URL
5. Replit will automatically detect the `.replit` configuration

### Step 3: Configure Environment Variables

In your Replit project, go to the "Secrets" tab (lock icon) and add:

**Backend Environment Variables:**
- `DATABASE_URL`: Your PostgreSQL connection string
- `PORT`: 3000

**Frontend Environment Variables:**
- `REACT_APP_API_URL`: Your deployed backend URL

### Step 4: Deploy

Click the "Run" button in Replit. The application will:
1. Install all dependencies
2. Build both applications
3. Start the backend server

## Available Scripts

- `npm run install:all` - Install dependencies for both apps
- `npm run dev` - Run both apps in development mode
- `npm run dev:backend` - Run only backend in dev mode
- `npm run dev:frontend` - Run only frontend in dev mode
- `npm run build` - Build both apps for production
- `npm run build:backend` - Build only backend
- `npm run build:frontend` - Build only frontend
- `npm run start` - Start production backend server
- `npm run prisma:generate` - Generate Prisma client

## Database Setup

### Generate Prisma Client

```bash
npm run prisma:generate
```

### Run Migrations (in bidly-backend directory)

```bash
cd bidly-backend
npx prisma migrate dev
```

## Troubleshooting

### Port Conflicts

If you encounter port conflicts, you can modify the ports in:
- Backend: `bidly-backend/src/main.ts`
- Frontend: Create `.env` file with `PORT=YOUR_DESIRED_PORT`

### Database Connection Issues

Ensure your `DATABASE_URL` in the backend `.env` file is correct and the database is accessible.

### Build Errors

1. Clear all node_modules: `rm -rf node_modules bidly-backend/node_modules bidly-frontend/node_modules`
2. Reinstall: `npm run install:all`

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

UNLICENSED - Private Project
