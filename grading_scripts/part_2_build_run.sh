#!/bin/bash

# Output file
output_file="part_2_autograder_output.txt"
summary_file="part_2_summary.md"

# API key for testing
API_KEY="${DATA_241_API_KEY:-test_grading_key_2024}"

# Port for Flask
FLASK_PORT=4000

# Create temp directory for JSON results
results_dir=$(mktemp -d)
trap "rm -rf $results_dir" EXIT

# Clear the output files if they exist
> "$output_file"
> "$summary_file"

# Function to wait for Flask to be ready
wait_for_flask() {
    local max_wait=60
    local wait_count=0
    
    # Initial wait already done before calling this function
    
    while ! curl -s http://localhost:${FLASK_PORT}/api/v1/row_count >/dev/null 2>&1; do
        sleep 1
        wait_count=$((wait_count + 1))
        if [ $wait_count -ge $max_wait ]; then
            echo "Flask server did not start within $max_wait seconds"
            return 1
        fi
        # Show progress every 10 seconds
        if [ $((wait_count % 10)) -eq 0 ]; then
            echo "  Still waiting... ($wait_count seconds elapsed)"
        fi
    done
    return 0
}

# Function to stop all running containers
stop_containers() {
    echo "Stopping any running containers..."
    docker ps -q | xargs -r docker stop >/dev/null 2>&1
}

# Function to process a single repository
process_repo() {
    local repo_name=$1
    # Convert repo name to lowercase for Docker image tag
    local image_name=$(echo "$repo_name" | tr '[:upper:]' '[:lower:]')
    
    {
        echo "==== Processing $repo_name ===="
        
        # Change to the repository directory
        cd "$repo_name" || { echo "Failed to enter $repo_name directory"; return 1; }
        
        # Build Docker image
        echo "Building Docker image for $repo_name..."
        if docker build -q . -t "$image_name" 2>&1; then
            echo "✓ Docker build successful for $repo_name"
        else
            echo "✗ Docker build failed for $repo_name"
            cd ..
            return 1
        fi
        
        # Check if Makefile exists
        if [ ! -f "Makefile" ]; then
            echo "✗ No Makefile found in $repo_name"
            cd ..
            return 1
        fi
        
        # Start Flask server in background
        echo "Starting Flask server for $repo_name..."
        export DATA_241_API_KEY="$API_KEY"
        # Redirect stdin to avoid TTY issues with 'docker run -it' in background
        # Also set PYTHONUNBUFFERED for immediate output
        PYTHONUNBUFFERED=1 make flask < /dev/null > flask_output.log 2>&1 &
        FLASK_PID=$!
        
        # Give Docker time to start the container
        echo "Waiting for Docker container to start..."
        sleep 3
        
        # Check if the process is still running
        if ! kill -0 $FLASK_PID 2>/dev/null; then
            echo "⚠ Warning: make flask process died quickly. Checking for running containers..."
            # Look for any running containers (make might have detached)
            if docker ps | grep -q "$image_name"; then
                echo "✓ Found running Docker container"
            else
                echo "✗ No container found running"
                cat flask_output.log
                cd ..
                return 1
            fi
        fi
        
        # Wait for Flask to be ready
        echo "Waiting for Flask to be ready..."
        if wait_for_flask; then
            echo "✓ Flask server is ready"
            
            # Run the autograder (regular output for logs)
            echo ""
            echo "--- Running autograder for $repo_name ---"
            python3 ../flask_autograder.py \
                --api v1 \
                --key "$API_KEY" \
                --url "http://localhost:${FLASK_PORT}"
            
            AUTOGRADER_EXIT_CODE=$?
            
            # Also capture JSON results for summary (run again in JSON mode)
            python3 ../flask_autograder.py \
                --api v1 \
                --key "$API_KEY" \
                --url "http://localhost:${FLASK_PORT}" \
                --json > "$results_dir/${repo_name}.json" 2>/dev/null
            
            if [ $AUTOGRADER_EXIT_CODE -eq 0 ]; then
                echo "✓ All tests passed for $repo_name"
            else
                echo "✗ Some tests failed for $repo_name (exit code: $AUTOGRADER_EXIT_CODE)"
            fi
        else
            echo "✗ Flask server failed to start for $repo_name"
            AUTOGRADER_EXIT_CODE=1
        fi
        
        # Stop Flask server
        echo "Stopping Flask server..."
        if [ ! -z "$FLASK_PID" ]; then
            kill $FLASK_PID 2>/dev/null
            wait $FLASK_PID 2>/dev/null
        fi
        
        # Also stop any Docker containers
        stop_containers
        
        # Clean up log file
        rm -f flask_output.log
        
        echo "==== Finished processing $repo_name ===="
        echo ""
        
        # Return to the parent directory
        cd ..
        
        return $AUTOGRADER_EXIT_CODE
        
    } 2>&1 | tee -a "$output_file"
    
    return ${PIPESTATUS[0]}
}

# Main script
echo "Starting Part 2 autograder process for all repositories" | tee -a "$output_file"
echo "Using API key: $API_KEY" | tee -a "$output_file"
echo "" | tee -a "$output_file"

# Track results
total_repos=0
passed_repos=0
failed_repos=0

# Loop through all Group directories
for dir in 2025-Data-24100-Group-*/; do
    # Remove trailing slash from directory name
    repo_name=${dir%/}
    
    # Skip if not a directory
    [ -d "$repo_name" ] || continue
    
    total_repos=$((total_repos + 1))
    
    # Process this repository
    if process_repo "$repo_name"; then
        passed_repos=$((passed_repos + 1))
    else
        failed_repos=$((failed_repos + 1))
    fi
done

# Generate markdown summary table
echo "Generating summary table..."
RESULTS_DIR="$results_dir" python3 << 'PYTHON_SCRIPT' > "$summary_file"
import json
import os
import sys
from pathlib import Path

results_dir = os.environ.get('RESULTS_DIR', '')
if not results_dir:
    print("Error: RESULTS_DIR not set", file=sys.stderr)
    sys.exit(1)

# Collect all results
results = []
for json_file in sorted(Path(results_dir).glob('*.json')):
    group_name = json_file.stem
    try:
        with open(json_file) as f:
            data = json.load(f)
            results.append({
                'group': group_name,
                'data': data
            })
    except Exception as e:
        print(f"Error reading {json_file}: {e}", file=sys.stderr)

if not results:
    print("# Part 2 Summary\n\nNo results found.")
    sys.exit(0)

# Print markdown table
print("# Part 2 Autograder Summary\n")
print("## Overall Results\n")
print("| Group | Status | Tests Passed | Row Count | NYSE Stocks | NASDAQ Stocks | Issues |")
print("|-------|--------|--------------|-----------|-------------|---------------|--------|")

for result in results:
    group = result['group']
    data = result['data']
    
    status = "✅ PASS" if data.get('all_passed', False) else "❌ FAIL"
    tests = f"{data.get('passed', 0)}/{data.get('total_tests', 0)}"
    
    endpoint_data = data.get('endpoint_data', {})
    row_count = endpoint_data.get('row_count', {}).get('row_count', 'N/A')
    nyse_count = endpoint_data.get('unique_nyse_stock_count', {}).get('unique_nyse_stock_count', 'N/A')
    nasdaq_count = endpoint_data.get('unique_nasdaq_stock_count', {}).get('unique_nasdaq_stock_count', 'N/A')
    
    issues = []
    if not data.get('all_passed', False):
        issues.append("Failed tests")
    if data.get('header_issues', False):
        issues.append("Header formatting")
    
    issues_str = ", ".join(issues) if issues else "None"
    
    print(f"| {group} | {status} | {tests} | {row_count} | {nyse_count} | {nasdaq_count} | {issues_str} |")

# Check for data consistency
print("\n## Data Validation\n")

row_counts = set()
nyse_counts = set()
nasdaq_counts = set()

for result in results:
    data = result['data']
    if data.get('all_passed', False):
        endpoint_data = data.get('endpoint_data', {})
        rc = endpoint_data.get('row_count', {}).get('row_count')
        nc = endpoint_data.get('unique_nyse_stock_count', {}).get('unique_nyse_stock_count')
        nq = endpoint_data.get('unique_nasdaq_stock_count', {}).get('unique_nasdaq_stock_count')
        
        if rc is not None:
            row_counts.add(rc)
        if nc is not None:
            nyse_counts.add(nc)
        if nq is not None:
            nasdaq_counts.add(nq)

if len(row_counts) <= 1 and len(nyse_counts) <= 1 and len(nasdaq_counts) <= 1:
    print("✅ **All groups that passed returned consistent data values**")
else:
    print("⚠️ **Warning: Groups returned different values**")
    if len(row_counts) > 1:
        print(f"- Row counts vary: {sorted(row_counts)}")
    if len(nyse_counts) > 1:
        print(f"- NYSE counts vary: {sorted(nyse_counts)}")
    if len(nasdaq_counts) > 1:
        print(f"- NASDAQ counts vary: {sorted(nasdaq_counts)}")

if row_counts:
    print(f"\n**Expected Values (from passing groups):**")
    if len(row_counts) == 1:
        print(f"- Row count: {list(row_counts)[0]}")
    if len(nyse_counts) == 1:
        print(f"- NYSE unique stocks: {list(nyse_counts)[0]}")
    if len(nasdaq_counts) == 1:
        print(f"- NASDAQ unique stocks: {list(nasdaq_counts)[0]}")

PYTHON_SCRIPT

# Print summary
{
    echo ""
    echo "========================================================================"
    echo "FINAL SUMMARY"
    echo "========================================================================"
    echo "Total repositories: $total_repos"
    echo "Passed: $passed_repos"
    echo "Failed: $failed_repos"
    echo ""
    
    if [ $failed_repos -eq 0 ] && [ $total_repos -gt 0 ]; then
        echo "✓ ALL REPOSITORIES PASSED!"
    elif [ $total_repos -eq 0 ]; then
        echo "⚠ No repositories found to test"
    else
        echo "✗ $failed_repos REPOSITORY(IES) FAILED"
    fi
    
    echo ""
    echo "Detailed results saved to: $output_file"
    echo "Summary table saved to: $summary_file"
    echo ""
    echo "========================================================================"
    echo "SUMMARY TABLE"
    echo "========================================================================"
    echo ""
    cat "$summary_file"
} | tee -a "$output_file"

# Exit with failure if any repos failed
if [ $failed_repos -gt 0 ]; then
    exit 1
else
    exit 0
fi

