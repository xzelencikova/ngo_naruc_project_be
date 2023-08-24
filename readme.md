Requirements:
    - python

Configuration:
    To create a virtual environment:

    <i>python -m venv venv</i>

    To activate a virtual environment:

    <i>venv\Scripts\activate</i>

    To install library:

    <i>pip install <library></i>

    To install libraries from requirements.txt file:

    <i>pip install -r requirements.txt</i>

Run:
    To run the application:
    
    <i>python app.py</i>

Rules:
    1. Api calls for each feature should have its own Python file. 
    2. The files should be created in <i>namespaces</i> folder with <i>ns_</i> preffix.
    3. Import file into <i>app.py</i> and add to namespace with 
        
        <i>ngo_naruc.add_resource(<class of imported endpoint>, path)</i>
