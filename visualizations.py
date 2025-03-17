'''
This code generates the visualizations used in the poster. The figures produced are saved in "./figures".
'''
import matplotlib.pyplot as plt
import pandas as pd
import pyreadr

df = pyreadr.read_r("data/ds_final.rds")[None]

valueMaps = {
    "Carbon Tax Support" : {
        1 : "Not at all",
        2 : "Moderately",
        3 : "Very much"
    },
    "Sex" : {
        "1" : "Male",
        "0" : "Female"
    },
    "Highest Education" : {
        "1" : "Did not attend school",
        "2" : "Primary education",
        "3" : "Secondary education",
        "4" : "Higher education"
    },
    "Living Area" : {
        "1" : "Urban",
        "0" : "Rural"
    }
}

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

for col, mapping in valueMaps.items():
    if col in canada_df.columns:
        canada_df[col] = canada_df[col].replace(mapping)





def aggregateByColumn(colName : str, df : pd.DataFrame) -> pd.DataFrame:
    '''
    Produces a dataframe of with total of responses to "do you support raising carbon tax" aggregated by the given column

    Any rows with NaN in the specified column are not included in the final dataframe.
    '''
    df = df.dropna(subset = [colName])

    aggregate_df = df.groupby(colName)["Carbon Tax Support"].value_counts().unstack()

    return aggregate_df



def plotAggregateSideFig(aggregated_df: pd.DataFrame, colName : str, filename: str):
    aggregated_percent = aggregated_df.div(aggregated_df.sum(axis=1), axis=0) * 100
    
    species = aggregated_percent.index

    if colName == "Living Area":
        fig, ax = plt.subplots(figsize=(6, 6))
    else:
        fig, ax = plt.subplots(figsize=(12, 6))

    if colName == "Living Area":
        ax.text(0.3, 0.95, "Mann-Whitney U P-Value < 0.001",  ha="center", va="center", fontsize=10, color="black", transform=ax.transAxes)
    elif colName == "Age Range":
        ax.text(0.22, 0.06, "Spearman’s Rank Correlation: -0.095 (P < 0.001)",  ha="center", va="center", fontsize=10, color="black", transform=ax.transAxes)
    else:
        ax.text(0.25, 0.96, "Spearman’s Rank Correlation: 0.071 (P < 0.001)",  ha="center", va="center", fontsize=10, color="black", transform=ax.transAxes)

    

    ymin = - max(aggregated_percent['Not at all'] + (aggregated_percent['Moderately'] / 2))
    ymax = max(aggregated_percent['Very much'] + (aggregated_percent['Moderately'] / 2))
    ax.set_ylim(ymin - 5, ymax + 5)

    bottom = - aggregated_percent['Not at all'] - (aggregated_percent['Moderately'] / 2)

    bar1 = ax.bar(species, aggregated_percent["Not at all"], 0.5, label="Not at all", bottom=bottom, color = '#FA8933')
    bottom += aggregated_percent["Not at all"].values
    bar2 = ax.bar(species, aggregated_percent["Moderately"], 0.5, label="Moderately", bottom=bottom, color = 'lightgray')
    bottom += aggregated_percent["Moderately"].values
    bar3 = ax.bar(species, aggregated_percent["Very much"], 0.5, label="Very much", bottom=bottom, color = '#73EAFA')

    for bar in [bar1, bar2, bar3]:
        for rect in bar:
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2,  
                rect.get_y() + height / 2,            
                f'{height:.0f}%',                     
                ha='center',                          
                va='center',                          
                fontsize=10                            
            )


    total_counts = aggregated_df.sum(axis=1)
    ax.set_yticks([])
    ax.axhline(0, color='grey', linewidth=0.2, zorder = 0)
    
    x_labels = [f"{species[i]}\nN = {total_counts.iloc[i]}" for i in range(len(species))]

    x_positions = [rect.get_x() + rect.get_width() / 2 for rect in bar1]

    ax.set_xticks(x_positions)
    ax.tick_params(axis="x") 
    ax.set_xticklabels(x_labels, ha="center") 

    ax.set_title(f"Support for Raising Carbon Tax by {colName}")

    plt.savefig(filename, dpi=300, bbox_inches="tight", transparent=False)



def plotAggregateMainFig(aggregated_df: pd.DataFrame):
    '''
    Plot the distribution of responses for the given dataframe, then save it to file.
    '''
    aggregated_percent = aggregated_df.div(aggregated_df.sum(axis=1), axis=0) * 100
    
    species = aggregated_percent.index

    fig, ax = plt.subplots(figsize=(12, 6))

    

    ymin = - max(aggregated_percent['Not at all'] + (aggregated_percent['Moderately'] / 2))
    ymax = max(aggregated_percent['Very much'] + (aggregated_percent['Moderately'] / 2))
    ax.set_ylim(ymin - 5, ymax + 5)

    bottom = - aggregated_percent['Not at all'] - (aggregated_percent['Moderately'] / 2)

    bar1 = ax.bar(species, aggregated_percent["Not at all"], 0.5, label="Not at all", bottom=bottom, color = '#FA8933')
    bottom += aggregated_percent["Not at all"].values
    bar2 = ax.bar(species, aggregated_percent["Moderately"], 0.5, label="Moderately", bottom=bottom, color = 'lightgray')
    bottom += aggregated_percent["Moderately"].values
    bar3 = ax.bar(species, aggregated_percent["Very much"], 0.5, label="Very much", bottom=bottom, color = '#73EAFA')

    for bar in [bar1, bar2, bar3]:
        for rect in bar:
            height = rect.get_height()
            ax.text(
                rect.get_x() + rect.get_width() / 2,  
                rect.get_y() + height / 2,            
                f'{height:.0f}%',                     
                ha='center',                          
                va='center',                          
                fontsize=10                            
            )


    total_counts = aggregated_df.sum(axis=1)
    ax.set_yticks([])
    ax.axhline(0, color='grey', linewidth=0.2, zorder = 0)

    x_labels = [
        f"Strongly Liberal\nN = {total_counts.iloc[i]}" if i == 0 else
        f"Strongly Conservative\nN = {total_counts.iloc[i]}" if i == 4 else
        f"-\nN = {total_counts.iloc[i]}"
        for i in range(len(species))
    ]


    x_positions = [rect.get_x() + rect.get_width() / 2 for rect in bar1]

    ax.set_xticks(x_positions)
    ax.tick_params(axis="x", colors="white") 
    ax.set_xticklabels(x_labels, ha="center", color = "white") 

    ax.spines["bottom"].set_color("white") 
    ax.spines["left"].set_color("white") 

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    legend = ax.legend([bar3, bar2, bar1], ["Very much", "Moderately", "Not at all"], loc="upper right",  title = "Support for raising carbon taxes", labelcolor="white")

    legend.get_title().set_color("white")
    legend.get_frame().set_facecolor("none")

    ax.text(
    0.25, 0.08, 
    "Spearman’s Rank Correlation: -0.325 (P < 0.001)",  
    ha="center", va="center", fontsize=10, color="white", transform=ax.transAxes
    )

    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    plt.savefig("figures/conservative.png", dpi=300, bbox_inches="tight", transparent=True)

    legend_fig = plt.figure(figsize=(4, 2))  
    ax_legend = legend_fig.add_axes([0, 0, 1, 1])  
    ax_legend.legend([bar3, bar2, bar1], ["Very much", "Moderately", "Not at all"], loc="center", title="Support for raising carbon taxes")
    ax_legend.axis("off") 
    legend_fig.savefig("figures/legend.png", dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.1)


plotAggregateMainFig(aggregateByColumn("Political Orientation", canada_df))

plotAggregateSideFig(aggregateByColumn("Age", canada_df), "Age Range", "figures/age.png")
plotAggregateSideFig(aggregateByColumn("Living Area", canada_df), "Living Area", "figures/urban.png")
plotAggregateSideFig(aggregateByColumn("Highest Education", canada_df), "Highest Education", "figures/education.png")