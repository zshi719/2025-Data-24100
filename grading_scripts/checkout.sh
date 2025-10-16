#!/bin/bash

# Color codes for terminal output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

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
# Array of commit hashes
hashes=(
f40bf1fd46ce6a8688e2fe02f350c8c4be037978
3f09301860400c53ad210e01bf59a066e080af2f
b01c285f01842092263df305d7fdb8e85187bc4e
ee73dcdeb66b12dcad52f03f58e102b3aaa4e3a8
b66c3d70417076e68702d15836d5f252fde52d46
55038d39f270ecd00b687e0b19ef45498c012f77
c8e84e488c0d94a570b3ef74af58075c33b9d082
)

# Track any warnings
warnings_count=0
warnings_summary=()

# Check if the number of repos matches the number of hashes
if [ ${#repos[@]} -ne ${#hashes[@]} ]; then
    echo -e "${RED}Error: The number of repositories does not match the number of hashes.${NC}"
    exit 1
fi

# Ask for user confirmation
echo "This script will clone or update the following repositories:"
for repo in "${repos[@]}"; do
    echo "  - $(basename $repo .git)"
done
echo ""
read -p "Do you want to proceed? (y/n): " confirmation
if [[ $confirmation != [yY] ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Loop through the repos and clone or update them
for i in "${!repos[@]}"; do
    repo=${repos[$i]}
    hash=${hashes[$i]}
    
    # Extract the repo name from the URL
    repo_name=$(basename $repo .git)
    
    if [ -d "$repo_name" ]; then
        echo "Directory $repo_name already exists. Updating to commit $hash"
        
        # Change to the repo directory
        cd $repo_name
        
        # Fetch the latest changes
        git fetch origin
        
        # Check if the commit is reachable from main (i.e., merged into main)
        if ! git merge-base --is-ancestor $hash origin/main 2>/dev/null; then
            echo -e "${YELLOW}⚠ Warning: Commit $hash is not merged into main for $repo_name!${NC}"
            echo -e "${YELLOW}  This commit exists on these branches:${NC}"
            git branch -r --contains $hash | while read branch; do
                echo -e "${YELLOW}    - $branch${NC}"
            done
            
            # Check if it's ahead of main
            if git merge-base --is-ancestor origin/main $hash 2>/dev/null; then
                echo -e "${YELLOW}  → This commit is ahead of main (not yet merged)${NC}"
            else
                echo -e "${YELLOW}  → This commit is on a different branch altogether${NC}"
            fi
            
            warnings_count=$((warnings_count + 1))
            warnings_summary+=("$repo_name: Commit not on main (hash: ${hash:0:8}...)")
        else
            echo -e "${GREEN}✓ Commit $hash is merged into main${NC}"
        fi
        
        # Checkout the specific commit regardless of warning
        git checkout $hash 2>/dev/null || git checkout $hash
        
        # Return to the parent directory
        cd ..
    else
        echo "Cloning $repo_name at commit $hash"
        
        # Clone the repo
        git clone $repo $repo_name
        
        # Change to the repo directory
        cd $repo_name
        
        # Check if the commit is reachable from main
        if ! git merge-base --is-ancestor $hash origin/main 2>/dev/null; then
            echo -e "${YELLOW}⚠ Warning: Commit $hash is not merged into main for $repo_name!${NC}"
            echo -e "${YELLOW}  This commit exists on these branches:${NC}"
            git branch -r --contains $hash | while read branch; do
                echo -e "${YELLOW}    - $branch${NC}"
            done
            
            # Check if it's ahead of main
            if git merge-base --is-ancestor origin/main $hash 2>/dev/null; then
                echo -e "${YELLOW}  → This commit is ahead of main (not yet merged)${NC}"
            else
                echo -e "${YELLOW}  → This commit is on a different branch altogether${NC}"
            fi
            
            warnings_count=$((warnings_count + 1))
            warnings_summary+=("$repo_name: Commit not on main (hash: ${hash:0:8}...)")
        else
            echo -e "${GREEN}✓ Commit $hash is merged into main${NC}"
        fi
        
        # Checkout the specific commit regardless of warning
        git checkout $hash 2>/dev/null || git checkout $hash
        
        # Return to the parent directory
        cd ..
    fi
    
    echo "Finished processing $repo_name"
    echo "------------------------"
done

echo ""
echo "All repositories have been processed."

# Show summary of warnings if any
if [ $warnings_count -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Summary: $warnings_count warning(s) encountered:${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    for warning in "${warnings_summary[@]}"; do
        echo -e "${YELLOW}  ⚠ $warning${NC}"
    done
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
else
    echo -e "${GREEN}✓ All commits are properly merged into main!${NC}"
fi