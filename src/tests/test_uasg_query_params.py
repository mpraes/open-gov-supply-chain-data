from etl.ingestion.uasg.query_params import (
    uasg_job_name,
    uasg_orgao_job_name,
    uasg_orgao_query_params,
    uasg_query_params,
)


def test_uasg_query_params_requires_status() -> None:
    assert uasg_query_params(True) == {"statusUasg": True}
    assert uasg_query_params(False) == {"statusUasg": False}


def test_uasg_orgao_query_params_requires_status() -> None:
    assert uasg_orgao_query_params(True) == {"statusOrgao": True}
    assert uasg_orgao_query_params(False) == {"statusOrgao": False}


def test_uasg_job_name_includes_status() -> None:
    assert uasg_job_name(True) == "uasg:true"
    assert uasg_job_name(False) == "uasg:false"


def test_uasg_orgao_job_name_includes_status() -> None:
    assert uasg_orgao_job_name(True) == "uasg_orgao:true"
    assert uasg_orgao_job_name(False) == "uasg_orgao:false"
