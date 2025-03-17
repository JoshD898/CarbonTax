# What individual factors correlate with Canadians' support for raising carbon taxes on gas, fossil fuels, or coal?  
## A secondary analysis of the TISP dataset


### Introduction

Carbon taxes are a key policy tool used to reduce greenhouse gas emissions by placing a financial cost on fossil fuel consumption. Advocates argue that such taxes encourage cleaner energy use and help combat climate change [1], while opponents criticize them for increasing living costs, particularly for lower-income households [2]. In Canada, carbon pricing has been a highly debated issue, with campaigns like "Axe the Tax" reflecting strong opposition in certain regions [3].

The TISP dataset is a collection of questionnaire responses from 71 922 participants in 68 countries in 2022, offering insight on public attitudes towards science and climate change [4]. 

### Objectives

The objective of this analysis is to look at the Canadian participants in the TISP dataset and determine if any of the following factors correlate with self-reported level of support for raising carbon taxes on gas and fossil fuels or coal:
* Age
* Sex
* Religiosity
* Political Orientation
* Rural vs Urban Residence
* Income

### Methods

Support for increasing carbon tax is an ordinal variable, so nonparametric statistical tests were used.

The Mann-Whitney U Test was used to compare two independent groups (e.g., Sex, Rural vs Urban)

Spearman’s Rank Correlation was used to assess relationships between ordinal variables (e.g., Education, Political Ideology)

* Age and Income were grouped in intervals to turn them into ordinal variables


Statistical tests were performed in Python using the Scipy library.

Visualizations were generated in Python using the Matplotlib library.

### Results

Urban residence, conservative ideology, higher age and lower levels of education are correlated with higher opposition to increasing carbon taxes on gas and fossil fuel. No significant relationship was found for sex or religiosity.

Refer to `Poster.pdf`, `analysis.py` and `visualizations.py` for more detailed results.

### Discussion
While statistically significant, it should be noted that the magnitudes of correlation that age and level of education have with support for increased carbon tax is small. Furthermore, the distribution of responses for level of education is overwhelmingly skewed towards higher education.

Overall, this analysis is helpful for understanding public support for raising carbon taxes in Canada, which can inform policy decisions aimed at addressing climate change.

### References
[1] Ambasta A, Buonocore JJ. Carbon pricing: a win-win environmental and public health policy. Canadian Journal of Public Health. 2018;109(5):779-781.

[2] Why are carbon taxes unfair? Disentangling public perceptions of fairness. Global Environmental Change. 2021;70:102356.

[3] AXE THE TAX. Conservative Party of Canada. April 6, 2023. Accessed March 16, 2025. https://www.conservative.ca/cpc/axe-the-tax/

[4] Mede NG, Cologna V, Berger S, et al. Perceptions of science, science communication, and climate change attitudes in 68 countries – the TISP dataset. Scientific Data. 2025;12(1):1-27.
