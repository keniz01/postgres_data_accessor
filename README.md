Simple package distribution
---------------------------
# Build package
1. uv build
# Go to the package folder and run a simple http server
2. cd dist && python -m http.server 8080
# Install package on client 
3. uv add --find-links http://localhost:8080 --index https://pypi.org/simple data_accessor
# Optional - remove installed package
4. uv remove data_accessor

Running unit tests using pytest
-------------------------------
# Run tests in a single file
uv run hatch run dev:pytest tests/test_music_query_controller.py
# Run tests in all files
uv run hatch run dev:test
