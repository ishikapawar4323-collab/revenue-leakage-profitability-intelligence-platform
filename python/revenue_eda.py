import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("Mysql@1234")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost/revenue_leakages_db"
)

df = pd.read_sql(
    "SELECT * FROM revenue_transactions",
    engine
)

print(df.head())
print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.info())
print("========EXECUTIVE KPI SNAPSHOT==============")
print("\n===== EXECUTIVE KPI SNAPSHOT =====")
print("Total Revenue:",round(df["Revenue"].sum(),2))
print("Total Profit:",round (df["Profit"].sum(),2))
print("Average Revenue:",round (df["Revenue"].mean(),2))
print("Average Profit;",round (df["Profit"].mean(),2))
print("Total Orders:",len(df))
profit_margin = (df["Profit"].sum()/df["Revenue"])*100
print("Profit Margin %",round(profit_margin,2))
print("\nTop Regions by Revenue")

print(
    df.groupby("Region")["Revenue"]
      .sum()
      .sort_values(ascending=False))
print("\nTop Categories by Revenue")

print(
    df.groupby("Category")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)
print("\n===== RETURN ANALYSIS =====")

print("Returned Orders:",
      df["Returned"].sum())

print("Total Return Cost:",
      round(df["ReturnCost"].sum(),2))
print("\n===== DISCOUNT ANALYSIS =====")

print("Average Discount %:",
      round(df["DiscountPct"].mean(),2))

print("Maximum Discount %:",
      round(df["DiscountPct"].max(),2))
print("\n===== LOSS MAKING ORDERS =====")

loss_orders = df[df["Profit"] < 0]

print("Number of Loss Making Orders:",
      len(loss_orders))

print("Total Loss Amount:",
      round(loss_orders["Profit"].sum(),2))
print("\n===== RETURN LEAKAGE =====")

returned_orders = df[df["Returned"] == 1]

print("Returned Orders:",
      len(returned_orders))

print("Return Cost:",
      round(returned_orders["ReturnCost"].sum(),2))

print("Revenue Impact:",
      round(returned_orders["Revenue"].sum(),2))
print("\n===== HIGH DISCOUNT ANALYSIS =====")

high_discount = df[df["DiscountPct"] > 25]

print("Orders with >25% Discount:",
      len(high_discount))

print("Revenue from High Discount Orders:",
      round(high_discount["Revenue"].sum(),2))

print("Profit from High Discount Orders:",
      round(high_discount["Profit"].sum(),2))
print("\n===== PROFIT BY REGION =====")

print(
    df.groupby("Region")["Profit"]
      .sum()
      .sort_values(ascending=False)
)
print("\n===== PROFIT BY CATEGORY =====")

print(
    df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)
print("\n===== TOP 10 PROFITABLE CUSTOMERS =====")

top_customers = (
    df.groupby("CustomerID")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_customers)
print("\n===== BOTTOM 10 CUSTOMERS =====")

bottom_customers = (
    df.groupby("CustomerID")["Profit"]
      .sum()
      .sort_values()
      .head(10)
)

print(bottom_customers)
print("\n===== TOP 10 CUSTOMERS BY REVENUE =====")

top_revenue_customers = (
    df.groupby("CustomerID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_revenue_customers)
df["ProfitMarginPct"] = (
    df["Profit"] / df["Revenue"]
) * 100
df["DiscountBand"] = pd.cut(
    df["DiscountPct"],
    bins=[0,10,20,30,100],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)
df["RevenueBand"] = pd.qcut(
    df["Revenue"],
    q=4,
    labels=[
        "Low Revenue",
        "Medium Revenue",
        "High Revenue",
        "Very High Revenue"
    ]
)
df["LeakageFlag"] = (
    (df["Profit"] < 0)
    |
    (df["Returned"] == 1)
    |
    (df["DiscountPct"] > 25)
)
df["OrderDate"] = pd.to_datetime(
    df["OrderDate"],
    origin="1899-12-30",
    unit="D"
)

print(df[["OrderDate"]].head())
import numpy as np

df["LeakageScore"] = (
    0.4 * df["Returned"] * 100
    +
    0.3 * (df["DiscountPct"] / df["DiscountPct"].max()) * 100
    +
    0.2 * (df["FreightCost"] / df["FreightCost"].max()) * 100
    +
    0.1 * np.where(df["Profit"] < 0, 100, 0)
)
df["RiskLevel"] = np.where(
    df["LeakageScore"] > 70,
    "Critical",
    np.where(
        df["LeakageScore"] > 50,
        "High",
        np.where(
            df["LeakageScore"] > 30,
            "Medium",
            "Low"
        )
    )
)
import matplotlib.pyplot as plt

region_rev = (
    df.groupby("Region")["Revenue"]
      .sum()
)

region_rev.plot(kind="bar")

plt.title("Revenue by Region")
plt.ylabel("Revenue")

plt.show()
category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
)

category_profit.plot(kind="bar")

plt.title("Profit by Category")

plt.show()
customer_rev = (
    df.groupby("CustomerID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)
import plotly.express as px

fig = px.histogram(
    df,
    x="LeakageScore",
    title="Revenue Leakage Risk Distribution"
)

fig.show()
fig = px.pie(
    df,
    names="RiskLevel",
    title="Leakage Risk Classification"
)

fig.show()
fig = px.bar(
    df.groupby("Region")["Profit"]
      .sum()
      .reset_index(),
    x="Region",
    y="Profit",
    title="Profit by Region"
)

fig.show()
executive_summary = pd.DataFrame({

    "Metric":[
        "Total Revenue",
        "Total Profit",
        "Total Orders",
        "Returned Orders",
        "Loss Making Orders"
    ],

    "Value":[
        df["Revenue"].sum(),
        df["Profit"].sum(),
        len(df),
        df["Returned"].sum(),
        len(df[df["Profit"]<0])
    ]
})

print(executive_summary)
df.to_csv(
    "clean_transactions.csv",
    index=False
)

executive_summary.to_csv(
    "executive_summary.csv",
    index=False
)

print("Files exported successfully")

