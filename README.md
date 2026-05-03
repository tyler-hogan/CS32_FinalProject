# CS32 Final Project – City Ranker

A command-line tool that helps recent graduates decide which U.S. city to move to after college, taking into account career field, cost of living, and—most importantly—where their friends are planning to go.

---

## What This Project Does

City Ranker collects three preference scores from the user (proximity to friends/family, career opportunity, and cost of living), then applies a weighted formula across a hand-curated database of 10 major U.S. cities to produce a ranked list and a detailed breakdown of the top pick.

The **multi-client feature** is the core learning objective: multiple users can each run `client.py` at the same time against a shared `server.py`.  After every user submits their top city, the server broadcasts all results back.  Each client then re-runs the ranking with a **+1 proximity bonus** applied to any city already chosen by a friend, nudging the algorithm toward cities where the user's social network is forming.

---

## File Structure

| File | Purpose |
|------|---------|
| `rank_cities.py` | Standalone version – full ranking logic with no networking |
| `server.py` | Multi-client TCP server – collects and broadcasts user results |
| `client.py` | Network client – runs ranking, shares result, re-ranks with friend data |
| `README.md` | This file |

---

## How to Run

### Standalone (no networking)

```
python3 rank_cities.py
```

Answer the prompts and your ranked city list will be printed immediately.

### Multi-client mode (with friend-location feature)

**Terminal 1 – start the server first:**

```
python3 server.py
```

**Terminal 2+ – each friend runs the client in their own terminal:**

```
python3 client.py
```

Each person answers the questionnaire.  Once connected to the server, they will see a leaderboard of every friend's top city and then be shown a re-ranked list that gives a proximity bonus to the cities their friends chose.

> **Note:** All terminals must run on the same machine (localhost) unless you change `HOST` in both `server.py` and `client.py` to a shared IP address.  The server must be started before any clients connect.

---

## Requirements

- Python 3.8 or later
- No external packages required (uses `socket`, `threading`, and `json` from the standard library)

---

## Attribution

- City data (job counts, average rent, notable firms, descriptions) was researched and compiled manually using publicly available sources including U.S. Bureau of Labor Statistics data and cost-of-living indices.
- Socket programming patterns referenced from the Python 3 standard library documentation: https://docs.python.org/3/library/socket.html
- Claude (Anthropic) was used as a GAI assistant to help write the server/client networking code, add inline comments, implement the friend-city proximity bonus feature, and update this README.
