import os
import random
import pandas as pd

# STEP 1: Load your Excel file
input_file = "data/input/Data-Input.xlsx"   # Path to input file
df = pd.ExcelFile(input_file)

# Pick the first sheet (or loop through all)
sheet_name = df.sheet_names[0]
data = df.parse(sheet_name)

# STEP 2: Extract schema (column names)
columns = list(data.columns)

# Define schema from Excel (simplified for illustration)
valid_tags = [
    "Relationship", "Solution", "Capability_or_Credentials", "Commercials", "Strategic_Initiatives",
    "Client Relationship (CXOs, decision makers, influencers)", "Technical Response Quality (coherent, competitive, consultative, competitive)",
    "Domain/ Functional Expertise / Industry trends", "Deviation/fit to win price", "Mahindra Group leverage",
    "Quality 360° Deal Intelligence/Validation (incl win price)", "PoV/ Thought Leadership",
    "References (Scale, Domain, Usecase) & Case Studies", "Loading/Input parameters as per guidelines (productivity, HTR, Premium/niche, offshore)",
    "Customer GTM Growth", "Deal Coach availability/ fit", "Business value proposition",
    "Language/ Regional/ Gender Diversity", "Commercial parameters as per guidelines (contigency, bought out)",
    "Strong Outcome-based Deal Strategy", "Quality of RFP/ Proactive Deal sourcing", "Availability of SMEs",
    "Analyst Quadrant/ Brand Perception", "Cost & Rate benchmarks not available/non-standardised across org",
    "Competition and Incumbency (strategic, CSAT, delivery track record)", "Demo/ Show & Tell/ Video",
    "Delivery Readiness", "Strong Business case/ Savings", "Analyst/ TPA Relations", "Orals Performance",
    "Local Presence", "Effort estimation methodology", "Alliances/ Partners fit",
    "Process issues (Bid management, reviews, timeline available)", "Pricing model innovation/ Commercial Structure",
    "Customer Bias", "Cookie cutter solutions for commoditised services vis-à-vis peers", "Optimized partner Rate cards",
    "Incumbency advantage/discounting"
]

# Define L1 → L2 mapping
l1_to_l2 = {
    "Relationship": [
        "Client Relationship (CXOs, decision makers, influencers)",
        "Deal Coach availability/ fit",
        "Customer Bias",
        "Quality 360° Deal Intelligence/Validation (incl win price)",
        "Quality of RFP/ Proactive Deal sourcing",
        "Competition and Incumbency (strategic, CSAT, delivery track record)",
        "Analyst/ TPA Relations",
        "Alliances/ Partners fit",
        "Customer Bias"
    ],
    "Solution": [
        "Business value proposition",
        "Technical Response Quality (coherent, competitive, consultative, competitive)",
        "PoV/ Thought Leadership",
        "Demo/ Show & Tell/ Video",
        "Availability of SMEs",
        "Orals Performance",
        "Process issues (Bid management, reviews, timeline available)",
        "Cookie cutter solutions for commoditised services vis-à-vis peers"
    ],
    "Capability_or_Credentials": [
        "Language/  Regional/ Gender Diversity",
        "Domain/ Functional Expertise / Industry trends",
        "References (Scale, Domain, Usecase) & Case Studies",
        "Delivery Readiness (incl local presence)",
        "Analyst Quadrant/ Brand Perception",
        "Local Presence"
    ],
    "Commercials": [
        "Deviation/fit to win price",
        "Loading/Input parameters as per guidelines (productivity, HTR, Premium/niche, offshore)",
        "Pricing model innovation/ Commercial Structure",
        "Commercial parameters as per guidelines (contingency, bought out)",
        "Cost & Rate benchmarks not available/non-standardised across org",
        "Optimized partner Rate cards",
        "Incumbency advantage/discounting",
        "Strong Business case/ Savings",
        "Effort estimation methodology",
        "Optimized partner Rate cards"
    ],
    "Strategic_Initiatives": [
        "Mahindra Group leverage",
        "Strong Outcome-based Deal Strategy",
        "Customer GTM Growth"
    ]
}

# Helper for weighted selection
def pick_weighted(options, weights):
    # options: list of values
    # weights: list of probabilities (should sum to 1.0 or approx)
    return random.choices(options, weights=weights, k=1)[0]

# Synthetic record generator
def generate_record(index, target_status=None):
    # --- EXISTING FIELDS ---
    sbu = random.choice(["Europe", "IMEA", "APJ", "ASV"])
    account_name = random.choice(["HSBC", "MOHRE", "Cummins", "Cadent", "GSK", "Etihad"])
    type_of_business = random.choice(["EE", "EN", "NN"])
    tcv = round(random.uniform(5, 100), 2)
    deal_size_bucket = "<250M" if tcv < 250 else ">=250M"
    
    # Initialize variables
    primary_l1, primary_l2, secondary_l1, secondary_l2, tertiary_l1, tertiary_l2 = "", "", "", "", "", ""

    # --- DEFINE WEIGHTS BASED ON TARGET STATUS ---
    # Probabilities for [Best_Option, Mid_Option, Worst_Option]
    if target_status == "Won":
        w = [0.90, 0.10, 0.0] # Almost exclusively Top/High
    elif target_status == "Lost":
        w = [0.0, 0.10, 0.90] # Almost exclusively Low/Weak
    elif target_status == "Aborted":
        w = [0.10, 0.80, 0.10]   # Skewed to Average/Mid
    else:
        w = [0.33, 0.33, 0.33] # Random

    # ---------------------------------------------------------
    # 1. Enforce Business Logic Consistency
    # ---------------------------------------------------------
    
    # Logic: NN (Net New) vs Existing (EE/EN)
    # If we WANT to WIN, it helps if we are NOT NN (Net New), or if we are NN, we need strong factors.
    # To ensure "Won" scores are high enough, we'll bias the Type of Business for Won deals.
    if target_status == "Won":
        # Bias towards Existing business for Wins to allow higher incumbency scores
        type_of_business = random.choice(["EE", "EN", "EE", "EN", "NN"]) 
    else:
        # Random for others
        type_of_business = random.choice(["EE", "EN", "NN"])

    if type_of_business == "NN":
        # New Client: No Incumbency, Low Engagement
        incumbency = "None"
        acc_engagement = "Low (New Account)"
    else: 
        # Existing Client: must have some history
        # Determine Incumbency first
        # Incumbency Options: ["High (>50%)", "Medium (20-50%)", "Low (<20%)"]
        incumbency = pick_weighted(["High (>50%)", "Medium (20-50%)", "Low (<20%)"], w)
        
        # Determine Engagement based on Incumbency
        # Engagement Options: ["High (Existing+Good)", "Medium (Existing+Poor)", "Low (New Account)"] (mapped to Best/Mid/Worst)
        if incumbency == "High (>50%)":
            acc_engagement = pick_weighted(["High (Existing+Good)", "Medium (Existing+Poor)"], [w[0], w[1]+w[2]])
        elif incumbency == "Medium (20-50%)":
            acc_engagement = pick_weighted(["High (Existing+Good)", "Medium (Existing+Poor)"], [w[0], w[1]+w[2]])
        else: # Low (<20%)
            acc_engagement = pick_weighted(["High (Existing+Good)", "Medium (Existing+Poor)"], [w[0], w[1]+w[2]])

    # ---------------------------------------------------------
    # 2. Calculate Feature Scores
    # ---------------------------------------------------------
    
    # Track individual contributions for Factor determination
    contributions = []

    # A. Relationship
    score_engagement_map = {"High (Existing+Good)": 10, "Medium (Existing+Poor)": 5, "Low (New Account)": 0}
    score_engagement = score_engagement_map[acc_engagement]
    contributions.append((score_engagement, 10, "Account Engagement", acc_engagement, "Relationship", "Client Relationship (CXOs, decision makers, influencers)"))

    # Options: ["Strong", "Neutral", "Weak"]
    if acc_engagement == "High (Existing+Good)":
        # Rule: High Engagement implies at least Neutral or Strong relationship (No "Weak")
        if target_status == "Lost":
             # If target is Lost, we'd normally want Weak, but business logic prevents it here.
             # We rely on other factors (Price/Solution) to drive the Loss.
             # Skew to Neutral to be "worse" than Strong.
             rel_weights = [0.2, 0.8] 
        elif target_status == "Won":
             rel_weights = [0.9, 0.1]
        else:
             rel_weights = [0.5, 0.5]
        
        client_rel = pick_weighted(["Strong", "Neutral"], rel_weights)
    else:
        # Standard weighted logic based on status
        client_rel = pick_weighted(["Strong", "Neutral", "Weak"], w)

    score_rel_map = {"Strong": 10, "Neutral": 5, "Weak": 0}
    score_rel = score_rel_map[client_rel]
    contributions.append((score_rel, 10, "Client Relationship", client_rel, "Relationship", "Client Relationship (CXOs, decision makers, influencers)"))
    
    # Options: ["Active & Available", "Passive", "Not Available"]
    deal_coach = pick_weighted(["Active & Available", "Passive", "Not Available"], w)
    score_coach_map = {"Active & Available": 10, "Passive": 5, "Not Available": 0}
    score_coach = score_coach_map[deal_coach]
    contributions.append((score_coach, 10, "Deal Coach", deal_coach, "Relationship", "Deal Coach availability/ fit"))
    
    score_relationship = score_engagement + score_rel + score_coach

    # B. Competition
    # Options: ["Top", "Middle", "Bottom"]
    bidder_rank = pick_weighted(["Top", "Middle", "Bottom"], w)
    score_rank_map = {"Top": 15, "Middle": 5, "Bottom": 0}
    score_rank = score_rank_map[bidder_rank]
    contributions.append((score_rank, 15, "Bidder Rank", bidder_rank, "Relationship", "Competition and Incumbency (strategic, CSAT, delivery track record)"))
    
    score_inc_map = {"High (>50%)": 10, "Medium (20-50%)": 5, "Low (<20%)": 2, "None": 0}
    score_incumbency = score_inc_map[incumbency]
    contributions.append((score_incumbency, 10, "Incumbency Share", incumbency, "Commercials", "Incumbency advantage/discounting"))
    
    score_competition = score_rank + score_incumbency

    # C. Solution
    # Options: ["Strong (Domain+Tech)", "Average", "Weak/None"]
    references = pick_weighted(["Strong (Domain+Tech)", "Average", "Weak/None"], w)
    score_refs_map = {"Strong (Domain+Tech)": 7, "Average": 3, "Weak/None": 0}
    score_refs = score_refs_map[references]
    contributions.append((score_refs, 7, "References", references, "Capability_or_Credentials", "References (Scale, Domain, Usecase) & Case Studies"))
    
    # Options: ["Strong (Covers all)", "Average (Gaps)", "Weak"]
    sol_strength = pick_weighted(["Strong (Covers all)", "Average (Gaps)", "Weak"], w)
    score_sol_map = {"Strong (Covers all)": 7, "Average (Gaps)": 3, "Weak": 0}
    score_sol = score_sol_map[sol_strength]
    contributions.append((score_sol, 7, "Solution Strength", sol_strength, "Solution", "Technical Response Quality (coherent, competitive, consultative, competitive)"))
    
    # Options: ["Positive", "Neutral", "Negative"]
    client_impression = pick_weighted(["Positive", "Neutral", "Negative"], w)
    score_imp_map = {"Positive": 6, "Neutral": 3, "Negative": 0}
    score_imp = score_imp_map[client_impression]
    contributions.append((score_imp, 6, "Client Impression", client_impression, "Solution", "PoV/ Thought Leadership"))
    
    score_solution = score_refs + score_sol + score_imp

    # D. Orals
    # Options: ["Strong", "At Par", "Weak"]
    orals_score_val = pick_weighted(["Strong", "At Par", "Weak"], w)
    score_orals_map = {"Strong": 15, "At Par": 8, "Weak": 0}
    score_orals = score_orals_map[orals_score_val]
    contributions.append((score_orals, 15, "Orals Score", orals_score_val, "Solution", "Orals Performance"))

    # E. Price
    # Options: ["Aligned", "Deviating", "No Intel"] -> Note: "No Intel" is worst (0)
    price_alignment = pick_weighted(["Aligned", "Deviating", "No Intel"], w)
    score_align_map = {"Aligned": 5, "Deviating": 2, "No Intel": 0}
    score_align = score_align_map[price_alignment]
    contributions.append((score_align, 5, "Price Alignment", price_alignment, "Commercials", "Deviation/fit to win price"))
    
    # Options: ["Lowest", "Competitive", "Expensive"]
    price_position = pick_weighted(["Lowest", "Competitive", "Expensive"], w)
    score_pos_map = {"Lowest": 5, "Competitive": 3, "Expensive": 0}
    score_pos = score_pos_map[price_position]
    contributions.append((score_pos, 5, "Price Position", price_position, "Commercials", "Pricing model innovation/ Commercial Structure"))
    
    score_price = score_align + score_pos

    # --- TOTAL SCORE & STATUS ---
    total_score = score_relationship + score_competition + score_solution + score_orals + score_price
    total_score += random.randint(-2, 2)
    
    # Force alignment with Target Status
    # This prevents random "bad luck" features from dragging a "Won" deal into "Aborted/Lost" territory
    if target_status == "Won" and total_score < 60:
        total_score = random.randint(62, 85)
    elif target_status == "Lost" and total_score > 45:
        total_score = random.randint(20, 43)
    elif target_status == "Aborted":
        if total_score < 46 or total_score > 59:
             total_score = random.randint(48, 58)
    
    deal_status = target_status
    
    # ---------------------------------------------------------
    # 3. Determine Contributing Factors (Real World Logic)
    # ---------------------------------------------------------
    # Calculate 'Impact' for each factor.
    # Impact = (Score / MaxScore) - 0.5.
    factor_impacts = []
    for score, max_score, name, val, l1, l2 in contributions:
        normalized = score / max_score if max_score > 0 else 0
        if normalized >= 0.7:
            sentiment = "(Positive)"
            magnitude = normalized
        elif normalized <= 0.3:
            sentiment = "(Negative)"
            magnitude = (1.0 - normalized)
        else:
            sentiment = "(Neutral)"
            magnitude = 0.5
            
        factor_impacts.append({
            "name": name,
            "value": val,
            "l1": l1,
            "l2": l2,
            "sentiment": sentiment,
            "magnitude": magnitude
        })

    factor_impacts.sort(key=lambda x: x["magnitude"], reverse=True)
    
    final_factors = []
    
    if deal_status == "Won":
        candidates = [f for f in factor_impacts if "Positive" in f["sentiment"]]
        candidates += [f for f in factor_impacts if "Positive" not in f["sentiment"]]
    elif deal_status in ["Lost", "Aborted"]:
        candidates = [f for f in factor_impacts if "Negative" in f["sentiment"]]
        candidates += [f for f in factor_impacts if "Negative" not in f["sentiment"]]
    else:
        candidates = factor_impacts

    selected = candidates[:3]
    
    if len(selected) > 0:
        primary_l1 = selected[0]["l1"]
        primary_l2 = f"{selected[0]['l2']} - {selected[0]['value']} {selected[0]['sentiment']}"
    if len(selected) > 1:
        secondary_l1 = selected[1]["l1"]
        secondary_l2 = f"{selected[1]['l2']} - {selected[1]['value']} {selected[1]['sentiment']}"
    if len(selected) > 2:
        tertiary_l1 = selected[2]["l1"]
        tertiary_l2 = f"{selected[2]['l2']} - {selected[2]['value']} {selected[2]['sentiment']}"

    # Generate remarks
    if deal_status == "Won":
        remarks = f"Won. Key drivers: {primary_l2}, {secondary_l2}. Total Score: {total_score}"
    else:
        remarks = f"{deal_status}. Main issues: {primary_l2}, {secondary_l2}. Total Score: {total_score}"

    return {
        "CRM ID": f"CRM{300000 + index}",
        "SBU": sbu,
        "Qtr of closure": random.choice(["Q1'25","Q2'25","Q1'24","Q2'24","Q3'25","Q4'24"]),
        "Deal Status": deal_status,
        "Account Name": account_name,
        "Opportunity Name": f"Opportunity {index}",
        "Expected TCV ($Mn)": tcv,
        "Deal Size bucket": deal_size_bucket,
        "Type of Business": type_of_business,
        
        # New Factors
        "Account Engagement": acc_engagement,
        "Client Relationship": client_rel,
        "Deal Coach": deal_coach,
        "Bidder Rank": bidder_rank,
        "Incumbency Share": incumbency,
        "References": references,
        "Solution Strength": sol_strength,
        "Client Impression": client_impression,
        "Orals Score": orals_score_val,
        "Price Alignment": price_alignment,
        "Price Position": price_position,
        "Calculated Score": total_score,

        "Primary L1": primary_l1,
        "Primary L2": primary_l2,
        "Secondary L1": secondary_l1,
        "Secondary L2": secondary_l2,
        "Tertiary L1": tertiary_l1,
        "Tertiary L2": tertiary_l2,
        "Detailed Remarks": remarks,
        "Bid Qualification (BQ)  Score": None,
        "Winnability/ BQ  Feedback": None,
        "SBU Head Involved": None,
        "SL Heads Involved": None,
        "Were we the lowest price? Y/N": "Y" if price_position == "Lowest" else "N",
        "Bid Timeline": f"Q{random.randint(1,4)}'25",
        "Bid-Team size": 0,
        "Deal Scope": "",
        "DD": "",
        "EA": "",
        "Client Partner/ Opp. Owner":"",
        "BM":""    
    }


# STEP 4: Generate 1000 synthetic records using the generate_record function
print("Generating 1000 synthetic records...")
synthetic_records = []
target_distribution = ["Won", "Lost", "Aborted"]
for i in range(1, 1001):
    # Cycle through targets to ensure roughly equal distribution
    target = target_distribution[i % 3]
    record = generate_record(i, target_status=target)
    synthetic_records.append(record)
    if i % 50 == 0:
        print(f"Generated {i}/1000 records...")

# STEP 5: Convert to DataFrame
synthetic_df = pd.DataFrame(synthetic_records)

# STEP 6: Save to Excel
project_root = os.getcwd()
output_dir = os.path.join(project_root, "data", "output")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "synthetic_data_v3.xlsx")

try:
    synthetic_df.to_excel(output_file, index=False)
    print(f"\nSynthetic data generation complete!")
    print(f"Generated {len(synthetic_df)} records")
    print(f"Saved to: {output_file}")
except PermissionError:
    # File is locked (probably open in Excel), save with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"data/output/synthetic_data_v2_{timestamp}.xlsx"
    synthetic_df.to_excel(backup_file, index=False)
    print(f"\n[WARNING] Could not save to {output_file} (file is open)")
    print(f"[SUCCESS] Saved to backup file: {backup_file}")
    print(f"Generated {len(synthetic_df)} records")

