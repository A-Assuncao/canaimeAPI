"""
Implementação do scraper usando Playwright para extrair dados do sistema Canaimé
"""
import asyncio
import logging
import os
import sys
from typing import Dict, List, Optional
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
# Tenta carregar tanto do diretório atual quanto do diretório raiz do projeto
load_dotenv()
load_dotenv(Path(__file__).parents[2] / ".env")

# Configuração para Vercel - Definir antes de importar playwright
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

# Agora importa o Playwright após configurar a variável
from playwright.async_api import async_playwright, Page, Route, Request

# Configuração de codificação para o sistema
# Força UTF-8 para entrada/saída padrão
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Configuração de logging com suporte a UTF-8
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding='utf-8',  # Especifica UTF-8 para os logs
)
logger = logging.getLogger("canaime_scraper")

# URL do site Canaimé
CANAIME_URL = os.getenv("CANAIME_URL", "https://canaime.com.br/sgp2rr/areas/impressoes/UND_ChamadaFOTOS_todos2.php?id_und_prisional=PAMC")
CANAIME_LOGIN_URL = os.getenv("CANAIME_LOGIN_URL", "https://canaime.com.br/sgp2rr/login/login_principal.php")
# URL base para fotos
CANAIME_FOTOS_URL = os.getenv("CANAIME_FOTOS_URL", "https://canaime.com.br/sgp2rr/fotos/presos/")
# Credenciais para login (substitua pelas credenciais reais em variáveis de ambiente)
CANAIME_USER = os.getenv("CANAIME_USER", "usuario")
CANAIME_PASSWORD = os.getenv("CANAIME_PASSWORD", "senha")

# Log das configurações para debug
logger.info(f"CANAIME_URL: {CANAIME_URL}")
logger.info(f"CANAIME_LOGIN_URL: {CANAIME_LOGIN_URL}")
logger.info(f"CANAIME_USER definido: {'Sim' if CANAIME_USER else 'Não'}")
logger.info(f"CANAIME_PASSWORD definido: {'Sim' if CANAIME_PASSWORD else 'Não'}")
logger.info(f"PLAYWRIGHT_BROWSERS_PATH: {os.environ.get('PLAYWRIGHT_BROWSERS_PATH')}")

class CanaimeScraper:
    """Classe responsável por fazer scraping no sistema Canaimé"""

    def __init__(self):
        """Inicializa o scraper"""
        self._dados_presos: Optional[pd.DataFrame] = None
        self._ultima_atualizacao: Optional[str] = None

    @property
    def dados_presos(self) -> Optional[pd.DataFrame]:
        """Retorna o DataFrame com os dados dos presos"""
        return self._dados_presos

    @property
    def ultima_atualizacao(self) -> Optional[str]:
        """Retorna a data e hora da última atualização"""
        return self._ultima_atualizacao

    @property
    def dados_json(self) -> str:
        """Retorna os dados em formato JSON"""
        if self._dados_presos is None:
            return "[]"
        return self._dados_presos.to_json(orient="records", force_ascii=False)
    
    def normalize_text(self, text):
        """
        Normaliza textos que começam com 'REMI' e terminam com '01' ou '02' para
        'REMIÇÃO01' e 'REMIÇÃO02', independentemente dos caracteres intermediários.

        Parameters
        ----------
        text : str
            Texto a ser normalizado.

        Returns
        -------
        str
            Texto normalizado.
        """
        if text.startswith("REMI") and text.endswith("01"):
            logger.debug(f"Texto recebido: {text} -> Texto normalizado: REMIÇÃO01")
            return "REMIÇÃO01"
        elif text.startswith("REMI") and text.endswith("02"):
            logger.debug(f"Texto recebido: {text} -> Texto normalizado: REMIÇÃO02")
            return "REMIÇÃO02"
        else:
            return text
            
    async def block_images(self, route: Route, request: Request):
        """
        Função para bloquear o carregamento de imagens
        """
        if request.resource_type in ["image", "media", "font"]:
            logger.debug(f"Bloqueando recurso: {request.url}")
            await route.abort()
        else:
            await route.continue_()

    async def realizar_login(self, page: Page):
        """
        Realiza o login no sistema Canaimé conforme a lógica fornecida
        
        Args:
            page: Instância da página do Playwright
        """
        logger.info(f"Acessando a página de login: {CANAIME_LOGIN_URL}")
        await page.goto(CANAIME_LOGIN_URL, timeout=0)
        
        logger.info("Realizando login no sistema")
        await page.locator("input[name=\"usuario\"]").click()
        await page.locator("input[name=\"usuario\"]").fill(CANAIME_USER)
        await page.locator("input[name=\"usuario\"]").press("Tab")
        await page.locator("input[name=\"senha\"]").fill(CANAIME_PASSWORD)
        await page.locator("input[name=\"senha\"]").press("Enter")
        
        # Aguardar a navegação após o login
        await page.wait_for_load_state("networkidle")

    async def extrair_dados(self, headless=False) -> None:
        """
        Realiza o scraping de dados do sistema Canaimé
        
        Acessa o site, faz login e extrai informações dos presos,
        organizando em um DataFrame com as colunas: Código, Ala, Cela e Nome.
        """
        logger.info("Iniciando extração de dados do Canaimé")
        raw_unit_list = []
        
        try:
            async with async_playwright() as p:
                # Configuração do browser para desativar JavaScript e não baixar imagens
                browser = await p.chromium.launch(headless=headless)
                context = await browser.new_context(
                    java_script_enabled=False,  # Desativa JavaScript
                )
                
                # Configura o bloqueio de imagens (ainda bloqueamos o download, mas extraímos as URLs)
                page = await context.new_page()
                await page.route("**/*", self.block_images)
                
                # Realiza o login no sistema
                await self.realizar_login(page)
                
                # Acessa a página com os dados dos presos
                logger.info(f"Acessando a página de dados: {CANAIME_URL}")
                await page.goto(CANAIME_URL, timeout=0)
                await page.wait_for_load_state("networkidle")
                
                # Usando a lógica específica do arquivo logica_implementar.py
                logger.info("Extraindo dados dos presos")
                
                # Localiza os elementos conforme a lógica original
                all_entries = page.locator('.titulobkSingCAPS')
                names = page.locator('.titulobkSingCAPS .titulo12bk')
                fotos = page.locator('img')
                
                # Conta o número de entradas
                count = await all_entries.count()
                fotos_count = await fotos.count()
                logger.info(f"Total de entradas encontradas: {count}")
                logger.info(f"Total de fotos encontradas: {fotos_count}")
                
                # Extrai dados de cada entrada
                for i in range(count):
                    # Obtém o conteúdo de texto e processa-o
                    processed_entry = (await all_entries.nth(i).text_content()).replace(" ", "").strip()
                    elements = processed_entry.split('\n')
                    
                    # Verifica se temos elementos suficientes
                    if len(elements) >= 5:
                        code = elements[0]
                        wing_cell = elements[4]
                        inmate = await names.nth(i).text_content()
                        inmate = inmate.strip()
                        
                        # Processa ala e cela
                        wing_cell = wing_cell.replace("ALA:", "")
                        split_index = wing_cell.rfind('/')
                        
                        # Obtém a URL da foto
                        foto_url = ""
                        try:
                            foto_src = await fotos.nth(i).get_attribute('src')
                            if foto_src:
                                foto_url = CANAIME_FOTOS_URL + foto_src[19:]
                                logger.debug(f"URL da foto extraída: {foto_url}")
                        except Exception as e:
                            logger.warning(f"Erro ao extrair URL da foto para o item {i}: {e}")
                        
                        if split_index != -1:
                            wing = self.normalize_text(wing_cell[:split_index].strip())
                            cell = wing_cell[split_index + 1:].strip()
                            
                            # Adiciona os dados à lista
                            raw_unit_list.append({
                                "Código": code[2:] if len(code) > 2 else code,  # Remove os 2 primeiros caracteres
                                "Ala": wing,
                                "Cela": cell,
                                "Foto": foto_url,
                                "Nome": inmate
                            })
                        else:
                            logger.warning(f"Formato inesperado para ala/cela: {wing_cell}")
                    else:
                        logger.warning(f"Formato inesperado para entrada: {processed_entry}")
                
                # Fecha o navegador
                await browser.close()
                
                # Converte para DataFrame
                if raw_unit_list:
                    logger.info(f"Dados extraídos com sucesso. Total de registros: {len(raw_unit_list)}")
                    self._dados_presos = pd.DataFrame(raw_unit_list)
                    self._ultima_atualizacao = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    logger.warning("Nenhum dado foi extraído")
                    
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {e}")
            raise

    async def executar_scraping(self, headless=False) -> None:
        """Função auxiliar para executar o scraping"""
        await self.extrair_dados(headless=headless)


# Instância única do scraper para ser usada em toda a aplicação
scraper = CanaimeScraper()


async def atualizar_dados(headless=False) -> None:
    """
    Função para atualizar os dados via scraping.
    Pode ser chamada pelo agendador de tarefas.
    """
    await scraper.executar_scraping(headless=headless)


# Função para testes
async def main(headless=False):
    """Função principal para testes"""
    await atualizar_dados(headless=headless)
    print(scraper.dados_json)


if __name__ == "__main__":
    asyncio.run(main(headless=False)) 