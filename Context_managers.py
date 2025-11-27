import copy

print('first example')
print('-' * 150)
class TransactionalSaver:
    def __init__(self, object):
        self.object = object
        self.backup = copy.deepcopy(object)
    def __enter__(self):
        return self.object
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.object.clear() if hasattr(self.object, 'clear') else None
            if hasattr(self.object, 'update'):
                self.object.update(self.backup)
            else:
                for attr in dir(self.backup):
                    if not attr.startswith('_'):
                        try:
                            setattr(self.object, attr, getattr(self.backup, attr))
                        except:
                            pass
            print(f'object has returned: {exc_type}: {exc_val}')

data = {'name': 'islam', 'age': '20'}
print(f' before transaction: {data}')
try:
    with TransactionalSaver(data) as transaction_data:
        transaction_data['age'] = 18
        transaction_data['city'] = 'Kazan'
        print(f' during transaction: {transaction_data}')
except Exception as e:
    pass
print(f' after transaction: {data}')
print('-' * 150)

# import logging
# print('second example')
# print('-' * 150)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# class ErrorSuppressor:
#     def __init__(self, *error_to_suppress, log_message=' Attention caused mistake'):
#         self.error_to_suppress = error_to_suppress or (Exception,)
#         self.log_message = log_message
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_type and  any(issubclass(exc_type, error) for error in self.error_to_suppress):
#             logging.warning(f'{self.log_message}: {exc_type}: {exc_val}')
#             return True
#         return False
#
# with ErrorSuppressor(ValueError, ZeroDivisionError, log_message=' Dont calculated') :
#     result = 10/0
#
# with ErrorSuppressor(ValueError):
#     raise ValueError('This mistake dont caused')
print('third example')
print('-' * 150)
import pickle
import os
from functools import wraps

class CacheManager:
    def __init__(self, cache_file ='cache.pkl'):
        self.cache_file = cache_file
        self.cache = {}
        self.new_entries = {}

    def __enter__(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
            except (pickle.PickleError, EOFError):
                self.cache = {}
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.cache.update(self.new_entries)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
            print(f'cache saved to {self.cache_file}')
        return False
    def get(self, key):
        return self.cache.get(key)
    def set(self, key, value):
        self.cache[key] = value
        return value
    def cached(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                print(f'Use cache result for {func.__name__}')
                return self.cache[key]
            result = func(*args, **kwargs)
            self.new_entries[key] = result
            return result
        return wrapper

def expensive_calculation(x, y):
    print(f'calculating {x} + {y}...')
    return x + y

with CacheManager('my_cache.pkl') as cache:
    result1 = cache.cached(expensive_calculation)(5, 3)
    result2 = cache.cached(expensive_calculation)(10, 20)
    print(f'results: {result1}, {result2}')

with CacheManager('my_cache.pkl') as cache:
    result1 = cache.cached(expensive_calculation)(5, 3)
    result3 = cache.cached(expensive_calculation)(100, 200)
    print(f'results: {result1}, {result3}')
print('-' * 150)
print('fourth example')
class MockManager:
    def __init__(self, obj, **mock_attrs):
        self.obj = obj
        self.mock_attrs = mock_attrs
        self.original_attrs = {}
    def __enter__(self):
        for attr, value in self.mock_attrs.items():
            if hasattr(self.obj, attr) and not attr.startswith('_'):
                self.original_attrs[attr] = getattr(self.obj, attr)
            setattr(self.obj, attr, value)
        return self.obj
    def __exit__(self, exc_type, exc_val, exc_tb):
        for attr in self.mock_attrs:
            if attr in self.original_attrs:
                setattr(self.obj, attr, self.original_attrs[attr])
            elif hasattr(self.obj, attr):
                delattr(self.obj, attr)
        return False

class TestClass:
    def __init__(self):
        self.name = 'Original Name'
        self.value = 52
        self._private = 'private'
    def get_info(self):
        return f'{self.name}, {self.value}'

test_obj = TestClass()
with MockManager(test_obj, name = 'Mocked Name', value = 100, new_attr = 'new'):
    print('During Mocking:', test_obj.get_info())
    print('New attr:', test_obj.new_attr)

print('After mock:', test_obj.get_info())
print('have new_attr?', hasattr(test_obj, 'new_attr'))
