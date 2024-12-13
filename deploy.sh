#!/bin/bash

# Variables
REGION="us-central1"

# Step 1: Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy agentic-ecommerce \
  --source .\
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080

