from textblob import TextBlob
from textblob import Word

zen = TextBlob("Beautiful is better than ugly,Explicit is better than implicit,Simple is better than complex,Use 4 spaces per indentation level")
print(zen.words)  # 分词

print(zen.words.singularize()) #名词变单数

u=zen.words.pluralize()  # 名词变复数
for term in u:
    w = Word(term)
    print(w.lemmatize()) #默认名词 还原
    print(w.lemmatize('v'))