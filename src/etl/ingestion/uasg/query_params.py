def uasg_query_params(status_uasg: bool) -> dict[str, bool]:
    """Required filter for consultarUasg.

    Example:
        uasg_query_params(True) == {"statusUasg": True}
    """
    return {"statusUasg": status_uasg}


def uasg_orgao_query_params(status_orgao: bool) -> dict[str, bool]:
    """Required filter for consultarOrgao.

    Example:
        uasg_orgao_query_params(False) == {"statusOrgao": False}
    """
    return {"statusOrgao": status_orgao}


def uasg_job_name(status_uasg: bool) -> str:
    """Resume-cursor name for one UASG status slice.

    Example:
        uasg_job_name(True) == "uasg:true"
    """
    return f"uasg:{_status_label(status_uasg)}"


def uasg_orgao_job_name(status_orgao: bool) -> str:
    """Resume-cursor name for one órgão status slice.

    Example:
        uasg_orgao_job_name(False) == "uasg_orgao:false"
    """
    return f"uasg_orgao:{_status_label(status_orgao)}"


def _status_label(status: bool) -> str:
    return str(status).lower()
