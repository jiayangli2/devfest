# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text1 = u'I want to have dinner tonight at 8 pm'
document = types.Document(
    content=text1,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
# sentiment = client.analyze_sentiment(document=document).document_sentiment
response = client.analyze_entities(
     document=document,
     encoding_type='UTF32',
)
for entity in response.entities:
    print('=' * 20)
    print('         name: {0}'.format(entity.name))
    print('         type: {0}'.format(entity.type))
    print('     metadata: {0}'.format(entity.metadata))
    print('     salience: {0}'.format(entity.salience))
# print('Text: {}'.format(text1))
# print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))