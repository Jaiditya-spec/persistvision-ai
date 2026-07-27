from app.data import df


def overall_persistency():
    """
    Returns the overall persistency.
    """

    numerator = df["Numerator"].sum()
    denominator = df["Denominator"].sum()

    if denominator == 0:
        return {
            "status": "error",
            "message": "Denominator is zero."
        }

    persistency = float(round((numerator / denominator) * 100, 2))

    return {
        "status": "success",
        "overall_persistency": persistency
    }


def product_persistency(product_name):
    """
    Returns persistency for a given product.
    """

    product_name = product_name.upper().strip()

    filtered = df[df["Product_Name"] == product_name]

    if filtered.empty:
        return {
            "status": "error",
            "message": f"Product '{product_name}' not found."
        }

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {
            "status": "error",
            "message": "Denominator is zero."
        }

    persistency = float(round((numerator / denominator) * 100, 2))

    return {
        "status": "success",
        "product": product_name,
        "persistency": persistency
    }


def lob_persistency(lob_name):
    """
    Returns persistency for a Line of Business.
    """

    lob_name = lob_name.upper().strip()

    filtered = df[df["Line_of_business"] == lob_name]

    if filtered.empty:
        return {
            "status": "error",
            "message": f"Line of Business '{lob_name}' not found."
        }

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {
            "status": "error",
            "message": "Denominator is zero."
        }

    persistency = float(round((numerator / denominator) * 100, 2))

    return {
        "status": "success",
        "line_of_business": lob_name,
        "persistency": persistency
    }


def duration_persistency(duration):
    """
    Returns persistency for a given duration.
    """

    try:
        duration = int(duration)
    except ValueError:
        return {
            "status": "error",
            "message": "Duration must be an integer."
        }

    filtered = df[df["Duration"] == duration]

    if filtered.empty:
        return {
            "status": "error",
            "message": f"No data found for duration {duration}."
        }

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {
            "status": "error",
            "message": "Denominator is zero."
        }

    persistency = float(round((numerator / denominator) * 100, 2))

    return {
        "status": "success",
        "duration": duration,
        "persistency": persistency
    }