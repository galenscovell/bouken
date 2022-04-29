# Bouken

### Description

Bouken is (currently) an exterior and interior map generator that takes into account many features such as humidity, elevation, and landforms to create biomes and rooms. Eventually I hope to turn this into an interactive game where the user will control a small party of adventurers across a randomly generated world, complete with events, creatures, traps, and other exciting experiences. The idea is for it to play like a simplified version of DND mixed with a boardgame.

### Running Backend (Docker)

0. (Optional) Prune old builds: `docker image prune`
1. Build: `docker build -t bouken:latest .` in backend dir
2. Run: `docker run -it --rm -p 8080:8080 bouken`
3. Access documentation at either http://localhost:8080/docs (Swagger) or http://localhost:8080/redoc (Redoc)
4. Hit the service at http://localhost:8080

### Running Frontend (Docker)