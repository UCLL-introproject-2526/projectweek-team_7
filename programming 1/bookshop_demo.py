books = {
    "1984": ["George Orwell", "Fiction", 5],
    "Sapiens": ["Yuval Noah Harari", "Non-Fiction", 10],
    "To Kill a Mockingbird": ["Harper Lee", "Fiction", 8],
    "A Brief History of Time": ["Stephen Hawking", "Science", 7],
    "The Catcher in the Rye": ["J.D. Salinger", "Fiction", 6],
    "Becoming": ["Michelle Obama", "Biography", 12],
    "The Great Gatsby": ["F. Scott Fitzgerald", "Fiction", 4],
    "Homo Deus": ["Yuval Noah Harari", "Non-Fiction", 9],
    "The Subtle Art of Not Giving a F*ck": ["Mark Manson", "Self-Help", 15],
    "Educated": ["Tara Westover", "Biography", 10]
}

def add_book(books, title, author, genre, stock):
    if title in books:
        books[title][2] += stock
    else:
        books[title] = [author, genre, stock]

def books_by_author(books, author):

    lis = set()

    for title, info in books.items():
        if info[0] == author:
            lis.add(title)
    
    return lis

print(books_by_author(books, "Yuval Noah Harari"))

def check_availability(books, title):
    return title in books and books[title][2] > 0

customers = {
    "Alice": ("Fiction", "Non-Fiction"),
    "Bob": ("Fiction", "Science"),
    "Charlie": ("Biography", "Non-Fiction"),
    "Diana": ("Self-Help", "Fiction"),
    "Eve": ("Non-Fiction", "Science", "Biography"),
    "Frank": ("Fiction", "Biography"),
    "Grace": ("Self-Help", "Non-Fiction")
}

def add_genre(customers, name, genre):
    if genre not in customers[name]:
         customers[name] = (genre,)
    else:
        genre_set = set(customers[name])
        genre_set.add(genre)
        customers[name] = tuple(genre_set)

def all_genres(customers):
    genre_set = set()
    for genres in customers.values():
        genre_set.update(genres)
    return genre_set

def recommend_books(books, customers, name):
    preferred_genres = customers[name]
    recommended = set()

    for title, info in books.items():
        if info[1] in preferred_genres:
            recommended.add(title)
    
    return recommended
