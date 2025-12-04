class Links():
    def __init__(self,
                 links: list[str],
                 titles: list[str]):
        if len(links) != len(titles): raise Exception()
        self.data = [(l, t) for l, t in zip(links, titles)]
    
    def get(self):
        f = '<div class="sidebar-mtr sidebar-title-two more-weight" style="margin-top:4%;">'
        l = '</div>'
        return f + ", ".join([f'<a class="sidebar-text" href="{l}">{t}</a>' for l, t in self.data]) + l

class Head:
    def __init__(self, head: str):
        self.head = head
    def get(self) -> str:
        return f'<div class="borderline-spacer-sidebar sidebar-mtr sidebar-title-one" style="margin-top:8%;">{self.head}</div>'
    
class Title:
    def __init__(self, title: str):
        self.title = title
    def get(self) -> str:
        return f'<div class="sidebar-mtr sidebar-title-two more-weight" style="margin-top:4%;">{self.title}</div>'

class Content:
    def __init__(self, content: str):
        self.content = content
    def get(self) -> str:
        return f'<div><p class="sidebar-mtr sidebar-text">{self.content}</p></div>'

class Bulletpoint:
    def __init__(self, content: str):
        self.content = content
    def get(self) -> str:
        return f'<p class="better-text-view">{self.content}</p>'

class Project:
    def __init__(self,
                 TITLE, 
                 SPAN,
                 LINK,
                 LINK_TITLE,
                 BULLETPOINTS):
        
        self.TITLE = TITLE
        self.SPAN = SPAN
        self.LINK = LINK
        self.LINK_TITLE = LINK_TITLE
        self.BULLETPOINTS = BULLETPOINTS
        
class EducationOrExperience:
    def __init__(self,
                 TITLE, 
                 SPAN,
                 PROFESSION,
                 LOCATION,
                 BULLETPOINTS):
        
        self.TITLE = TITLE
        self.SPAN = SPAN
        self.PROFESSION = PROFESSION
        self.LOCATION = LOCATION
        self.BULLETPOINTS = BULLETPOINTS