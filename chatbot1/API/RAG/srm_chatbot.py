# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# """
# Converted Jupyter Notebook (srm_chatbot.ipynb) to Python Script.

# This script builds and runs a Retrieval-Augmented Generation (RAG)
# system using LangChain, Ollama, and FAISS.

# It loads PDF documents, chunks them, creates vector embeddings,
# and sets up a retrieval chain.

# The script will continuously ask for user queries and provide answers
# until the user enters '987654321' to quit.

# NOTE: Please update the file paths in the 'pdf_paths' list
# to match the locations on your local machine.
# """

# # Imports from the notebook
# import os
# import sys
# import bs4
# import langchain
# from dotenv import load_dotenv
# from langchain_community.document_loaders import TextLoader, WebBaseLoader, PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.llms import Ollama
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# # Helper function from the notebook
# def format_docs(docs):
#     """Helper function to format documents for the context."""
#     return "\n\n".join(doc.page_content for doc in docs)

# def main():
#     """Main function to run the RAG chatbot."""
    
#     # --- Cell 1: TextLoader (Informational) ---
#     # data injestion steps how can we learn from rom a data source like a web page, pdf, txt file and more
#     print("Attempting to load text document (as per original notebook)...")
#     try:
#         # in the quotation is the name of the file that the loader is going to read
#         loader_txt = TextLoader(r"D:\Download\Report on the Development of a Lang.txt")
#         text_documents = loader_txt.load()
#         print(f"Loaded {len(text_documents)} text document.")
#         # print(text_documents) # Uncomment to display the loaded text document
#     except Exception as e:
#         print(f"Could not load text file: {e}")
#         print("This file is not essential for the main RAG chain.")
    
#     # --- Cell 2: API Key Loading ---
#     print("\n--- Loading Environment Variables ---")
#     load_dotenv()
#     gemini_key = os.environ.get('GEMINI_API_KEY')
#     if gemini_key:
#         os.environ['GEMINI_API_KEY'] = gemini_key
#         print("GEMINI_API_KEY loaded successfully.")
#     else:
#         # Not raising a ValueError to allow the script to proceed
#         # as it seems to be using local Ollama, not Gemini.
#         print("GEMINI_API_KEY not found in .env. Proceeding...")

#     # --- Cell 3: WebBaseLoader (Defined, but not used to load) ---
#     # This list now contains all 172 unique URLs you provided
#     srm_urls = [
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1760608493END-TERM-NOV-2025-EXAMINATION-CIRCULAR-AND-ARREAR-FORM.pdf',
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1760348856FINAL-SCHEULE-OCTOBER-2025.pdf',
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1759745185Schedule-Timeline-for-the-collection-of-Grade-Card-MAY-2025.pdf',
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1759481955CIRCULAR-and-Form-SPECIAL-MERCY-OCTOBER-2025.pdf',
#         'https://srmuniversity.ac.in/center-of-excellence',
#         'https://srmuniversity.ac.in/examination',
#         'https://erpsrm.com/srmparentportal/parents/loginManager/youLogin.jsp',
#         'https://erpsrm.com/srmhonline/students/loginManager/youLogin.jsp',
#         'https://erpsrm.com/srmhonline/srmhalumni/loginManager/youLogin.jsp',
#         'https://erpsrm.com/evarsitysrmh/usermanager/loginManager/youLogin.jsp',
#         'https://srmuniversity.ac.in/third-convocation',
#         'https://srmuniversity.ac.in/feekart',
#         'https://srmuniversity.ac.in/downloads',
#         'https://srmuniversity.ac.in/faq',
#         'https://wa.me/918816033306?text=Hi',
#         'https://www.facebook.com/SRMUniversityDelhiNCR/',
#         'https://twitter.com/SRMH_University',
#         'https://www.linkedin.com/company/srm-university-haryana/',
#         'https://youtu.be/H0VRcAds2UM',
#         'https://www.instagram.com/srmuniversity.delhi/',
#         'https://srmuniversity.ac.in/blog/',
#         'https://admissions.srmuniversity.ac.in/',
#         'https://srmuniversity.ac.in/',
#         'https://srmuniversity.ac.in/srm-heritage',
#         'https://srmuniversity.ac.in/vision-mission',
#         'https://srmuniversity.ac.in/sponsoring-body',
#         'https://srmuniversity.ac.in/institutional-development-plan-idp',
#         'https://srmuniversity.ac.in/mandatory-disclosure',
#         'https://srmuniversity.ac.in/regulatory-approvals-recognitions',
#         'https://srmuniversity.ac.in/accreditation-rankings',
#         'https://srmuniversity.ac.in/annual-reports',
#         'https://srmuniversity.ac.in/annual-audited-account-report',
#         'https://srmuniversity.ac.in/public-self-disclosure-by-hei',
#         'https://srmuniversity.ac.in/chancellor',
#         'https://srmuniversity.ac.in/vice-chancellor',
#         'https://srmuniversity.ac.in/pro-vice-chancellor',
#         'https://srmuniversity.ac.in/registrar',
#         'https://srmuniversity.ac.in/finance-officer',
#         'https://srmuniversity.ac.in/controller-of-examination',
#         'https://srmuniversity.ac.in/ombudsperson-sgrc',
#         'https://srmuniversity.ac.in/srmu-statutory-bodies',
#         'https://srmuniversity.ac.in/statutory-committees',
#         'https://srmuniversity.ac.in/board-of-studies-bos',
#         'https://srmuniversity.ac.in/academic-leadership',
#         'https://srmuniversity.ac.in/website/#',
#         'https://srmuniversity.ac.in/undergraduate-programmes',
#         'https://srmuniversity.ac.in/postgraduate-programmes',
#         'https://srmuniversity.ac.in/ug-pg-integrated-programmes',
#         'https://srmuniversity.ac.in/ph-d-programmes',
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1756529151Academic-Calender-2025-26.pdf',
#         'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1757405130Academic-Planner-2025-26.pdf',
#         'https://srmuniversity.ac.in/download-brochure',
#         'https://srmuniversity.ac.in/internal-quality-assurance-cell-iqac',
#         'https://srmuniversity.ac.in/srmuh-library',
#         'https://srmuniversity.ac.in/affiliation-collaborations',
#         'https://srmuniversity.ac.in/international-collaborations',
#         'https://srmuniversity.ac.in/department/department-of-computer-science-engineering-cse',
#         'https://srmuniversity.ac.in/department/department-of-biomedical-engineering',
#         'https://srmuniversity.ac.in/department/department-of-civil-engineering',
#         'https://srmuniversity.ac.in/department/department-of-electrical-electronics-engineering',
#         'https://srmuniversity.ac.in/department/department-of-electronics-communication-engineering',
#         'https://srmuniversity.ac.in/department/department-of-mechanical-engineering',
#         'https://srmuniversity.ac.in/department/department-of-finance-commerce',
#         'https://srmuniversity.ac.in/department/department-of-hotel-management',
#         'https://srmuniversity.ac.in/department/department-of-law',
#         'https://srmuniversity.ac.in/department/department-of-management-studies',
#         'https://srmuniversity.ac.in/department/department-of-agriculture',
#         'https://srmuniversity.ac.in/department/department-of-biotechnology',
#         'https://srmuniversity.ac.in/department/department-of-chemistry',
#         'https://srmuniversity.ac.in/department/department-of-computer-sciences',
#         'https://srmuniversity.ac.in/department/department-of-environmental-sciences',
#         'https://srmuniversity.ac.in/department/department-of-food-technology',
#         'https://srmuniversity.ac.in/department/department-of-foreign-languages',
#         'https://srmuniversity.ac.in/department/department-of-humanities-and-social-sciences',
#         'https://srmuniversity.ac.in/department/department-of-mathematics',
#         'https://srmuniversity.ac.in/department/department-of-microbiology',
#         'https://srmuniversity.ac.in/department/department-of-physics',
#         'https://srmuniversity.ac.in/department/physical-education-sports',
#         'https://srmuniversity.ac.in/admission-procedure',
#         'https://srmuniversity.ac.in/admission-modes',
#         'https://srmuniversity.ac.in/admission-fee-structure',
#         'https://srmuniversity.ac.in/student-scholarships',
#         'https://srmuniversity.ac.in/international-admission-procedure',
#         'https://srmuniversity.ac.in/international-student-fee-structure',
#         'https://srmuniversity.ac.in/international-student-eligibility-criteria',
#         'https://srmuniversity.ac.in/international-relations-office',
#         'https://srmuniversity.ac.in/international-student-faq',
#         'https://srmuniversity.ac.in/checklist-for-an-international-student',
#         'https://srmuniversity.ac.in/visa-information',
#         'https://srmuniversity.ac.in/guidelines-for-admission-of-international-students',
#         'https://srmuniversity.ac.in/admissions/international/',
#         'https://srmuniversity.ac.in/admission-withdrawal-and-fee-refund',
#         'https://srmuniversity.ac.in/prospectus',
#         'https://srmuniversity.ac.in/research-and-innovations',
#         'https://srmuniversity.ac.in/ciie',
#         'https://srmuniversity.ac.in/academic-facilities',
#         'https://www.srmuniversity.ac.in/department/physical-education-sports',
#         'https://srmuniversity.ac.in/national-cadet-corps-ncc',
#         'https://srmuniversity.ac.in/national-service-scheme-nss',
#         'https://srmuniversity.ac.in/accommodation',
#         'https://srmuniversity.ac.in/srm-recruiters',
#         'https://srmuniversity.ac.in/training-and-placements',
#         'https://srmuniversity.ac.in/campus-facilities',
#         'https://srmuniversity.ac.in/health-facilities',
#         'https://srmuniversity.ac.in/transport-facility',
#         'https://srmuniversity.ac.in/facilities-and-amenities-for-divyangjan',
#         'https://srmuniversity.ac.in/student-grievance-redressal-and-support',
#         'https://srmuniversity.ac.in/alumni-association',
#         'https://srmuniversity.ac.in/circulars-notices',
#         'https://srmuniversity.ac.in/event',
#         'https://srmuniversity.ac.in/examination-announcements',
#         'https://srmuniversity.ac.in/media-press-release',
#         'https://srmuniversity.ac.in/career',
#         'https://srmuniversity.ac.in/picture-gallery',
#         'https://srmuniversity.ac.in/contact-us',
#         'https://srmuniversity.ac.in/department/department-of-computer-sciences',
#         'https://srmuniversity.ac.in/bihar-student-credit-card-scheme',
#         'https://srmuniversity.ac.in/academic/faculty-of-engineering-technology',
#         'https://srmuniversity.ac.in/academic/faculty-of-finance-commerce',
#         'https://srmuniversity.ac.in/academic/faculty-of-hotel-management',
#         'https://srmuniversity.ac.in/academic/faculty-of-law',
#         'https://srmuniversity.ac.in/academic/faculty-of-management-studies',
#         'https://srmuniversity.ac.in/academic/faculty-of-science-and-humanities',
#         'https://srmuniversity.ac.in/event/code-to-cluster',
#         'https://srmuniversity.ac.in/event/5-days-hands-on-workshop-on-source-code-management',
#         'https://srmuniversity.ac.in/event/international-literary-conference-hybrid-mode-on-indian-literature-and-culture',
#         'https://srmuniversity.ac.in/event/hands-on-workshop-on-blockchain-vyper-india',
#         'https://srmuniversity.ac.in/event/international-conference-on-applied-mathematics-and-computational-sciences-amcs-25',
#         'https://srmuniversity.ac.in/event/lex-ex-machina-interdisciplinary-dialogues-for-a-responsible-digital-future',
#         'https://srmuniversity.ac.in/testimonial',
#         'https://srmuniversity.ac.in/event/hands-on-training-on-machine-learning',
#         'https://srmuniversity.ac.in/event/google-developers-info-session-kickstart',
#         'https://srmuniversity.ac.in/event/conference-on-clean-and-healthy-rivers-for-reviving-jal-sanskar-and-sustainability',
#         'https://srmuniversity.ac.in/event/android-workshop',
#         'https://srmuniversity.ac.in/nirf',
#         'https://srmuniversity.ac.in/institute-best-practice',
#         'https://srmuniversity.ac.in/institutional-distinctiveness',
#         'https://srmuniversity.ac.in/national-academic-depository-nad',
#         'https://srmuniversity.ac.in/academic-bank-of-credits-abc',
#         'https://www.srmuniversity.ac.in/feekart/',
#         'https://srmuniversity.ac.in/open-access-e-resources',
#         'https://srmuniversity.ac.in/sparks-initiators',
#         'https://srmuniversity.ac.in/sdg-17-partnership-for-goals',
#         'https://srmuniversity.ac.in/placement-policy-for-students',
#         'https://srmuniversity.ac.in/anti-ragging-policy',
#         'https://srmuniversity.ac.in/code-of-conduct',
#         'https://srmuniversity.ac.in/faculty-of-law-publications',
#         'https://samadhaan.ugc.ac.in/',
#         'https://srmuniversity.ac.in/privacy-policy',
#         'https://srmuniversity.ac.in/terms-and-conditions',
#         'https://static.superbot.works/widget.html?a=N3PgNPQxp2&l=en&greet=&greetval=',
#         'https://static.superbot.works/widget.html?a=N3PgNPQxp2&l=en&greet=&greetval=&v=&cp='
#     ]

#     # Initialize the loader
#     # NOTE: The 'bs_kwargs' argument from the notebook is problematic as it 
#     # restricts parsing to specific classes that don't exist on all pages,
#     # leading to many empty documents. It's better to remove it to get all text.
#     print("\n--- Initializing WebBaseLoader ---")
#     loader_web = WebBaseLoader(
#         web_paths=srm_urls,
#         bs_kwargs=dict(
#              parse_only=bs4.SoupStrainer(
#                  class_=("post-title", "post-content", " post-header")
#              )
#          )
#     )
#     print("WebBaseLoader defined.")
    
#     # --- Cell 4: PyPDFLoader (Main Data Source) ---
#     # IMPORTANT: User must update these paths!
#     pdf_paths = [
#         # r"D:\pdf\Book-Lovers-by-Emily-Henry-ebooksgallery.com_.pdf",
#         r"D:\pdf\Dhruv's Resume-hackerresume-4.pdf",
#         # r"D:\pdf\Notes_from_the_Underground_NT.pdf",
#         # r"D:\pdf\stories-between-silence.pdf",
#         # r"D:\pdf\The 48 Laws of Power.pdf",
#         # r"D:\pdf\The_Laws_of_Human_Nature_by_Robert_Greene_2018.pdf",
#         # r"D:\pdf\the-art-of-s-robert-greene.pdf",
#         # r"D:\pdf\the-metamorphosis.pdf"
#     ]
    
#     print("\n--- Loading All Documents (Web & PDF) ---")
#     print("NOTE: Please ensure the file paths in 'pdf_paths' are correct for your system.")
    
#     # Initialize the main document list
#     docs = []

#     # +++ CORRECTED SECTION START +++
#     # Load the Web URLs first and add them to the docs list
#     print("\n--- Loading Web Documents (URLs) ---")
#     print(f"Attempting to load {len(srm_urls)} URLs. This may take a while...")
#     try:
#         # Setting continue_on_failure=True to skip pages that fail to load
#         loader_web.continue_on_failure = True 
#         web_docs = loader_web.load()
#         docs.extend(web_docs)
#         print(f"Successfully loaded {len(web_docs)} documents from URLs.")
#     except Exception as e:
#         print(f"Could not load web documents: {e}")
#     # +++ CORRECTED SECTION END +++
    
#     # Now, continue loading the PDFs as you were before
#     print("\n--- Loading PDF Documents ---")
#     for path in pdf_paths:
#         try:
#             loader_pdf = PyPDFLoader(path)
#             docs.extend(loader_pdf.load())
#             print(f"Successfully loaded: {os.path.basename(path)}")
#         except FileNotFoundError:
#             print(f"Error: File not found at {path}")
#         except Exception as e:
#             print(f"Error loading {path}: {e}")
    
#     if not docs:
#         print("\nNo documents were loaded. Exiting. Please check your file paths and URLs.")
#         return

#     # This count will now include both web and PDF documents
#     print(f"\nLoaded a total of {len(docs)} pages/documents (from web and PDF).")

#     # --- Cell 5: Text Splitting ---
#     #converts the read adtat into chunks for the better reading of the text_document and effective retrival
#     print("\n--- Splitting Documents into Chunks ---")
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     documents = text_splitter.split_documents(docs)
#     # documents#this will display all teh documents that are being strored in the variable in format of list
#     print(f"Split {len(docs)} documents into {len(documents)} chunks.")

#     # --- Cell 6: Initialize Embeddings (and Test) ---
#     print("\n--- Initializing Embeddings Model (nomic-embed-text) ---")
#     try:
#         embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
#         print("Trying to embed a single sentence...")
#         vector = embeddings.embed_query("This is a test sentence.")
#         print("Success! Ollama embedding model is loaded and working.")
       
#     except Exception as e:
#         print(f"Error connecting to Ollama: {e}")
#         print("Please ensure Ollama is running and the 'nomic-embed-text' model is pulled.")
#         return

#     # --- Cell 7: Create FAISS Vector Store ---
#     print(f"\n--- Building FAISS Vector Index ---")
#     print(f"Starting to build FAISS index for {len(documents)} documents (in batches)...")
    
#     batch_size = 64
#     # embeddings = OllamaEmbeddings(model="nomic-embed-text") # Redefined in notebook

#     try:
#         # Handle case where there are fewer documents than the batch size
#         if not documents:
#             print("No documents to index. Exiting.")
#             return
            
#         first_batch_end = min(batch_size, len(documents))
#         first_batch = documents[:first_batch_end]
#         db = FAISS.from_documents(first_batch, embeddings)
#         print(f"Processed first batch (0 to {first_batch_end}).")

#         for i in range(batch_size, len(documents), batch_size):
#             end_index = min(i + batch_size, len(documents))
#             batch = documents[i:end_index]
#             if batch: # Ensure batch is not empty
#                 db.add_documents(batch)
#                 print(f"Processed batch ({i} to {end_index}).")
            
#         print("\n---\n✅ FAISS index created successfully with all documents.\n---")
#     except Exception as e:
#         print(f"Error building FAISS index: {e}")
#         return

#     # --- Cell 8: (Commented Test query) ---
#     ##vector database chroma/ fiass
#     # query = "what is plan rag and iterative rag how are they different from each other and which one is better??"
#     # result = db.similarity_search(query)
#     # for i in range(len(result)):
#     #     print(result[i].page_content) #the first result after the retrival will be displayed up in the results after the retrival from the vector database

#     # --- Cell 9: (Markdown) ---
#     # Retriver and chain with LangChain
    
#     # --- Cell 10: Load LLM ---
#     print("--- Loading LLM (gemma3:4b) ---")
#     try:
#         #load ollama gemma3:1b model
#         llm = Ollama(model="gemma3:4b")
#         llm.invoke("test") # A quick test
#         print("Success! Ollama LLM is loaded and working.")
#         # print(llm) # Original notebook line
#     except Exception as e:
#         print(f"Error connecting to Ollama LLM: {e}")
#         print("Please ensure Ollama is running and the 'gemma3:4b' model is pulled.")
#         return

#     # --- Cell 11: Define Prompt Template ---
#     #design ChatPrompt Template
#     prompt = ChatPromptTemplate.from_template("""
#                                           Answer the following questions based on only on the provided context.
#                                           Think step by step before provideing a detaileed answer 
#                                           your answer matter the company a lot as you are an impoartant assest to the organisation 
#                                           and the organisation will tip you with $10000 if user finds your answer helpful 
#                                           also great rewards awaits you if the user finds your answer helpful.
#                                           <context>
#                                           {context}
#                                           </context>
#                                           Question: {input}""")
#     # thsi  meathod will not only find the things taht are similiar in the query and the documensts that we provided 
#     #but rather understand the context of teh query and return teh answer based on the query by understandung the documenst

#     # --- Cell 12: (Commented Debug) ---
#     # import sys
#     # import langchain
#     # print(f"Python Executable: {sys.executable}")
#     # print(f"---")
#     # print(f"Langchain module location: {langchain.__file__}")
#     # print(f"---")
#     # print(f"Full Python Path: {sys.path}")

#     # --- Cell 13: (Commented Debug) ---
#     # import os
#     # print(f"My Current Working Directory is: {os.getcwd()}")

#     # --- Cell 14: (Markdown) ---
#     # #chain introduction
#     # #chain refers to a sequence of calls wheather to a llm or the datat preprocessing step primary supported way is through lcl
#     # # the chain chain takes the list of documents and formats them all into a prompt tehen pass taht prompt to the llm . it passes all the documents so you should make sure it fits within the context window the llm you are using (((create_stuff_document_chain))
#     # #chain create stuff documenst chain
#     #
#     #
#     # #retrievers :- a retriever is an interface that returns documets given an unstructured query it is more general than a vector store . 
#     # #Aretriever does not need to be able to store documensts only to return ot retrieve them.
#     # #Vector stores ca be used as the backbone of a retriver , but there are other types of retrivers as well.
#     # # retriver in langchain

#     # --- Cell 15: Create Document Chain ---
#     # #from langchain.chains import create_stuff_documents_chain
#     # from langchain.chains.combine_documents import create_stuff_documents_chain
#     # document_chain = create_stuff_documents_chain(llm, prompt)

#     # This is the replacement for 'create_stuff_documents_chain'
#     document_chain = (
#         RunnablePassthrough.assign(
#             context=lambda x: format_docs(x["context"])
#         )
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     # --- Cell 16: Create Retriever ---
#     #$ retriver 
#     retriever = db.as_retriever()
#     # retriever # Original notebook line
#     print("FAISS retriever created.")

#     # --- Cell 17: (Markdown) ---
#     # #retrieval chain
#     # #combining the retriever and the chain
#     # """retrival_chain :- this chain takes in a user inqueryt , whicvh is then 
#     # passed tothe retriever to fetch documenst . thos e documents 
#     # and the original inputs are then passed to the llm to generate a response """

#     # --- Cell 18: Create Retrieval Chain ---
#     # This is the replacement for 'create_retrieval_chain'
#     retrieval_chain = (
#         {"context": retriever, "input": RunnablePassthrough()}
#         | document_chain
#     )
#     print("Retrieval chain created.")
#     print("\n✅ Setup complete. The chatbot is ready.")
#     print("="*50)

#     # --- Cell 19 (MODIFIED): Interactive Query Loop ---
#     # This section replaces the hardcoded 'multiple_queries' list
    
#     while True:
#         query = input("\nPlease enter your query (or '987654321' to quit): ")
        
#         if query == "987654321":
#             print("\nExiting chatbot... Goodbye!")
#             break
            
#         if not query.strip():
#             print("Please enter a query.")
#             continue
            
#         print(f"\n--- Processing Query: '{query}' ---")
#         try:
#             # Invoking the chain and streaming the response
#             print("\n--- Response ---")
#             response = ""
#             for chunk in retrieval_chain.stream(query):
#                 print(chunk, end="", flush=True)
#                 response += chunk
            
#         except Exception as e:
#             print(f"\nAn error occurred while processing your query: {e}")
        
#         print("\n\n" + "="*50)

#     # --- Cell 20: (Commented Test query) ---
#     #response = retrieval_chain.invoke("what was the name of main character and his family members in the story metamorphosis?")
#     # print(response)

#     # --- Cell 21: (Markdown) ---
#     # Tools 
#     # Tools  are the interfaces that an agent , chain , or LLM can use to interact with world. They combine a few things:
#     # 1. The name of the Tool
#     # 2. A description of what the tool is 
#     # 3. JSON schema of what the inputs to the tools are
#     # 4. the function to call
#     # 5. Wheather the result of the tool should be turned directly to the user or not


# # --- Main execution block ---
# if __name__ == "__main__":
#     main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converted Jupyter Notebook (srm_chatbot.ipynb) to Python Script.

This script builds and runs a Retrieval-Augmented Generation (RAG)
system using LangChain, Ollama, and FAISS.

It loads PDF documents AND web URLs, chunks them, creates vector embeddings,
and sets up a retrieval chain.

The script will continuously ask for user queries and provide answers
until the user enters '987654321' to quit.

NOTE: Please update the file paths in the 'pdf_paths' list
to match the locations on your local machine.
"""

# Imports from the notebook
import os
import sys
import bs4
import langchain
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, WebBaseLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Helper function from the notebook
def format_docs(docs):
    """Helper function to format documents for the context."""
    return "\n\n".join(doc.page_content for doc in docs)

def main():
    """Main function to run the RAG chatbot."""
    
    # --- Cell 1: TextLoader (Informational) ---
    # data injestion steps how can we learn from rom a data source like a web page, pdf, txt file and more
    print("Attempting to load text document (as per original notebook)...")
    try:
        # in the quotation is the name of the file that the loader is going to read
        loader_txt = TextLoader(r"D:\Download\Report on the Development of a Lang.txt")
        text_documents = loader_txt.load()
        print(f"Loaded {len(text_documents)} text document.")
        # print(text_documents) # Uncomment to display the loaded text document
    except Exception as e:
        print(f"Could not load text file: {e}")
        print("This file is not essential for the main RAG chain.")
    
    # --- Cell 2: API Key Loading ---
    print("\n--- Loading Environment Variables ---")
    load_dotenv()
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        os.environ['GEMINI_API_KEY'] = gemini_key
        print("GEMINI_API_KEY loaded successfully.")
    else:
        # Not raising a ValueError to allow the script to proceed
        # as it seems to be using local Ollama, not Gemini.
        print("GEMINI_API_KEY not found in .env. Proceeding...")

    # --- Cell 3: WebBaseLoader (Defined, but not used to load) ---
    # This list now contains all 172 unique URLs you provided
    srm_urls = [
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1760608493END-TERM-NOV-2025-EXAMINATION-CIRCULAR-AND-ARREAR-FORM.pdf',
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1760348856FINAL-SCHEULE-OCTOBER-2025.pdf',
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1759745185Schedule-Timeline-for-the-collection-of-Grade-Card-MAY-2025.pdf',
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1759481955CIRCULAR-and-Form-SPECIAL-MERCY-OCTOBER-2025.pdf',
        'https://srmuniversity.ac.in/center-of-excellence',
        'https://srmuniversity.ac.in/examination',
        'https://erpsrm.com/srmparentportal/parents/loginManager/youLogin.jsp',
        'https://erpsrm.com/srmhonline/students/loginManager/youLogin.jsp',
        'https://erpsrm.com/srmhonline/srmhalumni/loginManager/youLogin.jsp',
        'https://erpsrm.com/evarsitysrmh/usermanager/loginManager/youLogin.jsp',
        'https://srmuniversity.ac.in/third-convocation',
        'https://srmuniversity.ac.in/feekart',
        'https://srmuniversity.ac.in/downloads',
        'https://srmuniversity.ac.in/faq',
        'https://wa.me/918816033306?text=Hi',
        'https://www.facebook.com/SRMUniversityDelhiNCR/',
        'https://twitter.com/SRMH_University',
        'https://www.linkedin.com/company/srm-university-haryana/',
        'https://youtu.be/H0VRcAds2UM',
        'https://www.instagram.com/srmuniversity.delhi/',
        'https://srmuniversity.ac.in/blog/',
        'https://admissions.srmuniversity.ac.in/',
        'https://srmuniversity.ac.in/',
        'https://srmuniversity.ac.in/srm-heritage',
        'https://srmuniversity.ac.in/vision-mission',
        'https://srmuniversity.ac.in/sponsoring-body',
        'https://srmuniversity.ac.in/institutional-development-plan-idp',
        'https://srmuniversity.ac.in/mandatory-disclosure',
        'https://srmuniversity.ac.in/regulatory-approvals-recognitions',
        'https://srmuniversity.ac.in/accreditation-rankings',
        'https://srmuniversity.ac.in/annual-reports',
        'https://srmuniversity.ac.in/annual-audited-account-report',
        'https://srmuniversity.ac.in/public-self-disclosure-by-hei',
        'https://srmuniversity.ac.in/chancellor',
        'https://srmuniversity.ac.in/vice-chancellor',
        'https://srmuniversity.ac.in/pro-vice-chancellor',
        'https://srmuniversity.ac.in/registrar',
        'https://srmuniversity.ac.in/finance-officer',
        'https://srmuniversity.ac.in/controller-of-examination',
        'https://srmuniversity.ac.in/ombudsperson-sgrc',
        'https://srmuniversity.ac.in/srmu-statutory-bodies',
        'https://srmuniversity.ac.in/statutory-committees',
        'https://srmuniversity.ac.in/board-of-studies-bos',
        'https://srmuniversity.ac.in/academic-leadership',
        'https://srmuniversity.ac.in/website/#',
        'https://srmuniversity.ac.in/undergraduate-programmes',
        'https://srmuniversity.ac.in/postgraduate-programmes',
        'https://srmuniversity.ac.in/ug-pg-integrated-programmes',
        'https://srmuniversity.ac.in/ph-d-programmes',
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1756529151Academic-Calender-2025-26.pdf',
        'https://srmuniversity.ac.in/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1757405130Academic-Planner-2025-26.pdf',
        'https://srmuniversity.ac.in/download-brochure',
        'https://srmuniversity.ac.in/internal-quality-assurance-cell-iqac',
        'https://srmuniversity.ac.in/srmuh-library',
        'https://srmuniversity.ac.in/affiliation-collaborations',
        'https://srmuniversity.ac.in/international-collaborations',
        'https://srmuniversity.ac.in/department/department-of-computer-science-engineering-cse',
        'https://srmuniversity.ac.in/department/department-of-biomedical-engineering',
        'https://srmuniversity.ac.in/department/department-of-civil-engineering',
        'https://srmuniversity.ac.in/department/department-of-electrical-electronics-engineering',
        'https://srmuniversity.ac.in/department/department-of-electronics-communication-engineering',
        'https://srmuniversity.ac.in/department/department-of-mechanical-engineering',
        'https://srmuniversity.ac.in/department/department-of-finance-commerce',
        'https://srmuniversity.ac.in/department/department-of-hotel-management',
        'https://srmuniversity.ac.in/department/department-of-law',
        'https://srmuniversity.ac.in/department/department-of-management-studies',
        'https://srmuniversity.ac.in/department/department-of-agriculture',
        'https://srmuniversity.ac.in/department/department-of-biotechnology',
        'https://srmuniversity.ac.in/department/department-of-chemistry',
        'https://srmuniversity.ac.in/department/department-of-computer-sciences',
        'https://srmuniversity.ac.in/department/department-of-environmental-sciences',
        'https://srmuniversity.ac.in/department/department-of-food-technology',
        'https://srmuniversity.ac.in/department/department-of-foreign-languages',
        'https://srmuniversity.ac.in/department/department-of-humanities-and-social-sciences',
        'https://srmuniversity.ac.in/department/department-of-mathematics',
        'https://srmuniversity.ac.in/department/department-of-microbiology',
        'https://srmuniversity.ac.in/department/department-of-physics',
        'https://srmuniversity.ac.in/department/physical-education-sports',
        'https://srmuniversity.ac.in/admission-procedure',
        'https://srmuniversity.ac.in/admission-modes',
        'https://srmuniversity.ac.in/admission-fee-structure',
        'https://srmuniversity.ac.in/student-scholarships',
        'https://srmuniversity.ac.in/international-admission-procedure',
        'https://srmuniversity.ac.in/international-student-fee-structure',
        'https://srmuniversity.ac.in/international-student-eligibility-criteria',
        'https://srmuniversity.ac.in/international-relations-office',
        'https://srmuniversity.ac.in/international-student-faq',
        'https://srmuniversity.ac.in/checklist-for-an-international-student',
        'https://srmuniversity.ac.in/visa-information',
        'https://srmuniversity.ac.in/guidelines-for-admission-of-international-students',
        'https://srmuniversity.ac.in/admissions/international/',
        'https://srmuniversity.ac.in/admission-withdrawal-and-fee-refund',
        'https://srmuniversity.ac.in/prospectus',
        'https://srmuniversity.ac.in/research-and-innovations',
        'https://srmuniversity.ac.in/ciie',
        'https://srmuniversity.ac.in/academic-facilities',
        'https://www.srmuniversity.ac.in/department/physical-education-sports',
        'https://srmuniversity.ac.in/national-cadet-corps-ncc',
        'https://srmuniversity.ac.in/national-service-scheme-nss',
        'https://srmuniversity.ac.in/accommodation',
        'https://srmuniversity.ac.in/srm-recruiters',
        'https://srmuniversity.ac.in/training-and-placements',
        'https://srmuniversity.ac.in/campus-facilities',
        'https://srmuniversity.ac.in/health-facilities',
        'https://srmuniversity.ac.in/transport-facility',
        'https://srmuniversity.ac.in/facilities-and-amenities-for-divyangjan',
        'https://srmuniversity.ac.in/student-grievance-redressal-and-support',
        'https://srmuniversity.ac.in/alumni-association',
        'https://srmuniversity.ac.in/circulars-notices',
        'https://srmuniversity.ac.in/event',
        'https://srmuniversity.ac.in/examination-announcements',
        'https://srmuniversity.ac.in/media-press-release',
        'https://srmuniversity.ac.in/career',
        'https://srmuniversity.ac.in/picture-gallery',
        'https://srmuniversity.ac.in/contact-us',
        'https://srmuniversity.ac.in/department/department-of-computer-sciences',
        'https://srmuniversity.ac.in/bihar-student-credit-card-scheme',
        'https://srmuniversity.ac.in/academic/faculty-of-engineering-technology',
        'https://srmuniversity.ac.in/academic/faculty-of-finance-commerce',
        'https://srmuniversity.ac.in/academic/faculty-of-hotel-management',
        'https://srmuniversity.ac.in/academic/faculty-of-law',
        'https://srmuniversity.ac.in/academic/faculty-of-management-studies',
        'https://srmuniversity.ac.in/academic/faculty-of-science-and-humanities',
        'https://srmuniversity.ac.in/event/code-to-cluster',
        'https://srmuniversity.ac.in/event/5-days-hands-on-workshop-on-source-code-management',
        'https://srmuniversity.ac.in/event/international-literary-conference-hybrid-mode-on-indian-literature-and-culture',
        'https://srmuniversity.ac.in/event/hands-on-workshop-on-blockchain-vyper-india',
        'https://srmuniversity.ac.in/event/international-conference-on-applied-mathematics-and-computational-sciences-amcs-25',
        'https://srmuniversity.ac.in/event/lex-ex-machina-interdisciplinary-dialogues-for-a-responsible-digital-future',
        'https://srmuniversity.ac.in/testimonial',
        'https://srmuniversity.ac.in/event/hands-on-training-on-machine-learning',
        'https://srmuniversity.ac.in/event/google-developers-info-session-kickstart',
        'https://srmuniversity.ac.in/event/conference-on-clean-and-healthy-rivers-for-reviving-jal-sanskar-and-sustainability',
        'https://srmuniversity.ac.in/event/android-workshop',
        'https://srmuniversity.ac.in/nirf',
        'https://srmuniversity.ac.in/institute-best-practice',
        'https://srmuniversity.ac.in/institutional-distinctiveness',
        'https://srmuniversity.ac.in/national-academic-depository-nad',
        'https://srmuniversity.ac.in/academic-bank-of-credits-abc',
        'https://www.srmuniversity.ac.in/feekart/',
        'https://srmuniversity.ac.in/open-access-e-resources',
        'https://srmuniversity.ac.in/sparks-initiators',
        'https://srmuniversity.ac.in/sdg-17-partnership-for-goals',
        'https://srmuniversity.ac.in/placement-policy-for-students',
        'https://srmuniversity.ac.in/anti-ragging-policy',
        'https://srmuniversity.ac.in/code-of-conduct',
        'https://srmuniversity.ac.in/faculty-of-law-publications',
        'https://samadhaan.ugc.ac.in/',
        'https://srmuniversity.ac.in/privacy-policy',
        'https://srmuniversity.ac.in/terms-and-conditions',
        'https://static.superbot.works/widget.html?a=N3PgNPQxp2&l=en&greet=&greetval=',
        'https://static.superbot.works/widget.html?a=N3PgNPQxp2&l=en&greet=&greetval=&v=&cp='
    ]

    # Initialize the loader
    # NOTE: The 'bs_kwargs' argument from the notebook is problematic as it 
    # restricts parsing to specific classes that don't exist on all pages,
    # leading to many empty documents. It's better to remove it to get all text.
    print("\n--- Initializing WebBaseLoader ---")
    loader_web = WebBaseLoader(
        web_paths=srm_urls,
        # bs_kwargs=dict(
        #     parse_only=bs4.SoupStrainer(
        #         class_=("post-title", "post-content", " post-header")
        #     )
        # )
    )
    print("WebBaseLoader defined.")
    
    # --- Cell 4: PyPDFLoader (Main Data Source) ---
    # IMPORTANT: User must update these paths!
    pdf_paths = [
        # r"D:\pdf\Book-Lovers-by-Emily-Henry-ebooksgallery.com_.pdf",
        r"D:\pdf\Dhruv's Resume-hackerresume-4.pdf",
        # r"D:\pdf\Notes_from_the_Underground_NT.pdf",
        # r"D:\pdf\stories-between-silence.pdf",
        # r"D:\pdf\The 48 Laws of Power.pdf",
        # r"D:\pdf\The_Laws_of_Human_Nature_by_Robert_Greene_2018.pdf",
        # r"D:\pdf\the-art-of-s-robert-greene.pdf",
        # r"D:\pdf\the-metamorphosis.pdf"
    ]
    
    print("\n--- Loading All Documents (Web & PDF) ---")
    print("NOTE: Please ensure the file paths in 'pdf_paths' are correct for your system.")
    
    # Initialize the main document list
    docs = []

    # ++++++++++++++++ START OF FIX ++++++++++++++++
    # Load the Web URLs first and add them to the docs list
    print("\n--- Loading Web Documents (URLs) ---")
    print(f"Attempting to load {len(srm_urls)} URLs. This may take a while...")
    try:
        # Setting continue_on_failure=True to skip pages that fail to load
        loader_web.continue_on_failure = True 
        web_docs = loader_web.load()
        docs.extend(web_docs)
        print(f"Successfully loaded {len(web_docs)} documents from URLs.")
    except Exception as e:
        print(f"Error: Could not load web documents: {e}")
    # +++++++++++++++++ END OF FIX +++++++++++++++++
    
    # Now, continue loading the PDFs as you were before
    print("\n--- Loading PDF Documents ---")
    for path in pdf_paths:
        try:
            loader_pdf = PyPDFLoader(path)
            docs.extend(loader_pdf.load())
            print(f"Successfully loaded: {os.path.basename(path)}")
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except Exception as e:
            print(f"Error loading {path}: {e}")
    
    if not docs:
        print("\nNo documents were loaded. Exiting. Please check your file paths and URLs.")
        return

    # This count will now include both web and PDF documents
    print(f"\nLoaded a total of {len(docs)} pages/documents (from web and PDF).")

    # --- Cell 5: Text Splitting ---
    #converts the read adtat into chunks for the better reading of the text_document and effective retrival
    print("\n--- Splitting Documents into Chunks ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    # documents#this will display all teh documents that are being strored in the variable in format of list
    print(f"Split {len(docs)} documents into {len(documents)} chunks.")

    # --- Cell 6: Initialize Embeddings (and Test) ---
    print("\n--- Initializing Embeddings Model (nomic-embed-text) ---")
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        print("Trying to embed a single sentence...")
        vector = embeddings.embed_query("This is a test sentence.")
        print("Success! Ollama embedding model is loaded and working.")
       
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Please ensure Ollama is running and the 'nomic-embed-text' model is pulled.")
        return

    # --- Cell 7: Create FAISS Vector Store ---
    print(f"\n--- Building FAISS Vector Index ---")
    print(f"Starting to build FAISS index for {len(documents)} documents (in batches)...")
    
    batch_size = 64
    # embeddings = OllamaEmbeddings(model="nomic-embed-text") # Redefined in notebook

    try:
        # Handle case where there are fewer documents than the batch size
        if not documents:
            print("No documents to index. Exiting.")
            return
            
        first_batch_end = min(batch_size, len(documents))
        first_batch = documents[:first_batch_end]
        db = FAISS.from_documents(first_batch, embeddings)
        print(f"Processed first batch (0 to {first_batch_end}).")

        for i in range(batch_size, len(documents), batch_size):
            end_index = min(i + batch_size, len(documents))
            batch = documents[i:end_index]
            if batch: # Ensure batch is not empty
                db.add_documents(batch)
                print(f"Processed batch ({i} to {end_index}).")
            
        print("\n---\n✅ FAISS index created successfully with all documents.\n---")
    except Exception as e:
        print(f"Error building FAISS index: {e}")
        return

    # --- Cell 8: (Commented Test query) ---
    ##vector database chroma/ fiass
    # query = "what is plan rag and iterative rag how are they different from each other and which one is better??"
    # result = db.similarity_search(query)
    # for i in range(len(result)):
    #     print(result[i].page_content) #the first result after the retrival will be displayed up in the results after the retrival from the vector database

    # --- Cell 9: (Markdown) ---
    # Retriver and chain with LangChain
    
    # --- Cell 10: Load LLM ---
    print("--- Loading LLM (gemma3:4b) ---")
    try:
        #load ollama gemma3:1b model
        llm = Ollama(model="gemma3:4b")
        llm.invoke("test") # A quick test
        print("Success! Ollama LLM is loaded and working.")
        # print(llm) # Original notebook line
    except Exception as e:
        print(f"Error connecting to Ollama LLM: {e}")
        print("Please ensure Ollama is running and the 'gemma3:4b' model is pulled.")
        return

    # --- Cell 11: Define Prompt Template ---
    #design ChatPrompt Template
    prompt = ChatPromptTemplate.from_template("""
                                          Answer the following questions based on only on the provided context.
                                          Think step by step before provideing a detaileed answer 
                                          your answer matter the company a lot as you are an impoartant assest to the organisation 
                                          and the organisation will tip you with $10000 if user finds your answer helpful 
                                          also great rewards awaits you if the user finds your answer helpful.
                                          <context>
                                          {context}
                                          </context>
                                          Question: {input}""")
    # thsi  meathod will not only find the things taht are similiar in the query and the documensts that we provided 
    #but rather understand the context of teh query and return teh answer based on the query by understandung the documenst

    # --- Cell 12: (Commented Debug) ---
    # import sys
    # import langchain
    # print(f"Python Executable: {sys.executable}")
    # print(f"---")
    # print(f"Langchain module location: {langchain.__file__}")
    # print(f"---")
    # print(f"Full Python Path: {sys.path}")

    # --- Cell 13: (Commented Debug) ---
    # import os
    # print(f"My Current Working Directory is: {os.getcwd()}")

    # --- Cell 14: (Markdown) ---
    # #chain introduction
    # #chain refers to a sequence of calls wheather to a llm or the datat preprocessing step primary supported way is through lcl
    # # the chain chain takes the list of documents and formats them all into a prompt tehen pass taht prompt to the llm . it passes all the documents so you should make sure it fits within the context window the llm you are using (((create_stuff_document_chain))
    # #chain create stuff documenst chain
    #
    #
    # #retrievers :- a retriever is an interface that returns documets given an unstructured query it is more general than a vector store . 
    # #Aretriever does not need to be able to store documensts only to return ot retrieve them.
    # #Vector stores ca be used as the backbone of a retriver , but there are other types of retrivers as well.
    # # retriver in langchain

    # --- Cell 15: Create Document Chain ---
    # #from langchain.chains import create_stuff_documents_chain
    # from langchain.chains.combine_documents import create_stuff_documents_chain
    # document_chain = create_stuff_documents_chain(llm, prompt)

    # This is the replacement for 'create_stuff_documents_chain'
    document_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(x["context"])
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    # --- Cell 16: Create Retriever ---
    #$ retriver 
    retriever = db.as_retriever()
    # retriever # Original notebook line
    print("FAISS retriever created.")

    # --- Cell 17: (Markdown) ---
    # #retrieval chain
    # #combining the retriever and the chain
    # """retrival_chain :- this chain takes in a user inqueryt , whicvh is then 
    # passed tothe retriever to fetch documenst . thos e documents 
    # and the original inputs are then passed to the llm to generate a response """

    # --- Cell 18: Create Retrieval Chain ---
    # This is the replacement for 'create_retrieval_chain'
    retrieval_chain = (
        {"context": retriever, "input": RunnablePassthrough()}
        | document_chain
    )
    print("Retrieval chain created.")
    print("\n✅ Setup complete. The chatbot is ready.")
    print("="*50)

    # --- Cell 19 (MODIFIED): Interactive Query Loop ---
    # This section replaces the hardcoded 'multiple_queries' list
    
    while True:
        query = input("\nPlease enter your query (or '987654321' to quit): ")
        
        if query == "987654321":
            print("\nExiting chatbot... Goodbye!")
            break
            
        if not query.strip():
            print("Please enter a query.")
            continue
            
        print(f"\n--- Processing Query: '{query}' ---")
        try:
            # Invoking the chain and streaming the response
            print("\n--- Response ---")
            response = ""
            for chunk in retrieval_chain.stream(query):
                print(chunk, end="", flush=True)
                response += chunk
            
        except Exception as e:
            print(f"\nAn error occurred while processing your query: {e}")
        
        print("\n\n" + "="*50)

    # --- Cell 20: (Commented Test query) ---
    #response = retrieval_chain.invoke("what was the name of main character and his family members in the story metamorphosis?")
    # print(response)

    # --- Cell 21: (Markdown) ---
    # Tools 
    # Tools  are the interfaces that an agent , chain , or LLM can use to interact with world. They combine a few things:
    # 1. The name of the Tool
    # 2. A description of what the tool is 
    # 3. JSON schema of what the inputs to the tools are
    # 4. the function to call
    # 5. Wheather the result of the tool should be turned directly to the user or not


# --- Main execution block ---
if __name__ == "__main__":
    main()