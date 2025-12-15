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
   primary_l1 = random.choice(list(l1_to_l2.keys()))
   secondary_l1 = random.choice(list(l1_to_l2.keys()))
   tertiary_l1 = random.choice(list(l1_to_l2.keys()))

   primary_l2 = random.choice(l1_to_l2[primary_l1])
   secondary_l2 = random.choice(l1_to_l2[secondary_l1])
   tertiary_l2 = random.choice(l1_to_l2[tertiary_l1])

   deal_status = random.choice(["Won", "Lost", "Aborted"])
   
   tcv = round(random.uniform(5, 100), 2)
   
   if(tcv<250):
    deal_size_bucket = "<250M"
   else:
    deal_size_bucket = ">=250M"

 # Generate realistic remarks
   if deal_status == "Won":
       remarks = f"Won due to strong {primary_l1.lower()} and compelling {secondary_l1.lower()} story. TCV ${tcv} validated."
   elif deal_status == "Lost":
       remarks = f"Lost due to gaps in {primary_l2.lower()} and competitive pressure on {secondary_l2.lower()}."
   else:
       remarks = f"Aborted due to qualification issues or lack of alignment in {tertiary_l2.lower()}."
   print(f"Deal Status: {deal_status} | Type: {type(deal_status)}")
   print(remarks)
   
   return {
       "CRM ID": f"CRM{300000 + index}",
       "SBU": random.choice(["Europe", "IMEA", "APJ", "ASV"]),
       "Qtr of closure":random.choice(["Q1'25","Q2'25","Q1'24","Q2'24","Q3'25","Q4'24" ]),
       "Deal Status": deal_status,
       "Account Name": random.choice(["HSBC", "MOHRE", "Cummins", "Cadent", "GSK", "Etihad"]),
       "Opportunity Name": f"Opportunity {index}",
       "Expected TCV ($Mn)": round(random.uniform(5, 100), 2),
       "Deal Size bucket": deal_size_bucket,
       "Type of Business": random.choice(["EE", "EN", "NN"]),
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
       "Were we the lowest price? Y/N":random.choice(["Y","N"]),
       "Bid Timeline": f"Q{random.randint(1,4)}'25",
       "Bid-Team size":0,
       "Deal Scope":"",
       "DD":"",
       "EA":"",
       "Client Partner/ Opp. Owner":"",
       "BM":""    
    }


# STEP 4: Generate 100 synthetic records using the generate_record function
print("Generating 100 synthetic records...")
synthetic_records = []
for i in range(1, 101):
    record = generate_record(i)
    synthetic_records.append(record)
    if i % 10 == 0:
        print(f"Generated {i}/100 records...")

# STEP 5: Convert to DataFrame
synthetic_df = pd.DataFrame(synthetic_records)

# STEP 6: Save synthetic data
output_file = "data/output/Synthetic_Data.xlsx"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
synthetic_df.to_excel(output_file, index=False)
print(f"\nSynthetic data generation complete!")
print(f"Generated {len(synthetic_df)} records")
print(f"Saved to: {output_file}")

