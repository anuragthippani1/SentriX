#!/bin/bash

echo "Starting SentriX - Multi-Agent Supply Chain Risk Intelligence Platform"
echo

echo "Installing dependencies..."
npm run install-all

echo
echo "Starting SentriX..."
echo "Backend will run on http://localhost:8000"
echo "Frontend will run on http://localhost:3000"
echo

npm run dev
