import pandas as pd
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

# Load your dataset
# data = [['financebench_id_03029', '3M_2018_10K', 'doc_link', 'doc_period', 'question_type', 'question', 'answer', 'evidence_text', 'page_number']]
# columns = ['financebench_id', 'doc_name', 'doc_link', 'doc_period', 'question_type', 'question', 'answer', 'evidence_text', 'page_number']
df = pd.read_csv('data/FinancialBench.csv')

# Prepare the context for the RAG model
contexts = df.apply(lambda row: f"{row['doc_name']} - {row['evidence_text']}", axis=1).tolist()

# Initialize the RAG tokenizer and retriever
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_name="financebench")

# Encode the documents and create a retriever index
index = retriever.index(contexts)

# Define a function to answer user queries
def answer_question(user_query):
    # Encode the user query
    inputs = tokenizer(user_query, return_tensors="pt")

    # Use the retriever to find relevant documents
    retriever_results = retriever.retrieve(inputs["input_ids"].numpy(), index=index)
    context_input_ids = retriever_results["context_input_ids"]

    # Generate an answer using the RAG model
    generator = RagSequenceForGeneration.from_pretrained("facebook/rag-token-base")
    outputs = generator.generate(context_input_ids)

    # Decode and return the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Example usage
user_query = "What is the financial information for 3M in 2018?"
result = answer_question(user_query)
print("Answer:", result)
