#!/bin/bash
# Deploy Element-145 API to Google Cloud Run
# Prerequisites: gcloud CLI authenticated, project set

set -e

PROJECT_ID="${GCP_PROJECT_ID:-aluminum-os}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="element145-api"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=== Deploying Element-145 API to Cloud Run ==="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo ""

# Copy ontology files into deploy context
echo "Copying ontology files..."
cp ../../registries/lattice_ontology.yaml ./lattice_ontology.yaml
cp ../../registries/module_registry.yaml ./module_registry.yaml

# Build and push
echo "Building container..."
gcloud builds submit --tag "${IMAGE}" .

# Deploy
echo "Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "LATTICE_ONTOLOGY_PATH=lattice_ontology.yaml,MODULE_REGISTRY_PATH=module_registry.yaml,CORS_ORIGINS=*" \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3

# Get URL
URL=$(gcloud run services describe "${SERVICE_NAME}" --region "${REGION}" --format 'value(status.url)')
echo ""
echo "=== DEPLOYED ==="
echo "URL: ${URL}"
echo ""
echo "Verify:"
echo "  curl ${URL}/health"
echo "  curl -X POST ${URL}/classify -H 'Content-Type: application/json' -d '{\"text\": \"quantum computing\"}'"

# Cleanup copied files
rm -f lattice_ontology.yaml module_registry.yaml
