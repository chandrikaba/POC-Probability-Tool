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
    # 2. Calculate Feature Scores (With "Missing Data" Simulation)
    # ---------------------------------------------------------
    
    # Simulation: Late-stage data (Price, Orals, certain Solution aspects) 
    # might not be available for all deals (especially early stage).
    # We randomly "hide" this info (convert to None/Not Available) to ensure
    # the model learns that missing data doesn't auto-mean "Lost".
    
    is_early_stage = random.choice([True, False]) # 50% chance of being incomplete

    # Special Case: sparse_win
    # If target is Won and early stage, we force a "Solution Only" win scenario 15% of the time
    # to ensure the model learns that "Strong Solution + Missing Details" can still be a Win.
    force_sparse_win = False
    if target_status == "Won" and is_early_stage and random.random() < 0.30: # increased prob
        force_sparse_win = True
    
    # Special Case: force_relationship_loss
    # Even with a Strong Solution, a deal can be Lost due to:
    # - Weak Client Relationship (no access to decision makers)
    # - Poor Price Alignment (pricing not competitive)
    # - Net-New (NN) account with no existing relationship
    # This models scenarios like the Dyson case where fundamentals override solution quality.
    force_relationship_loss = False
    if target_status == "Lost" and random.random() < 0.25:  # 25% of Lost deals
        force_relationship_loss = True
        # Force NN (Net-New) to ensure no incumbency advantage
        type_of_business = "NN"
        incumbency = "None"
        acc_engagement = "Low (New Account)"
    
    # Track scores
    current_score = 0
    max_possible_score = 0
    contributions = []

    # Helper to add score only if available
    def add_score(val, max_points, name, l1, l2):
        nonlocal current_score, max_possible_score
        # Check if value indicates "missing" or "not applicable"
        if val in ["Not Available", "No Intel", "Unknown", None]:
            return # Do not punish scalar score, do not add to max possible
        
        # Calculate scalar score based on maps (re-defined locally for clarity)
        # We need the numeric score here. 
        # For simplicity, we define the maps inside.
        score = 0
        if name == "Account Engagement":
            score = {"High (Existing+Good)": 10, "Medium (Existing+Poor)": 5, "Low (New Account)": 0}.get(val, 0)
        elif name == "Client Relationship":
            score = {"Strong": 10, "Neutral": 5, "Weak": 0}.get(val, 0)
        elif name == "Deal Coach":
            score = {"Active & Available": 10, "Passive": 5, "Not Available": 0}.get(val, 0)
        elif name == "Bidder Rank":
            score = {"Top": 15, "Middle": 5, "Bottom": 0}.get(val, 0)
        elif name == "Incumbency Share":
            score = {"High (>50%)": 10, "Medium (20-50%)": 5, "Low (<20%)": 2, "None": 0}.get(val, 0)
        elif name == "References":
            score = {"Strong (Domain+Tech)": 7, "Average": 3, "Weak/None": 0}.get(val, 0)
        elif name == "Solution Strength":
            score = {"Strong (Covers all)": 7, "Average (Gaps)": 3, "Weak": 0}.get(val, 0)
        elif name == "Client Impression":
            score = {"Positive": 6, "Neutral": 3, "Negative": 0}.get(val, 0)
        elif name == "Orals Score":
            score = {"Strong": 15, "At Par": 8, "Weak": 0}.get(val, 0)
        elif name == "Price Alignment":
            score = {"Aligned": 5, "Deviating": 2, "No Intel": 0}.get(val, 0)
        elif name == "Price Position":
            score = {"Lowest": 5, "Competitive": 3, "Expensive": 0}.get(val, 0)
            
        current_score += score
        max_possible_score += max_points
        contributions.append((score, max_points, name, val, l1, l2))

    # A. Relationship (Can now be missing in very early stages)
    # ---------------------------------------------------------
    # Options: ["High (Existing+Good)", "Medium (Existing+Poor)", "Low (New Account)"]
    # Logic: If early stage, might be unknown.
    if force_relationship_loss:
        # Already set to Low (New Account) for relationship loss
        pass  # acc_engagement already set above
    elif force_sparse_win:
        acc_engagement = "Unknown"
    elif is_early_stage and random.random() < 0.5:
        acc_engagement = "Unknown"
    else:
        # Normal generation
        if type_of_business == "NN":
            acc_engagement = "Low (New Account)"
        else:
            if incumbency == "High (>50%)":
                acc_engagement = pick_weighted(["High (Existing+Good)", "Medium (Existing+Poor)"], [w[0], w[1]+w[2]])
            else:
                acc_engagement = pick_weighted(["High (Existing+Good)", "Medium (Existing+Poor)"], [w[0], w[1]+w[2]])
    
    add_score(acc_engagement, 10, "Account Engagement", "Relationship", "Client Relationship (CXOs, decision makers, influencers)")

    # Client Relationship
    # Options: ["Strong", "Neutral", "Weak"]
    if force_relationship_loss:
        # Force Weak relationship for relationship-based losses
        client_rel = "Weak"
    elif force_sparse_win:
        client_rel = "Unknown"
    elif is_early_stage and random.random() < 0.5:
        client_rel = "Unknown"
    elif acc_engagement == "High (Existing+Good)":
         if target_status == "Lost": rel_weights = [0.2, 0.8] 
         elif target_status == "Won": rel_weights = [0.9, 0.1]
         else: rel_weights = [0.5, 0.5]
         client_rel = pick_weighted(["Strong", "Neutral"], rel_weights)
    else:
        client_rel = pick_weighted(["Strong", "Neutral", "Weak"], w)
        
    add_score(client_rel, 10, "Client Relationship", "Relationship", "Client Relationship (CXOs, decision makers, influencers)")
    
    # Deal Coach (Maybe Missing)
    deal_coach = pick_weighted(["Active & Available", "Passive", "Not Available"], w)
    if force_sparse_win or (is_early_stage and random.random() < 0.3): deal_coach = "Not Available"
    add_score(deal_coach, 10, "Deal Coach", "Relationship", "Deal Coach availability/ fit")
    
    # B. Competition (Rank maybe missing)
    bidder_rank = pick_weighted(["Top", "Middle", "Bottom"], w)
    if force_sparse_win or is_early_stage: bidder_rank = "Not Available" # Often unknown early
    add_score(bidder_rank, 15, "Bidder Rank", "Relationship", "Competition and Incumbency (strategic, CSAT, delivery track record)")
    
    # Incumbency (Known)
    # incumbency generated above (but could be None for NN)
    if force_sparse_win or (is_early_stage and random.random() < 0.3):
        incumbency = "Unknown"
        
    add_score(incumbency, 10, "Incumbency Share", "Commercials", "Incumbency advantage/discounting")
    
    # C. Solution (References known, others maybe not)
    references = pick_weighted(["Strong (Domain+Tech)", "Average", "Weak/None"], w)
    if force_sparse_win: references = "Weak/None" # Or Unknown? Let's say absent.
    add_score(references, 7, "References", "Capability_or_Credentials", "References (Scale, Domain, Usecase) & Case Studies")
    
    sol_strength = pick_weighted(["Strong (Covers all)", "Average (Gaps)", "Weak"], w)
    if force_relationship_loss:
        # Force Strong solution for relationship-based losses
        # This teaches the model that strong solution alone isn't enough
        sol_strength = "Strong (Covers all)"
    elif force_sparse_win:
        sol_strength = "Strong (Covers all)" # Force Strong for sparse win
    elif is_early_stage and random.random() < 0.5: 
        sol_strength = "Not Available"
    add_score(sol_strength, 7, "Solution Strength", "Solution", "Technical Response Quality (coherent, competitive, consultative, competitive)")
    
    client_impression = pick_weighted(["Positive", "Neutral", "Negative"], w)
    if force_sparse_win or is_early_stage: client_impression = "Neutral" 
    add_score(client_impression, 6, "Client Impression", "Solution", "PoV/ Thought Leadership")
    
    # D. Orals (Often missing early)
    orals_score_val = pick_weighted(["Strong", "At Par", "Weak"], w)
    if force_sparse_win or is_early_stage: orals_score_val = "Not Available"
    add_score(orals_score_val, 15, "Orals Score", "Solution", "Orals Performance")

    # E. Price (Often missing early)
    price_alignment = pick_weighted(["Aligned", "Deviating", "No Intel"], w)
    if force_relationship_loss:
        # Force Deviating price for relationship-based losses
        price_alignment = "Deviating"
    elif force_sparse_win or is_early_stage: 
        price_alignment = "No Intel"
    add_score(price_alignment, 5, "Price Alignment", "Commercials", "Deviation/fit to win price")
    
    price_position = pick_weighted(["Lowest", "Competitive", "Expensive"], w)
    if force_relationship_loss:
        # Force Expensive price position for relationship-based losses
        price_position = "Expensive"
    elif force_sparse_win or is_early_stage: 
        price_position = "Not Available"
    add_score(price_position, 5, "Price Position", "Commercials", "Pricing model innovation/ Commercial Structure")
    
    # --- CALCULATE FINAL PERCENTAGE SCORE ---
    if max_possible_score == 0:
        final_percentage = 0
    else:
        final_percentage = (current_score / max_possible_score) * 100
        
    # Add noise
    final_percentage += random.randint(-5, 5)
    final_percentage = max(0, min(100, final_percentage))
    
    # Store numerical score for checking
    total_score = round(final_percentage, 2)
    
    # Force alignment with Target Status using the PERCENTAGE metric now
    # 60% is a reasonable cutoff for Win if we only consider *available* data.
    if target_status == "Won" and total_score < 60:
        total_score = random.randint(65, 95)
    elif target_status == "Lost" and total_score > 50:
        total_score = random.randint(20, 45)
    elif target_status == "Aborted":
        if total_score < 40 or total_score > 60:
             total_score = random.randint(45, 58)
    
    deal_status = target_status
    
    # ---------------------------------------------------------
    # 3. Determine Contributing Factors (Real World Logic)
    # ---------------------------------------------------------
    # Calculate 'Impact' for each factor.
    # Impact = (Score / MaxScore) - 0.5.
    factor_impacts = []
    for score, max_score, name, val, l1, l2 in contributions:
        # If max_score was 0 ?? No, add_score only adds if max_points > 0
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
        remarks = f"Won. Key drivers: {primary_l2}, {secondary_l2}. Win Prob Score: {total_score}%"
    else:
        remarks = f"{deal_status}. Main issues: {primary_l2}, {secondary_l2}. Win Prob Score: {total_score}%"

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

