import requests

# Sample Python code to test the analyzer
code = """
x = 5
y = 10
print('Hello', x)
def test():
    pass
def test():
    pass
"""

# Send a POST request to the Flask app
response = requests.post("http://127.0.0.1:5000/review", json={"code": code})

# Print the analysis results
print(response.json())
