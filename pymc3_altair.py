import altair as alt
import pymc3 as pm
import pandas as pd
import numpy as np

def plot_fit_altair(m, t, df, x_range=(1, 134)):
    with m:
        posterior_predictor = pm.sample_posterior_predictive(t)

    df = pd.DataFrame(
        {
            "min_posterior_predictor": np.min(posterior_predictor["y"], axis=0) * 10000,
            "max_posterior_predictor": np.max(posterior_predictor["y"], axis=0) * 10000,
            "mean_posterior_predictor": np.mean(posterior_predictor["y"], axis=0)
            * 10000,
            "Total_scaled": df["Total_scaled"].to_numpy() * 10000,
            "Week_nr": df["Week_nr"],
        }
    )

    tooltip = [
        alt.Tooltip("Total_scaled:Q", title="Registered Decks", format=",.0f"),
        alt.Tooltip("max_posterior_predictor:Q", title="Model Max", format=",.0f"),
        alt.Tooltip("mean_posterior_predictor:Q", title="Model Mean", format=",.0f"),
        alt.Tooltip("min_posterior_predictor:Q", title="Model Min", format=",.0f"),
    ]

    x = alt.X(
        "Week_nr:Q",
        title="Week",
        scale=alt.Scale(domain=x_range, zero=False, nice=False),
    )

    real_registrations = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=x,
            y="Total_scaled",
            tooltip=tooltip,
        )
    )

    model_min_max = (
        alt.Chart(df)
        .mark_area(opacity=0.2, color="#333333")
        .encode(
            x=x,
            y="min_posterior_predictor:Q",
            y2="max_posterior_predictor:Q",
            tooltip=tooltip,
        )
    )

    model_mean = (
        alt.Chart(df)
        .mark_line(color="#333333", opacity=0.7)
        .encode(
            x=x,
            y="mean_posterior_predictor",
            tooltip=tooltip,
        )
    )

    chart = model_min_max + model_mean + real_registrations
    chart.layer[0].encoding.y.title = "Decks Registered"
    return chart

def plot_prior_predictor_altair(m, df, x_range=(1, 134)):
    with m:
        posterior_predictor = pm.sample_prior_predictive()

    df = pd.DataFrame(
        {
            "min_posterior_predictor": np.min(posterior_predictor["y"], axis=0) * 10000,
            "max_posterior_predictor": np.max(posterior_predictor["y"], axis=0) * 10000,
            "mean_posterior_predictor": np.mean(posterior_predictor["y"], axis=0)
            * 10000,
            "Total_scaled": df["Total_scaled"].to_numpy() * 10000,
            "Week_nr": df["Week_nr"],
        }
    )

    tooltip = [
        alt.Tooltip("Total_scaled:Q", title="Registered Decks", format=",.0f"),
        alt.Tooltip("max_posterior_predictor:Q", title="Model Max", format=",.0f"),
        alt.Tooltip("mean_posterior_predictor:Q", title="Model Mean", format=",.0f"),
        alt.Tooltip("min_posterior_predictor:Q", title="Model Min", format=",.0f"),
    ]

    x = alt.X(
        "Week_nr:Q",
        title="Week",
        scale=alt.Scale(domain=x_range, zero=False, nice=False),
    )

    real_registrations = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=x,
            y="Total_scaled",
            tooltip=tooltip,
        )
    )

    model_min_max = (
        alt.Chart(df)
        .mark_area(opacity=0.2, color="#333333")
        .encode(
            x=x,
            y="min_posterior_predictor:Q",
            y2="max_posterior_predictor:Q",
            tooltip=tooltip,
        )
    )

    model_mean = (
        alt.Chart(df)
        .mark_line(color="#333333", opacity=0.7)
        .encode(
            x=x,
            y="mean_posterior_predictor",
            tooltip=tooltip,
        )
    )

    chart = model_min_max + model_mean + real_registrations
    chart.layer[0].encoding.y.title = "Decks Registered"
    return chart