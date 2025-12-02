"""
Utility functions for data analysis and processing
"""
import pandas as pd
import json
import os
from typing import Dict, Any




def print_section_header(title: str, width: int = 80) -> None:
    """
    Print a formatted section header
    
    Args:
        title: Title of the section
        width: Width of the header line
    """
    print("\n" + "=" * width)
    print(title.upper())
    print("=" * width)


def print_subsection_header(title: str, width: int = 80) -> None:
    """
    Print a formatted subsection header
    
    Args:
        title: Title of the subsection
        width: Width of the header line
    """
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def print_success(message: str) -> None:
    """Print a success message"""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message"""
    print(f"✗ {message}")


def print_warning(message: str) -> None:
    """Print a warning message"""
    print(f"⚠ {message}")


def print_info(message: str) -> None:
    """Print an info message"""
    print(f"ℹ {message}")
