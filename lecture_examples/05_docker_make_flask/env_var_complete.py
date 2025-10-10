import os

if __name__ == "__main__":
    container_api_key = os.environ.get("API_KEY_IN_CONTAINER", None)
    if not container_api_key:
        raise KeyError("API key not found")

    print(f"API key found: {container_api_key}")