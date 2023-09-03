# Use the official Nginx image as the base image
FROM nginx:alpine3.18-slim

# Copy the contents of your frontend app to the Nginx default directory
COPY app /usr/share/nginx/html

# Expose the default Nginx port (80)
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
