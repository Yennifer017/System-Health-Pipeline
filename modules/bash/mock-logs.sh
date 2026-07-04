#!/bin/bash

# Ensure the script is run with root privileges to allow package installation
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root to install and manage rsyslog."
    exit 1
fi

# Function to check, install, and start rsyslog
setup_rsyslog() {
    echo "Checking for rsyslog installation..."
    
    # Check if rsyslog is installed
    if ! command -v rsyslogd &> /dev/null; then
        echo "rsyslog is not installed. Installing now..."
        apt-get update -qq
        apt-get install -y rsyslog
        
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install rsyslog. Please check your package manager."
            exit 1
        fi
        echo "rsyslog installed successfully."
    else
        echo "rsyslog is already installed."
    fi

    # Ensure the rsyslog service is active and enabled to start on boot
    if ! systemctl is-active --quiet rsyslog; then
        echo "Starting rsyslog service..."
        systemctl start rsyslog
        systemctl enable rsyslog
    else
        echo "rsyslog service is already running."
    fi
}

# Run the setup function
setup_rsyslog
echo "Generating mock telemetry data..."

TAG="SystemHealthMonitor"
ITERATIONS=50

for (( i=1; i<=ITERATIONS; i++ )); do
    # ---------------------------------------------------------
    # INFO: Normal behavior
    # CPU & Disk between 0% and 60%
    # RAM Free between 2048MB and 8192MB
    # ---------------------------------------------------------
    INFO_CPU=$(( RANDOM % 61 ))
    INFO_DISK=$(( RANDOM % 61 ))
    INFO_RAM=$(( RANDOM % 6145 + 2048 ))
    logger -p user.info -t $TAG "INFO: Metrics stable. CPU_USAGE=${INFO_CPU}% DISK_USAGE=${INFO_DISK}% RAM_FREE=${INFO_RAM}MB."

    # ---------------------------------------------------------
    # WARNING: Elevated behavior
    # CPU & Disk between 61% and 85%
    # RAM Free between 500MB and 2047MB
    # ---------------------------------------------------------
    WARN_CPU=$(( RANDOM % 25 + 61 ))
    WARN_DISK=$(( RANDOM % 25 + 61 ))
    WARN_RAM=$(( RANDOM % 1548 + 500 ))
    logger -p user.warning -t $TAG "WARNING: Elevated metrics detected. CPU_USAGE=${WARN_CPU}% DISK_USAGE=${WARN_DISK}% RAM_FREE=${WARN_RAM}MB."

    # ---------------------------------------------------------
    # CRITICAL: Severe resource exhaustion
    # CPU & Disk between 86% and 100%
    # RAM Free between 10MB and 499MB
    # ---------------------------------------------------------
    CRIT_CPU=$(( RANDOM % 15 + 86 ))
    CRIT_DISK=$(( RANDOM % 15 + 86 ))
    CRIT_RAM=$(( RANDOM % 490 + 10 ))
    logger -p user.crit -t $TAG "CRITICAL: Resource threshold exceeded! CPU_USAGE=${CRIT_CPU}% DISK_USAGE=${CRIT_DISK}% RAM_FREE=${CRIT_RAM}MB."
done

echo "Success! Injected 150 events (50 INFO, 50 WARNING, 50 CRITICAL) into the system log."
echo "You can verify the logs using: grep '$TAG' /var/log/syslog"