import pandas as pd

file_name = 'data/Financebench.csv'
df = pd.read_csv(file_name)

print(list(df.columns))
print(df.head())
# Dummy dataset class for illustration purposes
from torch.utils.data import Dataset, DataLoader
class QADataset(Dataset):
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        question = self.df.iloc[idx]['question']
        doc_link = self.df.iloc[idx]['doc_link']

        # Load and preprocess PDF context
        context = self.load_pdf_context(doc_link)

        answer = self.df.iloc[idx]['answer']

        return {
            "input_text": question,
            "context": context,
            "target": answer
        }

    def load_pdf_context(self, doc_link):
        # Download PDF from the provided link
        response = requests.get(doc_link)
        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        # Extract text from the PDF
        pdf_document = fitz.open("temp.pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        pdf_document.close()
        return text


import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration, RagSequenceForGeneration

import requests
import fitz  # PyMuPDF

# print('tokenizing')
# tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")

# print('Retreiecin...')
# retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq",  index_name="legacy",use_dummy_dataset=False,trust_remote_code=True )
# model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

#acebook/rag-sequence-base

from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-base")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-base")
model = RagTokenForGeneration.from_pretrained("facebook/rag-sequence-base", retriever=retriever)
print("--------------------------------")

dataset = QADataset(df)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

# Initialize optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Train the model
train_model(model, dataloader, optimizer, num_epochs=3)

sample_query = 'Is 3M a capital-intensive business based on FY2022 data?'
input_dict = tokenizer.prepare_seq2seq_batch("how many countries are in europe", return_tensors="pt") 

generated = model.generate(input_ids=input_dict["input_ids"]) 
print(tokenizer.batch_decode(generated, skip_special_tokens=True)[0]) 