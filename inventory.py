import json
from pathlib import Path
from library_manager.book import Book
import logging

logging.basicConfig(level=logging.INFO, filename="library.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

CATALOG_FILE = Path("catalog.json")

class LibraryInventory:

    def __init__(self):
        self.books = []
        self.load_catalog()

    def load_catalog(self):
        try:
            if CATALOG_FILE.exists():
                with open(CATALOG_FILE, "r") as f:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
            else:
                self.save_catalog()
        except Exception as e:
            logging.error("Error loading catalog: %s", e)
            self.books = []
            self.save_catalog()

    def save_catalog(self):
        try:
            with open(CATALOG_FILE, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error("Error saving catalog: %s", e)

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_catalog()
        logging.info("Book added: %s", title)

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books