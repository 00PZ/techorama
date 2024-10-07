# Use the official Python 3.11 image from the devcontainers repository
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Switch back to vscode user
USER vscode
