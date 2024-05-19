from flask import Flask, request, jsonify, render_template
from gpt4all import GPT4All

# Using model_name to specify the GPT4All model
model = GPT4All(model_name='nous-hermes-llama2-13b.Q4_0.gguf')

app = Flask(__name__)

def generate_documentation(generated_code):
  lines = generated_code.split('\n')
  documentation = ""
  for line in lines:
    stripped_line = line.strip()
    comment_start = stripped_line.find("#")  # Find the first occurrence of a comment

    # Check for code (everything before the comment or the entire line if no comment)
    code_part = stripped_line[:comment_start] if comment_start != -1 else stripped_line  # Extract code part (excluding comment)

    # Check for function definition
    if code_part.startswith("def") and "(" in code_part and ":" in code_part:
      documentation += line  # Add code line first, no newline
      documentation += " 「Defines a function.」\n"
    elif code_part.startswith("public class") and code_part.endswith("{"):  # Handle Java class definitions
      documentation += line  # Add code line first, no newline
      documentation += " 「Defines a class.」\n"

    # Check for variable declaration
    elif code_part.startswith("int ") or code_part.startswith("float ") or \
       code_part.startswith("double ") or code_part.startswith("char ") or \
       code_part.startswith("string ") or code_part.startswith("bool "):
      documentation += line  # Add code line first, no newline
      documentation += " 「Declares a variable.」\n"

    # Check for print statements
    elif code_part.startswith("cout") or code_part.startswith("print("):
      documentation += line
      documentation += " 「Prints the content.」\n"
    elif code_part.startswith("System.out.println("):
      documentation += line  # Add code line first, no newline
      documentation += " 「Prints the content.」\n"

    # Check for other known keywords (can be extended)
    elif code_part.startswith("#include") or code_part.startswith("using namespace"):
      documentation += line
      documentation += " 「Performs an operation.」\n"
    elif code_part.startswith("int main"):
      documentation += line
      documentation += " 「Defines the main function.」\n"
    elif code_part.startswith("//"):  # Handle single-line comments in Java (optional)
      documentation += line  # Add comment line (optional)

    else:
      documentation += line  # Add code line for anything else

  return documentation



@app.route("/generate_code", methods=["POST"])
def generate_code():
    try:
        # Get user input and selected language from the request
        data = request.json
        prompt = data["prompt"]

        # Generate code using GPT4All
        generated_code = model.generate(prompt=prompt)

        # Check if generation was successful
        if generated_code:
            # Document the generated code
            documentation = generate_documentation(generated_code)  # Assuming you have a function for generating documentation

            # Return generated code and documentation
            return jsonify({"generated_code": generated_code, "documentation": documentation})
        else:
            return jsonify({"error": "Failed to generate code"}), 500
    except Exception as e:  # Catch any exception during code generation
        return jsonify({"error": f"Error generating code: {str(e)}"}), 500
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
