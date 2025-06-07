import os

def load_sql(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    sql_path = os.path.normpath(os.path.join(base_dir, "..", "sql", filename))
    
    if not os.path.isfile(sql_path):
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    
    with open(sql_path, 'r', encoding='utf-8') as file:
        return file.read()
