FROM node:18-alpine

WORKDIR /app

# Install dependencies using npm install (safer than ci if lockfile varies)
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Build the application (Standalone mode)
RUN npm run build

# Expose port
EXPOSE 3000

# Start production server
# Note: standalone folder is at .next/standalone, but 'npm start' works fine 
# and is easier to configure with default next.config.js
CMD ["npm", "start"]
