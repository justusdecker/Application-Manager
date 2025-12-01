from html.parser import HTMLParser
from requests import get
import re
from src.coding_tags import TAG_LIST, CRECOLORS, TAG_COLOR_LINK
def attr_finder(attrs, search_for) -> list:
    return [i for i in attrs if i[0] == search_for]

class IDGetterSearch(HTMLParser):
    def __init__(self, *, convert_charrefs = True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.data_job_ids = []
    def handle_starttag(self, _, attrs):
        if attrs: 
            if attr_finder(attrs, 'data-job-id'):
                self.data_job_ids.append(attrs[0][1])

class FetchJob(HTMLParser):
    def __init__(self, *, convert_charrefs = True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.logo = None
        self.job_title = None
        self.next_is_job_title = False
        self.company_name = None
        self.next_is_company_name = False
        self.company_name_miss = 0
        self.description = ""
        self.error = False
        
    def feed(self, data):
        # Find the current job
        start_index = data.find('<section class="show-more-less-html"')
        end_index = data[start_index:].find("</div>")
        if start_index == -1:
            self.error = True
            return
        new_data = data[start_index:end_index+start_index]
        for old, new in (('<span>',''),('</span>',''),('<br>','\n'), ('<p>',''), ('<strong>',''),('</strong>',''),('</div>',''),('</p>','\n'),('<!---->',''), ('</li>',''), ('<li>','\n* '), ('<ul>',''), ('</ul>','')):
            new_data = new_data.replace(old, new)
        new_data = new_data.split('">\n')[-1].strip()
        self.description = new_data

        return super().feed(data)
    
    def handle_starttag(self, tag, attrs):
        SRC = attr_finder(attrs, 'src')
        ALT = attr_finder(attrs, 'alt')
        HREF = attr_finder(attrs, 'href')
        DATA_DELAYED_URL = attr_finder(attrs, 'data-delayed-url')
        if tag == 'img':
            if attrs: 
                if not self.logo and DATA_DELAYED_URL and ALT and 'company' in DATA_DELAYED_URL[0][1].lower():
                    # Searches for the company logo
                    self.logo = DATA_DELAYED_URL[0][1]
        if tag == 'a':
            
            if not self.company_name and HREF and 'company' in HREF[0][1]:
                self.next_is_company_name = True
            if HREF and 'company' in HREF[0][1]:
                #print(HREF[0][1])
                ...
        if not self.job_title and tag == 'h1':
            self.next_is_job_title = True

    def handle_data(self, data):
        if self.next_is_job_title:
            # Gets the job title
            self.job_title = data
            self.next_is_job_title = False
        if self.next_is_company_name and self.company_name_miss == 2:
            if data.strip() and data.strip():
                self.company_name = data.strip()
                self.next_is_company_name = False
        if self.next_is_company_name and self.company_name_miss < 2:
            self.company_name_miss += 1
            self.next_is_company_name = False            

def phone_number_compatible_char(char: str) -> bool:
    return char.isdecimal() or char == '+' or char.isspace()

def get_phone_number(text: str):
    nums = set()
    for idx, char in enumerate(text):
        if phone_number_compatible_char(char):
            number = ''
            for num_char in text[idx:]:
                if phone_number_compatible_char(num_char):
                    number += num_char
                else: break
            if not number or number.isspace() or number == '+': continue
            number = number.strip()
            if number[0] == '+' and number.count('+') == 1:
                number = number[1:].replace(' ', '')
                if len(number) <= 17 and len(number) >= 6:
                    nums.add(number)

    return list(nums)

def get_mails(text: str) -> list[str]:
    return [word for word in text.split() if '@' in word]

def get_links(text: str) -> list[str]:
    return [word for word in text.split() if word.startswith(('www.', 'https://'))]

def get_tags(text: str) -> list[str]:
    f = {}
    _ret = set()
    for r in '()-,':
        text = text.replace(r, '')
    for word in text.lower().split():
        if word in TAG_LIST:
            c = TAG_LIST.index(word)
            l = TAG_COLOR_LINK[c]
            _ret.add((word, CRECOLORS[l]))
            if word in f:
                f[word] += 1
            else:
                f[word] = 1
    return _ret
        
def get_linkedin_job_site(job_id: int):
    try:
        return get(f'https://www.linkedin.com/jobs/view/{job_id}/')._content.decode()
    except: ...

def fetch_linkedin_job_data(job_id: int) -> dict:
    """
    Gets you the logo, job_title, company_name, description & also returns the job_id in the dict.
    """
    print(job_id)
    content = get_linkedin_job_site(job_id)
    if content is None: 
        return {'error': 'Get return is none'}
    parser = FetchJob()
    parser.feed(content)
    if None in [parser.logo, parser.job_title, parser.company_name, parser.description, job_id]:
        #! Investigate this error further
        return None
    return {
        'logo': parser.logo, 
        'job_title': parser.job_title, 
        'company': parser.company_name,
        'description': parser.description,
        'lid': job_id
    }
    
def fetch_job_ids(html: str) -> list:
    """
    Takes a html-structure in string form, runs the HTML parser and fetches the job ids from there.
    For this to work you need to copy the html from your browser and paste this into a file!
    """
    parser = IDGetterSearch()
    parser.feed(html)
    return parser.data_job_ids
