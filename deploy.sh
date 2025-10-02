#!/bin/bash

# Fission Core - One-Click Deploy Script
# Usage: ./deploy.sh <function-name> <github-url> [entrypoint]

FUNCTION_NAME=$1
GITHUB_URL=$2
ENTRY_POINT=${3:-"server.js"}

if [ -z "$FUNCTION_NAME" ] || [ -z "$GITHUB_URL" ]; then
    echo "❌ Usage: ./deploy.sh <function-name> <github-url> [entrypoint]"
    echo "📝 Example: ./deploy.sh my-api https://github.com/user/repo"
    exit 1
fi

echo "🚀 Deploying $FUNCTION_NAME from $GITHUB_URL..."

# Delete existing function if exists
echo "🗑️  Cleaning up existing function..."
fission function delete --name $FUNCTION_NAME 2>/dev/null || true

# Create function
echo "📦 Creating function..."
fission function create --name $FUNCTION_NAME \
  --env nodejs \
  --sourcearchive $GITHUB_URL/archive/main.zip \
  --entrypoint express-wrapper.js

# Create HTTP trigger
echo "🌐 Creating HTTP trigger..."
fission route create --name $FUNCTION_NAME-route \
  --function $FUNCTION_NAME \
  --url /$FUNCTION_NAME \
  --method GET

echo "✅ Deploy completed!"
echo "🔗 API URL: http://localhost:8080/$FUNCTION_NAME"
echo "📊 Check status: kubectl get functions -n default"
