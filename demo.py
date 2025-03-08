from jinja_env import get_environment
from db import *

# first let's see how we can define prompts using jinja2

# let's get the sandboxed jinja environment which is more secured and we also have an additional reuire filter defined
env = get_environment()

# define prompt, use the power of jinja: include conditional rendering, placeholders, filters etc.
# this prompt will vary based on if we provide a context or not.

prompt = """
{% if context %}
Context: {{ context }}
Based on the context provided above, answer the following question:
{% else %}
Answer the following question:
{% endif %}
Question: {{ question | require("question") }}
"""

# convert prompt to template
template = env.from_string(prompt)

# render values to fill placeholders, usually you will use inputs from the user, outputs from other llms etc to fill them
final_prompt = template.render(question="ques", context="cont").strip()

# let's print the final prompt
print(final_prompt)
print("==========" * 2)

# let's try without context
final_prompt = template.render(question="ques").strip()
print(final_prompt)
print("==========" * 2)


# nice often we test a lot of prompts but how to manage them? 
# we can use a database for versioning and management
# we do versioning for a particular problem and model name

prompt1 = """
{% if context %}
Context: {{ context }}
Based on the context provided above, answer the following question:
{% else %}
Answer the following question:
{% endif %}
Question: {{ question | require("question") }}
"""
prompt2 = """
{% if context %}
Answer the question based on the context below:
Context: {{ context }}
{% else %}
Answer the following question:
{% endif %}
Question: {{ question | require("question") }}
"""

# let's print the prompt2 as well to confirm it works as expected
template = env.from_string(prompt2)
final_prompt = template.render(question="ques", context="cont").strip()
print(final_prompt)
print("==========" * 2)

# let's initialize the sqlite db and save both the prompts
initialize_db()

# our problem is rag(any problem you are testing prompts for and we are testing gpt4)

save_prompt(problem="rag", model_name="gpt-4", prompt=prompt1)
save_prompt(problem="rag", model_name="gpt-4", prompt=prompt2)
all_prompts = get_all_prompts(problem="rag", model_name="gpt-4")

# let's check
print(all_prompts)
print("==========" * 2)


"""
now you can do some testing on prompts, assign scores, comments and select one for production 
"""

# let's say i did my testing and now want to assign score of 0.4 to prompt1 
# and 0.8 to prompt2

update_score(
    problem="rag", model_name="gpt-4", version=1, score=0.4, comment="low precision"
)
update_score(
    problem="rag", model_name="gpt-4", version=2, score=0.9, comment="high precision"
)

# now we decide to set prompt 2 as production prompt for problem rag and model gpt4
# note : only one prompt can be set as production

set_production_prompt("rag", "gpt-4", 2)
production_prompt = get_production_prompt(problem="rag", model_name="gpt-4")
template = env.from_string(production_prompt)
final_prompt = template.render(question="ques", context="raise('ok')").strip()
print(final_prompt)


# we can also delete one or all prompts for a particular problem and model name


# delete_prompt("rag", "gpt-4", 1)
# delete_all_prompts("rag", "gpt-4")
# all_prompts = get_all_prompts(problem="rag", model_name="gpt-4")
# print(all_prompts)
remove_db()
