#!/bin/bash
# ================================================
# Lior Pozin's Branding Factory — One-Click Launcher
# ================================================
# Double-click this file to run the factory.
# (First time: right-click → Open → Open to allow it)

cd "$(dirname "$0")"
echo "🏭 Starting Lior Pozin's Branding Factory..."
echo ""
python3 main.py
echo ""
echo "Press any key to close..."
read -n 1
