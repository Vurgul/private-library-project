import click
import requests


def create_cli(MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument('tags', nargs=-1, type=click.UNPROCESSED)
    def library_filling(tags):
        for tag in tags:
            res = requests.get(f'https://api.itbook.store/1.0/search/{tag}')
            books = res.json()
            print(books)


    #@cli.command()
    #def consumer():
    #    MessageBus.declare_scheme()
    #    MessageBus.consumer.run()

    return cli
