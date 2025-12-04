# syntax = docker/dockerfile:1

# Adjust NODE_VERSION as desired
ARG NODE_VERSION=21.6.2
FROM node:${NODE_VERSION} as base

# Arguments for PostGIS and PostgreSQL
ARG POSTGIS_MAJOR=3
ARG PG_MAJOR=13

LABEL fly_launch_runtime="NestJS/Prisma"

# NestJS/Prisma app lives here
WORKDIR /app

# Set production environment
ENV NODE_ENV="production"

# Throw-away build stage to reduce size of final image
FROM base as build

# Install dependencies for building the application and Python
RUN apt-get update && apt-get install -y \
    sudo \
    vim \
    python3 \
    python3-pip \
    python3-venv \
    postgresql-server-dev-all \
    postgis \
    build-essential \
    node-gyp \
    openssl \
    pkg-config \
    python-is-python3 && \
    rm -rf /var/lib/apt/lists/*

# Set up virtual environment for Python
RUN python3 -m venv /app/venv
RUN /app/venv/bin/python -m pip install --upgrade pip

# Activate the virtual environment and install Python dependencies
RUN /bin/bash -c "source /app/venv/bin/activate && pip install geopy scrapeghost selenium beautifulsoup4 webdriver-manager requests"

# Install Node.js dependencies
COPY package.json package-lock.json ./
RUN npm ci --include=dev

# Generate Prisma Client
COPY prisma .
RUN npx prisma generate

# Copy application code
COPY . .

# Build application
RUN npm run build

# Final stage for app image
FROM base

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    openssl \
    python3 \
    python3-pip \
    python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Copy Python virtual environment from the build stage
COPY --from=build /app/venv /app/venv

# Ensure the virtual environment is activated in the final image
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy built application and Node.js dependencies
COPY --from=build /app /app

# Expose the application port
EXPOSE 3000

# Start the server by default, this can be overwritten at runtime
CMD [ "npm", "run", "start" ]
