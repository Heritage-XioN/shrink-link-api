import pytest

# test for shortening a url
def test_shorten_url(authorized_user):
    res = authorized_user.post("/url/", json={"original_url": "http://example.com"})
    assert res.status_code == 201


# test for getting limited number of urls
def test_get_limit_shortened_url(authorized_user, test_urls):
    res = authorized_user.get("/url/")
    assert res.status_code == 200
    assert len(res.json()) == 3


# test for getting all urls
def test_get_all_shortened_url(authorized_user, test_urls):
    res = authorized_user.get("/url/all")
    assert res.status_code == 200
    assert len(res.json()) == len(test_urls)


# test for updating a url
@pytest.mark.parametrize("id, update_url, updated_url, status_code",[
    (1, "http://example12.com", "http://example12.com", 200),
    (2, "http://example123.com", "http://example123.com", 200),
    (3, "http://example124.com", "http://example124.com", 200),
    (4, "http://example125.com", "http://example125.com", 200),
])
def test_update_url(authorized_user, test_urls, id, update_url, updated_url, status_code):
    res = authorized_user.put(f"/url/{id}", json={"original_url": update_url})
    assert res.status_code == status_code
    assert res.json().get("original_url") == updated_url

# test for updating a url under error prone situations
@pytest.mark.parametrize("id, update_url, detail, status_code",[
    (10, "http://example23.com", 'url with the id 10 does not exists', 404),
    (2, "http://example1.com", 'url already exists', 403)
])
def test_update_url_exception(authorized_user, test_urls, id, update_url, detail, status_code):
    res = authorized_user.put(f"/url/{id}", json={"original_url": update_url})
    assert res.status_code == status_code
    assert res.json().get("detail") == detail
    
# test for deleting a url 
@pytest.mark.parametrize("id, status_code",[
    (1, 204),
    (2, 204),
    (3, 204),
    (4, 204),
])
def test_delete_url(authorized_user, test_urls, id, status_code):
    res = authorized_user.delete(f"/url/{id}")
    assert res.status_code == status_code

# test for deleting a url under error prone situations
@pytest.mark.parametrize("id, status_code",[
    (10, 404),
    (20, 404),
    (30, 404),
    (40, 404),
])
def test_delete_url_exception(authorized_user, test_urls, id, status_code):
    res = authorized_user.delete(f"/url/{id}")
    assert res.status_code == status_code