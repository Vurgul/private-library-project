from evraz.classic.app.errors import AppError


class NoUser(AppError):
    msg_template = 'No user with id {id}'
    code = 'user.no_user'


class NoBook(AppError):
    msg_template = 'No book with id {id}'
    code = 'book.no_book'


class NoJournal(AppError):
    msg_template = 'User with id {id} does not have active book'
    code = 'journal.no_active_book'


class BookBusy(AppError):
    msg_template = 'Book with id {id} busy'
    code = 'book.book_busy'
