#!/bin/bash

echo "Starting Document Extractor Frontend..."
echo

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "ERROR: package.json not found"
    echo "Make sure you're running this from the frontend directory"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo
echo "Starting React development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Backend should be running at: http://localhost:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

npm start