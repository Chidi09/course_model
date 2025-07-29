# course_model/core.py

"""
This module contains the core logic for the course_model package,
including functions to generate course structures and list available school types.
"""

from .presets import preset_data
from .utils import _validate_options, _apply_customizations, _format_output


def generate_structure(school_type='secondary', **options):
    """
    Generates a course structure based on the specified school type and options.

    Args:
        school_type (str): The type of school (e.g., 'primary', 'secondary', 'university').
                           Defaults to 'secondary'.
        **options:
            custom_subjects (list or dict): Subjects to add. For university type,
                                            can be a nested dict.
            exclude_subjects (list): Subjects to remove from the preset.
            custom_levels (list): Levels to add.
            exclude_levels (list): Levels to remove from the preset.
            level_pattern (str): A pattern for level naming (e.g., "Year {i}").
                                 Must contain '{i}'.
            output_format (str): 'standard' (default) for Python dict/JSON,
                                 'db_schema' for database schema hints.
            integration_metadata (dict): Optional dictionary with 'external_id'
                                         and 'lms_tag' to include in output.

    Returns:
        dict or list: The generated course structure. Format depends on `output_format`.

    Raises:
        ValueError: If an invalid school_type is provided or options are malformed.
        TypeError: If an option has an incorrect type.
    """
    if school_type not in preset_data:
        raise ValueError(
            f"Invalid school_type: '{school_type}'. "
            f"Available types are: {', '.join(list_school_types())}"
        )

    # Validate options before proceeding
    _validate_options(options)

    # Get the base structure from presets
    base_structure = preset_data[school_type]

    # Apply customizations
    customized_structure = _apply_customizations(base_structure, options)

    # Format the output and add metadata
    final_structure = _format_output(customized_structure, options)

    return final_structure


def list_school_types():
    """
    Returns a list of available school types for which presets are defined.

    Returns:
        list: A list of strings representing available school types.
    """
    return list(preset_data.keys())

