from inquirer import prompt, Text, List
from .licenses import LICENSES
from validate_email import validate_email


def entry_point():

    questions = [
        Text('name', message="What's your package name"),
        Text('author_name', message="What's the name of package's author"),
        Text('author_email', message="What's the e-mail of package's author",
             validate=lambda _, x: validate_email(x)),
        Text('description', message="Brief description the package"),
        List(
            'license', message="What's the package license", choices=LICENSES),
    ]
    answers = prompt(questions)
    print(answers)
