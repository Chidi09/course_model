Course Model
A lightweight, plug-and-play Python package designed to simplify how Learning Management System (LMS) developers structure course data. It provides smart presets based on school types and allows for deep customization and overrides.

Core Philosophy
"Don’t overcomplicate. Just simplify how LMS devs structure course data—based on school type—with smart presets, while allowing deeper customization."

Features
Auto-generate Structure: Quickly generate levels, subjects, and departments based on school_type presets.

Clean API: Simple functions like generate_structure() and list_school_types().

Granular Customization:

Add custom subjects or levels (custom_subjects, custom_levels).

Exclude unwanted preset entries (exclude_subjects, exclude_levels).

Define naming conventions for levels (level_pattern).

Support for hierarchical subjects/departments for university types.

Extended Output Formats:

Standard Python Dictionary/JSON (default).

DB Schema Hints (output_format='db_schema') to suggest basic column names for direct database integration.

Integration Metadata: Include optional placeholders for external_id or lms_tag on generated items.

Robustness: Basic validation for input parameters and informative error messages.

Lightweight: Install via pip, no external dependencies.

Framework Agnostic: No frameworks (like Django) are baked in.

Installation
Install the package using pip:

pip install course-model

(Note: The package name course-model is a placeholder. You might need to adjust this if the name is already taken on PyPI or if you choose a different name for your project.)

Usage
Basic Generation
from course_model import generate_structure, list_school_types

# Generate a secondary school structure
structure_secondary = generate_structure("secondary")
print("Secondary School Structure:")
print(structure_secondary)

# Generate a primary school structure
structure_primary = generate_structure("primary")
print("\nPrimary School Structure:")
print(structure_primary)

Custom Additions & Exclusions
from course_model import generate_structure

structure_uni = generate_structure(
    "university",
    custom_subjects={
        "Faculty of Engineering": {
            "Computer Engineering": ["Embedded Systems", "VLSI Design"]
        },
        "Faculty of Arts": {
            "Philosophy": ["Ethics", "Logic"]
        }
    },
    exclude_levels=["Year 4"], # Exclude a specific year
    level_pattern="Semester {i}", # Custom level naming
    integration_metadata={"external_id": "ORG123", "lms_tag": "v1"}
)
print("\nCustomized University Structure:")
print(structure_uni)

# Example with flat subjects (primary school)
structure_primary_custom = generate_structure(
    "primary",
    custom_subjects=["Fine Arts", "Music"],
    exclude_subjects=["Civic Education"],
    level_pattern="Grade {i}"
)
print("\nCustomized Primary School Structure:")
print(structure_primary_custom)

Database Schema Hints
from course_model import generate_structure

db_schema_output = generate_structure(
    "secondary",
    output_format='db_schema',
    integration_metadata={"external_id": "SEC001", "lms_tag": "current"}
)
print("\nSecondary School DB Schema Hints:")
print(db_schema_output)

Listing Available School Types
from course_model import list_school_types

available_types = list_school_types()
print("\nAvailable School Types:")
print(available_types)

Package Structure
course_model/
│
├── course_model/
│   ├── __init__.py          # Package initialization, expose API
│   ├── core.py              # Main logic, generate_structure function
│   ├── presets.py           # Preset data for each school type
│   └── utils.py             # Helper functions for customization logic, validation
│
├── setup.py                 # Package setup script
├── README.md                # This file
└── LICENSE                  # Project license

Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.# course_model
