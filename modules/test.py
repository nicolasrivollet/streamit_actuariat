import smithwilson as sw

# Input - Switzerland EIOPA spot rates with LLP of 25 years
# Source: https://eiopa.europa.eu/Publications/Standards/EIOPA_RFR_20190531.zip
#         EIOPA_RFR_20190531_Term_Structures.xlsx; Tab: RFR_spot_no_VA
rates = [-0.00803, -0.00814, -0.00778, -0.00725, -0.00652,
         -0.00565, -0.0048, -0.00391, -0.00313, -0.00214,
         -0.0014, -0.00067, -0.00008, 0.00051, 0.00108,
         0.00157, 0.00197, 0.00228, 0.0025, 0.00264,
         0.00271, 0.00274, 0.0028, 0.00291, 0.00309]
terms = [float(y + 1) for y in range(len(rates))] # [1.0, 2.0, ..., 25.0]
ufr = 0.029
alpha = 0.128562
# Extrapolate to 150 years
terms_target = [float(y + 1) for y in range(150)] # [1.0, 2.0, ..., 150.0]
# Interpolate to quarterly granularity
terms_target = [float(y + 1) / 4 for y in range(25*4)] # [0.25, 0.5, ..., 25.0]
# Get rates for a well-specified set of maturities only
terms_target = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
# Calculate fitted rates based on actual observations and two parametes alpha & UFR
fitted_rates = sw.fit_smithwilson_rates(rates_obs=rates, t_obs=terms,
                                        t_target=terms_target, ufr=ufr,
                                        alpha=alpha)  # Optional
# Ensure pandas package is imported
import pandas as pd

# ...

# Turn inputs & outputs into dataframe
observed_df = pd.DataFrame(data=rates, index=terms, columns=["observed"])
extrapolated_df = pd.DataFrame(data=fitted_rates, index=terms_target, columns=["extrapolated"])

# Combine and print dataframe
print(observed_df.join(extrapolated_df, how="outer"))