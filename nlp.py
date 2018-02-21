# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client


# The text to analyze

def get_action(tokens, id1, id2):
    str = ""
    for i in range(id1, id2 + 1):
        str += tokens[i].lemma + " "

    return str.strip()

def parser(text):
    client = language.LanguageServiceClient()
    document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
    syntax = client.analyze_syntax(document=document, encoding_type='UTF32',)
    tokens = syntax.tokens
    actions = []
    count = 0
    for token in tokens:
        if token.part_of_speech.tag == 6:
            head_idx = token.dependency_edge.head_token_index
            if tokens[head_idx].part_of_speech.tag == 11:
              child_idx = count
              [id1, id2] = sorted([head_idx, child_idx])
              actions.append(get_action(tokens, id1, id2))
        count += 1

    if len(actions) == 0:
        actions.append(text)

    return (tokens, actions)


