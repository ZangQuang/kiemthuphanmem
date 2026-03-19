from eapp.dao import load_products
from test.test_base import test_app, sample_products, test_session


def test_all(sample_products):

    actual_products = load_products()
    assert len(actual_products) == len(sample_products)


def test_paging(test_app, sample_products):
    actual_products = load_products(page=1)
    assert len(actual_products) == test_app.config["PAGE_SIZE"]
    actual_products = load_products(page=2)
    assert len(actual_products) == test_app.config["PAGE_SIZE"]
    actual_products = load_products(page=3)
    assert len(actual_products) == 1

def  test_cate_id(sample_products):
    actual_products = load_products(cate_id=1)
    assert len(actual_products) == 3
    assert all(p.category_id == 1 for p in actual_products)

def test_kw(sample_products):
    actual_products = load_products(kw='Iphone')
    assert len(actual_products) == 3
    assert all('Iphone' in p.name for p in actual_products)

def test_pasing_id(sample_products):
    actual_products = load_products(page=1, cate_id=1)
    assert len(actual_products) == 2
    assert all(p.category_id == 1 for p in actual_products)

    actual_products = load_products(page=2, cate_id=1)
    assert len(actual_products) == 1
    assert actual_products[0].name == 'Iphone 16 plus'
    assert actual_products[0].category_id == 1

def test_pasing_kw(sample_products):
    actual_products = load_products(page=1, kw='Iphone')
    assert len(actual_products) == 2
    assert all('Iphone' in p.name for p in actual_products)

    actual_products = load_products(page=2, kw='Iphone')
    assert len(actual_products) == 1
    assert 'Iphone' in actual_products[0].name

def test_cate_id_kw(sample_products):
    actual_products = load_products(kw='Iphone', cate_id=1)
    assert len(actual_products) == 2
    assert all('Iphone' in p.name and p.category_id == 1 for p in actual_products)
