"""Generate a 3D asset from text and poll its Muapi result."""

import os
import time

import requests


BASE_URL = os.getenv("MUAPI_BASE_URL", "https://api.muapi.ai/api/v1")
API_KEY = os.environ["MUAPI_API_KEY"]


def main() -> None:
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    response = requests.post(
        f"{BASE_URL}/tripo3d-h31-text-to-3d",
        headers=headers,
        json={"prompt": "a low-poly red panda astronaut, game-ready asset"},
        timeout=60,
    )
    response.raise_for_status()
    submission = response.json()
    request_id = (
        submission.get("id")
        or submission.get("request_id")
        or submission.get("prediction_id")
    )
    if not request_id:
        raise RuntimeError(f"No request id in response: {submission}")

    for _ in range(180):
        result = requests.get(
            f"{BASE_URL}/predictions/{request_id}/result",
            headers={"x-api-key": API_KEY},
            timeout=60,
        )
        result.raise_for_status()
        body = result.json()
        status = str(body.get("status", "")).lower()
        if status in {"succeeded", "completed", "success"}:
            print(body)
            return
        if status in {"failed", "error", "cancelled"}:
            raise RuntimeError(body)
        time.sleep(2)

    raise TimeoutError(f"Timed out while waiting for {request_id}")


if __name__ == "__main__":
    main()
