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
fabf0c434a71ae5c046b7228a61a4706569f9650
6b8e3056a2516471dddb384014323c0821b252fa
a9c074f912c51575f0a4ff97cd5b6e896a569f50
8b637da0877a9679c5ec26df0f574feea4029f28
2907514cd345b5312826561a0e072ef4f718d042
7e8bac13c7c30ba77ea978375f9495d79ed514cc
2118727f30d894a73edaf94e5670e0d4d31d0a46
47401e423a1e75eec85fee4f0d60c98500277388
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
