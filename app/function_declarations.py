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

                    "type":"OBJECT",

                    "properties":{

                        "product_name":{

                            "type":"STRING"

                        }

                    },

                    "required":["product_name"]

                }

            ),

            types.FunctionDeclaration(

                name="lob_persistency",

                description="Returns persistency of a Line of Business",

                parameters={

                    "type":"OBJECT",

                    "properties":{

                        "lob_name":{

                            "type":"STRING"

                        }

                    },

                    "required":["lob_name"]

                }

            ),

            types.FunctionDeclaration(

                name="duration_persistency",

                description="Returns persistency for a duration",

                parameters={

                    "type":"OBJECT",

                    "properties":{

                        "duration":{

                            "type":"INTEGER"

                        }

                    },

                    "required":["duration"]

                }

            )

        ]

    )

]