from google.genai import types

tools = [
    types.Tool(
        function_declarations=[

            types.FunctionDeclaration(
                name="overall_persistency",
                description="Returns overall persistency"
            ),

            types.FunctionDeclaration(
                name="product_persistency",
                description="Returns persistency of a product",
                parameters={
                    "type": "OBJECT",
                    "properties": {"product_name": {"type": "STRING"}},
                    "required": ["product_name"]
                }
            ),

            types.FunctionDeclaration(
                name="lob_persistency",
                description="Returns persistency of a Line of Business",
                parameters={
                    "type": "OBJECT",
                    "properties": {"lob_name": {"type": "STRING"}},
                    "required": ["lob_name"]
                }
            ),

            types.FunctionDeclaration(
                name="duration_persistency",
                description="Returns persistency for a duration",
                parameters={
                    "type": "OBJECT",
                    "properties": {"duration": {"type": "INTEGER"}},
                    "required": ["duration"]
                }
            ),

            types.FunctionDeclaration(
                name="experience_analysis",
                description="Compares persistency between two periods (Oct 25 vs Jun 26), grouped by ERA, Channel, and Short/Long Pay, and flags improvements or declines."
            ),

            types.FunctionDeclaration(
                name="filtered_persistency",
                description=(
                    "Flexible persistency lookup. Use this whenever the question refers to "
                    "ERA (e.g. 'Savings_Lumpsum_ERA3', 'Protection_ERA2'), Channel (e.g. Axis, "
                    "Own, Online, Others), Short/Long Pay, or any combination of Product, Line "
                    "of Business, ERA, Channel, Pay Type, and Duration together. Prefer this "
                    "over the single-purpose tools whenever more than one filter applies, or "
                    "when the filter is ERA, Channel, or Pay Type specifically, since there is "
                    "no dedicated tool for those alone."
                ),
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "product": {"type": "STRING", "description": "Product name, e.g. SWP, SWAG, CNSSP, CNSTEP"},
                        "lob": {"type": "STRING", "description": "Line of Business, e.g. SAVINGS, PROTECTION"},
                        "era": {"type": "STRING", "description": "ERA category, e.g. Savings_Lumpsum_ERA3, Protection_ERA2"},
                        "channel": {"type": "STRING", "description": "Distribution channel, e.g. Axis, Own, Online, Others"},
                        "pay_type": {"type": "STRING", "description": "Short Pay or Long Pay"},
                        "duration": {"type": "INTEGER", "description": "Policy duration"},
                        "period": {"type": "STRING", "description": "'oct_25' or 'jun_26' to restrict to one period; omit for the latest period"}
                    }
                }
            ),

            types.FunctionDeclaration(
                name="run_assumption_setting",
                description=(
                    "Runs the full assumption-setting cycle: blends actual experience "
                    "(Oct'25 and Jun'26) with prior assumptions per ERA x Channel x "
                    "Short/Long Pay cohort, produces duration-banded proposed persistency "
                    "assumptions, and generates a Prophet-format lapse table file. Use "
                    "for requests like 'do assumption setting', 'update the Prophet "
                    "table', 'refresh assumptions', or 'set new assumptions'."
                )
            ),

            types.FunctionDeclaration(
                name="identify_red_zone",
                description=(
                    "Compares latest actual experience against the proposed assumptions "
                    "(per the assumption-setting methodology), at the exact ERA x Channel x "
                    "Short/Long Pay cohort level, for Duration 1 only. Flags cohorts where "
                    "the deviation exceeds 2 percentage points in either direction, and "
                    "generates a Prophet table with only those cohorts updated. Use for "
                    "requests like 'identify red zone', 'which cohorts are out of line with "
                    "assumptions', or 'show me problem areas'."
                )
            ),

            types.FunctionDeclaration(
                name="red_zone_product_breakdown",
                description=(
                    "Shows persistency by Product at Duration 1, comparing the latest "
                    "period against the previous period, within a single flagged ERA x "
                    "Channel x Pay Type cohort. Use to drill down on which product is "
                    "driving a flagged cohort's deviation."
                ),
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "era": {"type": "STRING", "description": "The exact ERA name, e.g. Savings_Lumpsum_ERA3"},
                        "channel": {"type": "STRING", "description": "Channel, e.g. Axis, Own, Online, Others"},
                        "pay_type": {"type": "STRING", "description": "Short Pay or Long Pay"}
                    },
                    "required": ["era", "channel", "pay_type"]
                }
            )

        ]
    )
]