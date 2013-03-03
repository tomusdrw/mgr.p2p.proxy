from cache.test import StoreEverytingStorage
from mock import patch
from twisted.web.http_headers import Headers
from unittest.case import TestCase
import cache.algo as cut

def test_BaseCacheLogicShouldForwardMethods():
    with patch('cache.CacheStorage') as mock:
        # Given
        instance = mock.return_value
        header = object()
        metadata = object()
        
        cl = cut.CacheLogic(instance)
        
        # When
        cl.get("someKey", header)
        cl.items()
        cl.remove("someKey2")
        cl.put("x", header, "abc", metadata)
        
        
        # Then
        instance.get.assert_called_once_with("someKey", headers=header)
        instance.items.assert_called_once_with()
        instance.remove.assert_called_once_with("someKey2")
        instance.put.assert_called_once_with("x", header, "abc", metadata)
        
class TestFifoLogic(TestCase):
    
    def test_FifoLogic(self):
        # Given
        mock = StoreEverytingStorage()
        
        cl = cut.Fifo(mock, 2)
        cl.put("key1", Headers(), "value1")
        cl.put("key2", Headers(), "value2")
        len(cl.items()).should.equal(2)
        
        # When
        cl.put("key3", Headers(), "value3")
        
        # Then
        items = cl.items()
        len(items).should.equal(2)
        items[0].key.should.equal("key2")
        items[1].key.should.equal("key3")
        
