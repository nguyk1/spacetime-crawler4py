import requests
import cbor
import time

from utils.response import Response

def download(url, config, logger=None) -> Response:
    host, port = config.cache_server
    resp = requests.get(
        f"http://{host}:{port}/",
        params=[("q", f"{url}"), ("u", f"{config.user_agent}")])
    try:
        if resp and resp.content:
            return Response(resp.headers, cbor.loads(resp.content))
    except (EOFError, ValueError) as e:
        pass
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({}, {
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})

def download2(url, config, logger=None) -> Response:
    resp = requests.get(url)
    try:
        if resp and resp.content:
            return Response(resp.headers, {
                "url": url,
                "status": resp.status_code,
                "error": resp.reason,
                "response": {"content": resp.content, "url": url}
            })
    except (EOFError, ValueError) as e:
        pass
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({}, {
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})
    
download = download2