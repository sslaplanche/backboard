import os
import json
from datetime import datetime, timedelta
from functools import wraps

CACHE_DIRECTORY = 'cache'
EXPIRY_MINUTES = 1

def cacheify(cache_file_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if cache file exists
            if os.path.exists(cache_file_path):
                with open(cache_file_path, 'r') as cache_file:
                    cache_object = json.loads(cache_file.read())
                    cache_timestamp = datetime.strptime(cache_object['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if datetime.now() - cache_timestamp < timedelta(minutes=EXPIRY_MINUTES):
                        print('Cache hit!')
                        return cache_object['data']

            print('Fetching fresh data')

            # Fetch data using the wrapped function
            data = func(*args, **kwargs)

            # Create cache object
            cache_object = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': data
            }

            # Write cache object to file
            with open(cache_file_path, 'w') as cache_file:
                cache_file.write(json.dumps(cache_object, indent=4))

            return data

        return wrapper

    return decorator
import os
import json
from datetime import datetime, timedelta
from functools import wraps

CACHE_DIRECTORY = 'cache'
EXPIRY_MINUTES = 1

def cacheify(cache_filename):
    cache_file_path = os.path.join(CACHE_DIRECTORY, cache_filename)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if cache file exists
            if os.path.exists(cache_file_path):
                with open(cache_file_path, 'r') as cache_file:
                    cache_object = json.loads(cache_file.read())
                    cache_timestamp = datetime.strptime(cache_object['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if datetime.now() - cache_timestamp < timedelta(minutes=EXPIRY_MINUTES):
                        print('Cache hit!')
                        return cache_object['data']

            print('Fetching fresh data')

            # Fetch data using the wrapped function
            data = func(*args, **kwargs)

            # Create cache object
            cache_object = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': data
            }

            # Write cache object to file
            with open(cache_file_path, 'w') as cache_file:
                cache_file.write(json.dumps(cache_object, indent=4))

            return data

        return wrapper

    return decorator
