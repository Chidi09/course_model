# course_model/utils.py

"""
This module provides utility functions for the course_model package,
handling input validation, applying customizations to preset data,
and formatting the output structure.
"""

def _validate_options(options):
    """
    Validates the input options provided to generate_structure.

    Args:
        options (dict): A dictionary of options.

    Raises:
        ValueError: If any option is invalid or malformed.
        TypeError: If an option has an incorrect type.
    """
    if not isinstance(options, dict):
        raise TypeError("Options must be a dictionary.")

    for key, value in options.items():
        if key == 'custom_subjects':
            if not isinstance(value, (list, dict)):
                raise TypeError("custom_subjects must be a list or a dictionary.")
        elif key == 'exclude_subjects':
            if not isinstance(value, list):
                raise TypeError("exclude_subjects must be a list.")
        elif key == 'custom_levels':
            if not isinstance(value, list):
                raise TypeError("custom_levels must be a list.")
        elif key == 'exclude_levels':
            if not isinstance(value, list):
                raise TypeError("exclude_levels must be a list.")
        elif key == 'level_pattern':
            if not isinstance(value, str):
                raise TypeError("level_pattern must be a string.")
            if "{i}" not in value:
                raise ValueError("level_pattern must contain '{i}' placeholder.")
        elif key == 'output_format':
            if value not in ['standard', 'db_schema']:
                raise ValueError("output_format must be 'standard' or 'db_schema'.")
        elif key == 'integration_metadata':
            if not isinstance(value, dict):
                raise TypeError("integration_metadata must be a dictionary.")
            if not all(k in value for k in ['external_id', 'lms_tag']):
                raise ValueError("integration_metadata must contain 'external_id' and 'lms_tag'.")
        # Add more validation for other options if needed
        else:
            # Allow unknown options to be passed through, but log a warning if desired
            pass


def _apply_customizations(preset_structure, options):
    """
    Applies custom additions, exclusions, and naming conventions to the
    preset course structure.

    Args:
        preset_structure (dict): The base structure from presets.py.
        options (dict): Customization options provided by the user.

    Returns:
        dict: The customized course structure.
    """
    customized_structure = {
        "levels": list(preset_structure.get("levels", [])),
        "subjects": _deep_copy_subjects(preset_structure.get("subjects", {}))
    }

    # Apply level customizations
    if 'custom_levels' in options:
        customized_structure["levels"].extend(options['custom_levels'])
        # Ensure uniqueness
        customized_structure["levels"] = list(dict.fromkeys(customized_structure["levels"]))

    if 'exclude_levels' in options:
        customized_structure["levels"] = [
            level for level in customized_structure["levels"]
            if level not in options['exclude_levels']
        ]

    if 'level_pattern' in options and customized_structure["levels"]:
        num_levels = len(customized_structure["levels"])
        customized_structure["levels"] = [
            options['level_pattern'].format(i=i + 1) for i in range(num_levels)
        ]

    # Apply subject customizations
    if 'custom_subjects' in options:
        if isinstance(customized_structure["subjects"], dict):
            # For hierarchical subjects (e.g., university)
            _merge_nested_subjects(customized_structure["subjects"], options['custom_subjects'])
        elif isinstance(customized_structure["subjects"], list):
            # For flat subjects (e.g., primary)
            if isinstance(options['custom_subjects'], list):
                customized_structure["subjects"].extend(options['custom_subjects'])
                customized_structure["subjects"] = list(dict.fromkeys(customized_structure["subjects"]))
            else:
                # Log warning or raise error if custom_subjects type doesn't match
                pass # For simplicity, we'll assume matching types or handle gracefully

    if 'exclude_subjects' in options:
        if isinstance(customized_structure["subjects"], dict):
            # For hierarchical subjects
            _filter_nested_subjects(customized_structure["subjects"], options['exclude_subjects'])
        elif isinstance(customized_structure["subjects"], list):
            # For flat subjects
            customized_structure["subjects"] = [
                subject for subject in customized_structure["subjects"]
                if subject not in options['exclude_subjects']
            ]

    return customized_structure


def _deep_copy_subjects(subjects):
    """
    Helper to deep copy subject structures, handling lists and nested dictionaries.
    """
    if isinstance(subjects, dict):
        return {k: _deep_copy_subjects(v) for k, v in subjects.items()}
    elif isinstance(subjects, list):
        return list(subjects)
    else:
        return subjects


def _merge_nested_subjects(target_dict, source_dict):
    """
    Recursively merges source_dict into target_dict for nested subject structures.
    Handles lists of subjects at the deepest level.
    """
    for key, value in source_dict.items():
        if isinstance(value, dict) and key in target_dict and isinstance(target_dict[key], dict):
            _merge_nested_subjects(target_dict[key], value)
        elif isinstance(value, list) and key in target_dict and isinstance(target_dict[key], list):
            target_dict[key].extend(value)
            target_dict[key] = list(dict.fromkeys(target_dict[key])) # Ensure uniqueness
        else:
            target_dict[key] = value


def _filter_nested_subjects(target_dict, exclude_list):
    """
    Recursively filters subjects from a nested dictionary structure.
    """
    for key, value in target_dict.items():
        if isinstance(value, dict):
            _filter_nested_subjects(value, exclude_list)
        elif isinstance(value, list):
            target_dict[key] = [s for s in value if s not in exclude_list]


def _format_output(structure, options):
    """
    Formats the output structure based on the specified output_format
    and adds integration metadata.

    Args:
        structure (dict): The processed course structure.
        options (dict): Options including output_format and integration_metadata.

    Returns:
        dict or list: The formatted course structure.
    """
    output_format = options.get('output_format', 'standard')
    integration_metadata = options.get('integration_metadata', {})

    if output_format == 'standard':
        # Add metadata to each level/subject if provided
        final_structure = {
            "levels": [],
            "subjects": None # Will be set below
        }

        for level in structure["levels"]:
            level_entry = {"name": level}
            if integration_metadata:
                level_entry.update(integration_metadata)
            final_structure["levels"].append(level_entry)

        if isinstance(structure["subjects"], dict):
            final_structure["subjects"] = _add_metadata_to_nested_subjects(
                structure["subjects"], integration_metadata
            )
        elif isinstance(structure["subjects"], list):
            final_structure["subjects"] = []
            for subject in structure["subjects"]:
                subject_entry = {"name": subject}
                if integration_metadata:
                    subject_entry.update(integration_metadata)
                final_structure["subjects"].append(subject_entry)
        else:
            final_structure["subjects"] = structure["subjects"] # Handle None or other types

        return final_structure

    elif output_format == 'db_schema':
        db_schema_output = {
            "levels_table": [],
            "subjects_table": []
        }

        # Levels table schema hint
        for i, level_name in enumerate(structure["levels"]):
            level_entry = {
                "level_name": level_name,
                "level_order": i + 1,
                "external_id": integration_metadata.get('external_id', ''),
                "lms_tag": integration_metadata.get('lms_tag', '')
            }
            db_schema_output["levels_table"].append(level_entry)

        # Subjects table schema hint
        if isinstance(structure["subjects"], dict):
            _flatten_nested_subjects_for_db(
                structure["subjects"],
                db_schema_output["subjects_table"],
                integration_metadata
            )
        elif isinstance(structure["subjects"], list):
            for subject_name in structure["subjects"]:
                subject_entry = {
                    "subject_name": subject_name,
                    "external_id": integration_metadata.get('external_id', ''),
                    "lms_tag": integration_metadata.get('lms_tag', '')
                }
                db_schema_output["subjects_table"].append(subject_entry)

        return db_schema_output
    else:
        # This case should ideally be caught by _validate_options
        return structure # Fallback to original structure


def _add_metadata_to_nested_subjects(subjects_dict, metadata):
    """
    Recursively adds metadata to each subject in a nested dictionary structure.
    """
    new_dict = {}
    for key, value in subjects_dict.items():
        if isinstance(value, dict):
            new_dict[key] = _add_metadata_to_nested_subjects(value, metadata)
        elif isinstance(value, list):
            new_list = []
            for subject in value:
                subject_entry = {"name": subject}
                if metadata:
                    subject_entry.update(metadata)
                new_list.append(subject_entry)
            new_dict[key] = new_list
        else:
            new_dict[key] = value # Should not happen with current structure
    return new_dict


def _flatten_nested_subjects_for_db(subjects_dict, subject_list, metadata,
                                     faculty=None, department=None):
    """
    Recursively flattens nested subjects into a list suitable for a DB table,
    adding faculty and department context.
    """
    for key, value in subjects_dict.items():
        if isinstance(value, dict):
            # This is a faculty or department
            if faculty is None: # This level is a faculty
                _flatten_nested_subjects_for_db(value, subject_list, metadata, faculty=key)
            else: # This level is a department
                _flatten_nested_subjects_for_db(value, subject_list, metadata, faculty=faculty, department=key)
        elif isinstance(value, list):
            # This is a list of subjects
            for subject_name in value:
                subject_entry = {
                    "subject_name": subject_name,
                    "faculty_name": faculty if faculty else '',
                    "department_name": department if department else '',
                    "external_id": metadata.get('external_id', ''),
                    "lms_tag": metadata.get('lms_tag', '')
                }
                subject_list.append(subject_entry)

