from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


network_retry = retry(
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)