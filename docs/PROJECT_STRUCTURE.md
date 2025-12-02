# Project Structure

## Clean Directory Layout

```
POC - Probability Tool/
│
├── main.py                      # ⭐ Main entry point - Run this!
├── README.md                    # Complete documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── verify_structure.py          # Structure verification
│
├── config/                      # 📁 Configuration
│   ├── __init__.py
│   └── settings.py              # API key, paths, parameters
│
├── src/                         # 📁 Source Code
│   ├── data_analyzer.py         # Analyze source Excel
│   ├── data_generator.py        # Generate synthetic data
│   └── data_validator.py        # Validate output
│
├── utils/                       # 📁 Utilities
│   ├── __init__.py
│   └── helpers.py               # Helper functions
│
├── data/                        # 📁 Data
│   ├── input/                   # Source Excel files
│   │   ├── .gitkeep
│   │   └── CY2025_Gap Analysis_v1.1.xlsx
│   ├── output/                  # Generated files
│   │   └── .gitkeep
│   └── cache/                   # Analysis cache
│       └── .gitkeep
│
└── docs/                        # 📁 Documentation
    └── API_SETUP.md             # API setup guide
```

## Quick Start

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API key to config/settings.py
# GEMINI_API_KEY = "your-key-here"

# 3. Run
python main.py
```

## Files Overview

### Core Files
- **main.py** - Interactive entry point with setup checks
- **README.md** - Comprehensive project documentation
- **requirements.txt** - Python package dependencies
- **verify_structure.py** - Verify project structure

### Configuration
- **config/settings.py** - All settings (API, paths, parameters)

### Source Code
- **src/data_analyzer.py** - Analyzes source Excel file
- **src/data_generator.py** - Generates synthetic data via Gemini API
- **src/data_validator.py** - Validates generated data quality

### Utilities
- **utils/helpers.py** - Common helper functions

### Documentation
- **docs/API_SETUP.md** - Detailed API setup instructions

## Total Files
- **5** root files
- **2** config files
- **3** source files
- **2** utility files
- **1** documentation file
- **3** data directories with placeholders

**Total: 13 essential files + 3 directories**
