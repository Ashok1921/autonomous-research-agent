import time


def invoke_with_retry(
    structured_model,
    prompt: str,
    max_retries: int = 3,
    retry_delay: int = 5,
):
    """
    Invoke a structured Gemini model with limited retry handling.

    429 quota errors are not retried because retrying will not
    restore an exhausted quota.

    503 / temporary failures are retried a few times.
    """

    for attempt in range(max_retries + 1):

        try:
            return structured_model.invoke(prompt)

        except Exception as exc:
            error_text = str(exc).lower()

            # Gemini quota / rate-limit exhaustion
            if "429" in error_text or "resource_exhausted" in error_text:
                print("\n[LLM ERROR] Gemini quota/rate limit reached.")
                print("The workflow will stop this LLM call instead of repeatedly retrying.")
                raise

            # Temporary Gemini overload
            if "503" in error_text or "unavailable" in error_text:
                if attempt >= max_retries:
                    print("\n[LLM ERROR] Gemini remained unavailable after retries.")
                    raise

                wait_time = retry_delay * (attempt + 1)

                print(
                    f"\n[LLM RETRY] Gemini temporarily unavailable. "
                    f"Retry {attempt + 1}/{max_retries} in {wait_time}s..."
                )

                time.sleep(wait_time)
                continue

            # Other temporary-looking connection failures
            if any(
                word in error_text
                for word in [
                    "timeout",
                    "timed out",
                    "connection",
                    "temporarily",
                ]
            ):
                if attempt >= max_retries:
                    raise

                wait_time = retry_delay * (attempt + 1)

                print(
                    f"\n[LLM RETRY] Temporary error. "
                    f"Retry {attempt + 1}/{max_retries} in {wait_time}s..."
                )

                time.sleep(wait_time)
                continue

            # Unknown / programming / validation error:
            # don't hide it with retries.
            raise

    raise RuntimeError("LLM invocation failed unexpectedly.")