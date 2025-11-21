text = ''
with open('./src/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"').strip("'")
            major, minor, patch = map(int, version.split('.'))
            patch += 1
            version = f"{major}.{minor}.{patch}"
            text += f'__version__ = "{version}"\n'
        else:
            text += line
        
with open('./src/version.py', 'w') as fw:
    fw.write(text)