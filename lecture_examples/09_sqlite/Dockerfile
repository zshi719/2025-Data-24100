FROM astral/uv:python3.13-bookworm
WORKDIR /app

# Put the pyproject.toml & print_date.py file into the container
COPY pyproject.toml .

RUN apt-get update
RUN apt-get install -y sqlite3
# Create a virtual environment and set the location to /app/.venv
RUN uv venv
RUN uv sync

ENV PYTHONUNBUFFERED=1
CMD [ "uv", "run", "jupyter", "notebook", "--allow-root", "--no-browser", "--ip=0.0.0.0" ]