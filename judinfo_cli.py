import click

@click.command()
@click.help_option('--help', '-h', help='Mensagem de ajuda.')
def main():
    """
    JudInfo CLI - Consulta processos judiciais brasileiros na API DataJud.
    """
    click.echo("Hello, world! JudInfo CLI is starting.")

if __name__ == '__main__':
    main()