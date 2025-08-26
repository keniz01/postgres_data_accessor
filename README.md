1) Generate wheel.
Run `uv build` to generate wheel.
The files will be generate in the dist folder

Use pypi-server to distribute data_accessor by following the steps here:
1) uv pip install pypiserver
2) cd to dist and pypi-server run -p 8000 dist
3) uv pip install --index-url http://localhost:8000 --trusted-host localhost hello-package

pytests
uv run hatch run dev:pytest tests/test_music_query_controller.py
uv run pytest tests/test_music_query_controller.py
