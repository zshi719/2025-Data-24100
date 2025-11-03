#!/bin/bash

# Parse command line arguments
SINGLE_GROUP=""
INDIVIDUAL_FILES=false
while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--group)
            SINGLE_GROUP="$2"
            shift 2
            ;;
        -i|--individual)
            INDIVIDUAL_FILES=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [-g|--group GROUP_NUMBER] [-i|--individual]"
            echo ""
            echo "Options:"
            echo "  -g, --group NUMBER    Test only a specific group (e.g., -g 1 for Group-1)"
            echo "  -i, --individual      Generate individual output files per group"
            echo "  -h, --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Test all groups, single output file"
            echo "  $0 -g 1              # Test only Group-1"
            echo "  $0 --group 3         # Test only Group-3"
            echo "  $0 -i                # Test all groups, individual files per group"
            echo "  $0 -g 1 -i           # Test Group-1, individual file"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Output file
output_file="part_3_autograder_output.txt"
summary_file="part_3_summary.md"

# API key for testing
API_KEY="${DATA_241_API_KEY:-test_grading_key_2024}"

# RAW_DATA_DIR - location of ZIP files on host machine
# Default location for grading data
RAW_DATA_DIR="/Users/nickross/data_grading/project_data"

# Port for Flask
FLASK_PORT=4000

# Create temp directory for JSON results
results_dir=$(mktemp -d)
trap "rm -rf $results_dir" EXIT

# Clear the output files if they exist (only if not using individual files)
if [ "$INDIVIDUAL_FILES" = false ]; then
    > "$output_file"
    > "$summary_file"
fi

# Function to wait for Flask to be ready
wait_for_flask() {
    local max_wait=60
    local wait_count=0
    
    # Try both v1 and v2 endpoints to check if Flask is ready
    while ! curl -s http://localhost:${FLASK_PORT}/api/v1/row_count >/dev/null 2>&1 && \
          ! curl -s http://localhost:${FLASK_PORT}/api/v2/2019 >/dev/null 2>&1; do
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
    
    # Determine output file for this group
    local group_output_file
    if [ "$INDIVIDUAL_FILES" = true ]; then
        group_output_file="part_3_${repo_name}_output.txt"
        > "$group_output_file"  # Clear individual file
    else
        group_output_file="$output_file"
    fi

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

        # Check that ZIP files are NOT in the repository
        repo_zip_count=$(find . -name "*.zip" -not -path "*/.venv/*" -not -path "*/site-packages/*" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$repo_zip_count" -gt 0 ]; then
            echo "⚠ WARNING: Found $repo_zip_count ZIP file(s) in repository (should be stored externally)"
            echo "  ZIP files found:"
            find . -name "*.zip" -not -path "*/.venv/*" -not -path "*/site-packages/*" 2>/dev/null | head -5
        else
            echo "✓ No ZIP files found in repository (correct)"
        fi

        # Verify RAW_DATA_DIR exists and has ZIP files
        if [ ! -d "$RAW_DATA_DIR" ]; then
            echo "⚠ Warning: RAW_DATA_DIR ($RAW_DATA_DIR) does not exist"
        else
            zip_count=$(find "$RAW_DATA_DIR" -name "*.zip" 2>/dev/null | wc -l | tr -d ' ')
            if [ "$zip_count" -eq 0 ]; then
                echo "⚠ Warning: No ZIP files found in RAW_DATA_DIR ($RAW_DATA_DIR)"
            else
                echo "✓ Found $zip_count ZIP file(s) in RAW_DATA_DIR"
            fi
        fi
        
        # Start Flask server in background
        echo "Starting Flask server for $repo_name..."
        export DATA_241_API_KEY="$API_KEY"
        export RAW_DATA_DIR="$RAW_DATA_DIR"
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
            
            # Run the autograder for both v1 and v2 APIs (regular output for logs)
            echo ""
            echo "--- Running autograder for $repo_name (v1 and v2 APIs) ---"
            python3 ../flask_autograder.py \
                --api v1 \
                --api v2 \
                --key "$API_KEY" \
                --url "http://localhost:${FLASK_PORT}"
            
            AUTOGRADER_EXIT_CODE=$?
            
            # Also capture JSON results for summary (run again in JSON mode)
            python3 ../flask_autograder.py \
                --api v1 \
                --api v2 \
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

    } 2>&1 | tee -a "$group_output_file"

    # Capture the exit code from the pipe
    local exit_code=${PIPESTATUS[0]}

    # If using individual files, also append to combined file and inform where output was saved
    if [ "$INDIVIDUAL_FILES" = true ]; then
        cat "$group_output_file" >> "$output_file"
        echo ""
        echo "✓ Output for $repo_name saved to: $group_output_file"
    fi

    return $exit_code
}

# Main script
if [ -n "$SINGLE_GROUP" ]; then
    echo "Starting Part 3 autograder process for Group-${SINGLE_GROUP}" | tee -a "$output_file"
else
    echo "Starting Part 3 autograder process for all repositories" | tee -a "$output_file"
fi
echo "Using API key: $API_KEY" | tee -a "$output_file"
echo "Using RAW_DATA_DIR: $RAW_DATA_DIR" | tee -a "$output_file"
echo "" | tee -a "$output_file"

# Track results
total_repos=0
passed_repos=0
failed_repos=0

# Determine which groups to test
if [ -n "$SINGLE_GROUP" ]; then
    # Test only the specified group
    repo_name="2025-Data-24100-Group-${SINGLE_GROUP}"
    if [ ! -d "$repo_name" ]; then
        echo "✗ ERROR: Directory $repo_name does not exist" | tee -a "$output_file"
        exit 1
    fi

    total_repos=1
    if process_repo "$repo_name"; then
        passed_repos=1
    else
        failed_repos=1
    fi
else
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
fi

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
    print("# Part 3 Summary\n\nNo results found.")
    sys.exit(0)

# Print markdown table
print("# Part 3 Autograder Summary\n")
print("## Overall Results\n")
print("| Group | Status | Tests Passed | V1 Status | V2 Status | Issues |")
print("|-------|--------|--------------|-----------|-----------|--------|")

for result in results:
    group = result['group']
    data = result['data']
    
    status = "✅ PASS" if data.get('all_passed', False) else "❌ FAIL"
    tests = f"{data.get('passed', 0)}/{data.get('total_tests', 0)}"
    
    # Try to determine v1 and v2 status from endpoint_data
    # We'll check if v1 endpoints exist vs v2 endpoints
    endpoint_data = data.get('endpoint_data', {})
    v1_passed = any(key in endpoint_data for key in ['row_count', 'unique_nyse_stock_count', 'unique_nasdaq_stock_count'])
    v2_passed = any(key.startswith('v2_') for key in endpoint_data.keys())
    
    # More accurate: check if we have year endpoints or price endpoints
    v2_passed = any(key.startswith('v2_year_') or key.startswith('v2_open_') or 
                    key.startswith('v2_close_') or key.startswith('v2_high_') or 
                    key.startswith('v2_low_') or key.startswith('v2_high_low_') 
                    for key in endpoint_data.keys())
    
    v1_status = "✓" if v1_passed else "✗"
    v2_status = "✓" if v2_passed else "✗"
    
    issues = []
    if not data.get('all_passed', False):
        issues.append("Failed tests")
    if data.get('header_issues', False):
        issues.append("Header formatting")
    
    issues_str = ", ".join(issues) if issues else "None"
    
    print(f"| {group} | {status} | {tests} | {v1_status} | {v2_status} | {issues_str} |")

# Check for data consistency
print("\n## Data Validation\n")

# Check v1 endpoint consistency (from Part 2)
row_counts = set()
nyse_counts = set()
nasdaq_counts = set()

# Check v2 endpoint consistency
v2_year_counts = {}  # year -> set of counts

for result in results:
    data = result['data']
    if data.get('all_passed', False):
        endpoint_data = data.get('endpoint_data', {})
        
        # V1 data
        rc = endpoint_data.get('row_count', {}).get('row_count')
        nc = endpoint_data.get('unique_nyse_stock_count', {}).get('unique_nyse_stock_count')
        nq = endpoint_data.get('unique_nasdaq_stock_count', {}).get('unique_nasdaq_stock_count')
        
        if rc is not None:
            row_counts.add(rc)
        if nc is not None:
            nyse_counts.add(nc)
        if nq is not None:
            nasdaq_counts.add(nq)
        
        # V2 data - collect year counts
        for key, value in endpoint_data.items():
            if key.startswith('v2_year_'):
                year = key.replace('v2_year_', '')
                if isinstance(value, dict) and 'count' in value:
                    if year not in v2_year_counts:
                        v2_year_counts[year] = set()
                    v2_year_counts[year].add(value['count'])

v1_consistent = len(row_counts) <= 1 and len(nyse_counts) <= 1 and len(nasdaq_counts) <= 1
v2_consistent = all(len(counts) <= 1 for counts in v2_year_counts.values())

if v1_consistent and v2_consistent:
    print("✅ **All groups that passed returned consistent data values**")
else:
    print("⚠️ **Warning: Groups returned different values**")
    if not v1_consistent:
        if len(row_counts) > 1:
            print(f"- Row counts vary: {sorted(row_counts)}")
        if len(nyse_counts) > 1:
            print(f"- NYSE counts vary: {sorted(nyse_counts)}")
        if len(nasdaq_counts) > 1:
            print(f"- NASDAQ counts vary: {sorted(nasdaq_counts)}")
    if not v2_consistent:
        for year, counts in v2_year_counts.items():
            if len(counts) > 1:
                print(f"- Year {year} counts vary: {sorted(counts)}")

if row_counts:
    print(f"\n**Expected Values (from passing groups):**")
    if len(row_counts) == 1:
        print(f"- Row count (v1): {list(row_counts)[0]}")
    if len(nyse_counts) == 1:
        print(f"- NYSE unique stocks (v1): {list(nyse_counts)[0]}")
    if len(nasdaq_counts) == 1:
        print(f"- NASDAQ unique stocks (v1): {list(nasdaq_counts)[0]}")
    
    if v2_year_counts:
        print(f"\n**V2 Year Counts (from passing groups):**")
        for year in sorted(v2_year_counts.keys()):
            counts = v2_year_counts[year]
            if len(counts) == 1:
                print(f"- Year {year}: {list(counts)[0]} rows")

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

