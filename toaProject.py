from flask import Flask, request, jsonify, render_template
import ast  # Abstract Syntax Tree for parsing Python code
import re   # Regular expressions for string pattern matching
import sys
import os

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

 # Creates the Flask application instance

def check_unused_variables(code):
    warnings = []
    try:
        # Parse the code into an Abstract Syntax Tree
        tree = ast.parse(code)
        
        # Sets to track assigned and used variables
        assigned = set()
        used = set()

        # Custom AST visitor class to analyze variable usage
        class VarVisitor(ast.NodeVisitor):
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):  # Variable assignment
                    assigned.add(node.id)
                elif isinstance(node.ctx, ast.Load):  # Variable usage
                    used.add(node.id)

        # Execute the visitor pattern
        VarVisitor().visit(tree)
        
        # Find variables that were assigned but never used
        unused = assigned - used
        for var in unused:
            warnings.append(f"Warning: Variable '{var}' is assigned but never used.")
            
    except Exception as e:  # Handle any parsing errors
        warnings.append(f"Error while parsing code: {str(e)}")
    return warnings

def check_duplicate_functions(code):
    warnings = []
    try:
        tree = ast.parse(code)
        function_names = {}  # Dictionary to track function names and their line numbers

        class FuncVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if node.name in function_names:  # Check for duplicate
                    warnings.append(f"Error: Duplicate function name '{node.name}' at line {node.lineno}.")
                else:
                    function_names[node.name] = node.lineno  # Record first occurrence

        FuncVisitor().visit(tree)
    except Exception as e:
        warnings.append(f"Error while parsing code: {str(e)}")
    return warnings

def check_quote_consistency(code):
    warnings = []
    # Regex pattern to find print statements
    print_pattern = re.compile(r'print\((.*?)\)', re.DOTALL)

    # Check each print statement found
    for match in print_pattern.finditer(code):
        content = match.group(1)  # Get the content inside print()
        has_single = "'" in content
        has_double = '"' in content

        # Flag if both quote types are used
        if has_single and has_double:
            # Estimate line number by counting newlines before the match
            line = code[:match.start()].count('\n') + 1
            warnings.append(
                f"Style: Mixed quotes in print() at line ~{line}. Content: {content[:30]}{'...' if len(content) > 30 else ''}"
            )
    return warnings

@app.route('/review', methods=['POST'])
def review_code():
    # Get JSON data from request
    data = request.get_json()
    code = data.get('code', '')
    
    # Validate input
    if not code:
        return jsonify({'error': 'No code provided'}), 400  # Bad request

    # Run all checks
    results = []
    results.extend(check_unused_variables(code))
    results.extend(check_duplicate_functions(code))
    results.extend(check_quote_consistency(code))

    # Return results (or a success message if no issues)
    return jsonify({
        'analysis': results or ["No issues found. Good job!"]
    })

@app.route('/')
def home():
    # Render the HTML template for the frontend
    return render_template('index.html')

if __name__ == '__main__':
    import webbrowser
    import threading

    # Function to run Flask in a background thread
    def run_app():
        app.run(debug=False, use_reloader=False)

    # Start Flask in a new thread
    threading.Thread(target=run_app).start()

    # Automatically open the default web browser
    webbrowser.open("http://127.0.0.1:5000/")
