#!/usr/bin/env bash

# pipeline_utils.sh
# Useful functions for logging and error handling in bash pipelines

# Print timestamped informational message
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*"
}

# Print timestamped error message to stderr and exit
log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
    exit 1
}


# Check if a file exists; if not, exit with error message
check_file_exists() {
    if [[ ! -f "$1" ]]; then
        log_error "File not found: $1"
    fi
}

# Check if a directory exists; if not, exit with error message
check_dir_exists() {
    if [[ ! -d "$1" ]]; then
        log_error "Directory not found: $1"
    fi
}
