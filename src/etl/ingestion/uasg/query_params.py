"""Monta filtros de status e nomes de cursor das consultas de UASG e órgão."""


def uasg_query_params(status_uasg: bool) -> dict[str, bool]:
    """Filtro obrigatório de consultarUasg.

    Exemplo:
        uasg_query_params(True) == {"statusUasg": True}
    """
    return {"statusUasg": status_uasg}


def uasg_orgao_query_params(status_orgao: bool) -> dict[str, bool]:
    """Filtro obrigatório de consultarOrgao.

    Exemplo:
        uasg_orgao_query_params(False) == {"statusOrgao": False}
    """
    return {"statusOrgao": status_orgao}


def uasg_job_name(status_uasg: bool) -> str:
    """Nome do cursor de retomada de uma fatia de status da UASG.

    Exemplo:
        uasg_job_name(True) == "uasg:true"
    """
    return f"uasg:{_status_label(status_uasg)}"


def uasg_orgao_job_name(status_orgao: bool) -> str:
    """Nome do cursor de retomada de uma fatia de status do órgão.

    Exemplo:
        uasg_orgao_job_name(False) == "uasg_orgao:false"
    """
    return f"uasg_orgao:{_status_label(status_orgao)}"


def _status_label(status: bool) -> str:
    """Converte o booleano de status na string 'true' ou 'false'."""
    return str(status).lower()
