#!/bin/bash
# Frontend build script

set -e

echo "Building frontend assets..."

# Create output directory
mkdir -p static_build/css

# Build CSS with Tailwind
npm run build:css

echo "✓ Frontend assets built"
