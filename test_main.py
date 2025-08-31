import pytest

from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("name", ["", "a" * 41])
    def test_add_new_book_not_added_when_name_invalid_length(self, collector, name):
        collector.add_new_book(name)

        assert name not in collector.get_books_genre()

    @pytest.mark.parametrize("name", ["a", "a" * 40])
    def test_add_new_book_adds_when_name_valid_and_not_exists(self, collector, name):
        collector.add_new_book(name)

        assert name in collector.books_genre

    def test_add_new_book_not_adds_duplicate(self, collector):
        name = "Гордость и предубеждение и зомби"
        collector.add_new_book(name)
        before_size = len(collector.get_books_genre())

        collector.add_new_book(name)
        after_size = len(collector.get_books_genre())

        assert after_size == before_size

    def test_set_book_genre_sets_valid_genre_for_existing_book(self, collector):
        name = "Гордость и предубеждение и зомби"
        collector.add_new_book(name)
        collector.set_book_genre(name, "Фантастика")

        assert collector.books_genre[name] == "Фантастика"

    def test_set_book_genre_ignores_invalid_genre(self, collector):
        name = "Гордость и предубеждение и зомби"
        collector.add_new_book(name)
        collector.set_book_genre(name, "Фанта111стика")

        assert collector.books_genre[name] == ""

    def test_set_book_genre_does_nothing_for_unknown_book(self, collector):
        unknown_book = "Несуществующая книга"
        collector.set_book_genre(unknown_book, "Фантастика")

        assert unknown_book not in collector.books_genre

    def test_get_books_genre_initially_empty(self, collector):
        assert collector.get_books_genre() == {}

    def test_get_books_genre_reflects_added_books_and_genres(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")

        result = collector.get_books_genre()

        assert result == {"Шерлок Холмс": "Детективы", }

    def test_get_book_genre_returns_empty_string_for_new_book(self, collector):
        name = "Гордость и предубеждение и зомби"
        collector.add_new_book(name)

        result = collector.get_book_genre(name)

        assert result == ""

    def test_get_book_genre_returns_set_genre(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")

        assert collector.get_book_genre("Шерлок Холмс") == "Детективы"

    def test_get_books_with_specific_genre_returns_empty_when_no_books(self, collector):
        assert collector.get_books_with_specific_genre("Детективы") == []

    def test_get_books_with_specific_genre_single_match_happy_path(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")

        assert collector.get_books_with_specific_genre("Детективы") == ["Шерлок Холмс"]

    def test_get_books_for_children_returns_empty_when_no_books(self, collector):
        assert collector.get_books_for_children() == []

    def test_get_books_for_children_single_match_happy_path(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")

        assert collector.get_books_for_children() == ["Дюна"]

    def test_children_list_updates_on_safe_to_restricted_change(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Комедии")
        assert collector.get_books_for_children() == ["Книга"]

        collector.set_book_genre("Книга", "Ужасы")
        assert collector.get_books_for_children() == []

    def test_add_book_in_favorites_adds_existing_book(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        assert collector.get_list_of_favorites_books() == ["Книга"]

    def test_add_book_in_favorites_does_not_add_nonexistent_book(self, collector):
        collector.add_book_in_favorites("Несуществующая")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_removes_existing_book(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")

        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_initially_empty(self, collector):

        assert collector.get_list_of_favorites_books() == []

    def test_added_favorite_appears_in_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")

        assert "Книга" in collector.get_list_of_favorites_books()