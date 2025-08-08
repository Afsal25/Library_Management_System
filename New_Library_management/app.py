from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

BOOK_FILE = 'books.json'

# --------------------
# Utility Functions
# --------------------
def load_books():
    with open(BOOK_FILE, 'r') as f:
        return json.load(f)

def save_books(books):
    with open(BOOK_FILE, 'w') as f:
        json.dump(books, f, indent=4)

# --------------------
# Home / Menu Page
# --------------------
@app.route('/')
@app.route('/menu')
def menu():
    books = load_books()
    return render_template('menu.html', books=books)

# --------------------
# Add (Book) a Book
# --------------------
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    result=None
    if request.method == 'POST':
        title = request.form['title'].strip()
        books = load_books()
        found = False
        for book in books:
            if book['title'].strip().lower() == title.lower():
                found = True    
                if book['status'] == 'available':
                    book['status'] = 'issued'
                    save_books(books)
                    break
            #if book['title'].strip().lower() != title.lower():
                #result= f"{title} this book as not in library"
                #break
    
        return redirect(url_for('menu'))

    # This part is for GET request → show the form
    books = load_books()
    return render_template('add_book.html', books=books,result=result)



# --------------------
# Search a Book
# --------------------
@app.route('/search', methods=['GET', 'POST'])
def search_book():
    result = None
    if request.method == 'POST':
        search_title = request.form['title'].strip().lower()
        books = load_books()
        found = False

        for book in books:
            if book['title'].strip().lower() == search_title:
                found = True
                if book['status'] == 'available':
                    result = f"✅ '{book['title']}' is available in the library."
                else:
                    result = f"❌ '{book['title']}' is currently issued."
                break

        if not found:
            result = "🚫 This book is not available in the library."

    return render_template('search_book.html', result=result)

# --------------------
# Issue a Book
# --------------------
@app.route('/issued', methods=['GET', 'POST'])
def issued_book():
    result = None
    if request.method == 'POST':
        title = request.form['title'].strip().lower()
        books = load_books()
        for book in books:
            if (book['title'].strip().lower() == title and book['status'] == 'issued'):
                    #book['status'] = 'issued'
                    #save_books(books)
                    result = f"❌ '{book['title']}' is already issued."
                    break
            elif(book['title'].strip().lower() == title and book['status']=='available'):
                    book['status'] = 'available'
                    save_books(books)
                    result = f"✅ '{book['title']}' has not been issued."
                    break
            else:
              result = "🚫 This book is not available in the library."
    return render_template('issued_book.html', result=result)

# --------------------
# Return a Book
# --------------------
@app.route('/return', methods=['GET', 'POST'])
def return_book():
    result = None
    if request.method == 'POST':
        title = request.form['title'].strip().lower()
        books = load_books()
        for book in books:
            if book['title'].strip().lower() == title:
                if book['status'] == 'available':
                    result = f"ℹ️ '{book['title']}' is already available in the library."
                else:
                    book['status'] = 'available'
                    save_books(books)
                    result = f"✅ '{book['title']}' has been returned successfully."
                break
        else:
            result = "🚫 This book is not available in the library."
    return render_template('return_book.html', result=result)
@app.route('/update', methods=['GET', 'POST'])
def update_book():
    result = None

    if request.method == 'POST':
        title = request.form['title'].strip()
        books = load_books()
        
        # Check if this title already exists
        for book in books:
            if book['title'].strip().lower() == title.lower():
                result = f"⚠️ '{title}' already exists."
                break
        else:
            # Only add if title not found
            books.append({"title": title, "status": "available"})
            save_books(books)
            result = f"✅ '{title}' added successfully!"

        # Optionally, redirect or just render the page with message
        return render_template('add_book.html', result=result)

    return render_template('update_book.html', result=result)

# --------------------
# Run the App
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
