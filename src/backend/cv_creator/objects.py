class Links:
    """
    Represents a collection of hyperlinked text elements, typically for a sidebar,
    and generates the corresponding HTML string.
    """
    def __init__(self,
                 links: list[str],
                 titles: list[str]):
        if len(links) != len(titles): raise Exception()
        self.data = [(l, t) for l, t in zip(links, titles)]
    
    def get(self):
        """
        Generates the HTML string containing all links, enclosed in a div with
        specific sidebar styling.

        :return: An HTML string of linked titles separated by ", ".
        """
        f = '<div class="sidebar-mtr sidebar-title-two more-weight" style="margin-top:4%;">'
        l = '</div>'
        return f + ", ".join([f'<a class="sidebar-text" href="{l}">{t}</a>' for l, t in self.data]) + l

class Head:
    """
    Represents a main heading for a section, typically in a sidebar,
    and generates the corresponding HTML string.
    """
    def __init__(self, head: str):
        self.head = head
        
    def get(self) -> str:
        """
        Generates the HTML string for the heading, wrapped in a div with
        border and main title styling.

        :return: An HTML string for the section heading.
        """
        return f'<div class="borderline-spacer-sidebar sidebar-mtr sidebar-title-one" style="margin-top:8%;">{self.head}</div>'
    
class Title:
    """
    Represents a sub-title or secondary heading, typically in a sidebar,
    and generates the corresponding HTML string.
    """
    def __init__(self, title: str):
        self.title = title
        
    def get(self) -> str:
        """
        Generates the HTML string for the sub-title, wrapped in a div with
        secondary title styling.

        :return: An HTML string for the sub-title.
        """
        return f'<div class="sidebar-mtr sidebar-title-two more-weight" style="margin-top:4%;">{self.title}</div>'

class Content:
    """
    Represents a block of general text content, typically in a sidebar,
    and generates the corresponding HTML string.
    """
    def __init__(self, content: str):
        self.content = content
        
    def get(self) -> str:
        """
        Generates the HTML string for the content, wrapped in a div and a paragraph
        tag with specific sidebar text styling.

        :return: An HTML string for the content block.
        """
        return f'<div><p class="sidebar-mtr sidebar-text">{self.content}</p></div>'

class Bulletpoint:
    """
    Represents a single bullet point item, and generates the corresponding HTML string.
    Note: This does not wrap the content in a standard HTML list (ul/li).
    """
    def __init__(self, content: str):
        self.content = content
        
    def get(self) -> str:
        """
        Generates the HTML string for the bullet point content, wrapped in a paragraph
        tag with a specific class for viewing.

        :return: An HTML string for the bullet point.
        """
        return f'<p class="better-text-view">{self.content}</p>'

class Project:
    """
    A data structure class representing a project entry, likely for a resume or portfolio.
    It holds data but does not generate HTML itself.
    """
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
    """
    A data structure class representing an entry for education or professional experience.
    It holds data but does not generate HTML itself.
    """
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