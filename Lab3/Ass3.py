import json
import math
from datetime import datetime
import csv
import os

# Tool implementations

def calculator(expression: str) -> float:
    """Evaluates arithmetic expressions in a restricted namespace."""
    allowed_names = {
        "sqrt": math.sqrt,
        "pow": math.pow,
        "pi": math.pi,
        "__builtins__": None
    }
    return eval(expression, allowed_names, {})

def days_between(d1: str, d2: str) -> int:
    """Returns the whole number of days between two dates."""
    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(d1, date_format)
    date2 = datetime.strptime(d2, date_format)
    delta = date2 - date1
    return abs(delta.days)

def unit_convert(value: float, frm: str, to: str) -> float:
    """Converts a value between km/miles, kg/lb or C/F."""
    conversions = {
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x / 0.621371,
        ("kg", "lb"): lambda x: x * 2.20462,
        ("lb", "kg"): lambda x: x / 2.20462,
        ("C", "F"): lambda x: (x * 9/5) + 32,
        ("F", "C"): lambda x: (x - 32) * 5/9,
    }
    key = (frm, to)
    if key in conversions:
        return conversions[key](value)
    else:
        raise ValueError(f"Unsupported conversion from {frm} to {to}")

def csv_column_mean(filepath: str, column_name: str) -> float:
    """Reads a CSV file and returns the mean of a named column."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if column_name not in reader.fieldnames:
            raise ValueError(f"Column '{column_name}' not found in CSV")
        
        total = 0.0
        count = 0
        for row in reader:
            val = row[column_name]
            if val is not None and val.strip() != "":
                total += float(val)
                count += 1
        
        if count == 0:
            return 0.0
        return total / count

# Tool Registry
TOOL_REGISTRY = {
    "calculator": calculator,
    "days_between": days_between,
    "unit_convert": unit_convert,
    "csv_column_mean": csv_column_mean
}

# JSON Schemas for tools
TOOL_SCHEMAS = [
    {
        "name": "calculator",
        "description": "Value of an arithmetic expression evaluated in a restricted namespace (sqrt, pow, pi)",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "days_between",
        "description": "Whole number of days between the two dates",
        "parameters": {
            "type": "object",
            "properties": {
                "d1": {
                    "type": "string",
                    "description": "First date (ISO YYYY-MM-DD)"
                },
                "d2": {
                    "type": "string",
                    "description": "Second date (ISO YYYY-MM-DD)"
                }
            },
            "required": ["d1", "d2"]
        }
    },
    {
        "name": "unit_convert",
        "description": "The value converted between km/miles, kg/lb or C/F",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "Value to convert"
                },
                "frm": {
                    "type": "string",
                    "description": "Source unit (km, miles, kg, lb, C, F)"
                },
                "to": {
                    "type": "string",
                    "description": "Target unit (km, miles, kg, lb, C, F)"
                }
            },
            "required": ["value", "frm", "to"]
        }
    },
    {
        "name": "csv_column_mean",
        "description": "Reads a CSV file and returns the mean of a named column",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the CSV file"
                },
                "column_name": {
                    "type": "string",
                    "description": "Name of the column to calculate the mean for"
                }
            },
            "required": ["filepath", "column_name"]
        }
    }
]

# Dispatch function with error handling (Exercise 1)
def dispatch(tool_call_json: str) -> dict:
    try:
        call_data = json.loads(tool_call_json)
    except json.JSONDecodeError as e:
        return {"error": "Malformed JSON", "details": str(e)}

    # Ensure required structure
    if not isinstance(call_data, dict) or "name" not in call_data or "arguments" not in call_data:
        return {"error": "Invalid call format", "details": "Requires 'name' and 'arguments' keys"}

    tool_name = call_data["name"]
    arguments = call_data["arguments"]

    if tool_name not in TOOL_REGISTRY:
        return {"error": "Unknown tool name", "details": f"Tool '{tool_name}' is not registered."}

    tool_func = TOOL_REGISTRY[tool_name]
    
    try:
        result = tool_func(**arguments)
        return {"observation": result}
    except TypeError as e:
        return {"error": "Wrong argument name or types", "details": str(e)}
    except Exception as e:
        return {"error": "Exception raised inside tool", "details": str(e)}

if __name__ == "__main__":
    print("--- Tool Schemas ---")
    print(json.dumps(TOOL_SCHEMAS, indent=2))
    print("\n--- Scripted Sequence of Tool Calls ---")
    
    calls = [
        # Normal calls
        {"name": "calculator", "arguments": {"expression": "pow(2, 3) + sqrt(16)"}},
        {"name": "days_between", "arguments": {"d1": "2023-01-01", "d2": "2023-12-31"}},
        {"name": "unit_convert", "arguments": {"value": 100, "frm": "km", "to": "miles"}},
        
        # Malformed JSON (Exercise 1)
        '{"name": "calculator", "arguments": {"expression": "1+1"', 
        
        # Unknown tool name (Exercise 1)
        {"name": "weather_api", "arguments": {"location": "London"}},
        
        # Wrong argument name (Exercise 1)
        {"name": "calculator", "arguments": {"expr": "1+1"}},
        
        # Exception inside tool (Exercise 1)
        {"name": "calculator", "arguments": {"expression": "1/0"}},
    ]
    
    for call in calls:
        if isinstance(call, dict):
            call_json = json.dumps(call)
        else:
            call_json = call
            
        print(f"\nCall: {call_json}")
        observation = dispatch(call_json)
        print(f"Observation: {json.dumps(observation, indent=2)}")

    print("\n--- Exercise 2: Register a 4th tool ---")
    # Setup dummy CSV
    csv_file = "test_data.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "score"])
        writer.writerow([1, 80])
        writer.writerow([2, 90])
        writer.writerow([3, 100])
        
    csv_call = {"name": "csv_column_mean", "arguments": {"filepath": csv_file, "column_name": "score"}}
    csv_call_json = json.dumps(csv_call)
    
    print(f"\nCall: {csv_call_json}")
    csv_observation = dispatch(csv_call_json)
    print(f"Observation: {json.dumps(csv_observation, indent=2)}")
    
    # Cleanup dummy CSV
    if os.path.exists(csv_file):
        os.remove(csv_file)
