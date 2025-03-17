'''
This script uses the scipy library to perform statistical tests on differences in support for increased carbon tax between demographic groups.

- Mann-Whitney U Test: Used to compare two independent groups (e.g., Sex, Rural vs. Urban).
- Spearman's Rank Correlation: Used to assess the relationship between ordinal variables (e.g., Education, Political Affiliation, Age, Income).

    - Note: Age and Income have been binned to make them ordinal.

The test results are printed to the command line and stored here for convenience:

>> Mann-Whitney U Tests:
>>
>> Sex U-statistic: 707277.0
>> Sex P-value: 0.23144956228456004
>> 
>> Location U-statistic: 459573.0
>> Location P-value: 3.3569456524959816e-07
>> 
>> Spearman's Rank Correlation Tests:
>> 
>> Religiosity Spearman's Rank Correlation: -6.810212605037167e-05
>> Religiosity P-value: 0.9973333055710417
>> 
>> Education Spearman's Rank Correlation: 0.070878797241149
>> Education P-value: 0.0004960837319453988
>> 
>> Political Spearman's Rank Correlation: -0.32521569168172926
>> Political P-value: 5.328714631776798e-53
>> 
>> Age Spearman's Rank Correlation: -0.09474646101671817
>> Age P-value: 3.157355788824674e-06
>> 
>> Income Spearman's Rank Correlation: 0.009086767524994419
>> Income P-value: 0.6581826439313639
'''
import pandas as pd
import pyreadr
import scipy as sp

df = pyreadr.read_r("data/ds_final.rds")[None]

nameMaps = {
    "CLIM_POLSUPPORT_fueltax" : "Carbon Tax Support",
    "DEM_AGEGRP" : "Age",
    "DEM_GENDER_male" : "Sex",
    "DEM_INCOME" : "Income (CAD)",
    "DEM_POL_conservative" : "Political Orientation",
    "DEM_RELIGIOUS" : "Religiosity",
    "DEM_RESIDENCE" : "Living Area",
    "DEM_EDU" : "Highest Education"
}

canada_df = df[(df["COUNTRY_NAME"] == "Canada") & (df["CLIM_POLSUPPORT_fueltax"] != 4)].rename(columns = nameMaps)

income_bins = [0, 50000, 100000, 150000, float('inf')]
income_labels = ['0 - 50000', '50000 - 100000', '100000 - 150000', '150000+']
canada_df['Income (CAD)'] = pd.cut(canada_df['Income (CAD)'], bins=income_bins, labels=income_labels, right=False)

# Mann-Whitney U Tests

print("Mann-Whitney U Tests:\n")

sex_df = canada_df.dropna(subset=["Carbon Tax Support", "Sex"])
female_responses = canada_df.loc[canada_df["Sex"] == "0", "Carbon Tax Support"].to_list()
male_responses = canada_df.loc[canada_df["Sex"] == "1", "Carbon Tax Support"].to_list()

sex_stat, sex_p_value = sp.stats.mannwhitneyu(female_responses, male_responses, alternative="two-sided")

print(f"Sex U-statistic: {sex_stat}")
print(f"Sex P-value: {sex_p_value}\n")


location_df = canada_df.dropna(subset=["Carbon Tax Support", "Living Area"])
urban_responses = canada_df.loc[canada_df["Living Area"] == "0", "Carbon Tax Support"].to_list()
rural_responses = canada_df.loc[canada_df["Living Area"] == "1", "Carbon Tax Support"].to_list()

location_stat, location_p_value = sp.stats.mannwhitneyu(urban_responses, rural_responses, alternative="two-sided")

print(f"Location U-statistic: {location_stat}")
print(f"Location P-value: {location_p_value}\n")


# Spearman's Rank Correlation tests

print("Spearman's Rank Correlation Tests:\n")

religiosity_df = canada_df.dropna(subset = ["Carbon Tax Support", "Religiosity"])

relig_spearman_corr, relig_p_value = sp.stats.spearmanr(religiosity_df["Carbon Tax Support"], religiosity_df["Religiosity"])

print(f"Religiosity Spearman's Rank Correlation: {relig_spearman_corr}")
print(f"Religiosity P-value: {relig_p_value}\n")


education_df = canada_df.dropna(subset = ["Carbon Tax Support", "Highest Education"])

education_spearman_corr, education_p_value = sp.stats.spearmanr(education_df["Carbon Tax Support"], education_df["Highest Education"])

print(f"Education Spearman's Rank Correlation: {education_spearman_corr}")
print(f"Education P-value: {education_p_value} \n")

political_df = canada_df.dropna(subset = ["Carbon Tax Support", "Political Orientation"])

political_spearman_corr, political_p_value = sp.stats.spearmanr(political_df["Carbon Tax Support"], political_df["Political Orientation"])

print(f"Political Spearman's Rank Correlation: {political_spearman_corr}")
print(f"Political P-value: {political_p_value}\n")


age_df = canada_df.dropna(subset = ["Carbon Tax Support", "Age"])

age_spearman_corr, age_p_value = sp.stats.spearmanr(age_df["Carbon Tax Support"], age_df["Age"])

print(f"Age Spearman's Rank Correlation: {age_spearman_corr}")
print(f"Age P-value: {age_p_value}\n")


income_df = canada_df.dropna(subset = ["Carbon Tax Support", "Income (CAD)"])

income_spearman_corr, income_p_value = sp.stats.spearmanr(income_df["Carbon Tax Support"], income_df["Income (CAD)"])

print(f"Income Spearman's Rank Correlation: {income_spearman_corr}")
print(f"Income P-value: {income_p_value}\n")