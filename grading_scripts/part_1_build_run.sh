#!/bin/bash

# Output file
output_file="docker_build_run_output.txt"

# Clear the output file if it exists
> $output_file
docker_build_run() {
    local repo_name=$1
    # Convert repo name to lowercase for Docker image tag
    local image_name=$(echo "$repo_name" | tr '[:upper:]' '[:lower:]')
    
    {
        echo "==== Processing $repo_name ===="
        
        # Change to the repository directory
        cd "$repo_name" || { echo "Failed to enter $repo_name directory"; return; }
        
        echo "Starting Docker build for $repo_name (image: $image_name)"
        if docker build -q . -t "$image_name"; then
            echo "Docker build successful for $repo_name"
        else
            echo "Docker build failed for $repo_name"
            cd ..
            return
        fi
        
        echo "Starting Docker run for $repo_name (image: $image_name)"
        echo "Container output for $repo_name:"
        if docker run --rm "$image_name"; then
            echo "Docker run completed successfully for $repo_name"
        else
            echo "Docker run failed for $repo_name"
        fi
        
        echo "==== Finished processing $repo_name ===="
        echo ""
        
        # Return to the parent directory
        cd ..
    } 2>&1 | tee -a "$output_file"
}

# Main script
echo "Starting Docker build and run process for all repositories" >> $output_file

# Loop through all directories
for dir in */; do
    # Remove trailing slash from directory name
    repo_name=${dir%/}
    
    # Run docker commands for this repository
    docker_build_run "$repo_name"
done

echo "Process completed. Check $output_file for details."
