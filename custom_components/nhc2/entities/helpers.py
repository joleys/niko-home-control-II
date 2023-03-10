import re


def camel_case_to_words(string: str) -> str:
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', string)
