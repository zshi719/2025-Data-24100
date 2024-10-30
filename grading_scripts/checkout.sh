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
d0384af021797bfca0fb2c36a8f7a6927f4280e6
90de715a525bd8eca70e7e136bcf6c1d7dfa45ee
d57c511440abc3c0a7b90ec0e24c990469f06269
0afb2d04e9512e19d64feb7c776ea1c1aa1b4c10
7c3de3590e1430f594596d4fe93f11e273a6c242
636e3e95af54181159570512b654baee160debc9
08ce9c2bec40e190d51c334617312aedc05722dc
8702ed96697eceed622e0800b45942306777312f
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
