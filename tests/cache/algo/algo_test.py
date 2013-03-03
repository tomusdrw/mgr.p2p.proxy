from cache.test import StoreEverytingStorage
from mock import patch, MagicMock
import cache.algo as cut

def test_BaseCacheLogicShouldForwardMethods():
    with patch('cache.CacheStorage') as mock:
        # Given
        instance = mock.return_value
        header = object()
        
        cl = cut.CacheLogic(instance)
        
        # When
        cl.get("someKey", header)
        cl.items()
        cl.remove("someKey2")
        cl.store("x", header, "abc")
        
        
        # Then
        instance.get.assert_called_once_with("someKey", headers=header)
        instance.items.assert_called_once_with()
        instance.remove.assert_called_once_with("someKey2")
        instance.store.assert_called_once_with("x", header, "abc")
        

def test_FifoLogicForwarding():
    # Given
    mock = StoreEverytingStorage()
    mock.store = MagicMock()
    
    cl = cut.Fifo(mock, 2)
    cl.store("key1", "header", "value")
    mock.store.assert_called_with("key1", "header", "value")
    cl.store("key2", "header", "value")
    mock.store.assert_called_with("key2", "header", "value")
    
    # When
    
    #
