#!/bin/bash

echo "Installing AbletonMCP Remote Script..."

# Create the directory
sudo mkdir -p "/Applications/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/AbletonMCP"

# Copy the Remote Script file
sudo cp "/Users/megmac/Documents/Cline/MCP/ableton-mcp/RemoteScript/__init__.py" "/Applications/Ableton Live 12 Suite.app/Contents/App-Resources/MIDI Remote Scripts/AbletonMCP/"

echo "Installation complete!"
echo "Now restart Ableton Live and configure AbletonMCP in MIDI settings."
