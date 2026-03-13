def detect_conflicts(inspection_text: str, thermal_text: str):
    """
    Detect conflicts between inspection observations and thermal data
    """

    conflicts = []

    inspection_text_lower = inspection_text.lower()
    thermal_text_lower = thermal_text.lower()

    # Moisture conflict
    if "moisture" in inspection_text_lower and "no moisture" in thermal_text_lower:
        conflicts.append(
            "Inspection report indicates moisture presence, but thermal report states no moisture detected."
        )

    # Temperature anomaly conflict
    if "temperature anomaly" in thermal_text_lower and "no issue" in inspection_text_lower:
        conflicts.append(
            "Thermal report indicates temperature anomaly, but inspection report mentions no visible issue."
        )

    # Leakage conflict
    if "leak" in inspection_text_lower and "normal temperature" in thermal_text_lower:
        conflicts.append(
            "Inspection report indicates possible leakage, but thermal readings appear normal."
        )

    if len(conflicts) == 0:
        conflicts.append("No major conflicts detected between inspection and thermal reports.")

    return conflicts