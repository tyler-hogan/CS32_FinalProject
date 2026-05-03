import socket
import json
import sys

# ─── Network configuration (must match server.py) ─────────────────────────────
HOST = "127.0.0.1"
PORT = 65432

# ─── Validation helper ────────────────────────────────────────────────────────
def get_valid_input(prompt, min_val, max_val):
    """Prompt the user until they enter an integer in [min_val, max_val]."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# ─── Core ranking logic ───────────────────────────────────────────────────────
def run_ranking(friend_cities=None):
    """Run the interactive city ranking questionnaire and return the top result.

    Parameters
    ----------
    friend_cities : list[str] or None
        Cities already chosen by friends (received from the server on a
        previous pass).  Each city in this list receives a +1 proximity bonus
        applied to its raw proximity_score before weighting, encouraging the
        user to consider living near their friends.

    Returns
    -------
    tuple : (username, top_city, top_score, career_label)
    """
    # ── City database ─────────────────────────────────────────────────────────
    # Each entry stores raw scores (out of 10), metadata, and a short blurb.
    # proximity_score  – how good the city is for meeting/living near people
    # career_score     – job market strength for the chosen career field
    # cost_score       – affordability (10 = cheapest)
    city_data_set = {
        "New York, NY": {
            "proximity_score": 9,
            "career_score":    9,
            "cost_score":      2,
            "avg_rent":        3800,
            "career_jobs":     "~350,000 finance jobs",
            "notable_firms":   "Goldman Sachs, JPMorgan, Blackstone, Citadel",
            "description":     "The undisputed global finance capital. Extremely high cost of living.",
        },
        "San Francisco, CA": {
            "proximity_score": 7,
            "career_score":    10,
            "cost_score":      1,
            "avg_rent":        3500,
            "career_jobs":     "~200,000 tech jobs",
            "notable_firms":   "Google, Meta, Salesforce, Stripe",
            "description":     "Premier tech hub. Very high cost but unmatched tech opportunities.",
        },
        "Chicago, IL": {
            "proximity_score": 8,
            "career_score":    7,
            "cost_score":      6,
            "avg_rent":        2200,
            "career_jobs":     "~120,000 finance/tech jobs",
            "notable_firms":   "United Airlines, Boeing, Morningstar",
            "description":     "Midwest powerhouse with strong finance and trading scene.",
        },
        "Austin, TX": {
            "proximity_score": 8,
            "career_score":    8,
            "cost_score":      7,
            "avg_rent":        1900,
            "career_jobs":     "~80,000 tech jobs",
            "notable_firms":   "Dell, Apple (campus), Tesla (HQ)",
            "description":     "Fast-growing tech hub with no state income tax.",
        },
        "Boston, MA": {
            "proximity_score": 7,
            "career_score":    8,
            "cost_score":      4,
            "avg_rent":        3100,
            "career_jobs":     "~90,000 biotech/finance jobs",
            "notable_firms":   "Fidelity, State Street, Biogen, HubSpot",
            "description":     "Top-tier education and biotech corridor. Cold winters.",
        },
        "Seattle, WA": {
            "proximity_score": 6,
            "career_score":    9,
            "cost_score":      4,
            "avg_rent":        2400,
            "career_jobs":     "~100,000 tech jobs",
            "notable_firms":   "Amazon, Microsoft, Boeing",
            "description":     "Pacific Northwest tech giant. Rainy but vibrant culture.",
        },
        "Los Angeles, CA": {
            "proximity_score": 7,
            "career_score":    7,
            "cost_score":      3,
            "avg_rent":        2900,
            "career_jobs":     "~150,000 entertainment/tech jobs",
            "notable_firms":   "Netflix, Snap, SpaceX, Disney",
            "description":     "Entertainment and media capital with growing tech scene.",
        },
        "Atlanta, GA": {
            "proximity_score": 7,
            "career_score":    6,
            "cost_score":      8,
            "avg_rent":        1800,
            "career_jobs":     "~50,000 finance jobs",
            "notable_firms":   "NCR, Equifax, Intercontinental Exchange (ICE)",
            "description":     "Major financial technology hub and fast-growing market. Affordable with a strong Delta hub.",
        },
        "Miami, FL": {
            "proximity_score": 7,
            "career_score":    6,
            "cost_score":      5,
            "avg_rent":        2800,
            "career_jobs":     "~50,000 finance jobs",
            "notable_firms":   "Citadel (relocating HQ), Blackstone regional, BankUnited",
            "description":     "Rapidly emerging as a finance hub with no state income tax and an international network.",
        },
        "Denver, CO": {
            "proximity_score": 6,
            "career_score":    6,
            "cost_score":      6,
            "avg_rent":        2100,
            "career_jobs":     "~40,000 tech/energy jobs",
            "notable_firms":   "Lockheed Martin, Arrow Electronics, DaVita",
            "description":     "Outdoorsy lifestyle with a growing tech scene and lower cost than coastal cities.",
        },
    }

    # Career field options presented to the user
    career_options = {
        1: ("finance",        "Finance / Banking"),
        2: ("tech",           "Tech / Software"),
        3: ("consulting",     "Consulting / Strategy"),
        4: ("healthcare",     "Healthcare / Biotech"),
        5: ("entertainment",  "Entertainment / Media"),
    }

    # ── Step 1: Collect user preferences ─────────────────────────────────────
    print("\n" + "=" * 60)
    print("   CITY RANKER – Find Your Best City")
    print("=" * 60)

    username = input("\nEnter your name: ").strip() or "Anonymous"

    print("\nWhat career field are you interested in?")
    for num, (_, label) in career_options.items():
        print(f"  {num}. {label}")
    career_choice   = get_valid_input("Choose (1-5): ", 1, 5)
    career_key, career_label = career_options[career_choice]

    print("\nHow important is being close to friends/family? (1 = not at all, 10 = very important)")
    proximity_weight = get_valid_input("Proximity importance (1-10): ", 1, 10)

    print("\nHow important is career opportunity? (1-10)")
    career_weight = get_valid_input("Career importance (1-10): ", 1, 10)

    print("\nHow important is low cost of living? (1-10)")
    cost_weight = get_valid_input("Cost importance (1-10): ", 1, 10)

    # ── Step 2: Apply friend-city proximity bonus ──────────────────────────────
    # If friends have already submitted their top cities (received from the
    # server), boost the proximity_score of each friend's city by +1 (capped at
    # 10).  This nudges the algorithm toward cities where the user's social
    # network is already forming, satisfying the multi-client friend-location
    # feature described in the project spec.
    if friend_cities:
        print("\n[FRIEND BONUS] Applying +1 proximity boost to friend cities:")
        for city in friend_cities:
            if city in city_data_set:
                old_score = city_data_set[city]["proximity_score"]
                city_data_set[city]["proximity_score"] = min(10, old_score + 1)
                print(f"  {city}: proximity {old_score} -> {city_data_set[city]['proximity_score']}")

    # ── Step 3: Score every city ──────────────────────────────────────────────
    # Weighted formula:  total = (prox * prox_w + career * career_w + cost * cost_w)
    #                            / (prox_w + career_w + cost_w)  * 10
    total_weight = proximity_weight + career_weight + cost_weight

    scored = []
    for city_name, data in city_data_set.items():
        # Use career_score directly (all career fields share the same score in
        # this dataset – a future extension could add per-field scores).
        weighted_score = (
            (data["proximity_score"] * proximity_weight +
             data["career_score"]    * career_weight    +
             data["cost_score"]      * cost_weight)
            / total_weight * 10
        )
        scored.append((round(weighted_score, 1), city_name))

    # ── Step 4: Sort descending and display ranked list ───────────────────────
    results = sorted(scored, reverse=True)

    print("\n" + "=" * 60)
    print(f"  YOUR CITY RANKINGS  (career: {career_label})")
    print("=" * 60)

    def display_city(rank, city_name, score, data, career_lbl):
        """Print a single ranked city entry."""
        print(f"  #{rank:<3} {city_name:<25} Score: {score}/100"
              f"   |  {career_lbl} jobs: {data['career_jobs']}")

    for rank, (score, city_name) in enumerate(results, start=1):
        display_city(rank, city_name, score, city_data_set[city_name], career_label)

    # ── Step 5: Show detailed breakdown for the top pick ─────────────────────
    best_score, best_city = results[0]
    top = city_data_set[best_city]

    print("\n" + "=" * 60)
    print(f"  BEST MATCH: {best_city}  ({best_score}/100)")
    print("=" * 60)
    print(f"\n  Score breakdown for {best_city}:")
    print(f"    Proximity : {top['proximity_score']}/10  x weight {proximity_weight}")
    print(f"    {career_label:<9} : {top['career_score']}/10  x weight {career_weight}")
    print(f"    Cost       : {top['cost_score']}/10  x weight {cost_weight}")
    print(f"\n  Weighted total: {best_score}/100")
    print(f"\n  {top['description']}\n")

    return username, best_city, best_score, career_label


# ─── Main entry point ─────────────────────────────────────────────────────────
def main():
    """Run ranking, connect to the server, share results, and display friends."""

    # ── Pass 1: Run ranking without friend data (no server contact yet) ───────
    username, top_city, top_score, career = run_ranking(friend_cities=None)

    # ── Build the payload to send to the server ───────────────────────────────
    payload = {
        "username":  username,
        "top_city":  top_city,
        "top_score": top_score,
        "career":    career,
    }

    # ── Connect to the server, send result, receive all friends' results ──────
    print(f"\nConnecting to server at {HOST}:{PORT} to share your result...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # Send this client's result as a newline-terminated JSON string
            s.sendall((json.dumps(payload) + "\n").encode())

            # Wait to receive the broadcast of all results (including ours)
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in data:
                    break

        # ── Parse the broadcast and collect friend cities ─────────────────────
        all_results = json.loads(data.decode().strip())

        # Identify cities chosen by *other* users (not this one)
        friend_cities = [
            r["top_city"]
            for r in all_results
            if r["username"] != username
        ]

        # ── Display the full leaderboard of friend results ────────────────────
        print("\n" + "=" * 60)
        print("  FRIEND RESULTS (from server)")
        print("=" * 60)
        for r in all_results:
            tag = " <-- YOU" if r["username"] == username and r["top_city"] == top_city else ""
            print(f"  {r['username']:<20} top city: {r['top_city']} ({r['top_score']}/100, {r['career']}){tag}")
        print()

        # ── Pass 2: Re-run ranking with friend-city bonus if friends exist ─────
        if friend_cities:
            print("=" * 60)
            print("  RE-RANKING WITH FRIEND PROXIMITY BONUS")
            print("=" * 60)
            print(f"  Your friends chose: {', '.join(set(friend_cities))}")
            print("  Re-running ranking with +1 proximity boost for those cities...\n")
            run_ranking(friend_cities=friend_cities)

    except ConnectionRefusedError:
        print(f"  [ERROR] Could not connect to server. Make sure server.py is running on {HOST}:{PORT}.")
    except Exception as e:
        print(f"  [ERROR] {e}")


if __name__ == "__main__":
    main()
