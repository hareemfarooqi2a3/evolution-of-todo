# Use a Node.js base image for building the Next.js application
FROM node:18-alpine AS builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY chatbot_frontend/package.json ./
COPY chatbot_frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the chatbot_frontend application code
COPY chatbot_frontend/ .

# Build the Next.js application
RUN npm run build

# Use a lean production image
FROM node:18-alpine AS runner

WORKDIR /app

# Set production environment
ENV NODE_ENV production

# Copy necessary files from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.js ./next.config.js # Ensure this exists or is adjusted

# Expose the port Next.js runs on
EXPOSE 3000

# Command to run the Next.js application
CMD ["npm", "start"]
