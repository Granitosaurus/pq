import click
import sys

from pq import PQ


@click.command()
@click.argument('query')
@click.option('--css', help='use css selectors instead of xpath', is_flag=True)
@click.option('-t', '--text', 'to_text', help='get only the text (no markup)', is_flag=True)
@click.option('-tt', '--text_all', 'to_text_all', help='like to_text but gets all text including node\'s children', is_flag=True)
@click.option('-f', '--first', 'first', help='only the first element', is_flag=True)
# @click.option('-p', '--pretty', 'to_pretty', help='prettify the output', is_flag=True)
def cli(query, css, to_text, to_text_all, first):
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