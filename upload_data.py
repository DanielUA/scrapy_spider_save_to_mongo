import json
from models import Author, Quote

def load_authors(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            if not Author.objects(fullname=author_data['fullname']).first():
                author = Author(**author_data)
                author.save()

def load_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            if not Quote.objects(quote=quote_data['quote'], author=quote_data['author']).first():
                quote = Quote(**quote_data)
                quote.save()

if __name__ == "__main__":
    # Укажите пути к вашим JSON файлам
    authors_file = 'json_files/authors.json'
    quotes_file = 'json_files/quotes.json'
    
    # Загружаем данные
    load_authors(authors_file)
    load_quotes(quotes_file)
    
    print("Data successfully uploaded to MongoDB!")

