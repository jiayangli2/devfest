# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
# text1 = u'I want to have dinner tonight at 8 pm'
# text1 = 'Google, headquartered in Mountain View, unveiled the '
# 'new Android phone at the Consumer Electronic Show.  '
# 'Sundar Pichai said in his keynote that users love '
text1 = 'I want to eat chinese food at 8:00'
# 'their new Android phones.'
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
    print('         name: {}'.format(entity.name))
    print('         type: {}'.format(entity.type))
    for key in entity.metadata:
    	print('     metadata: {},{}'.format(key, entity.metadata[key]))
    print('     salience: {}'.format(entity.salience))
# print('Text: {}'.format(text1))
# print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))