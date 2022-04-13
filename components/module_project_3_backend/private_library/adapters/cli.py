import click
import requests
from evraz.classic.messaging import Message, Publisher


def create_cli(publisher: Publisher, MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def library_filling(tags):
        for tag in tags:
            URL_SEARCH = 'https://api.itbook.store/1.0/search'
            URL_BOOKS_ISBN = 'https://api.itbook.store/1.0/books'
            res = requests.get(f'{URL_SEARCH}/{tag}').json()
            count_search = int(res['total'])

            if count_search >= 41:
                page_number = 5
            else:
                page_number = count_search // 10 + 1

            for i in range(1, page_number+1):
                res_page = requests.get(f'{URL_SEARCH}/{tag}/{i}').json()
                books = res_page['books']
                for book in books:
                    isbn13 = book['isbn13']
                    res_book_info = requests.get(
                        f'{URL_BOOKS_ISBN}/{isbn13}'
                    ).json()

                    res_book_info['price_USD'] = float(res_book_info['price'][1:])
                    print(res_book_info)
                    if publisher:
                        publisher.publish(
                            Message(
                                'our_exchange',
                                {
                                    'object_date': res_book_info,
                                }
                            )
                        )

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        MessageBus.consumer.run()

    return cli
