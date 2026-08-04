from app.data import df, df_period1, df_period2


def overall_persistency():
    numerator = df["Numerator"].sum()
    denominator = df["Denominator"].sum()

    if denominator == 0:
        return {"status": "error", "message": "Denominator is zero."}

    persistency = float(round((numerator / denominator) * 100, 2))

    return {"status": "success", "overall_persistency": persistency}


def product_persistency(product_name):
    product_name = product_name.upper().strip()
    filtered = df[df["Product_Name"] == product_name]

    if filtered.empty:
        return {"status": "error", "message": f"Product '{product_name}' not found."}

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {"status": "error", "message": "Denominator is zero."}

    persistency = float(round((numerator / denominator) * 100, 2))

    return {"status": "success", "product": product_name, "persistency": persistency}


def lob_persistency(lob_name):
    lob_name = lob_name.upper().strip()
    filtered = df[df["Line_of_business"] == lob_name]

    if filtered.empty:
        return {"status": "error", "message": f"Line of Business '{lob_name}' not found."}

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {"status": "error", "message": "Denominator is zero."}

    persistency = float(round((numerator / denominator) * 100, 2))

    return {"status": "success", "line_of_business": lob_name, "persistency": persistency}


def duration_persistency(duration):
    try:
        duration = int(duration)
    except ValueError:
        return {"status": "error", "message": "Duration must be an integer."}

    filtered = df[df["Duration"] == duration]

    if filtered.empty:
        return {"status": "error", "message": f"No data found for duration {duration}."}

    numerator = filtered["Numerator"].sum()
    denominator = filtered["Denominator"].sum()

    if denominator == 0:
        return {"status": "error", "message": "Denominator is zero."}

    persistency = float(round((numerator / denominator) * 100, 2))

    return {"status": "success", "duration": duration, "persistency": persistency}


GROUP_COLUMNS = ["ERA", "Channel", "Short_Long_Pay"]


def _persistency(frame):
    numerator = frame["Numerator"].sum()
    denominator = frame["Denominator"].sum()

    if denominator == 0:
        return None

    return float(round((numerator / denominator) * 100, 2))


def experience_analysis():
    combos = (
        df_period2[GROUP_COLUMNS]
        .drop_duplicates()
        .sort_values(GROUP_COLUMNS)
        .to_dict("records")
    )

    results = []

    for combo in combos:
        mask1 = (
            (df_period1["ERA"] == combo["ERA"]) &
            (df_period1["Channel"] == combo["Channel"]) &
            (df_period1["Short_Long_Pay"] == combo["Short_Long_Pay"])
        )
        mask2 = (
            (df_period2["ERA"] == combo["ERA"]) &
            (df_period2["Channel"] == combo["Channel"]) &
            (df_period2["Short_Long_Pay"] == combo["Short_Long_Pay"])
        )

        p1 = _persistency(df_period1[mask1])
        p2 = _persistency(df_period2[mask2])

        if p1 is None or p2 is None:
            continue

        change = round(p2 - p1, 2)
        zone = "green" if change > 0 else "red" if change < 0 else "neutral"

        results.append({
            "era": combo["ERA"],
            "channel": combo["Channel"],
            "pay_type": combo["Short_Long_Pay"],
            "persistency_period1": p1,
            "persistency_period2": p2,
            "change": change,
            "zone": zone
        })

    return {"status": "success", "results": results}


PERIOD_MAP = {
    "oct_25": df_period1,
    "jun_26": df_period2
}


def dashboard_summary():
    overall = overall_persistency()
    savings = lob_persistency("SAVINGS")
    protection = lob_persistency("PROTECTION")

    return {
        "status": "success",
        "overall_persistency": overall.get("overall_persistency"),
        "savings_persistency": savings.get("persistency"),
        "protection_persistency": protection.get("persistency")
    }


def lob_product_breakdown(lob_name, period):
    period = period.lower().strip()

    if period not in PERIOD_MAP:
        return {"status": "error", "message": "Period must be 'oct_25' or 'jun_26'."}

    frame = PERIOD_MAP[period]
    lob_name = lob_name.upper().strip()

    lob_filtered = frame[frame["Line_of_business"] == lob_name]

    if lob_filtered.empty:
        return {"status": "error", "message": f"Line of Business '{lob_name}' not found."}

    products = sorted(lob_filtered["Product_Name"].unique().tolist())
    breakdown = []

    for product in products:
        product_rows = lob_filtered[lob_filtered["Product_Name"] == product]
        numerator = product_rows["Numerator"].sum()
        denominator = product_rows["Denominator"].sum()

        if denominator == 0:
            continue

        persistency = float(round((numerator / denominator) * 100, 2))
        breakdown.append({"product": product, "persistency": persistency})

    lob_numerator = lob_filtered["Numerator"].sum()
    lob_denominator = lob_filtered["Denominator"].sum()
    lob_value = float(round((lob_numerator / lob_denominator) * 100, 2)) if lob_denominator else None

    return {
        "status": "success",
        "line_of_business": lob_name,
        "period": period,
        "lob_persistency": lob_value,
        "products": breakdown
    }


def filtered_persistency(product=None, lob=None, era=None, channel=None, pay_type=None, duration=None, period=None):
    """
    Flexible persistency lookup across any combination of Product, Line of
    Business, ERA, Channel, Short/Long Pay, and Duration. Any filter left
    out is ignored. Optionally restrict to one period ('oct_25' or
    'jun_26'); if omitted, uses the latest period.
    """

    frame = df
    filters_applied = {}

    if period:
        period = period.lower().strip()
        if period not in PERIOD_MAP:
            return {"status": "error", "message": "Period must be 'oct_25' or 'jun_26'."}
        frame = PERIOD_MAP[period]

    def apply_filter(current_frame, column, value):
        if value is None:
            return current_frame
        value_upper = str(value).strip().upper()
        filters_applied[column] = value
        return current_frame[current_frame[column].astype(str).str.upper() == value_upper]

    frame = apply_filter(frame, "Product_Name", product)
    frame = apply_filter(frame, "Line_of_business", lob)
    frame = apply_filter(frame, "ERA", era)
    frame = apply_filter(frame, "Channel", channel)
    frame = apply_filter(frame, "Short_Long_Pay", pay_type)

    if duration is not None:
        try:
            duration = int(duration)
        except ValueError:
            return {"status": "error", "message": "Duration must be an integer."}
        filters_applied["Duration"] = duration
        frame = frame[frame["Duration"] == duration]

    if not filters_applied:
        return {"status": "error", "message": "No filters were provided."}

    if frame.empty:
        return {"status": "error", "message": f"No data found matching: {filters_applied}"}

    numerator = frame["Numerator"].sum()
    denominator = frame["Denominator"].sum()

    if denominator == 0:
        return {"status": "error", "message": "Denominator is zero for this filter combination."}

    persistency = float(round((numerator / denominator) * 100, 2))

    return {
        "status": "success",
        "filters": filters_applied,
        "period": period or "latest",
        "policy_count": int(len(frame)),
        "persistency": persistency
    }

def lob_graph_data(lob, period):
    """
    Persistency by ERA x Channel x Short/Long Pay, for Duration 1 only,
    within a single Line of Business and period. Used for the dashboard
    drill-down graph.
    """

    period = period.lower().strip()

    if period not in PERIOD_MAP:
        return {"status": "error", "message": "Period must be 'oct_25' or 'jun_26'."}

    frame = PERIOD_MAP[period]
    lob = lob.upper().strip()

    lob_filtered = frame[
        (frame["Line_of_business"] == lob) &
        (frame["Duration"] == 1)
    ]

    if lob_filtered.empty:
        return {"status": "error", "message": f"No data found for Line of Business '{lob}' at Duration 1."}

    eras = sorted(lob_filtered["ERA"].unique().tolist())
    channels = sorted(lob_filtered["Channel"].unique().tolist())
    pay_types = sorted(lob_filtered["Short_Long_Pay"].unique().tolist())

    results = []

    for era in eras:
        for channel in channels:
            for pay_type in pay_types:
                combo = lob_filtered[
                    (lob_filtered["ERA"] == era) &
                    (lob_filtered["Channel"] == channel) &
                    (lob_filtered["Short_Long_Pay"] == pay_type)
                ]

                if combo.empty:
                    continue

                numerator = combo["Numerator"].sum()
                denominator = combo["Denominator"].sum()

                if denominator == 0:
                    continue

                persistency = round((numerator / denominator) * 100, 2)

                results.append({
                    "era": era,
                    "channel": channel,
                    "pay_type": pay_type,
                    "persistency": persistency
                })

    return {"status": "success", "lob": lob, "period": period, "duration": 1, "data": results}