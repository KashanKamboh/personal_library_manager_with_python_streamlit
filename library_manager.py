# import json
# import os

# data_file = "library.txt"

# def load_library():
#     if os.path.exists(data_file):
#         with open(data_file, "r") as file:
#             return json.load(file)
#     return[]

# def save_library(library):
#     with open("data_file", "w") as file:
#         json.dump(library,file)

# def add_books(library):
#     title = input("Enter the tittle of the book")
#     author = input("Enter the author of the book")
#     year = input("Enter the year of the book")
#     genre = input("Enter the genre of the book")
#     read = input("Have you read the book? (yes/no)").lower() == "yes"

#     new_book = {
#         "title" : title,
#         "author": author,
#         "year": year,
#         "genre":genre,
#         "read": read
#         }
#     library.append(new_book)
#     save_library(library)
#     print(f"Book {title} Added Sucessfully!✨")
# def remove_books(library):
#     title = input("Enter the title of the book to remove: ").strip().lower()
#     for book in library:
#         if book["title"].lower() == title:
#             library.remove(book)
#             print("Book removed successfully!✨\n")
#             return
#     print("Book not found.\n")

# def search_book(library):
#     print("Search by:\n1. Title\n2. Author")
#     choice = input("Enter your choice: ")
#     keyword = input("Enter the search term: ").strip().lower()
#     found = []
#     for book in library:
#         if (choice == "1" and keyword in book["title"].lower()) or \
#            (choice == "2" and keyword in book["author"].lower()):
#             found.append(book)
#     if found:
#         print("Matching Books:")
#         for i, book in enumerate(found, 1):
#             status = "Read" if book["read"] else "Unread"
#             print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
#         print()
#     else:
#         print("No matching books found.\n")

# def display_books(library):
#     if not library:
#         print("Your Library is empty!")
#         return
#     print("Your Library:")
#     for i, book in enumerate(library, 1):
#                  status = "Read" if book["read"] else "Unread"
#                  print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
#                  print()

# def display_states(library):
#      total = len(library)
#      if total == 0:
#           print("No books are in the library!")
#           return
#      read_books = sum(1 for book in library if book["read"])
#      percent_read = (read_books / total) *100
#      print(f"Total Books: {total}")
#      print(f"Percentage read: {percent_read}%\n")

# def main():
#      library = load_library()
#      while True:
         
#          print("\n 📚 <<<<<------ Welcome to your Personal Library Manager ----->>>>>>  \n ")
         
#          print("1. ➕ Add a book")
#          print("2. 🗑️ Remove a book")
#          print("3. 🔍 Search for a book")
#          print("4. 📖 Display all books")
#          print("5. 📊 Display statistics")
#          print("6. 🚪 Exit")
#          choice = int(input("Enter your choice: "))
#          if choice == 1:
#                add_books(library)
#          elif choice == 2:
#                remove_books(library)
#          elif choice == 3:
#                search_book(library)
#          elif choice == 4:
#                display_books(library)
#          elif choice == 5:
#                display_states(library)
#          elif choice == 6:
#                save_library(library)
#                print("Library saved to file. Goodbye!🤗")
#                break
#          else:
#                print("Invalid Choice. Please try again!🙄")

# if __name__ == "__main__":
#     main()


import json
import os
import streamlit as st

data_file = "library.txt"

# Load books from file
def load_library():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

# Save books to file
def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

# Add a new book
def add_book_ui(library):
    st.subheader("➕ Add a Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read it?")
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and author:
                new_book = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read
                }
                library.append(new_book)
                save_library(library)
                st.success(f"Book '{title}' added successfully! ✨")
            else:
                st.warning("Please enter at least the title and author.")

# Remove a book
def remove_book_ui(library):
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        title_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            for book in library:
                if book["title"] == title_to_remove:
                    library.remove(book)
                    save_library(library)
                    st.success(f"Book '{title_to_remove}' removed!")
                    break
    else:
        st.info("No books available to remove.")

# Search books
def search_book_ui(library):
    st.subheader("🔍 Search Books")
    search_by = st.radio("Search by", ["Title", "Author"])
    keyword = st.text_input("Enter search keyword")

    if keyword:
        found = []
        for book in library:
            if (search_by == "Title" and keyword.lower() in book["title"].lower()) or \
               (search_by == "Author" and keyword.lower() in book["author"].lower()):
                found.append(book)
        if found:
            st.write("### Matching Books:")
            st.table(found)
        else:
            st.info("No matching books found.")

# Display all books
def display_books_ui(library):
    st.subheader("📖 All Books")
    if library:
        st.table(library)
    else:
        st.info("Your library is empty.")

# Display stats
def display_stats_ui(library):
    st.subheader("📊 Library Statistics")
    total = len(library)
    if total > 0:
        read_count = sum(1 for book in library if book["read"])
        percent = (read_count / total) * 100
        st.metric("Total Books", total)
        st.metric("Books Read", read_count)
        st.metric("Read %", f"{percent:.2f}%")
    else:
        st.info("No books in your library yet.")

# Main app
def main():
    st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
    st.title("📚 Personal Library Manager")
    st.write("Manage your personal book collection — add, remove, search, and track your reading progress.")

    library = load_library()

    menu = st.sidebar.radio("Menu", [
        "Add Book",
        "Remove Book",
        "Search Book",
        "Display All Books",
        "View Statistics"
    ])

    if menu == "Add Book":
        add_book_ui(library)
    elif menu == "Remove Book":
        remove_book_ui(library)
    elif menu == "Search Book":
        search_book_ui(library)
    elif menu == "Display All Books":
        display_books_ui(library)
    elif menu == "View Statistics":
        display_stats_ui(library)

if __name__ == "__main__":
    main()




     





        
        


