TAGS = {
    'languages': [ 
        'python',
        'javascript',
        'java',
        'c++',
        'c#',
        'c',
        'typescript',
        'golang',
        'swift',
        'kotlin',
        'ruby',
        'php',
        'dart'
    ],
    'script': [
        'batch',
        'cmd',
        'powershell',
        'shell',
        'vba',
        'vb.net',
        'visualbasic'
    ],
    'web': [
        'html',
        'css'
    ],
    'frontend': [
        'react',
        'angular',
        'vue.js',
        'svelte',
        'next.js',
        'nuxt.js',
        'bootstrap',
    ],
    'backend': [
        'django',
        'flask', # :D
        'express.js',
        'nestjs',
        'laravel',
        '.net'
    ],
    'databases': [
        'postgresql',
        'mysql',
        'mongodb',
        'redis',
        'sqlite',
        'sql',
        'nosql',
        'json',
        'csv'
    ],
    'devops': [
        'git', 
        'docker', 
        'kubernetes', 
        'aws', 
        'azure', 
        'gcp', 
        'terraform',
        'jenkins',
        'github'
    ]
}

CRECOLORS = {
    0: "#783151",
    1: "#316D78",
    2: "#587831",
    3: "#786B31",
    4: "#783131",
    5: "#784531",
    6: "#317870"
}

TAG_LIST = []
TAG_COLOR_LINK = []
for idx, tag in enumerate(TAGS):
    tags = [e for e in TAGS[tag]]
    
    TAG_COLOR_LINK.extend([idx for i in range(len(tags))])
    
    TAG_LIST.extend(tags)