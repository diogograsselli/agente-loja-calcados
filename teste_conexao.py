import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carrega as variáveis do ficheiro .env
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

print("Testando conexão com a Azure OpenAI...")

try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )

    resposta = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "Você é um assistente prestativo."},
            {"role": "user", "content": "Olá! Diga apenas: Conexão realizada com sucesso!"}
        ],
        max_completion_tokens=50
    )

    print("\n--- RESPOSTA DA AZURE ---")
    print(resposta.choices[0].message.content)
    print("-------------------------")

except Exception as erro:
    print("\nOcorreu um erro na conexão:")
    print(erro)