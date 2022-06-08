# test_ui.py
from dash import html

from EntryHomepage import sidebar, content, app, render_page_content, page_router


def test_sidebar():
    """
    test if sidebar layout is correctly set
    """
    assert type(sidebar) == html.Div


def test_content():
    """
    test if content layout is correctly set
    """
    assert type(content) == html.Div


def test_app_layout():
    """
    test if layout has been correctly bind to app
    """
    assert type(app.layout) == html.Div
    assert len(html.Div(app.layout).children) > 0


def test_render_page_content():
    """
    test if renderer successfully render the page
    """
    assert type(render_page_content("/")) == html.Div
    assert type(render_page_content("/name-cloud")) == html.Div
    assert type(render_page_content("/name-trend")) == html.Div
    assert type(render_page_content("/heat-map")) == html.Div
    assert type(render_page_content("/gender-classifier")) == html.Div


def test_page_router_existed():
    """
    test router successfully return code (existed page)
    """
    _, code = page_router("/")
    assert code == 200
    _, code = page_router("/name-cloud")
    assert code == 200
    _, code = page_router("/name-trend")
    assert code == 200
    _, code = page_router("/heat-map")
    assert code == 200
    _, code = page_router("/gender-classifier")
    assert code == 200


def test_page_router_non_existed():
    """
    test router successfully return code (non-existed page)
    """
    _, code = page_router("/error")
    assert code == 404

