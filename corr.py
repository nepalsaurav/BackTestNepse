import pandas as pd
from scipy import stats

df = pd.read_excel("result.xlsx")

correlation_coefficient = df['Return Percent'].corr(df['Beta'])

# Display the correlation coefficient
print("Correlation Coefficient:", correlation_coefficient)

# Perform the Pearson correlation test
corr_coeff, p_value = stats.pearsonr(
    df['Return Percent'], df['Beta'])

# Display the correlation coefficient and p-value
print("Correlation Coefficient:", corr_coeff)
print("P-value:", p_value)
