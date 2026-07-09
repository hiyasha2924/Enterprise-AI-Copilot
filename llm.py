"""from query_engine import search_chunks, build_prompt_from_chunks

def ask_llm(user_query):
    chunks = search_chunks(user_query)
    final_prompt = build_prompt_from_chunks(user_query, chunks)

    # Now use llama3 (Ollama)
    import subprocess
    result = subprocess.run(
        ["ollama", "run", "llama3", final_prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()
"""



import subprocess

def ask_llm(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode(),
            capture_output=True
        )
        output = result.stdout.decode()
        if ">" in output:
            output = output.split(">", 1)[-1].strip()
        return output.strip()
    except Exception as e:
        return f"❌ LLM Error:\n{e}"



#for using openrouter
""" 

import requests

def ask_llm(prompt):
    api_key = "sk-or-v1-f452ca385b82414b685ab5f27c60cd22686cb900b7bc771731c9cc0ae44"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://your-cluely-app.com",  # can be anything
        "X-Title": "Cluely Assistant"
    }

    body = {
        "model": "deepseek-chat:free",  # ✅ free model from OpenRouter
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ LLM API error: {e}"
"""