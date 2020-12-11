#!/usr/bin/env bash
set -exo pipefail

helm upgrade --install \
    submission-confirmation-consumer \
    k8s/helm \
    --set-string subscription_id="${SUBSCRIPTION_ID}" \
    --set-string notify_api_key="${NOTIFY_API_KEY}" \

kubectl rollout restart deployment.v1.apps/submission-confirmation-consumer
kubectl rollout status deployment.v1.apps/submission-confirmation-consumer
