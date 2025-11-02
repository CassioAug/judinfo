import json
from unittest.mock import patch, Mock

import pytest

from judinfo_cli import DataJudSimple, formatar_data


def make_mock_response(json_data, status_code=200):
    m = Mock()
    m.status_code = status_code
    m.json.return_value = json_data
    return m


@patch("judinfo_cli.requests.post")
def test_consultar_processo_returns_first_hit(mock_post):
    fake = {"hits": {"total": {"value": 1}, "hits": [{"_source": {"numeroProcesso": "0001", "tribunal": "tjmg"}}]}}
    mock_post.return_value = make_mock_response(fake, 200)

    client = DataJudSimple()
    res = client.consultar_processo("0001", "tjmg")
    assert isinstance(res, dict)
    assert res.get("numeroProcesso") == "0001"


@patch("judinfo_cli.requests.post")
def test_consultar_processo_no_hits_returns_none(mock_post):
    fake = {"hits": {"total": {"value": 0}, "hits": []}}
    mock_post.return_value = make_mock_response(fake, 200)

    client = DataJudSimple()
    res = client.consultar_processo("0002", "tjmg")
    assert res is None


@patch("judinfo_cli.requests.post")
def test_verificar_tribunal_success(mock_post):
    # status code 200 -> success True
    mock_post.return_value = make_mock_response({"hits": {}}, 200)
    client = DataJudSimple()
    result = client.verificar_tribunal("stj")
    assert result.get("success") is True


@patch("judinfo_cli.requests.post")
def test_verificar_tribunal_request_exception(mock_post):
    import requests

    mock_post.side_effect = requests.exceptions.RequestException("conn error")
    client = DataJudSimple()
    result = client.verificar_tribunal("stj")
    assert result.get("success") is False
    assert "error" in result


def test_formatar_data_valid_and_invalid():
    iso = "2021-06-01T12:30:00Z"
    formatted = formatar_data(iso)
    assert "01/06/2021" in formatted

    # invalid input returns original or 'N/A'
    assert formatar_data(None) == "N/A"
