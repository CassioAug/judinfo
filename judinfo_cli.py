import click
import requests
import json
from typing import Optional, Dict, Any

# Importa a chave de API do novo arquivo de configuração
from config import API_KEY

class DataJudSimple:
    def __init__(self):
        # Usa a chave de API importada do arquivo config.py
        self.api_key = API_KEY
        self.base_url = "https://api-publica.datajud.cnj.jus.br"

    def consultar_processo(self, numero: str, tribunal: str) -> Optional[Dict[str, Any]]:
        """Função para consultar processos."""
        url = f"{self.base_url}/api_publica_{tribunal}/_search"
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"APIKey {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"query": {"match": {"numeroProcesso": numero}}},
                timeout=30
            )
            
            if response.status_code != 200:
                click.echo(f"Erro na API ao consultar {tribunal.upper()}: {response.status_code}", err=True)
                return None
            
            data = response.json()
            
            # Se não encontrar resultados, retorna None
            if data['hits']['total']['value'] == 0:
                return None
            
            # Retorna o primeiro resultado encontrado
            return data['hits']['hits'][0]['_source']
            
        except requests.exceptions.RequestException as e:
            click.echo(f"Erro de conexão ao consultar {tribunal.upper()}: {e}", err=True)
            return None

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
@click.option('--verificar', '-v', help='Verifica o status da API ou de tribunais. Use "api", um código (tjsp), múltiplos (tjsp,tjrj) ou "all".')
@click.option('--saida', '-s', type=click.Choice(['json', 'resumo', 'completo']), default='resumo', help='Formato de saída da consulta.')
@click.help_option('--help', '-h', help='Mostra esta mensagem de ajuda.')

def main(processo, tribunal, verificar, saida):
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
        resultado = client.consultar_processo(processo, tribunal)
        if not resultado:
            click.echo(f"❌ Processo não encontrado no tribunal {tribunal.upper()}")
            click.echo("💡 Verifique se o n° está correto ou se há atraso na sincronização dos dados.")
        else:
            if saida == 'json':
                # Imprime o JSON em formato bruto retornado pela API
                click.echo(json.dumps(resultado, indent=2, ensure_ascii=False))
            elif saida == 'resumo':
                exibir_resumo(resultado)
            else: # 'completo'
                exibir_completo(resultado)
        return

    ctx = click.get_current_context()
    click.echo("Nenhuma opção válida fornecida. Use -h ou --help para ver os comandos.")
    click.echo(ctx.get_help())

def exibir_resumo(processo):
    """Exibe resuno organizado do processo, apenas com os dados essenciais."""
    click.echo("\n" + "="*50)
    click.echo("📄 RESUMO DO PROCESSO")
    click.echo("="*50)
    click.echo(f"🔢 Número: {processo.get('numeroProcesso', 'N/A')}")
    click.echo(f"🏛️  Tribunal: {processo.get('tribunal', 'N/A')}")
    
    if processo.get('classe'):
        click.echo(f"📋 Classe: {processo['classe'].get('nome', 'N/A')}")
    click.echo(f"📅 Data de Ajuizamento: {formatar_data(processo.get('dataAjuizamento'))}")
    click.echo(f"⚖️  Grau: {processo.get('grau', 'N/A')}")
    movimentos = processo.get('movimentos', [])
    click.echo(f"🔄 Total de Movimentos: {len(movimentos)}")
    if movimentos:
        # Captura movimento mais recente da lista
        ultimo = movimentos[-1]
        click.echo(f"📝 Último Movimento: {ultimo.get('nome', 'N/A')}")
        click.echo(f"⏰ Data: {formatar_data(ultimo.get('dataHora'))}")
    click.echo("="*50)

def exibir_completo(processo):
    """Exibe versão mais detalhada do processo."""
    exibir_resumo(processo)
    # continuar daqui...

def formatar_data(data_string):
    """Formata data para formato legível: DD/MM/AAAA HH:MM."""
    if not data_string:
        return "N/A"
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(data_string.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        # Se data estiver em formato inesperado retorna a string original
        return data_string

if __name__ == '__main__':
    main()