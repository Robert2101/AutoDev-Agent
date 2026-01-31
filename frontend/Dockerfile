FROM node:18-alpine

WORKDIR /app

# Install dependencies using npm install (safer than ci if lockfile varies)
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Accept API URLs as build arguments (Crucial for Next.js to bake them in during build)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ARG NEXT_PUBLIC_WS_URL
ENV NEXT_PUBLIC_WS_URL=${NEXT_PUBLIC_WS_URL}

# Build the application (Standalone mode)
RUN npm run build

# Expose port
EXPOSE 3000

# Start production server
# Note: standalone folder is at .next/standalone, but 'npm start' works fine 
# and is easier to configure with default next.config.js
CMD ["npm", "start"]
