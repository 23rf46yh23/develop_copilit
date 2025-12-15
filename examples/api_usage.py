"""
Example usage of Develop Copilit API
"""

import requests
import json


def example_usage():
    """Demonstrate API usage"""
    
    base_url = "http://localhost:5000"
    
    print("Develop Copilit API Examples")
    print("=" * 60)
    
    # Example 1: Health Check
    print("\n1. Health Check")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: Make sure the server is running (python run.py)")
    
    # Example 2: Code Completion
    print("\n2. Code Completion - Python")
    print("-" * 60)
    completion_request = {
        "code": "def calculate_sum",
        "language": "python"
    }
    print(f"Request: {json.dumps(completion_request, indent=2)}")
    try:
        response = requests.post(
            f"{base_url}/api/v1/complete",
            json=completion_request
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Code Analysis
    print("\n3. Code Analysis - Python")
    print("-" * 60)
    analysis_request = {
        "code": """def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

class Calculator:
    def add(self, x, y):
        return x + y
""",
        "language": "python"
    }
    print(f"Analyzing code...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/analyze",
            json=analysis_request
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        analysis = result.get('analysis', {})
        print(f"\nAnalysis Results:")
        print(f"  - Language: {analysis.get('language')}")
        print(f"  - Lines: {analysis.get('lines')}")
        print(f"  - Functions: {analysis.get('functions')}")
        print(f"  - Classes: {analysis.get('classes')}")
        print(f"  - Issues: {len(analysis.get('issues', []))}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Template Generation - Python Function
    print("\n4. Template Generation - Python Function")
    print("-" * 60)
    template_request = {
        "type": "function",
        "language": "python",
        "name": "process_data",
        "params": "data, options"
    }
    print(f"Request: {json.dumps(template_request, indent=2)}")
    try:
        response = requests.post(
            f"{base_url}/api/v1/template",
            json=template_request
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"\nGenerated Template:")
        print(result.get('template', ''))
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Template Generation - JavaScript Class
    print("\n5. Template Generation - JavaScript Class")
    print("-" * 60)
    template_request = {
        "type": "class",
        "language": "javascript",
        "name": "UserManager"
    }
    print(f"Request: {json.dumps(template_request, indent=2)}")
    try:
        response = requests.post(
            f"{base_url}/api/v1/template",
            json=template_request
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"\nGenerated Template:")
        print(result.get('template', ''))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")


if __name__ == "__main__":
    print("\nNote: Make sure the server is running first:")
    print("  python run.py")
    print("\nThen run this script in another terminal:")
    print("  python examples/api_usage.py\n")
    
    example_usage()
