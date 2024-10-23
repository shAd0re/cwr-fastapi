from fastapi import Body, FastAPI
#We imported fast API from fast API.

app = FastAPI()
#We are acknowledging that this is going to be a fast API application
# where we're setting app to what we're importing for fast API.

BOOKS = [
    {'title':'Title One', 'author': 'Author One', 'category': 'science'},
{'title':'Title Two', 'author': 'Author Two', 'category': 'science'},
{'title':'Title Three', 'author': 'Author Three', 'category': 'history'},
{'title':'Title Four', 'author': 'Author Four', 'category': 'math'},
{'title':'Title Five', 'author': 'Author Five', 'category': 'math'},
{'title':'Title Six', 'author': 'Author Two', 'category': 'math'},
]

#We created our own python function of async, which stands for asynchronous def, which is our function call.
@app.get("/books")#path/
async def read_all_books():
    return  BOOKS

@app.get("/books/")#path/
async def authorbooks(author_name):
    author_books = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            author_books.append(book)
    return  author_books

# @app.get("/books/{author_name}")#path/
# async def authorbooks(author_name):
#     author_books = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author_name.casefold():
#             author_books.append(book)
#     return  author_books

@app.get("/books/{book_title}")#path/
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return  book

@app.get("/{category}")#path/
async def get_category(category: str):
    list = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            list.append(book)

    return  list

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

