#!/bin/bash
# Check if agent-browser is installed
if ! command -v agent-browser &> /dev/null; then
    echo "Installing agent-browser..."
    npm install -g agent-browser
    agent-browser install
fi
