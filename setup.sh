#!/bin/bash

set -e

echo "=========================================="
echo "      Project Setup"
echo "=========================================="

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo."
    exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_HOME=$(eval echo "~${SUDO_USER:-$USER}")
VENV_DIR="$PROJECT_DIR/.venv"

echo
echo "Installing system dependencies..."

apt-get update

apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    rsyslog \
    curl \
    powershell

echo
echo "Checking rsyslog..."

systemctl enable rsyslog
systemctl start rsyslog

echo
echo "Creating output directory..."

mkdir -p "$PROJECT_DIR/output"

echo
echo "Creating virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    sudo -u "${SUDO_USER:-$USER}" python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo
echo "Installing Python dependencies..."

sudo -u "${SUDO_USER:-$USER}" \
"$VENV_DIR/bin/pip" install --upgrade pip

sudo -u "${SUDO_USER:-$USER}" \
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

echo
echo "Checking .env..."

if [ ! -f "$PROJECT_DIR/.env" ]; then
    if [ -f "$PROJECT_DIR/.env.example" ]; then
        cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
        echo ".env created from .env.example"
        echo "Remember to edit it before running the project."
    else
        echo "WARNING: .env not found."
    fi
fi

echo
echo "=========================================="
echo "        Setup completed successfully!"
echo "=========================================="
echo
echo "Available execution modes:"
echo
echo "  Generate mock telemetry and run pipeline:"
echo "      ./main.sh --mock"
echo
echo "  Analyze existing system logs:"
echo "      ./main.sh --no-mock"
echo
echo "Make sure your .env file contains valid"
echo "Telegram credentials before running."
echo
echo "=========================================="