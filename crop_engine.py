import pandas as pd

# ==========================================
# Load Crop Master Data
# ==========================================
df = pd.read_csv("d:/billing/lib/crop_master.csv")

# ==========================================
# Farmer Input
# ==========================================
farmer = {
    "nitrogen": 100,
    "phosphorus": 55,
    "potassium": 50,
    "ph": 6.8,
    "rainfall": 750,
    "season": "kharif"
}

# ==========================================
# Score Calculation
# ==========================================
def calculate_score(row):
    score = 0

    # NPK Matching
    if row["n_min"] <= farmer["nitrogen"] <= row["n_max"]:
        score += 10
    if row["p_min"] <= farmer["phosphorus"] <= row["p_max"]:
        score += 10
    if row["k_min"] <= farmer["potassium"] <= row["k_max"]:
        score += 10

    # pH Matching
    if row["ph_min"] <= farmer["ph"] <= row["ph_max"]:
        score += 10

    # Rainfall Matching (FIXED)
    if row["water_min"] <= farmer["rainfall"] <= row["water_max"]:
        score += 20

    # Season Matching
    if farmer["season"].strip().lower() == row["season"].strip().lower():
        score += 20

    return score

# ==========================================
# Apply scoring
# ==========================================
df["score"] = df.apply(calculate_score, axis=1)

# ==========================================
# Sort Best Crops
# ==========================================
result = df.sort_values(by="score", ascending=False)

# ==========================================
# Display Results
# ==========================================
print("\n🌾 SMART CROP RECOMMENDATION SYSTEM 🌾\n")
print(result[["crop_name", "score", "season", "water_min", "water_max"]])
print("\n====================================\n")

# ==========================================
# Best Crop
# ==========================================
best_crop = result.iloc[0]
print("✅ Recommended Crop :", best_crop["crop_name"])
print("⭐ Suitability Score :", best_crop["score"])
print("🌦️ Suitable Rainfall :", f"{best_crop['water_min']} - {best_crop['water_max']} mm")
print("🌱 Season :", best_crop["season"])
