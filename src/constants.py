GET, POST, DELETE = 'GET', 'POST', 'DELETE'

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


http_status_codes = {
    # 1xx: Informational
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",

    # 2xx: Success
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    208: "Already Reported",
    226: "IM Used",

    # 3xx: Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",  # Unused/Reserved
    307: "Temporary Redirect",
    308: "Permanent Redirect",

    # 4xx: Client Errors
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",

    # 5xx: Server Errors
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required"
}

HELP = {
    'Help': {
        'Jobs': [
            "You can create a job here",
            "You need to insert a few values here:",
            "* Company-name(*)",
            "* job-title(*): The job-title / profession of the job you are looking for(If a job-title not exists you need to create it first in job-titles/create",
            "* url(*): The url of the job you are looking",
            "* mail: The mail-address of the company",
            "* phone-number: The phone-number of the company",
            "* description: The description of the job you are looking for"
        ],
        'Job Ids': [
            "You can create a job-id / profession here",
            "This is used for Jobs"
        ]
    }
}