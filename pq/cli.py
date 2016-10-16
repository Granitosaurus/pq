import sys

import click

from pq import PQ


@click.command()
@click.argument('query')
@click.argument('infile', type=click.File('r'), required=False)
@click.option('--css', help='use css selectors instead of xpath', is_flag=True)
@click.option('-t', '--text', 'to_text', help='get only the text (no markup)', is_flag=True)
@click.option('-tt', '--text_all', 'to_text_all', help='like to_text but gets all text including node\'s children', is_flag=True)
@click.option('-f', '--first', 'first', help='only the first element', is_flag=True)
def cli(query, infile, css, to_text, to_text_all, first):
    """Command line xml and json processor for xpath and css selectors.
    """
    if infile:
        piped_data = infile.read()
    else:
        piped_data = ''.join(sys.stdin)
    pq = PQ(piped_data)
    if css:
        result = pq.css(query, to_text=to_text, to_text_all=to_text_all)
    else:
        result = pq.xpath(query, to_text=to_text, to_text_all=to_text_all)
    if first:
        result = result[0] if result else None
    pq.output(result)

if __name__ == "__main__":
    cli()