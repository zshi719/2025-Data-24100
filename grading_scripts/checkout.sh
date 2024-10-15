#!/bin/bash

# Array of repository URLs
repos=(
    "git@github.com:dsi-clinic/data_241_autumn_2024_1.git"
    "git@github.com:dsi-clinic/data_241_autumn_2024_2.git"
    "git@github.com:dsi-clinic/data_241_autumn_2024_3.git"
    "git@github.com:jbendavid/data_241_autumn_2024_4.git"
    "git@github.com:dsi-clinic/data_241_autumn_2024_GROUP_5.git"
    "git@github.com:dsi-clinic/data_241_autumn_2024_GROUP_6.git"
    "git@github.com:dsi-clinic/data_241_autumn_2024_GROUP_7.git"
    "git@github.com:michelangelopagan/data_241_autumn_2024_8.git"
)

# Array of commit hashes
hashes=(
    "5d120be1c473c7da67244361f6e105c328baba2c"
    "ebb5e232e867323dc5405cace0522b98dbea649f"
    "1460e8c37f2e73ba1f43742158a240865c31971f"
    "d5fc46bf370594d7e5c084bc3a2caac424431eb7"
    "b41e31a1d3283b7ca488109fa5630ba506f2a30e"
    "b47b5ba6af4da1e65a1cf648c0be5dd6c8331b30"
    "34339cb6c918038a0d27a3b9e5e080c29a39b66b"
    "b729a11abde69b00efad78c50ba9e4e684ef0eea"
)

# Check if the number of repos matches the number of hashes
if [ ${#repos[@]} -ne ${#hashes[@]} ]; then
    echo "Error: The number of repositories does not match the number of hashes."
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
        
        # Checkout the specific commit
        git checkout $hash
        
        # Return to the parent directory
        cd ..
    else
        echo "Cloning $repo_name at commit $hash"
        
        # Clone the repo
        git clone $repo $repo_name
        
        # Change to the repo directory
        cd $repo_name
        
        # Checkout the specific commit
        git checkout $hash
        
        # Return to the parent directory
        cd ..
    fi
    
    echo "Finished processing $repo_name"
    echo "------------------------"
done

echo "All repositories have been processed successfully."
