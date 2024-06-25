#!/bin/bash

echo "Choose an option:"
echo "1. Start monitoring containers"
echo "2. Stop monitoring containers"
echo "3. Restart monitoring containers"
read -p "Enter your choice (1, 2 or 3): " choice

if [ $choice -eq 1 ]; then
    sudo docker compose -f docker-compose.monitoring.yml up -d --build
elif [ $choice -eq 2 ]; then
    sudo docker compose -f docker-compose.monitoring.yml down
elif [ $choice -eq 3 ]; then
    sudo docker compose -f docker-compose.monitoring.yml down
    sudo docker compose -f docker-compose.monitoring.yml up -d --build
else
    echo "Invalid choice. Please enter 1 or 2."
fi
