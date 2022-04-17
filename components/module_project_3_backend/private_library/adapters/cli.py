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
            if publisher:
                publisher.publish(Message('our_exchange', {
                    'tag': tag,
                }))

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        MessageBus.consumer.run()

    return cli
