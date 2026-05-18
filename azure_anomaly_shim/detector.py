"""
A drop in replacement for the retired Azure Anomaly Detector service.
Provides the same function names and output shape, powered by PyOD.
"""

from pyod.models.iforest import IForest
import numpy as np


def detect_univariate_entire_series(series, sensitivity=95):
    """
    Detect anomalies in a single time series.

    Mimics the old Azure SDK function of the same name. Returns results
    in the same shape Azure used to return.

    Arguments:
        series: a list of numbers (the time series values).
        sensitivity: how strict to be when flagging anomalies, from 0 to 100.
                     Higher means fewer anomalies flagged.

    Returns:
        A dictionary with the same keys the old Azure service returned:
        - is_anomaly: list of True or False for each point.
        - expected_values: the model's guess of the normal value.
        - upper_margins: how far above normal a point can be without alarm.
        - lower_margins: how far below normal a point can be without alarm.
        - severity: how strongly each point is flagged, from 0 to 1.
    """

    # Convert the input list into the shape PyOD expects.
    data = np.array(series).reshape(-1, 1)

    # Set up the Isolation Forest model.
    # The contamination value tells the model what fraction of points to expect as anomalies.
    contamination = (100 - sensitivity) / 100
    model = IForest(contamination=contamination, random_state=42)

    # Train the model on the data and get predictions.
    model.fit(data)
    labels = model.labels_  # 1 for anomaly, 0 for normal.
    scores = model.decision_scores_  # higher score means more anomalous.

    # Build the output in the format Azure used to return.
    mean = float(np.mean(series))
    std = float(np.std(series))

    result = {
        "is_anomaly": [bool(label) for label in labels],
        "expected_values": [mean] * len(series),
        "upper_margins": [2 * std] * len(series),
        "lower_margins": [2 * std] * len(series),
        "severity": [float(s / max(scores)) if max(scores) > 0 else 0.0 for s in scores],
    }

    return result
"""
A drop in replacement for the retired Azure Anomaly Detector service.
Provides the same function names and output shape, powered by PyOD.
"""

from pyod.models.iforest import IForest
import numpy as np


def detect_univariate_entire_series(series, sensitivity=95):
    """
    Detect anomalies across an entire time series.

    Mimics the old Azure SDK function of the same name.

    Arguments:
        series: a list of numbers (the time series values).
        sensitivity: how strict to be when flagging anomalies, from 0 to 100.
                     Higher means fewer anomalies flagged.

    Returns:
        A dictionary with keys is_anomaly, expected_values, upper_margins,
        lower_margins, and severity.
    """

    data = np.array(series).reshape(-1, 1)
    contamination = (100 - sensitivity) / 100
    model = IForest(contamination=contamination, random_state=42)
    model.fit(data)
    labels = model.labels_
    scores = model.decision_scores_

    mean = float(np.mean(series))
    std = float(np.std(series))

    result = {
        "is_anomaly": [bool(label) for label in labels],
        "expected_values": [mean] * len(series),
        "upper_margins": [2 * std] * len(series),
        "lower_margins": [2 * std] * len(series),
        "severity": [float(s / max(scores)) if max(scores) > 0 else 0.0 for s in scores],
    }

    return result


def detect_univariate_last_point(series, sensitivity=95):
    """
    Detect whether the most recent point in the time series is an anomaly.

    Mimics the old Azure SDK function of the same name. Use this for live
    monitoring where you only care about the latest data point.

    Arguments:
        series: a list of numbers ending with the most recent value.
        sensitivity: how strict to be when flagging anomalies, from 0 to 100.

    Returns:
        A dictionary with these keys:
        - is_anomaly: True or False for the latest point.
        - expected_value: the model's guess of the normal value.
        - upper_margin: how far above normal is acceptable.
        - lower_margin: how far below normal is acceptable.
        - severity: how strongly the latest point is flagged, from 0 to 1.
    """

    # Run the same detection on the whole series.
    full_result = detect_univariate_entire_series(series, sensitivity)

    # Return only the result for the last point.
    last_index = len(series) - 1
    result = {
        "is_anomaly": full_result["is_anomaly"][last_index],
        "expected_value": full_result["expected_values"][last_index],
        "upper_margin": full_result["upper_margins"][last_index],
        "lower_margin": full_result["lower_margins"][last_index],
        "severity": full_result["severity"][last_index],
    }

    return result