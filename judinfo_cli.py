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

def get_all_courts():
    """Retorna uma lista de todos os códigos de tribunais suportados."""
    return [
        'tst', 'tse', 'stj', 'stm', 'trf1', 'trf2', 'trf3', 'trf4', 'trf5', 'trf6',
        'tjac', 'tjal', 'tjam', 'tjap', 'tjba', 'tjce', 'tjdft', 'tjes', 'tjgo',
        'tjma', 'tjmg', 'tjms', 'tjmt', 'tjpa', 'tjpb', 'tjpe', 'tjpi', 'tjpr',
        'tjrj', 'tjrn', 'tjro', 'tjrr', 'tjrs', 'tjsc', 'tjse', 'tjsp', 'tjto',
        'trt1', 'trt2', 'trt3', 'trt4', 'trt5', 'trt6', 'trt7', 'trt8', 'trt9',
        'trt10', 'trt11', 'trt12', 'trt13', 'trt14', 'trt15', 'trt16', 'trt17',
        'trt18', 'trt19', 'trt20', 'trt21', 'trt22', 'trt23', 'trt24',
        'tre-ac', 'tre-al', 'tre-am', 'tre-ap', 'tre-ba', 'tre-ce', 'tre-dft',
        'tre-es', 'tre-go', 'tre-ma', 'tre-mg', 'tre-ms', 'tre-mt', 'tre-pa',
        'tre-pb', 'tre-pe', 'tre-pi', 'tre-pr', 'tre-rj', 'tre-rn', 'tre-ro',
        'tre-rr', 'tre-rs', 'tre-sc', 'tre-se', 'tre-sp', 'tre-to',
        'tjmmg', 'tjmrs', 'tjmsp'
    ]

def get_all_courts_categorized():
    """Retorna uma lista de todos os códigos de tribunais suportados."""
    return {
        "STJ": ["stj"],
        "Tribunais Regionais": sorted([
            'tst', 'tse', 'stm', 'trf1', 'trf2', 'trf3', 'trf4', 'trf5', 'trf6',
            'trt1', 'trt2', 'trt3', 'trt4', 'trt5', 'trt6', 'trt7', 'trt8', 'trt9',
            'trt10', 'trt11', 'trt12', 'trt13', 'trt14', 'trt15', 'trt16', 'trt17',
            'trt18', 'trt19', 'trt20', 'trt21', 'trt22', 'trt23', 'trt24',
            'tre-ac', 'tre-al', 'tre-am', 'tre-ap', 'tre-ba', 'tre-ce', 'tre-dft',
            'tre-es', 'tre-go', 'tre-ma', 'tre-mg', 'tre-ms', 'tre-mt', 'tre-pa',
            'tre-pb', 'tre-pe', 'tre-pi', 'tre-pr', 'tre-rj', 'tre-rn', 'tre-ro',
            'tre-rr', 'tre-rs', 'tre-sc', 'tre-se', 'tre-sp', 'tre-to',
        ]),
        "Tribunais Estaduais": sorted([
            'tjac', 'tjal', 'tjam', 'tjap', 'tjba', 'tjce', 'tjdft', 'tjes', 'tjgo',
            'tjma', 'tjmg', 'tjms', 'tjmt', 'tjpa', 'tjpb', 'tjpe', 'tjpi', 'tjpr',
            'tjrj', 'tjrn', 'tjro', 'tjrr', 'tjrs', 'tjsc', 'tjse', 'tjsp', 'tjto',
            'tjmmg', 'tjmrs', 'tjmsp'
        ])
    }

@click.command()
@click.option('--processo', '-p', help='Número do processo para consulta.')
@click.option('--tribunal', '-t', help='Tribunal (ex: tjmg) ou "all" para todos.')
@click.option('--verificar', '-v', help='Verifica o status da API ou de tribunais. Use "api", um código (tjsp), múltiplos (tjsp,tjrj) ou "all".')
@click.option('--listar-tribunais', '-lt', is_flag=True, help='Lista todos os códigos de tribunais suportados.')
@click.option('--saida', '-s', type=click.Choice(['json', 'resumo', 'completo']), default='resumo', help='Formato de saída da consulta.')
@click.help_option('--help', '-h', help='Mostra esta mensagem de ajuda.')

def main(processo, tribunal, verificar, listar_tribunais, saida):
    """
    JudInfo CLI - Consulta processos judiciais brasileiros na API DataJud.
    \b
    EXEMPLOS DE USO:
      judinfo -lt                          # Lista todos os tribunais
      judinfo -v api                       # Verifica a saúde geral da API
      judinfo -v trf1                      # Verifica um tribunal específico
      judinfo -v tjsp,tjrj,tjmg            # Verifica múltiplos tribunais
      judinfo -v all                       # Verifica TODOS os tribunais
      judinfo -p <numero> -t tjmg          # Consulta um processo
      judinfo -p <numero> -t all           # Busca processo em TODOS tribunais
      judinfo -p <numero> -t tjmg -s json  # Consulta com saída em JSON
    """
    
    client = DataJudSimple()

    if listar_tribunais:
        exibir_todos_tribunais()
        return
    
    if verificar:
        if verificar.lower() == 'all':
            verificar_todos_tribunais(client)
        elif verificar.lower() == 'api':
            resultado = client.verificar_tribunal('stj')
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
        if tribunal.lower() == 'all':
            buscar_em_todos_tribunais(client, processo, saida)
        else:
            resultado = client.consultar_processo(processo, tribunal)
            if not resultado:
                click.echo(f"❌ Processo não encontrado no tribunal {tribunal.upper()}")
                click.echo("💡 Verifique se o número está correto ou se há atraso na sincronização dos dados.")
            else:
                if saida == 'json':
                    click.echo(json.dumps(resultado, indent=2, ensure_ascii=False))
                elif saida == 'resumo':
                    exibir_resumo(resultado)
                else:
                    exibir_completo(resultado)
        return

    ctx = click.get_current_context()
    click.echo("Nenhuma opção válida fornecida. Use -h ou --help para ver os comandos.")
    click.echo(ctx.get_help())

def verificar_todos_tribunais(client):
    """Verifica a conexão com todos os tribunais suportados."""
    todos_tribunais = get_all_courts()
    click.echo(f"Verificando {len(todos_tribunais)} tribunais...")
    online_count = 0
    
    with click.progressbar(todos_tribunais, label="Progresso") as bar:
        for tribunal in bar:
            resultado = client.verificar_tribunal(tribunal)
            if resultado['success']:
                online_count += 1
    
    click.echo(f"\nResultado: {online_count} de {len(todos_tribunais)} tribunais estão online.")

def exibir_todos_tribunais():
    """Exibe TODOS os tribunais suportados pela API."""
    tribunais = {
        "Tribunais Superiores": {"tst": "Tribunal Superior do Trabalho", "tse": "Tribunal Superior Eleitoral", "stj": "Superior Tribunal de Justiça", "stm": "Superior Tribunal Militar"},
        "Justiça Federal": {"trf1": "TRF 1ª Região", "trf2": "TRF 2ª Região", "trf3": "TRF 3ª Região", "trf4": "TRF 4ª Região", "trf5": "TRF 5ª Região", "trf6": "TRF 6ª Região"},
        "Justiça Estadual": {'tjac': 'TJ Acre', 'tjal': 'TJ Alagoas', 'tjam': 'TJ Amazonas', 'tjap': 'TJ Amapá', 'tjba': 'TJ Bahia', 'tjce': 'TJ Ceará', 'tjdft': 'TJ Distrito Federal', 'tjes': 'TJ Espírito Santo', 'tjgo': 'TJ Goiás', 'tjma': 'TJ Maranhão', 'tjmg': 'TJ Minas Gerais', 'tjms': 'TJ Mato Grosso do Sul', 'tjmt': 'TJ Mato Grosso', 'tjpa': 'TJ Pará', 'tjpb': 'TJ Paraíba', 'tjpe': 'TJ Pernambuco', 'tjpi': 'TJ Piauí', 'tjpr': 'TJ Paraná', 'tjrj': 'TJ Rio de Janeiro', 'tjrn': 'TJ Rio Grande do Norte', 'tjro': 'TJ Rondônia', 'tjrr': 'TJ Roraima', 'tjrs': 'TJ Rio Grande do Sul', 'tjsc': 'TJ Santa Catarina', 'tjse': 'TJ Sergipe', 'tjsp': 'TJ São Paulo', 'tjto': 'TJ Tocantins'},
        "Justiça do Trabalho": {"trt1": "TRT 1ª Região", "trt2": "TRT 2ª Região", "trt3": "TRT 3ª Região", "trt4": "TRT 4ª Região", "trt5": "TRT 5ª Região", "trt6": "TRT 6ª Região", "trt7": "TRT 7ª Região", "trt8": "TRT 8ª Região", "trt9": "TRT 9ª Região", "trt10": "TRT 10ª Região", "trt11": "TRT 11ª Região", "trt12": "TRT 12ª Região", "trt13": "TRT 13ª Região", "trt14": "TRT 14ª Região", "trt15": "TRT 15ª Região", "trt16": "TRT 16ª Região", "trt17": "TRT 17ª Região", "trt18": "TRT 18ª Região", "trt19": "TRT 19ª Região", "trt20": "TRT 20ª Região", "trt21": "TRT 21ª Região", "trt22": "TRT 22ª Região", "trt23": "TRT 23ª Região", "trt24": "TRT 24ª Região"},
        "Justiça Eleitoral": {'tre-ac': 'TRE Acre', 'tre-al': 'TRE Alagoas', 'tre-am': 'TRE Amazonas', 'tre-ap': 'TRE Amapá', 'tre-ba': 'TRE Bahia', 'tre-ce': 'TRE Ceará', 'tre-dft': 'TRE Distrito Federal', 'tre-es': 'TRE Espírito Santo', 'tre-go': 'TRE Goiás', 'tre-ma': 'TRE Maranhão', 'tre-mg': 'TRE Minas Gerais', 'tre-ms': 'TRE Mato Grosso do Sul', 'tre-mt': 'TRE Mato Grosso', 'tre-pa': 'TRE Pará', 'tre-pb': 'TRE Paraíba', 'tre-pe': 'TRE Pernambuco', 'tre-pi': 'TRE Piauí', 'tre-pr': 'TRE Paraná', 'tre-rj': 'TRE Rio de Janeiro', 'tre-rn': 'TRE Rio Grande do Norte', 'tre-ro': 'TRE Rondônia', 'tre-rr': 'TRE Roraima', 'tre-rs': 'TRE Rio Grande do Sul', 'tre-sc': 'TRE Santa Catarina', 'tre-se': 'TRE Sergipe', 'tre-sp': 'TRE São Paulo', 'tre-to': 'TRE Tocantins'},
        "Justiça Militar": {'tjmmg': 'TJM Minas Gerais', 'tjmrs': 'TJM Rio Grande do Sul', 'tjmsp': 'TJM São Paulo'}
    }
    
    total_tribunais = sum(len(lista) for lista in tribunais.values())
    click.echo(f"🏛️  TOTAL DE {total_tribunais} TRIBUNAIS SUPORTADOS PELA API:\n")
    
    for categoria, lista_tribunais in tribunais.items():
        click.echo(f"📊 {categoria} ({len(lista_tribunais)} tribunais):")
        sorted_tribunais = sorted(lista_tribunais.items())
        for codigo, nome in sorted_tribunais:
            click.echo(f"  {codigo:8} - {nome}")
        click.echo()

def buscar_em_todos_tribunais(client, processo, saida):
    """Busca um processo em TODOS os tribunais suportados."""
    todos_tribunais = get_all_courts()
    click.echo(f"🔍 Buscando processo {processo} em {len(todos_tribunais)} tribunais...")
    click.echo("⏰ Isso pode levar vários minutos...")
    click.echo("💡 Pressione Ctrl+C para interromper a busca\n")
    encontrado = False
    
    with click.progressbar(todos_tribunais, label="Progresso da Busca") as bar:
        for tribunal in bar:
            try:
                resultado = client.consultar_processo(processo, tribunal)
                if resultado:
                    click.echo(f"\n🎯 ENCONTRADO no tribunal: {tribunal.upper()}")
                    encontrado = True
                    if saida == 'json':
                        click.echo(json.dumps(resultado, indent=2, ensure_ascii=False))
                    elif saida == 'resumo':
                        exibir_resumo(resultado)
                    else:
                        exibir_completo(resultado)
                    return # Encerra a busca após encontrar o primeiro resultado
            except KeyboardInterrupt:
                click.echo(f"\n⏹️  Busca interrompida.")
                return
            except Exception:
                continue # Continua para o próximo tribunal em caso de erro
    
    if not encontrado:
        click.echo(f"\n❌ Processo não encontrado em {len(todos_tribunais)} tribunais testados.")

def exibir_resumo(processo):
    """Exibe resumo organizado do processo."""
    click.echo("\n" + "="*50)
    click.echo("📄 RESUMO DO PROCESSO")
    click.echo("="*50)
    click.echo(f"🔢 Número: {processo.get('numeroProcesso', 'N/A')}")
    click.echo(f"🏛️  Tribunal: {processo.get('tribunal', 'N/A')}")
    
    if processo.get('classe'):
        click.echo(f"📋 Classe: {processo['classe'].get('nome', 'N/A')}")
    click.echo(f"📅 Data de Ajuizamento: {formatar_data(processo.get('dataAjuizamento'))}")
    click.echo(f"⚖️  Grau: {processo.get('grau', 'N/A')}")
    if processo.get('sistema'):
        click.echo(f"🖥️  Sistema: {processo['sistema'].get('nome', 'N/A')}")
    if processo.get('formato'):
        click.echo(f"📁 Formato: {processo['formato'].get('nome', 'N/A')}")
    if processo.get('orgaoJulgador'):
        click.echo(f"👨‍⚖️  Órgão Julgador: {processo['orgaoJulgador'].get('nome', 'N/A')}")
    if processo.get('assuntos'):
        assuntos = ", ".join([a.get('nome', 'N/A') for a in processo['assuntos']])
        click.echo(f"🏷️  Assuntos: {assuntos}")
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
    movimentos = processo.get('movimentos', [])
    if movimentos:
        click.echo("\n📋 ÚLTIMOS 5 MOVIMENTOS:")
        click.echo("-" * 40)
        # Mostra os últimos 5 movimentos, do mais recente ao mais antigo
        for mov in reversed(movimentos[-5:]):
            data_formatada = formatar_data(mov.get('dataHora'))
            click.echo(f"  {data_formatada} - {mov.get('nome', 'N/A')}")

def formatar_data(data_string):
    """Formata data para: DD/MM/AAAA HH:MM."""
    if not data_string:
        return "N/A"
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(data_string.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        # Se formato inesperado retorna string original
        return data_string

if __name__ == '__main__':
    main()