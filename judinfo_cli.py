import click
import requests
from typing import Optional, Dict, Any

# Importa a chave de API do novo arquivo de configuração
from config import API_KEY

class DataJudSimple:
    def __init__(self):
        # Usa a chave de API importada do arquivo config.py
        self.api_key = API_KEY
        self.base_url = "https://api-publica.datajud.cnj.jus.br"

    def verificar_tribunal(self, tribunal: str) -> Dict[str, Any]:
        """Função para verificar o status de um tribunal."""
        try:
            # A API não tem endpoint próprio: utilizando STJ como referência de status.
            endpoint = tribunal if tribunal != 'api' else 'stj'
            response = requests.post(
                f"{self.base_url}/api_publica_{endpoint}/_search",
                headers={
                    "Authorization": f"APIKey {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"query": {"match_all": {}}, "size": 1},
                timeout=10
            )

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }

@click.command()
@click.option('--processo', '-p', help='Número do processo para consulta.')
@click.option('--tribunal', '-t', help='Tribunal (ex: tjmg) ou "all" para todos.')
@click.option('--verificar', '-v', help='Verifica o status da API ou de tribunais. Use "api", um código (tjsp) ou múltiplos (tjsp,tjrj).')
@click.help_option('--help', '-h', help='Mostra esta mensagem de ajuda.')
def main(processo, tribunal, verificar):
    """
    JudInfo CLI - Consulta processos judiciais brasileiros na API DataJud.
    """
    client = DataJudSimple()

    if verificar:
        if verificar.lower() == 'api':
            resultado = client.verificar_tribunal('api')
            if resultado['success']:
                click.echo("✅ API DataJud - Online")
            else:
                click.echo(f"❌ API DataJud - Offline: {resultado.get('error', 'Erro de conexão')}")
        else:
            tribunais_para_verificar = [t.strip() for t in verificar.split(',')]
            for trib in tribunais_para_verificar:
                resultado = client.verificar_tribunal(trib)
                if resultado['success']:
                    click.echo(f"✅ {trib.upper():<8} - Online")
                else:
                    click.echo(f"❌ {trib.upper():<8} - Offline: {resultado.get('error', 'Erro de conexão')}")
        return

    if processo and tribunal:
        click.echo(f"Buscando o processo {processo} no tribunal {tribunal}...")
        return


    ctx = click.get_current_context()
    click.echo("Nenhuma opção válida fornecida. Use -h ou --help para ver os comandos.")
    click.echo(ctx.get_help())


if __name__ == '__main__':
    main()