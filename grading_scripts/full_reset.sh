#!/bin/bash

# This resets the entire repo so that it is 
# the exact same as the remote. Handles untracked files and such
# Array of repository URLs
repos=(
    "git@github.com:dsi-clinic/2025-Data-24100-Group-1.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-2.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-3.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-4.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-5.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-6.git"
    "git@github.com:dsi-clinic/2025-Data-24100-Group-7.git"
)

# Ask for user confirmation
echo "This script will reset the following repositories to their main branch:"
for repo in "${repos[@]}"; do
    echo "  - $(basename $repo .git)"
done
echo "WARNING: This will remove all untracked files and reset all changes!"
echo ""
read -p "Do you want to proceed? (y/n): " confirmation
if [[ $confirmation != [yY] ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Loop through the repos and reset them
for repo in "${repos[@]}"; do
    # Extract the repo name from the URL
    repo_name=$(basename $repo .git)
    
    if [ -d "$repo_name" ]; then
        echo "Resetting $repo_name to clean state"
        
        # Change to the repo directory
        cd "$repo_name"
        
        # Fetch all branches
        echo "Fetching all branches..."
        git fetch --all
        
        # Discard all local changes, including staged changes
        echo "Discarding all local changes..."
        git reset --hard

        # Clean all untracked files and directories, including ignored ones
        echo "Removing untracked files and directories..."
        git clean -fdx

        # Checkout main branch (or master if main doesn't exist)
        echo "Checking out main branch..."
        if git show-ref --verify --quiet refs/remotes/origin/main; then
            git checkout main
            git reset --hard origin/main
        else
            git checkout master
            git reset --hard origin/master
        fi

        # Pull latest changes
        echo "Pulling latest changes..."
        git pull

        # Return to the parent directory
        cd ..
        
        echo "Finished resetting $repo_name"
        echo "------------------------"
    else
        echo "Directory $repo_name doesn't exist. Cloning fresh..."
        git clone $repo
        echo "Finished cloning $repo_name"
        echo "------------------------"
    fi
done

echo "All repositories have been reset successfully."
