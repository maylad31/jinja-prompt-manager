# jinja-prompt-manager

This repository provides a **Jinja2-based prompt management system** with **versioning, scoring, and production selection** for LLMs (Large Language Models). Jinja2 allows for the creation of templates that can adapt based on user input or context. This flexibility is particularly useful when prompts need to change dynamically. For example, you can include conditional statements and loops directly within the template to adjust the output based on provided variables. Still some work is needed.

## ✨ Features
- **Jinja2-based templating** for dynamic prompt generation using a sandboxed Jinja2 instance
- **Versioning system** to track and score prompts and finally select the best prompts for production

## 📦 Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/maylad31/jinja-prompt-manager.git
   cd jinja-prompt-manager
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## 📜 Usage

### 1️⃣ Define and Render Prompts
Check demo.py:
```python
from jinja_env import get_environment

# Get a secured Jinja2 environment
env = get_environment()

# Define a prompt template with conditional rendering
prompt = """
{% if context %}
Context: {{ context }}
Based on the context provided above, answer the following question:
{% else %}
Answer the following question:
{% endif %}
Question: {{ question | require("question") }}
"""

# Convert template and render it
template = env.from_string(prompt)
final_prompt = template.render(question="ques", context="cont").strip()
print(final_prompt)
```

### 2️⃣ Save Prompts to Database
```python
from db import save_prompt
save_prompt(problem="rag", model_name="gpt-4", prompt=prompt)
```

### 3️⃣ Retrieve and Display All Prompts
```python
from db import get_all_prompts
all_prompts = get_all_prompts(problem="rag", model_name="gpt-4")
print(all_prompts)
```

### 4️⃣ Score and Comment on Prompts
```python
from db import update_score
update_score(problem="rag", model_name="gpt-4", version=1, score=0.4, comment="Low precision")
update_score(problem="rag", model_name="gpt-4", version=2, score=0.9, comment="High precision")
```

### 5️⃣ Set a Production Prompt
```python
from db import set_production_prompt, get_production_prompt
set_production_prompt("rag", "gpt-4", 2)
production_prompt = get_production_prompt(problem="rag", model_name="gpt-4")
print(production_prompt)
```

### 6️⃣ Delete Prompts (Optional)
```python
from db import delete_prompt, delete_all_prompts, remove_db
# Delete a specific prompt version
delete_prompt("rag", "gpt-4", 1)

# Delete all prompts for a problem/model
delete_all_prompts("rag", "gpt-4")

# Remove the database completely
remove_db()
```

## 📂 Project Structure
```
├── jinja_env.py        # Jinja2 environment setup
├── db.py               # SQLite database operations
├── main.py             # Example usage
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🛠️ Requirements
- Python 3.10+
- Jinja2

## 📝 License
This project is licensed under the MIT License.



If you have an interesting project, let's connect!
https://www.linkedin.com/in/mayankladdha31/
