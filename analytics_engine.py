import pandas as pd


def normalize_categories(df):

    df["category"] = df["category"].astype(str).str.lower().str.strip()

    mapping = {
        "swiggy": "Food",
        "zomato": "Food",
        "restaurant": "Food",
        "food": "Food",

        "uber": "Transport",
        "ola": "Transport",
        "taxi": "Transport",

        "rent": "Housing",
        "electricity": "Bills",
        "wifi": "Bills",

        "shopping": "Shopping",
        "amazon": "Shopping"
    }

    df["category"] = df["category"].apply(lambda x: mapping.get(x, x.title()))

    return df



def generate_recommendations(df):

    recommendations = []

    category_spend = df.groupby("category")["amount"].sum()
    total = category_spend.sum()

    for cat, amt in category_spend.items():
        percent = (amt / total) * 100

        if percent > 40:
            recommendations.append(f"High spending in {cat}")

    return recommendations



def calculate_expenses(df):

    total_spend = df["amount"].sum()

    category_spend = df.groupby("category")["amount"].sum().to_dict()

    monthly_spend = (
        df.groupby(df["date_time"].dt.to_period("M"))["amount"]
        .sum()
        .to_dict()
    )

    monthly_spend = {
        str(k): float(v) for k, v in monthly_spend.items()
    }

    daily_avg = (
        df.groupby(df["date_time"].dt.date)["amount"]
        .sum()
        .mean()
    )

    return {
        "total_spend": float(total_spend),
        "category_spend": category_spend,
        "monthly_spend": monthly_spend,
        "daily_average": float(daily_avg)
    }


# =========================
# MAIN PIPELINE
# =========================
def run_analysis(df):

    df = normalize_categories(df)

    expenses = calculate_expenses(df)

    recommendations = generate_recommendations(df)

    return {
        "expenses": expenses,
        "recommendations": recommendations
    }