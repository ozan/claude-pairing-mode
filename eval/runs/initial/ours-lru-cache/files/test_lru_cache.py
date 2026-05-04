from lru_cache import LRUCache


def test_miss_returns_minus_one():
    c = LRUCache(2)
    assert c.get(1) == -1


def test_put_then_get():
    c = LRUCache(2)
    c.put(1, 10)
    assert c.get(1) == 10


def test_get_promotes_to_mru():
    c = LRUCache(2)
    c.put(1, 10)
    c.put(2, 20)
    c.get(1)        # key 1 is now MRU; key 2 is LRU
    c.put(3, 30)    # evicts key 2 (LRU), not key 1
    assert c.get(1) == 10
    assert c.get(2) == -1
    assert c.get(3) == 30


def test_eviction_on_overflow():
    c = LRUCache(2)
    c.put(1, 10)
    c.put(2, 20)
    c.put(3, 30)    # evicts key 1 (LRU)
    assert c.get(1) == -1
    assert c.get(2) == 20
    assert c.get(3) == 30


def test_update_existing_key_no_spurious_eviction():
    c = LRUCache(2)
    c.put(1, 10)
    c.put(2, 20)
    c.put(1, 99)    # update, cache is still size 2 — nothing should be evicted
    assert c.get(1) == 99
    assert c.get(2) == 20


if __name__ == "__main__":
    test_miss_returns_minus_one()
    test_put_then_get()
    test_get_promotes_to_mru()
    test_eviction_on_overflow()
    test_update_existing_key_no_spurious_eviction()
    print("All tests passed.")
