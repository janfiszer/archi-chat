# CHUNK_SIZE = 10000  #  Art. 29.; len(chunks[22].page_content)=20160 we don't want to many divisions in a given article, only to handle the max_token_length=2048
# CHUNK_OVERLAP = 200

CHUNK_SIZE = 2000  #  Art. 29.; len(chunks[22].page_content)=20160 we don't want to many divisions in a given article, only to handle the max_token_length=2048
CHUNK_OVERLAP = 200
NUM_CONTEXT_CHUNKS = 1  # most reasonable, and best tested for 1

LLM_TEMPERATURE = 0.1

EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.0-flash"

LOG_REMOVED_PATTERNS = True