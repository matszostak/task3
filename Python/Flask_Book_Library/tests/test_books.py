import unittest
from project import db, app
from project.books.models import Book

class TestBookModel(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()


    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test_valid_book_create(self):
        with app.app_context():
            test_book0 = Book(name="Book1", author="Author1", year_published=2024, book_type="Fiction", status='available')
            db.session.add(test_book0)
            db.session.commit()
            test_book0 = Book.query.filter_by(name="Book1").first()
            self.assertIsNotNone(test_book0)
            self.assertEqual(test_book0.name, "Book1")
            self.assertEqual(test_book0.author, "Author1")
            self.assertEqual(test_book0.year_published, 2024)
            self.assertEqual(test_book0.book_type, "Fiction")
            self.assertEqual(test_book0.status, "available")


    def test_duplicate_book_create(self):
        with app.app_context():
            test_book1 = Book(name="Book2", author="Author2", year_published=2024, book_type="Fiction")
            test_book2 = Book(name="Book2", author="Author2", year_published=2024, book_type="Fiction")
            db.session.add(test_book1)
            db.session.commit()
            db.session.add(test_book2)
            with self.assertRaises(Exception):
                db.session.commit()


    def test_invalid_book_name(self):
        with app.app_context():
            test_book = Book(name=None, author="Author3", year_published=2024, book_type="Fiction")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    def test_book_invalid_author(self):
        with app.app_context():
            test_book = Book(name="Book4", author=None, year_published=2024, book_type="Fiction")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    def test_book_invalid_year(self):
        with app.app_context():
            test_book = Book(name="Book5", author='Author5', year_published=None, book_type="Fiction")        
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    def test_book_invalid_book_type(self):
        with app.app_context():
            test_book = Book(name="Book6", author="Author6", year_published=1920, book_type=None)
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    # === === === ===
    def test_book_sql_injection(self):
        with app.app_context():
            test_book = Book(name="Book7'; DROP TABLE books; --", author="Author7", year_published=2024, book_type="Fiction")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    def test_book_xss(self):
        with app.app_context():
            test_book = Book(name="<script>alert('XSS')</script>", author="Author8", year_published=2024, book_type="Fiction")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    # === === === ===
    def test_create_book_long_name(self):
        with app.app_context():
            test_book = Book(name="Book9" * 1000, author="Author9", year_published=2024, book_type="Fiction")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


    def test_create_book_long_author(self):
        with app.app_context():
            test_book = Book(name="Book10", author="A" * 1000, year_published=2024, book_type="Ficiton")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()
    

    def test_create_book_long_year(self):
        with app.app_context():
            test_book = Book(name="Book11", author="Author11", year_published=2024202420242024, book_type="Ficiton")
            with self.assertRaises(Exception):
                db.session.add(test_book)
                db.session.commit()


if __name__ == '__main__':
    unittest.main()