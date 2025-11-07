#!/usr/bin/env bash

echo ""

# EDIT THESE VARIABLES TO CHOOSE WHICH ONE YOU WANT
K8S_NAMESPACE="ai-registry"
SECRETS_NAME="ai-registry-secrets"

echo "FROM NAMESPACE '$K8S_NAMESPACE'"

DATABASE_NAME=$(kubectl get secret $SECRETS_NAME -n $K8S_NAMESPACE -o jsonpath="{.data.DJANGO_DATABASE_NAME}" | base64 --decode)
DATABASE_USER=$(kubectl get secret $SECRETS_NAME -n $K8S_NAMESPACE -o jsonpath="{.data.DJANGO_DATABASE_USER}" | base64 --decode)
DATABASE_PASSWORD=$(kubectl get secret $SECRETS_NAME -n $K8S_NAMESPACE -o jsonpath="{.data.DJANGO_DATABASE_PASSWORD}" | base64 --decode)

echo "USING DATABASE '$DATABASE_NAME'"
echo "USING USER     '$DATABASE_USER'"

# make sure password is not empty or the pg_dump will fail with a misleading error
if [ -z "$DATABASE_PASSWORD" ]; then
    echo ""
    echo "ERROR: DATABASE_PASSWORD is empty. Make sure the secrets are set correctly."
    exit 1
fi

# check if db.dump already exists
if [ -f db.dump ]; then
    echo ""
    echo "ERROR: db.dump already exists."
    exit 1
fi

echo ""
echo "PORT FORWARDING ..."
nohup kubectl port-forward deployment/postgresql-djnd 54321:5432 --namespace=shared &>/dev/null &
# store the kubectl pid for later
KUBECTL_PID=$!
# cleanup function to stop port forwarding on exit
stop_port_forwarding() {
    echo ""
    echo "STOPPING PORT FORWARDING"
    kill $KUBECTL_PID
}

# wait for port forwarding to initialise
sleep 5

echo ""
echo "DUMPING DATABASE ..."
PGPASSWORD=$DATABASE_PASSWORD \
    pg_dump -U $DATABASE_USER \
        -f db.dump \
        -d "$DATABASE_NAME" \
        -p 54321 \
        -h localhost

# check the exit status of pg_dump
EXIT_STATUS=$?
if [ $EXIT_STATUS -ne 0 ]; then
    echo "ERROR: pg_dump failed with exit code $EXIT_STATUS"

    stop_port_forwarding
    exit $EXIT_STATUS
fi

echo "DUMP SAVED to db.dump"

stop_port_forwarding

echo ""
echo "To load the database dump run:"
echo "  docker-compose down -v && docker-compose up -d"
echo "  docker container exec -i \$(docker-compose ps -q db) psql -U $DATABASE_USER $DATABASE_NAME < db.dump"

exit 0
