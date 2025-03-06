from jinja2 import Template

prompt_template =  """
{% if context %}
Context: {{ context }}
Based on the context provided above, answer the following question:
{% else %}
Answer the following question:
{% endif %}
Question: {{ question | default("Default question") }}
Give a detailed and well-explained answer.
"""

template = Template(prompt_template,trim_blocks=True, lstrip_blocks=True)

#provide question and context
prompt = template.render(question="ques",context="con").strip()
print(prompt)
#provide only question
prompt = template.render(question="ques").strip()
print(prompt)
#provide nothing 
prompt = template.render().strip()
print(prompt)
