CHAPTER_SEP = "Rozdział"

# cleaning
HEADER_PATTERN = r'©Kancelaria Sejmu\s+s\.\s+\d+/\d+\s+\d{4}-\d{2}-\d{2}'
# HEADER_PATTERN = r'©Kancelaria Sejmu\s+s\.\s+\d+/\d+\s+\d{4}-\d{2}-\d{2}'
RIGHT_MARGIN_CHANGE_NOTES_PATTERN = r'\nZmiana w.*?(?=\n \n)'
LINEBREAK_PATTERN = r'-\s*\n\s*'

# separating
ART_PATTERN = r'Art. \d+[a-z]?.'
CHAPTER_PATTERN = r'Rozdział \d+[a-z]?'
ARTICLE_POINT_PATTERN = r'\n\d+.'