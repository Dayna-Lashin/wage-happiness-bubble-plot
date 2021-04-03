import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Standardizes currency to USD values so that we can better compare results
def format_currency(dataset):
  url = "https://api.exchangerate-api.com/v4/latest/USD"

  # Requests data from API
  response = requests.get(url)
  data = response.json()
  
  def convert_currency(row):
    rate = data["rates"][row["Unit Code"]]
    return row["Value"] / rate

  for index, row in dataset.iterrows():
    dataset.at[index,"Unit Code"] = "USD"
    dataset.at[index,"Value"] = convert_currency(row)
  return dataset


# ADD CODE: Pandas dataframes

# reads csv files
wage = pd.read_csv("wage.csv", delimiter = ",")
happiness = pd.read_csv("happiness.csv", delimiter = ",")

# converts currency to USD
wage_usd = format_currency(wage)

#merges csv files together
wage_and_happiness = wage.merge(happiness)

#print(wage_and_happiness)

# group data
wage_and_happiness_by_country = wage_and_happiness.groupby("Country")

# mean for Value series
wage_average_per_country = wage_and_happiness_by_country["Value"].mean()

# mean for Happiness Score series
happiness_average_per_country = wage_and_happiness_by_country["Happiness score"].mean()

#print(f"Countries with highest average wages:\n {wage_average_per_country.nlargest(10)}\n")
#print(f"Countries with highest average happiness:\n {happiness_average_per_country.nlargest(10)}\n")

#print(f"Countries with lowest average wages:\n {wage_average_per_country.nsmallest(10)}\n")
#print(f"Countries with lowest average happiness:\n {happiness_average_per_country.nsmallest(10)}")

# Bubble Plot
fig = sns.scatterplot(x="Value", y="Happiness score", hue="Happiness score", size="Happiness score", sizes=(20, 180), data=wage_and_happiness)

plt.title("Annual Salary and Happiness")
plt.xlabel("Annual Salary of Full-Time Workers (USD)")
plt.ylabel("Happiness Scores of Citizens")

fig.set_facecolor("#E5E5E5")
plt.legend(loc='lower right', title="Happiness Score")

plt.savefig("salary_and_happiness.png")

