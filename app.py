import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


log_file = "log.txt"
log_message = ""
with open(log_file, "r") as file:
    log_message = file.read()
    
#TODO convert this code to a api to not need to read the file
    
def main():
    agent_template = """Analise o log a seguir e explique a causa e a localização do erro, 
    caso tenha uma solução obvia explique-a com detalhes, caso necessite de mais detalhes solicite
    
    log: 
    {log_content}
    """

    load_dotenv()
    base_url = os.getenv("LMSTUDIO_API_BASE_URL")
    api_key = os.getenv("LMSTUDIO_API_KEY")
    if not base_url:
        print("Configure LMSTUDIO_API_BASE_URL no arquivo .env")
        return

    print(f"Usando base URL: {base_url}")

    llm = ChatOpenAI(
        openai_api_base=base_url,
        openai_api_key=api_key,
        model_name="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    )
    
    prompt = ChatPromptTemplate.from_template(agent_template)

    chain = prompt | llm | StrOutputParser()
    try:
        response = chain.invoke({"log_content": log_message})
        print("Resposta:\n", response)
    except Exception as e:
        print(f"Erro de conexão com LMStudio ({base_url}): {e}")

if __name__ == "__main__":
    main()