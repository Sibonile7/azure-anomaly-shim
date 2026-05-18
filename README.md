# azure-anomaly-shim

A drop in replacement for the retired Azure Anomaly Detector service, powered by PyOD.

Microsoft is retiring Azure AI Anomaly Detector on 1 October 2026. Any application built on that service will stop working. This small Python package lets you keep your existing code almost unchanged. Swap one import line and your anomaly detection runs locally using the open source PyOD library instead of the Azure service.

## Why this exists

Many production systems built on Azure Anomaly Detector are facing a forced migration. Microsoft recommends moving to Microsoft Fabric, which is a heavier solution that requires more changes. This package offers a lighter alternative for users who only need the core anomaly detection feature.

## Installation

```bash
pip install azure-anomaly-shim
```

## Quick start

If your code currently looks like this:

```python
from azure.ai.anomalydetector import AnomalyDetectorClient

client = AnomalyDetectorClient(endpoint, credential)
result = client.detect_univariate_entire_series(request)
```

You can switch to this:

```python
from azure_anomaly_shim.detector import detect_univariate_entire_series

result = detect_univariate_entire_series(series=[10, 11, 9, 50, 10, 11], sensitivity=95)
```

No API keys. No network calls. No subscription. Runs locally.

## What is supported

Two functions are currently available:

`detect_univariate_entire_series(series, sensitivity=95)`
Analyzes an entire time series and flags every point that looks anomalous.

`detect_univariate_last_point(series, sensitivity=95)`
Analyzes a time series and returns whether only the most recent point is anomalous. Useful for live monitoring.

Both return results in the same shape the old Azure SDK returned.

## Example output

```python
from azure_anomaly_shim.detector import detect_univariate_entire_series

data = [10, 11, 9, 10, 12, 9, 11, 10, 50, 10, 11]
result = detect_univariate_entire_series(data, sensitivity=85)

for i, is_anomaly in enumerate(result["is_anomaly"]):
    if is_anomaly:
        print(f"Position {i}: value = {data[i]}, severity = {result['severity'][i]:.2f}")
```

Output: Position 8: value = 50, severity = 1.00
## What is not supported yet

Multivariate detection. The old SDK had `train_multivariate_model` and `detect_multivariate_batch_anomaly` for analyzing multiple correlated signals at once. These are planned for a future release.

Streaming windowed detection. Currently the package re analyzes the full series each call. For very long histories this is slower than the original Azure service. A windowed approach is on the roadmap.

## How it works under the hood

The package uses Isolation Forest from the PyOD library. Isolation Forest works by randomly partitioning the data and counting how quickly each point can be isolated. Outliers get isolated faster than normal points, which makes them easy to spot.

The sensitivity parameter controls how strict the detection is. Higher values flag fewer anomalies, lower values flag more. The default is 95, which flags the top 5 percent of unusual points.

## License

MIT License. Free to use in commercial and personal projects.

## Author

Built by Sibonile Mthunzi as part of learning cloud migration tooling. Contributions and bug reports welcome.