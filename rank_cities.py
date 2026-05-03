# ============================================================
#  City Ranker - CS32 Final Project
#  Ranks cities: proximity to loved ones,
#  career (Finance OR Tech track), and cost of living.
# ============================================================

# ------------------------------------------------------------------
# FINANCE CITY DATA  (scores out of 10)
#   proximity_score : airport connectivity / how easy to visit family
#   career_score    : strength of local finance job market
#   cost_score      : affordability (10 = very cheap, 1 = very expensive)
# ------------------------------------------------------------------
finance_cities = {
    "New York, NY": {
        "proximity_score": 10,   # biggest US hub, flights everywhere
        "career_score":    10,   # #1 finance capital in the world
        "cost_score":       1,   # extremely expensive
        "avg_rent":      4500,
        "career_jobs":   "~330,000 finance jobs",
        "notable_firms": "Goldman Sachs, JPMorgan, Blackstone, Citi",
        "description":   "The global capital of finance. Unmatched career ceiling but the highest cost of living in the US."
    },
    "Chicago, IL": {
        "proximity_score": 8,
        "career_score":    8,
        "cost_score":      5,
        "avg_rent":      2000,
        "career_jobs":   "~110,000 finance jobs",
        "notable_firms": "CME Group, Morningstar, Citadel, Nuveen",
        "description":   "A top-tier finance hub with strong derivatives and trading culture. Much cheaper than NYC."
    },
    "San Francisco, CA": {
        "proximity_score": 6,
        "career_score":    8,
        "cost_score":      1,
        "avg_rent":      3800,
        "career_jobs":   "~85,000 finance jobs (heavy fintech/VC)",
        "notable_firms": "Visa, Wells Fargo, Salesforce, Charles Schwab",
        "description":   "Dominant in fintech and venture capital. Very expensive and geographically isolated."
    },
    "Boston, MA": {
        "proximity_score": 8,
        "career_score":    8,
        "cost_score":      4,
        "avg_rent":      3100,
        "career_jobs":   "~90,000 finance jobs",
        "notable_firms": "Fidelity, State Street, Liberty Mutual, Putnam",
        "description":   "World-class asset management scene. Expensive but strong network through elite universities."
    },
    "Charlotte, NC": {
        "proximity_score": 6,
        "career_score":    7,
        "cost_score":      7,
        "avg_rent":      1700,
        "career_jobs":   "~55,000 finance jobs",
        "notable_firms": "Bank of America HQ, Truist, LendingTree",
        "description":   "The #2 US banking city by assets. Lower cost of living with surprising career upside."
    },
    "Dallas, TX": {
        "proximity_score": 7,
        "career_score":    7,
        "cost_score":      7,
        "avg_rent":      1600,
        "career_jobs":   "~75,000 finance jobs",
        "notable_firms": "AT&T, ExxonMobil treasury, Goldman (regional), Comerica",
        "description":   "Fast-growing finance scene, no state income tax, affordable living, and a major airport hub."
    },
    "Miami, FL": {
        "proximity_score": 7,
        "career_score":    6,
        "cost_score":      5,
        "avg_rent":      2800,
        "career_jobs":   "~50,000 finance jobs",
        "notable_firms": "Citadel (relocating HQ), Blackstone regional, BankUnited",
        "description":   "Rapidly emerging as a finance hub with no state income tax and an international network."
    },
    "Denver, CO": {
        "proximity_score": 6,
        "career_score":    6,
        "cost_score":      6,
        "avg_rent":      1900,
        "career_jobs":   "~40,000 finance jobs",
        "notable_firms": "Charles Schwab HQ, USAA regional, Oppenheimer Funds",
        "description":   "Growing wealth management sector. Great quality of life and outdoor access at moderate cost."
    },
    "Atlanta, GA": {
        "proximity_score": 7,
        "career_score":    6,
        "cost_score":      7,
        "avg_rent":      1800,
        "career_jobs":   "~60,000 finance jobs",
        "notable_firms": "NCR, Equifax, Intercontinental Exchange (ICE)",
        "description":   "Major financial technology hub and fast-growing market. Affordable with a strong Delta hub."
    },
    "Seattle, WA": {
        "proximity_score": 5,
        "career_score":    6,
        "cost_score":      4,
        "avg_rent":      2400,
        "career_jobs":   "~35,000 finance jobs",
        "notable_firms": "Amazon Finance, Russell Investments, Washington Mutual alumni",
        "description":   "Mostly tech-driven but growing in fintech. No state income tax but high cost of living."
    },
}

# ------------------------------------------------------------------
# TECH CITY DATA  (same three scores, now through a tech lens)
# ------------------------------------------------------------------
tech_cities = {
    "San Francisco, CA": {
        "proximity_score": 6,
        "career_score":    10,   # #1 tech market in the world
        "cost_score":       1,   # brutally expensive
        "avg_rent":       3800,
        "career_jobs":    "~450,000 tech jobs",
        "notable_firms":  "Apple, Google, Meta, Salesforce, OpenAI",
        "description":    "The undisputed world capital of tech. Unrivaled job density and salaries, but brutally expensive."
    },
    "Seattle, WA": {
        "proximity_score": 5,
        "career_score":    10,   # Amazon + Microsoft anchor
        "cost_score":       3,
        "avg_rent":       2400,
        "career_jobs":    "~290,000 tech jobs",
        "notable_firms":  "Amazon HQ, Microsoft HQ, Boeing tech, Expedia",
        "description":    "A true tech powerhouse. No state income tax offsets the high rent. Amazon and Microsoft dominate."
    },
    "Austin, TX": {
        "proximity_score": 6,
        "career_score":    8,
        "cost_score":       6,
        "avg_rent":       1900,
        "career_jobs":    "~175,000 tech jobs",
        "notable_firms":  "Tesla HQ, Apple campus, Dell HQ, Oracle HQ",
        "description":    "The fastest-growing US tech hub. No state income tax, lower cost, and a booming startup scene."
    },
    "New York, NY": {
        "proximity_score": 10,
        "career_score":    8,
        "cost_score":       1,
        "avg_rent":       4500,
        "career_jobs":    "~350,000 tech jobs",
        "notable_firms":  "Google NYC, Amazon NYC, IBM, Spotify, Palantir",
        "description":    "Massive tech presence second only to SF. Best connectivity in the US, but very expensive."
    },
    "Boston, MA": {
        "proximity_score": 8,
        "career_score":    8,
        "cost_score":       4,
        "avg_rent":       3100,
        "career_jobs":    "~170,000 tech jobs",
        "notable_firms":  "MIT spinoffs, HubSpot, Wayfair, Rapid7, PTC",
        "description":    "Elite biotech and software scene fueled by world-class universities. Expensive but intellectually rich."
    },
    "Denver, CO": {
        "proximity_score": 6,
        "career_score":    7,
        "cost_score":       6,
        "avg_rent":       1900,
        "career_jobs":    "~120,000 tech jobs",
        "notable_firms":  "Palantir HQ, Arrow Electronics, Ibotta, Ping Identity",
        "description":    "A rising tech hub with outdoor lifestyle appeal. Good balance of salaries and cost of living."
    },
    "Chicago, IL": {
        "proximity_score": 8,
        "career_score":    7,
        "cost_score":       5,
        "avg_rent":       2000,
        "career_jobs":    "~135,000 tech jobs",
        "notable_firms":  "Motorola, Groupon, Grubhub, Braintree, Uptake",
        "description":    "Large and growing tech sector, especially in enterprise software and fintech. Central hub city."
    },
    "Dallas, TX": {
        "proximity_score": 7,
        "career_score":    7,
        "cost_score":       7,
        "avg_rent":       1600,
        "career_jobs":    "~140,000 tech jobs",
        "notable_firms":  "AT&T HQ, Texas Instruments HQ, Match Group, Dialexa",
        "description":    "Fast-growing tech sector with no state income tax and very affordable living. Great DFW airport hub."
    },
    "Raleigh, NC": {
        "proximity_score": 5,
        "career_score":    7,
        "cost_score":       8,   # best affordability in the list
        "avg_rent":       1500,
        "career_jobs":    "~90,000 tech jobs (Research Triangle)",
        "notable_firms":  "Cisco, IBM, Red Hat, SAS Institute HQ",
        "description":    "The Research Triangle offers strong tech jobs at a fraction of coastal costs. Underrated gem."
    },
    "Atlanta, GA": {
        "proximity_score": 7,
        "career_score":    6,
        "cost_score":       7,
        "avg_rent":       1800,
        "career_jobs":    "~100,000 tech jobs",
        "notable_firms":  "NCR, Cox Enterprises, Mailchimp, Global Payments",
        "description":    "Major fintech and cloud hub in the South. Affordable, diverse, and a top-tier airport for travel."
    },
}


# ------------------------------------------------------------------
# SCORING FUNCTION
# Multiplies each city score by the user weight, then normalizes
# to a 0-100 scale so results are always easy to compare.
# ------------------------------------------------------------------
def calculate_score(city_data, proximity_weight, career_weight, cost_weight):
    raw_score = (
        city_data["proximity_score"] * proximity_weight +
        city_data["career_score"]    * career_weight    +
        city_data["cost_score"]      * cost_weight
    )
    # max_possible: every category gets a perfect 10
    max_possible = 10 * (proximity_weight + career_weight + cost_weight)
    return round((raw_score / max_possible) * 100, 1)


# ------------------------------------------------------------------
# INPUT HELPER
# Keeps prompting until the user enters a valid integer in range.
# The try/except stops the program from crashing on typos.
# ------------------------------------------------------------------
def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# ------------------------------------------------------------------
# DISPLAY HELPER
# Prints a formatted card for one ranked city including an ASCII
# progress bar, rent, job count, firms, and a plain-English blurb.
# ------------------------------------------------------------------
def display_city(rank, city_name, score, city_data, career_label):
    filled = int(score / 5)              # 0-100 score -> 0-20 blocks
    bar = "#" * filled + "-" * (20 - filled)
    print(f"\n  #{rank}  {city_name}")
    print(f"       Score  : {score}/100  [{bar}]")
    print(f"       Rent   : ~${city_data['avg_rent']:,}/mo  |  {career_label} Jobs: {city_data['career_jobs']}")
    print(f"       Firms  : {city_data['notable_firms']}")
    print(f"       Why    : {city_data['description']}")


# ------------------------------------------------------------------
# MAIN PROGRAM
# Steps:
#  1. User picks Finance or Tech  -> selects the right dataset
#  2. User rates 3 priorities     -> becomes scoring weights
#  3. Optional rent budget filter -> removes cities over budget
#  4. Every city is scored        -> sorted highest to lowest
#  5. Ranked list is printed      -> with a breakdown of #1 pick
# ------------------------------------------------------------------
def main():
    print("=" * 60)
    print("              CITY RANKER - Career Edition")
    print("=" * 60)

    # --- Step 1: Pick a career track ---
    print("\nWhich career track are you planning for?")
    print("  1 = Finance  (banking, trading, asset management)")
    print("  2 = Tech     (software, engineering, data science)\n")

    track_choice = get_valid_input("Enter 1 or 2: ", 1, 2)

    if track_choice == 1:
        city_data_set = finance_cities
        career_label  = "Finance"
        track_name    = "Finance Career"
    else:
        city_data_set = tech_cities
        career_label  = "Tech"
        track_name    = "Tech Career"

    print(f"\n  Running rankings for: {track_name}\n")

    # --- Step 2: Collect user priorities ---
    print("-" * 60)
    print("Rate how important each factor is to YOU (1=low, 5=high).")
    print("-" * 60)
    proximity_weight = get_valid_input("How important is proximity to friends/family? (1-5): ", 1, 5)
    career_weight    = get_valid_input(f"How important is {career_label.lower()} career opportunity? (1-5): ", 1, 5)
    cost_weight      = get_valid_input("How important is a low cost of living?         (1-5): ", 1, 5)

    # --- Step 3: Optional rent budget filter ---
    print("\nWould you like to filter cities by a maximum monthly rent?")
    use_budget = input("Enter yes to filter, or press Enter to skip: ").strip().lower()
    rent_budget = None
    if use_budget == "yes":
        rent_budget = get_valid_input("Enter your max monthly rent budget ($): ", 500, 20000)

    # --- Step 4: Score and filter every city ---
    results = []
    for city_name, data in city_data_set.items():
        if rent_budget and data["avg_rent"] > rent_budget:
            continue    # skip cities over budget
        score = calculate_score(data, proximity_weight, career_weight, cost_weight)
        results.append((score, city_name))

    results.sort(reverse=True)   # highest score first

    # --- Step 5: Print the ranked list ---
    print("\n" + "=" * 60)
    print(f"          CITY RANKINGS  -  {track_name}")
    print("=" * 60)

    if not results:
        print("\n  No cities matched your rent budget. Try raising it.")
        return

    for rank, (score, city_name) in enumerate(results, start=1):
        display_city(rank, city_name, score, city_data_set[city_name], career_label)

    # --- Step 6: Detailed breakdown of the top pick ---
    best_score, best_city = results[0]
    top = city_data_set[best_city]

    print("\n" + "=" * 60)
    print(f"  BEST MATCH: {best_city}  ({best_score}/100)")
    print("=" * 60)
    print(f"\n  Score breakdown for {best_city}:")
    print(f"    Proximity  : {top['proximity_score']}/10  x weight {proximity_weight}")
    print(f"    {career_label:<9}  : {top['career_score']}/10  x weight {career_weight}")
    print(f"    Cost       : {top['cost_score']}/10  x weight {cost_weight}")
    print(f"\n  Weighted total: {best_score}/100")
    print(f"\n  {top['description']}\n")


if __name__ == "__main__":
    main()
