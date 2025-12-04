from src.backend.cv_creator.objects import *

class CVC:
    NAME = "John Doe"
    PROFESSION = "Developer"
    CITY = "Berlin"
    COUNTRY = "Germany"
    PHONE_NUMBER = "+49abcxyz"
    MAIL = "john.doe@xyz.com"
    SUMMARY_CONTENT = "This is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summaryThis is my summary"
    SIDEBAR_ELEMENTS = [
        Head('Profiles'),
            Links(['xyz.de','xyz.en'], ['GitHub', 'LinkedIn']),
        Head('Technical Skills'),
            Title('Programming Languages'),
                Content('Python, Java, C, Kotlin'),
            Title('Web Development'),
                Content('HTML, CSS, Javascript, jinja'),
            Title('Frameworks & Libraries'),
                Content('Flask, tkinter, win32api, selenium, sqlite3, pytest'),
            Title('Databases'),
                Content('SQLite, SQLAlchemy'),
            Title('Project & Development Tools'),
                Content('Git, GitHub, Git Actions'),
            Title('OS'),
                Content('Windows, Linux, Mac OS X, WSL Ubuntu'),
            Title('Other'),
                Content('OOP'),
        Head('Soft Skills'),
            Title('Problem-solving'),
            Title('Teamwork'),
            Title('Communication'),
            Title('Analytical thinking'),
            Title('Fast learner'),
        Head('Languages'),
            Title('German'),
                Content('Native'),
            Title('English'),
                Content('B2'),
    ]
    PROJECTS = [
        Project('Test', '2024 - 2025', '#nope', 'GitHub Repository', 
                [
                    Bulletpoint('ABC'),
                    Bulletpoint('DEF'),
                    Bulletpoint('GHI')
                ]),
        Project('This repo', '2023 - 2024', '#nope', 'GitHub Repository', 
                [
                    Bulletpoint('KLM'),
                    Bulletpoint('NOP'),
                    Bulletpoint('QRS')
                ])
    ]
    EDUCATION = [
        EducationOrExperience('School', '2006 - 2015', 'Student', 'Berlin, Germany',
                              [
                                  Bulletpoint('This is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpointThis is a bulletpoint'),
                                  Bulletpoint('me too')
                              ])
    ]
    EXPERIENCE = [
        EducationOrExperience('Job', '2016 - 2022', 'Developer', 'Berlin, Germany',
                              [
                                  Bulletpoint('This is a bulletpoint'),
                                  Bulletpoint('me too')
                              ])
    ]