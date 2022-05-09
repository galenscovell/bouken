# Bouken

### Description

Bouken is (currently) an exterior and interior map generator that takes into account many features such as humidity, elevation, and landforms to create biomes and rooms. Eventually I hope to turn this into an interactive game where the user will control a small party of adventurers across a randomly generated world, complete with events, creatures, traps, and other exciting experiences. The idea is for it to play like a simplified version of DND mixed with a boardgame.

### Running Backend

All operations performed in `backend` directory.
1. `python -m venv .venv` to create virtual env (if not already done)
2. `.venv/Scripts/activate` to activate venv (`deactivate` to deactivate)
3. `pip install -r requirements.txt` (if not already done)
4. Run: `uvicorn api_main:app --host 0.0.0.0 --port 5050 --reload`
5. Access documentation at either http://localhost:5050/docs (Swagger) or http://localhost:5050/redoc (Redoc)
6. Access service at http://localhost:5050

### Running Backend (Docker)

All operations performed in `backend` directory.
1. (Optional) Prune old builds: `docker image prune`
2. Build: `docker build -t bouken:latest .`
3. Run: `docker run -it --rm -p 5050:5050 bouken`
4. Access documentation at either http://localhost:5050/docs (Swagger) or http://localhost:5050/redoc (Redoc)
5. Access service at http://localhost:5050

### Running Frontend

All operations performed in `frontend` directory.
1. Build: `npm install`
2. Run: `npm run dev`
3. Access site at http://localhost:8080

### Running Frontend (Docker)

All operations performed in `frontend` directory.
1. (Optional) Prune old builds: `docker image prune`
2. Build: ``
3. Run: ``
4. Access site at http://localhost:8080