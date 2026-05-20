#!/bin/bash
# 🏭 Personal Branding Factory — Quick Launch (macOS/Linux)
# Double-click this file or run: bash launch_app.sh

cd "$(dirname "$0")"

# Check if profile exists
if [ ! -f "profile.yaml" ]; then
    echo "⚠️  No profile found! Running setup wizard..."
    python3 setup_profile.py
fi

python3 app.py
