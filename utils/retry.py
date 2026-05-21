import time

def retry_with_backoff(func, retries=3):

    for attempt in range(retries):

        try:
            return func()

        except Exception as e:

            if attempt == retries - 1:
                raise e

            sleep_time = 2 ** attempt
            time.sleep(sleep_time)