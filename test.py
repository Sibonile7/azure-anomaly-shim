"""
Test both functions in the wrapper.
"""

from azure_anomaly_shim.detector import (
    detect_univariate_entire_series,
    detect_univariate_last_point,
)

# Test data: 21 numbers with two clear anomalies (50 and 80).
data = [10, 11, 9, 10, 12, 9, 11, 10, 11, 9,
        50,
        10, 11, 9, 10, 11, 9,
        80,
        10, 11, 9]

print("=" * 60)
print("Test 1: detect_univariate_entire_series")
print("=" * 60)

result = detect_univariate_entire_series(data, sensitivity=85)
print(f"Original data: {data}")
print()
print("Anomalies flagged at these positions:")
for i, is_anomaly in enumerate(result["is_anomaly"]):
    if is_anomaly:
        print(f"  Position {i}: value = {data[i]}, severity = {result['severity'][i]:.2f}")

print()
print("=" * 60)
print("Test 2: detect_univariate_last_point")
print("=" * 60)

# Case A: latest point is normal.
normal_series = [10, 11, 9, 10, 12, 9, 11, 10, 11, 9]
result = detect_univariate_last_point(normal_series, sensitivity=85)
print(f"Series: {normal_series}")
print(f"Last point: {normal_series[-1]}")
print(f"Is anomaly: {result['is_anomaly']}, severity: {result['severity']:.2f}")

print()

# Case B: latest point is weird.
weird_series = [10, 11, 9, 10, 12, 9, 11, 10, 11, 80]
result = detect_univariate_last_point(weird_series, sensitivity=85)
print(f"Series: {weird_series}")
print(f"Last point: {weird_series[-1]}")
print(f"Is anomaly: {result['is_anomaly']}, severity: {result['severity']:.2f}")