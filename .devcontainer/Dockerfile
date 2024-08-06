# Use the official Node.js image as a parent image
FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:16

# Set the working directory in the container
WORKDIR /workspaces/wildfiresimulationapp

# Copy the current directory contents into the container at /workspaces/wildfiresimulationapp
COPY . .

# Install any needed packages specified in package.json
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run npm start when the container launches
CMD ["npm", "start"]
