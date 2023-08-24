Requirements: Python

Configuration:
To create a virtual environment:

    python -m venv venv

To activate a virtual environment:

    venv\Scripts\activate

To install library:

    pip install <library>

To install libraries from requirements.txt file:

    pip install -r requirements.txt

Run:
To run the application:
    
    python app.py

Rules:
1. Api calls for each feature should have its own Python file. 
2. The files should be created in <i>namespaces</i> folder with <i>ns_</i> preffix.
3. Import file into <i>app.py</i> and add to namespace with 
        
   ngo_naruc.add_resource(<class of imported endpoint>, path)
