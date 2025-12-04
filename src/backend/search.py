from src.backend.data import file_read
from typing import LiteralString
type Settings = list[tuple[str, ...], tuple[str, ...], tuple[str, ...]]

class LowerCaseStr(str):
    """
    The string should be in lower-case
    For performance & case-insensitive search reasons.
        
    ```python
    a: str = "".lower()
    ```
    """

def linkedin_search_result(
    search_term: LowerCaseStr, 
    company: LowerCaseStr, 
    profession: LowerCaseStr, 
    linkedin_id: str,
    tags: list[list[LowerCaseStr]], 
    settings: Settings
    ) -> bool:
    #! Optimize this even further:
    #* Only load from the database what's needed
    
    allowed_languages, allowed_professions, excluded_companys = settings
    
    search_bar = any(
        [
            search_term in company, #? search in title
            search_term in profession, #? search in jobtitle
            search_term in linkedin_id, #? search in
            any([search_term in s for s, _ in tags]), #? Does at minimum one search equals tag-content
        ]
    )
    
    company_okay = not any([c in company for c in excluded_companys])
    if not excluded_companys: company_okay = True
    
    profession_okay = any([p in profession for p in allowed_professions])
    if not allowed_professions: profession_okay = True
    
    languages_okay = any([any([p in t for t in tags]) for p in allowed_languages])
    if not allowed_languages: languages_okay = True
    
    return search_bar and company_okay and profession_okay and languages_okay

def get_jobsearch_settings() -> list:
    data = file_read('./settings/jobsearch_settings.json')
    return [[tag for tag in tags.split(',') if tag] for tags in data.split(';')]
        
def linkedin_search(search_term, jobs, tags):
    settings = get_jobsearch_settings()
    #settings = [[j.lower() for j in i] for i in settings] <- this is not necessesary, because the user-inputs are converted in jobsearch_settings
    tags = [[(t.lower(), c) for t, c in ta] for ta in tags]
    new_jobs = []
    new_tags = []

    for job, _tags in zip(jobs, tags):
        company = job['company'].lower()
        profession = job['job_title'].lower()
        linkedin_id = str(job['lid'])
        if linkedin_search_result(
            search_term, 
            company, 
            profession, 
            linkedin_id, 
            _tags, 
            settings):
            ...
            new_jobs.append(job)
            new_tags.append(_tags)
                        
    return new_jobs, new_tags