"""
Configuration settings for Synthetic Data Generator
"""

# ============================================================================
# GEMINI API CONFIGURATION
# ============================================================================
GEMINI_API_KEY = "AIzaSyCBUNznkpcuvquY25epIuJvDAOYLMHVg1k"  # Replace with your actual API key
GEMINI_MODEL = "gemini-flash-latest"  # Options: "gemini-1.5-flash", "gemini-1.5-pro"

# ============================================================================
# FILE PATHS
# ============================================================================
SOURCE_EXCEL_FILE = "data/input/CY2025_Gap Analysis_v1.1.xlsx"
SOURCE_SHEET_NAME = "SST Involved WLA_02.07.24"
OUTPUT_DIRECTORY = "data/output"
OUTPUT_FILE_NAME = "synthetic_deals_1000.xlsx"
SCHEMA_FILE = "data/cache/source_data_schema.json"

# ============================================================================
# GENERATION PARAMETERS
# ============================================================================
TOTAL_ROWS = 1000           # Total number of synthetic rows to generate
BATCH_SIZE = 50             # Number of rows to generate per API call
TEMPERATURE = 0.8           # AI creativity (0.0 = deterministic, 1.0 = creative)
API_DELAY_SECONDS = 2       # Delay between API calls to avoid rate limiting

# ============================================================================
# COLUMN CONFIGURATION
# ============================================================================
# Primary columns to include in synthetic data generation
PRIMARY_COLUMNS = [
    "CRM ID",
    "SBU",
    "Account Name",
    "Opportunity Name",
    "Expected TCV ($Mn) ",
    "Deal Director",
    "EA & Solutioning Team",
    "EA & Origination Team",
    "ADMSNXT Team",
    "Transiton Team",
    "Pursuit Excellence Team",
    "Opportunity Owner",
    "Bid Manager",
    "CRM Sales Stage",
    "CRM TCV"
]

# ============================================================================
# CATEGORICAL VALUES
# ============================================================================
# Known categorical values extracted from source data
CATEGORICAL_VALUES = {
    "SBU": ["IMEA", "APJ", "Europe", "ASV", "A Comms", "TME"],
    "CRM Sales Stage": ["P0", "P-1", "P-2", "P-3", "P4", "P5"],
    "Deal Director": [
        "EA Driven",
        "Sugata Chakraborty",
        "Mukund Adapala",
        "Suruchi",
        "Sravan Kumar Susarla",
        "Konark Bhasin",
        "Karthik Kashyap",
        "Bhoomi Patel",
        "Srishti Dhawan",
        "Divyam Vikash"
    ]
}

# ============================================================================
# NUMERICAL FIELD RANGES
# ============================================================================
# Expected ranges for numerical fields
NUMERICAL_RANGES = {
    "Expected TCV ($Mn) ": {"min": 5, "max": 250},
    "CRM TCV": {"min": 5, "max": 800}
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
VERBOSE_OUTPUT = True  # Show detailed progress information
