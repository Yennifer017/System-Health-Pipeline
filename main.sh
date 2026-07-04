#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VENV="$PROJECT_DIR/.venv/bin"

usage() {
    echo "Usage:"
    echo "  ./main.sh --mock"
    echo "  ./main.sh --no-mock"
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

case "$1" in

    --mock)

        echo "Generating mock logs..."
        sudo "$PROJECT_DIR/modules/bash/mock-logs.sh"
        ;;

    --no-mock)

        echo "Using existing system logs..."
        ;;

    *)

        usage
        ;;
esac

echo
echo "Collecting telemetry..."

bash "$PROJECT_DIR/modules/bash/recollection.sh"

echo
echo "Analyzing telemetry..."

pwsh "$PROJECT_DIR/modules/powershell/analysis.ps1"

echo
echo "Starting Telegram bot..."

"$VENV/python" "$PROJECT_DIR/modules/python/connect_telegram.py"