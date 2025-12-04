# Bidly - Full Stack Bidding Application

## Overview
Bidly is a full-stack web application for managing and tracking bidding opportunities. It features a NestJS backend API with PostgreSQL database and a React frontend with Material-UI components.

## Current State
- **Status**: Fully functional and running on Replit
- **Last Updated**: December 4, 2025
- **Environment**: Development mode on Replit

## Recent Changes
- **Dec 4, 2025**: Initial Replit setup completed
  - Configured backend to run on localhost:3001 with CORS enabled for all origins
  - Configured frontend to run on port 5000 with HOST=0.0.0.0
  - Set up PostgreSQL database and ran all migrations
  - Fixed missing image assets by adding placeholder images
  - Configured workflow to run both backend and frontend concurrently

## Technology Stack

### Backend
- **Framework**: NestJS (TypeScript)
- **Database**: PostgreSQL with Prisma ORM
- **Port**: 3001 (localhost)
- **Key Features**:
  - REST API for bid management
  - Task scheduling
  - Soft delete functionality
  - Geolocation support for bids

### Frontend
- **Framework**: React 18
- **UI Library**: Material-UI (MUI)
- **Port**: 5000 (0.0.0.0)
- **Build Tool**: Create React App (react-scripts 5.x)
- **Key Features**:
  - Bid listing and management interface
  - Distance-based filtering
  - Responsive design

## Project Structure

```
bidly/
├── bidly-backend/          # NestJS backend API
│   ├── src/
│   │   ├── bids/          # Bid management module
│   │   ├── task/          # Task scheduling module
│   │   └── main.ts        # Application entry point
│   ├── prisma/
│   │   ├── schema.prisma  # Database schema
│   │   └── migrations/    # Database migrations
│   └── package.json
├── bidly-frontend/         # React frontend
│   ├── src/
│   │   ├── Components/    # React components
│   │   ├── Assets/        # Images and static files
│   │   └── App.js
│   ├── public/
│   └── package.json
├── package.json           # Root package with concurrently scripts
└── replit.md             # This file
```

## Environment Variables

### Backend (Automatically configured)
- `DATABASE_URL`: PostgreSQL connection string (from Replit database)
- `PORT`: 3001 (default for backend)

### Frontend
- `PORT`: 5000 (configured in .env)
- `HOST`: 0.0.0.0 (configured in .env)
- `DANGEROUSLY_DISABLE_HOST_CHECK`: true (required for Replit proxy)
- `WDS_SOCKET_PORT`: 0 (for WebSocket configuration)
- `REACT_APP_NODE_ENV`: local (environment mode)

## Running the Application

The application runs automatically via the configured workflow:
```bash
npm run dev
```

This command uses `concurrently` to run both:
- Backend: `cd bidly-backend && npm run start:dev` (port 3001)
- Frontend: `cd bidly-frontend && npm start` (port 5000)

## Database

### Schema
The database includes the following main table:
- **bid**: Stores bidding opportunities with fields like title, status, url, location, city, bid_type, and deletedAt (for soft deletes)

### Migrations
All migrations are located in `bidly-backend/prisma/migrations/` and have been successfully applied.

## API Endpoints

### Bids
- `GET /bids` - Get all bids
- `GET /bids/type` - Get bids by type
- `POST /bids` - Create a new bid
- `POST /bids/distance` - Soft delete a bid
- `PATCH /bids/:id` - Update a bid
- `DELETE /bids/:id` - Delete a bid

### Tasks
- `GET /task` - Get tasks
- `GET /task/distance` - Get tasks by distance (with slider value parameter)

## Development Notes

### Frontend Configuration
- The frontend is configured to bypass host header verification, which is necessary for Replit's proxy setup
- The app uses environment variables to determine which backend URL to use (local/development/production)
- Currently set to "local" mode, which connects to localhost:3001

### Backend Configuration
- CORS is enabled for all origins to work with Replit's proxy
- The backend listens on 0.0.0.0:3001 to be accessible from the Replit proxy
- Prisma client is generated using version 5.11.0 to match the schema format

### Known Issues
- Some ESLint warnings exist in the frontend code (unused imports, === vs ==)
- These are non-blocking and the application functions correctly

## Deployment

When ready to deploy to production:
1. The deployment configuration uses the built React frontend
2. Backend will run in production mode
3. Environment variables will need to be configured for production database

## User Preferences
- Project uses existing code structure and conventions
- Maintains compatibility with original repository setup
- Uses Replit's built-in PostgreSQL database

## Next Steps
- Configure production deployment settings
- Set up production environment variables if needed
- Consider addressing ESLint warnings for code quality
