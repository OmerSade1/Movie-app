#!/bin/bash
# wait-for-it.sh

# This script waits for a given service to be available (TCP port to be open).
# Usage:
#   ./wait-for-it.sh host:port -- command_to_execute

TIMEOUT=30  # Timeout in seconds
INTERVAL=5   # Interval in seconds

wait_for_service() {
    local host=$1
    local port=$2
    local timeout=$3
    local interval=$4

    start_time=$(date +%s)
    while ! nc -z "$host" "$port"; do
        sleep $interval
        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))
        if [ $elapsed_time -ge $timeout ]; then
            echo "Timeout reached! Unable to connect to $host:$port"
            exit 1
        fi
        echo "Waiting for $host:$port to be ready..."
    done
}

# Main entry point
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 host:port -- command_to_execute"
    exit 1
fi

hostport=$1
shift
host=$(echo $hostport | cut -d: -f1)
port=$(echo $hostport | cut -d: -f2)

wait_for_service "$host" "$port" "$TIMEOUT" "$INTERVAL"

# Execute the command once the service is available
exec "$@"
