from __future__ import annotations

import pandas as pd


def variable_dictionary() -> pd.DataFrame:
    """Return human-readable metadata for the Air Quality dataset columns."""
    rows = [
        {
            "variable": "timestamp",
            "group": "Time",
            "meaning": "Parsed date and hour of the measurement.",
            "unit": "-",
            "interpretation": "Used to analyze temporal patterns, seasonality, missingness over time, and chronological model evaluation.",
        },
        {
            "variable": "CO(GT)",
            "group": "Reference gas",
            "meaning": "Carbon monoxide concentration from the certified reference analyzer.",
            "unit": "mg/m^3",
            "interpretation": "Higher values generally indicate stronger combustion or traffic influence.",
        },
        {
            "variable": "NMHC(GT)",
            "group": "Reference gas",
            "meaning": "Non-methane hydrocarbons from the certified reference analyzer.",
            "unit": "microg/m^3",
            "interpretation": "Often very incomplete in this dataset, so it is not a robust default target.",
        },
        {
            "variable": "C6H6(GT)",
            "group": "Reference gas",
            "meaning": "Benzene concentration from the certified reference analyzer.",
            "unit": "microg/m^3",
            "interpretation": "A key pollutant for this dataset and a strong candidate target for sensor calibration.",
        },
        {
            "variable": "NOx(GT)",
            "group": "Reference gas",
            "meaning": "Total nitrogen oxides from the certified reference analyzer.",
            "unit": "ppb",
            "interpretation": "Higher values often indicate combustion-related pollution. NOx is not the same as NO2.",
        },
        {
            "variable": "NO2(GT)",
            "group": "Reference gas",
            "meaning": "Nitrogen dioxide concentration from the certified reference analyzer.",
            "unit": "microg/m^3",
            "interpretation": "Important traffic-related pollutant. Higher values generally indicate more polluted episodes.",
        },
        {
            "variable": "PT08.S1(CO)",
            "group": "Sensor response",
            "meaning": "Metal oxide sensor response nominally associated with CO.",
            "unit": "sensor response",
            "interpretation": "This is not a certified CO concentration. It is a raw sensor signal used as a model input.",
        },
        {
            "variable": "PT08.S2(NMHC)",
            "group": "Sensor response",
            "meaning": "Metal oxide sensor response nominally associated with non-methane hydrocarbons.",
            "unit": "sensor response",
            "interpretation": "Useful as a predictor, but affected by cross-sensitivity and environmental conditions.",
        },
        {
            "variable": "PT08.S3(NOx)",
            "group": "Sensor response",
            "meaning": "Metal oxide sensor response nominally associated with nitrogen oxides.",
            "unit": "sensor response",
            "interpretation": "A sensor signal, not a direct NOx measurement.",
        },
        {
            "variable": "PT08.S4(NO2)",
            "group": "Sensor response",
            "meaning": "Metal oxide sensor response nominally associated with nitrogen dioxide.",
            "unit": "sensor response",
            "interpretation": "A model input that may help estimate reference pollutants but can drift over time.",
        },
        {
            "variable": "PT08.S5(O3)",
            "group": "Sensor response",
            "meaning": "Metal oxide sensor response nominally associated with ozone.",
            "unit": "sensor response",
            "interpretation": "The dataset does not include an O3(GT) target column, so this remains an input signal.",
        },
        {
            "variable": "T",
            "group": "Meteorology",
            "meaning": "Temperature.",
            "unit": "deg C",
            "interpretation": "Important because sensor responses can be temperature-sensitive.",
        },
        {
            "variable": "RH",
            "group": "Meteorology",
            "meaning": "Relative humidity.",
            "unit": "%",
            "interpretation": "Humidity can affect metal oxide sensor responses and pollutant behaviour.",
        },
        {
            "variable": "AH",
            "group": "Meteorology",
            "meaning": "Absolute humidity.",
            "unit": "-",
            "interpretation": "Useful environmental covariate for calibration models.",
        },
    ]
    return pd.DataFrame(rows)
