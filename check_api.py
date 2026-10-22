"""Quick check that the Gemini API key works for both the embedding model and the LLM."""
import os
import sys

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from config import local, parameters


def main():
    api_key = local.GENAI_API_KEY or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("FAIL: no API key - set GENAI_API_KEY in config/local.py or the GOOGLE_API_KEY env variable")
        return 1

    failed = False

    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=parameters.EMBEDDING_MODEL, api_key=api_key)
        vector = embeddings.embed_query("test")
        print(f"OK:   embeddings ({parameters.EMBEDDING_MODEL}), vector dim {len(vector)}")
    except Exception as e:
        print(f"FAIL: embeddings ({parameters.EMBEDDING_MODEL}): {e}")
        failed = True

    try:
        llm = ChatGoogleGenerativeAI(model=parameters.LLM_MODEL, api_key=api_key, temperature=0)
        response = llm.invoke("Reply with the single word: pong")
        # newer Gemini models return `content` as a list of blocks, `.text` joins the text ones
        print(f"OK:   LLM ({parameters.LLM_MODEL}), response: {response.text.strip()!r}")
    except Exception as e:
        print(f"FAIL: LLM ({parameters.LLM_MODEL}): {e}")
        failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
