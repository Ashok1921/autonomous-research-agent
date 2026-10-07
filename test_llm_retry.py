from app.utils.llm_retry import invoke_with_retry


class FakeModel:
    def __init__(self):
        self.calls = 0

    def invoke(self, prompt):
        self.calls += 1

        if self.calls < 3:
            raise Exception("503 Service Unavailable")

        return "SUCCESS"


class FakeQuotaModel:
    def __init__(self):
        self.calls = 0

    def invoke(self, prompt):
        self.calls += 1
        raise Exception("429 RESOURCE_EXHAUSTED")


print("\n===== TEST 1: 503 RETRY =====")

model = FakeModel()

result = invoke_with_retry(
    model,
    "test prompt",
    max_retries=3,
    retry_delay=1,
)

print("Result:", result)
print("Total calls:", model.calls)


print("\n===== TEST 2: 429 NO RETRY =====")

quota_model = FakeQuotaModel()

try:
    invoke_with_retry(
        quota_model,
        "test prompt",
        max_retries=3,
        retry_delay=1,
    )
except Exception as exc:
    print("Expected error:", exc)
    print("Total calls:", quota_model.calls)


print("\n===== RETRY TEST COMPLETED =====")