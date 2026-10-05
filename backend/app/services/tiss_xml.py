import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from lxml import etree

def gerar_xml_guia_sps_sadt(solicitacao_data: dict) -> str:
    """
    Gera uma estrutura XML simplificada no padrão TISS ANS para Guia SP/SADT.
    """
    # Namespaces padrão TISS
    ans_ns = "http://www.ans.gov.br/padroes/tiss/schemas"
    
    ET.register_namespace('ans', ans_ns)
    
    mensagem = ET.Element(f'{{{ans_ns}}}mensagemTISS')
    
    # Cabeçalho da Mensagem
    cabecalho = ET.SubElement(mensagem, f'{{{ans_ns}}}cabecalho')
    identificacao_transacao = ET.SubElement(cabecalho, f'{{{ans_ns}}}identificacaoTransacao')
    
    tipo_transacao = ET.SubElement(identificacao_transacao, f'{{{ans_ns}}}tipoTransacao')
    tipo_transacao.text = "SOLICITACAO_PROCEDIMENTOS"
    
    sequencial_transacao = ET.SubElement(identificacao_transacao, f'{{{ans_ns}}}sequencialTransacao')
    sequencial_transacao.text = str(solicitacao_data.get("id", 1))
    
    data_registro = ET.SubElement(identificacao_transacao, f'{{{ans_ns}}}dataRegistroTransacao')
    data_registro.text = datetime.now().strftime("%Y-%m-%d")
    
    hora_registro = ET.SubElement(identificacao_transacao, f'{{{ans_ns}}}horaRegistroTransacao')
    hora_registro.text = datetime.now().strftime("%H:%M:%S")

    # Prestador / Clínica
    origem = ET.SubElement(cabecalho, f'{{{ans_ns}}}origem')
    codigo_prestador = ET.SubElement(origem, f'{{{ans_ns}}}codigoPrestadorNaOperadora')
    codigo_prestador.text = str(solicitacao_data.get("clinica_id", "000000"))

    # Corpo da Guia TISS
    prestador_para_operadora = ET.SubElement(mensagem, f'{{{ans_ns}}}prestadorParaOperadora')
    solicitacao_sadt = ET.SubElement(prestador_para_operadora, f'{{{ans_ns}}}solicitacaoSPSADT')
    
    cabecalho_guia = ET.SubElement(solicitacao_sadt, f'{{{ans_ns}}}cabecalhoGuia')
    numero_guia = ET.SubElement(cabecalho_guia, f'{{{ans_ns}}}numeroGuiaPrestador')
    numero_guia.text = str(solicitacao_data.get("id"))

    # Dados do Beneficiário / Paciente
    dados_beneficiario = ET.SubElement(solicitacao_sadt, f'{{{ans_ns}}}dadosBeneficiario')
    numero_carteira = ET.SubElement(dados_beneficiario, f'{{{ans_ns}}}numeroCarteira')
    numero_carteira.text = solicitacao_data.get("paciente_carteira", "0000000000")

    # Procedimentos Solicitados
    procedimentos = ET.SubElement(solicitacao_sadt, f'{{{ans_ns}}}procedimentosSolicitados')
    procedimento = ET.SubElement(procedimentos, f'{{{ans_ns}}}procedimento')
    
    codigo_procedimento = ET.SubElement(procedimento, f'{{{ans_ns}}}codigoProcedimento')
    codigo_procedimento.text = solicitacao_data.get("procedimento", "").split(" - ")[0]
    
    descricao_procedimento = ET.SubElement(procedimento, f'{{{ans_ns}}}descricaoProcedimento')
    descricao_procedimento.text = solicitacao_data.get("procedimento", "")

    # Formatação com indentação
    raw_xml = ET.tostring(mensagem, encoding='utf-8')
    parsed_xml = minidom.parseString(raw_xml)
    return parsed_xml.toprettyxml(indent="  ")


def validar_estrutura_xml_tiss(xml_string: str) -> tuple[bool, str]:
    """
    Valida se a string XML possui uma estrutura bem-formada e respeita o namespace TISS ANS.
    """
    try:
        parser = etree.XMLParser(recover=False)
        tree = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        
        if "ans.gov.br" not in tree.tag:
            return False, "O XML não contém o namespace oficial TISS ANS (http://www.ans.gov.br/padroes/tiss/schemas)."
            
        return True, "XML TISS válido e estruturado corretamente!"
    except etree.XMLSyntaxError as e:
        return False, f"Erro de sintaxe no XML TISS: {str(e)}"
    except Exception as e:
        return False, f"Erro ao validar XML: {str(e)}"