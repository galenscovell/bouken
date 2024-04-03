# Bouken

[<img src="https://github.com/galenscovell/bouken/blob/master/bouken.png" width="500"/>](bouken.png)

### Description

Bouken is (currently) an exterior hexagon map generator that takes into account many features such as humidity, elevation, and landforms to create biomes. Eventually I hope to turn this into an interactive game where the user will control a small party of adventurers across a randomly generated world, complete with creatures, traps, and other events. The idea is for it to play like a simplified version of DND mixed with a boardgame.

[<img src="https://github.com/galenscovell/bouken/blob/master/generation.gif" width="500"/>](generation.gif)
[<img src="https://github.com/galenscovell/bouken/blob/master/hires-sample.gif" width="500"/>](hires-sample.gif)
[<img src="https://github.com/galenscovell/bouken/blob/master/lores-sample.gif" width="500"/>](lores-sample.gif)
[<img src="https://github.com/galenscovell/bouken/blob/master/design/parameters.png" width="500"/>](parameters.png)

### Usage

1. Launch Backend and Frontend as described below
2. Modify parameters using the Frontend UI at http://localhost:8080 and click Generate
3. Map will generate in realtime in a new window. This is technically debug rendering for troubleshooting, but it looks neat! It will also display additional debug details.
4. When the window is closed, the complete map (without debug info) will automatically save to `/backend/debug_output` as a jpg image.

### Running Backend

All operations performed in `backend` directory.
1. `python -m venv .venv` to create virtual env (if not already done)
2. `.venv/Scripts/activate` to activate venv (`deactivate` to deactivate)
3. `pip install -r requirements.txt` (if not already done)
4. Run: `uvicorn api_main:app --host 0.0.0.0 --port 5050 --reload`
5. Access documentation at either http://localhost:5050/docs (Swagger) or http://localhost:5050/redoc (Redoc)
6. Access service at http://localhost:5050

### Running Frontend

All operations performed in `frontend` directory.
1. Build: `npm install`
2. Run: `npm run dev`
3. Access site at http://localhost:8080

### Design

[<img src="https://github.com/galenscovell/bouken/blob/master/design/MVP_1_main.png" width="500"/>](MVP_1_main.png)
[<img src="https://github.com/galenscovell/bouken/blob/master/design/MVP_2_generating.png" width="500"/>](MVP_2_generating.png)
[<img src="https://github.com/galenscovell/bouken/blob/master/design/MVP_3_generated.png" width="500"/>](MVP_3_generated.png)

### Issues

* The process sometimes gets stuck when placing lakes. It never freezes entirely, but it can sit at this step for quite awhile (minutes, if pixel width is large, hex size is small and map conditions are just right). Will need to figure out a more performant way to handle that logic.
