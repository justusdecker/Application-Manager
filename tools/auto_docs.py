import os, ast
def get_python_paths() -> list[str]:
    _ret = []
    for rel, folders, files in os.walk('./'):
        rel = rel.replace('\\','/')
        for file in files:
            
            if file.endswith('.py'):
                p = "/".join([rel, file])
                _ret.append(p)
    return _ret

def get_status(f: int) -> str:
    return ['🔴','🟢','🟡'][f]

def get_table_element(p:str, m:str, f: int, t: str) -> str:
    return f'|[{m}](../{p.replace("./","")})|{t}|{get_status(f)}|\n'

def pprint(p:str, m: str, f: int) -> None:
    c = ['\033[33mNODOC', '\033[32mFOUND', '\033[35mSHORT'][f]
    print(f'[{c}\033[0m]\033[35m {p}\033[0m >> \033[34m{m}\033[0m')

def parse_files(skip_contains: list[str], paths: list[str] = get_python_paths()):
    """
    Creates automatically a README for the coder, you lazy butt :D
    """
    nodoc = 0
    numdocs = 0
    MD = "# Automatic-Documentator by Justus Decker\n\n"
    DOCS_MD = '# Documentation Status\n\n|file(object)|type|status|\n|---|---|---|\n'
    for path in paths:
        if any([sc in path for sc in skip_contains]): continue
            
        with open(path, 'rb') as file:
            data = file.read()
        tree = ast.parse(data)
        docs = ast.get_docstring(tree)
        
        MD += f'# {path}\n\n'
        if docs is not None:
            MD += docs + '\n\n'
        
        
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef):
                if n.name == '__init__': continue # This is the init dunder, i usually dont comment this
                numdocs += 1
                f_doc = ast.get_docstring(n)
                if f_doc is None:
                    nodoc += 1
                    DOCS_MD += get_table_element(path, n.name, 0, 'function')
                    pprint(path, n.name,0)
                    continue
                if len(f_doc) <= 30:
                    DOCS_MD += get_table_element(path, n.name, 2, 'function')
                    pprint(path, n.name,2)
                else:
                    pprint(path, n.name,1)
                    DOCS_MD += get_table_element(path, n.name, 1, 'function')
                MD += f'## {n.name}\n{f_doc}\n\n'
                

            if isinstance(n, ast.ClassDef):
                numdocs += 1
                c_doc = ast.get_docstring(n)
                if c_doc is None:
                    nodoc += 1
                    DOCS_MD += get_table_element(path, n.name, 0, 'class')
                    pprint(path, n.name,0)
                    continue
                if len(c_doc) <= 30:
                    DOCS_MD += get_table_element(path, n.name, 2, 'class')
                    pprint(path, n.name,2)
                else:
                    DOCS_MD += get_table_element(path, n.name, 1, 'class')
                    pprint(path, n.name,1)
                MD += f'## {n.name}\n{c_doc}\n\n'
    print(f'\033[35m{(1 - (nodoc / numdocs)) * 100:.2f}% \033[0m(\033[34m{numdocs - nodoc}\033[0m of \033[34m{numdocs}\033[0m)')   
    with open('./docs/auto-docs.md', 'wb') as file:
        file.write(MD.encode())
    with open('./docs/docs-progress.md','wb') as file:
        file.write(DOCS_MD.encode())
        
if __name__ == '__main__':
    parse_files(
        [
            'tools/',
            '__debug__.py'
        ]
    )