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

# Synthetic record generator
def generate_record(index):
    # --- EXISTING FIELDS ---
    sbu = random.choice(["Europe", "IMEA", "APJ", "ASV"])
    account_name = random.choice(["HSBC", "MOHRE", "Cummins", "Cadent", "GSK", "Etihad"])
    type_of_business = random.choice(["EE", "EN", "NN"])
    tcv = round(random.uniform(5, 100), 2)
    deal_size_bucket = "<250M" if tcv < 250 else ">=250M"
    
    primary_l1 = random.choice(list(l1_to_l2.keys()))
    secondary_l1 = random.choice(list(l1_to_l2.keys()))
    tertiary_l1 = random.choice(list(l1_to_l2.keys()))
    primary_l2 = random.choice(l1_to_l2[primary_l1])
    secondary_l2 = random.choice(l1_to_l2[secondary_l1])
    tertiary_l2 = random.choice(l1_to_l2[tertiary_l1])

    # --- NEW 5 FACTORS (User Defined Logic) ---
    
    # 1. Relationship (Impact: High) - Max Score: 30
    # a. Account Engagement
    acc_engagement = random.choice(["High (Existing+Good)", "Medium (Existing+Poor)", "Low (New Account)"])
    score_engagement = {"High (Existing+Good)": 10, "Medium (Existing+Poor)": 5, "Low (New Account)": 0}[acc_engagement]
    
    # b. Client Stakeholder Relationship
    client_rel = random.choice(["Strong", "Neutral", "Weak"])
    score_rel = {"Strong": 10, "Neutral": 5, "Weak": 0}[client_rel]
    
    # c. Deal Coach Availability
    deal_coach = random.choice(["Active & Available", "Passive", "Not Available"])
    score_coach = {"Active & Available": 10, "Passive": 5, "Not Available": 0}[deal_coach]
    
    score_relationship = score_engagement + score_rel + score_coach

    # 2. Competition & Incumbency (Impact: High) - Max Score: 25
    # a. Bidder Ranking
    bidder_rank = random.choice(["Top", "Middle", "Bottom"])
    score_rank = {"Top": 15, "Middle": 5, "Bottom": 0}[bidder_rank]
    
    # b. Incumbency Share
    incumbency = random.choice(["High (>50%)", "Medium (20-50%)", "Low (<20%)", "None"])
    score_incumbency = {"High (>50%)": 10, "Medium (20-50%)": 5, "Low (<20%)": 2, "None": 0}[incumbency]
    
    score_competition = score_rank + score_incumbency

    # 3. Solution Capability (Impact: Medium-High) - Max Score: 20
    # a. References/Case Studies
    references = random.choice(["Strong (Domain+Tech)", "Average", "Weak/None"])
    score_refs = {"Strong (Domain+Tech)": 7, "Average": 3, "Weak/None": 0}[references]
    
    # b. Solution Strength
    sol_strength = random.choice(["Strong (Covers all)", "Average (Gaps)", "Weak"])
    score_sol = {"Strong (Covers all)": 7, "Average (Gaps)": 3, "Weak": 0}[sol_strength]
    
    # c. Client Impression
    client_impression = random.choice(["Positive", "Neutral", "Negative"])
    score_imp = {"Positive": 6, "Neutral": 3, "Negative": 0}[client_impression]
    
    score_solution = score_refs + score_sol + score_imp

    # 4. Orals/Presentation (Impact: Medium-High) - Max Score: 15
    orals_score_val = random.choice(["Strong", "At Par", "Weak"])
    score_orals = {"Strong": 15, "At Par": 8, "Weak": 0}[orals_score_val]

    # 5. Price (Impact: Medium) - Max Score: 10
    # a. Price to Win Alignment
    price_alignment = random.choice(["Aligned", "Deviating", "No Intel"])
    score_align = {"Aligned": 5, "Deviating": 2, "No Intel": 0}[price_alignment]
    
    # b. Competitive Position
    price_position = random.choice(["Lowest", "Competitive", "Expensive"])
    score_pos = {"Lowest": 5, "Competitive": 3, "Expensive": 0}[price_position]
    
    score_price = score_align + score_pos

    # --- TOTAL SCORE & STATUS ---
    total_score = score_relationship + score_competition + score_solution + score_orals + score_price
    
    # Add small random noise (+/- 5) to simulate real-world uncertainty
    total_score += random.randint(-5, 5)

    if total_score >= 65:
        deal_status = "Won"
    elif total_score <= 40:
        deal_status = "Lost"
    else:
        deal_status = random.choices(["Won", "Lost", "Aborted"], weights=[20, 50, 30])[0]

    # Generate remarks
    if deal_status == "Won":
        remarks = f"Won due to {client_rel} relationship and {bidder_rank} ranking. Total Score: {total_score}"
    elif deal_status == "Lost":
        remarks = f"Lost due to {orals_score_val} orals and {price_position} pricing. Total Score: {total_score}"
    else:
        remarks = f"Aborted. Weak engagement ({acc_engagement}). Total Score: {total_score}"

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
        "Calculated Score": total_score, # Helpful for debugging/analysis

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
for i in range(1, 1001):
    record = generate_record(i)
    synthetic_records.append(record)
    if i % 50 == 0:
        print(f"Generated {i}/1000 records...")

# STEP 5: Convert to DataFrame
synthetic_df = pd.DataFrame(synthetic_records)

# STEP 6: Save synthetic data
output_file = "data/output/Synthetic_Data.xlsx"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

try:
    synthetic_df.to_excel(output_file, index=False)
    print(f"\nSynthetic data generation complete!")
    print(f"Generated {len(synthetic_df)} records")
    print(f"Saved to: {output_file}")
except PermissionError:
    # File is locked (probably open in Excel), save with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"data/output/Synthetic_Data_{timestamp}.xlsx"
    synthetic_df.to_excel(backup_file, index=False)
    print(f"\n[WARNING] Could not save to {output_file} (file is open)")
    print(f"[SUCCESS] Saved to backup file: {backup_file}")
    print(f"Generated {len(synthetic_df)} records")
    
# Also save as synthetic_deals.xlsx for Streamlit compatibility
try:
    synthetic_deals_file = "data/output/synthetic_deals.xlsx"
    synthetic_df.to_excel(synthetic_deals_file, index=False)
    print(f"[SUCCESS] Also saved to: {synthetic_deals_file}")
except PermissionError:
    print(f"[WARNING] Could not save to {synthetic_deals_file} (file is open)")

