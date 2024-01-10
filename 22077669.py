import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def process_world_bank_data(population_data):
    """
    Process World Bank data from the given CSV file.

    Parameters:
    - population_data : File path of the World Bank data in CSV format.

    Returns:
    - world_bank_data : Processed World Bank data - Population Growth
    - Transposed version of the processed data.
    """
    world_bank_data = pd.read_csv(population_data).iloc[: -5]
    world_bank_data.drop(columns=['Country Code', 'Series Code', 
                                  '2001 [YR2001]', '2002 [YR2002]', 
                                  '2003 [YR2003]', '2004 [YR2004]', 
                                  '2005 [YR2005]', '2006 [YR2006]', 
                                  '2007 [YR2007]',
                                  '2008 [YR2008]', '2009 [YR2009]', 
                                  '2010 [YR2010]', '2011 [YR2011]', 
                                  '2012 [YR2012]'], inplace=True)
    world_bank_data.columns = [col.split(' ')[0] for col in world_bank_data.columns]
    transpose = world_bank_data.T
    transpose.columns = transpose.iloc[0]
    transpose = transpose.iloc[1:]
    transpose = transpose[transpose.index.str.isnumeric()]
    transpose.index = pd.to_numeric(transpose.index)
    transpose['Years'] = transpose.index

    return world_bank_data, transpose

def barplot_urban_growth_data(ax, world_bank_data):
    """
    Plot a bar chart for urban population growth from 2015 to 2019.

    Parameters:
    - Axes on which the plot will be drawn.
    - Processed World Bank data.

    Returns:
    None
    """
    urban_growth_data = world_bank_data[world_bank_data['Series'] == 'Urban population growth (annual %)']

    urban_growth_data_melted = pd.melt(urban_growth_data, 
                                       id_vars=['Country'], 
                                       value_vars=['2015', '2016', 
                                                   '2017', '2018', '2019'],
                                       var_name='Year', 
                                       value_name='Urban Population Growth (Annual %)')

    urban_growth_data_melted['Urban Population Growth (Annual %)'] = urban_growth_data_melted['Urban Population Growth (Annual %)'].astype(float)
    urban_growth_data_melted['Year'] = urban_growth_data_melted['Year'].astype(int)

    sns.barplot(ax=ax, x='Country', y='Urban Population Growth (Annual %)',
                hue='Year', data=urban_growth_data_melted,
                palette='magma', dodge=True)

    ax.set_title('Urban Population Growth (Annual %) in 2015 - 2019')
    ax.set_xlabel('Country')
    ax.set_ylabel('Urban Population Growth (Annual %)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.legend(title='Year', loc=2)

def lineplot_urban_growth_data(ax, world_bank_data):
    """
    Plot a line chart for urban population growth from 2015 to 2019.

    Parameters:
    - Axes on which the plot will be drawn.
    - Processed World Bank data.

    Returns:
    None
    """
    urban_growth_data = world_bank_data[world_bank_data['Series'] == 'Urban population growth (annual %)']

    urban_growth_data_melted = pd.melt(urban_growth_data, 
                                       id_vars=['Country'], 
                                       value_vars=['2015', '2016',
                                                   '2017', '2018', '2019'],
                                       var_name='Year', 
                                       value_name='Urban Population Growth (Annual %)')

    urban_growth_data_melted['Urban Population Growth (Annual %)'] = urban_growth_data_melted['Urban Population Growth (Annual %)'].astype(float)
    urban_growth_data_melted['Year'] = urban_growth_data_melted['Year'].astype(int)

    sns.lineplot(ax=ax, x='Year', 
                 y='Urban Population Growth (Annual %)',
                 hue='Country', data=urban_growth_data_melted,
                 marker='o', markersize=8, linewidth=2)

    ax.set_title('Urban Population Growth (Annual %) Over the Years', 
                 fontsize=16, weight='bold')
    ax.set_xlabel('Year', fontsize=14)
    ax.set_xticks(range(2015, 2020, 1))
    ax.set_ylabel('Urban Population Growth (Annual %)', fontsize=14)

    ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='best', 
              fontsize=10)

def pie_chart_largest_city_population(ax, world_bank_data):
    """
    Plot a pie chart for population distribution in the largest city
    (% of urban population) in 2019.

    Parameters:
    - Axes on which the plot will be drawn.
    - Processed World Bank data.

    """
    largest_city_data = world_bank_data[world_bank_data['Series'] == 'Population in the largest city (% of urban population)']

    year = '2019'

    largest_city_data = largest_city_data.dropna(subset=[year])
    largest_city_data[year] = largest_city_data[year].astype(float)
    largest_city_data = largest_city_data.sort_values(by=year, ascending=False)

    top_countries = largest_city_data.head(6)

    ax.pie(top_countries[year], autopct='%1.1f%%',
           pctdistance=0.85, startangle=140, colors=sns.color_palette("Set3"),
           textprops={'fontsize': 10, 'weight': 'bold'})

    ax.axis('equal')
    ax.legend(title='Country', labels=top_countries['Country'], 
              loc='upper left', bbox_to_anchor=(1, 0.8), fontsize=10)

    ax.set_title(f'Population in the Largest City (% of Urban Population) ({year})',
                 fontsize=14, weight='bold', pad=10)

def histogram_rural_population(ax, world_bank_data):
    """
    Plot a histogram for the distribution of rural
    population across countries for the years 2015 to 2019.

    Parameters:
    - Axes on which the plot will be drawn.
    - Processed World Bank data.

    """
    rural_population_data = world_bank_data[world_bank_data['Series'] == 'Rural population']
    rural_population_data_melted = pd.melt(rural_population_data,
                                           id_vars=['Country'], 
                                           value_vars=['2015', '2016', 
                                                       '2017', '2018', '2019'],
                                           var_name='Year', 
                                           value_name='Rural Population')

    rural_population_data_melted['Rural Population'] = rural_population_data_melted['Rural Population'].astype(float)
    rural_population_data_melted['Year'] = rural_population_data_melted['Year'].astype(int)

    sns.histplot(ax=ax, data=rural_population_data_melted, 
                 x='Rural Population', bins=20, color='skyblue')
    ax.set_title('Distribution of Rural Population Across Countries (2015-2019)',
                 fontsize=16, weight='bold')
    ax.set_xlabel('Rural Population (in millions)', fontsize=14)
    ax.set_ylabel('Frequency', fontsize=14)


# Read the World Bank data from the specified CSV file path.
population_data_path = r"world_population_data.csv"
world_bank_data, _ = process_world_bank_data(population_data_path)

# Create subplots for the infographic
fig, axs = plt.subplots(2, 2, figsize=(20, 12), 
                        gridspec_kw={'hspace': 0.6, 'wspace': 0.4})

# Plotting individual components
barplot_urban_growth_data(axs[0, 0], world_bank_data)
lineplot_urban_growth_data(axs[0, 1], world_bank_data)
pie_chart_largest_city_population(axs[1, 0], world_bank_data)
histogram_rural_population(axs[1, 1], world_bank_data)

# Add student information on the right side
fig.suptitle('Population Growth Analysis - Urban & Rural (2015 - 2019)', 
             fontsize=40, weight='bold',x=1, y=1)

# Descriptions
combined_description = """

Name       : Gokul Anand Srinivasan
Student ID : 22077669

This illustration shows World urban and rural population growth, generates four different plots to visualize various aspects of the data. 

1. Bar plot illustrating the annual urban population growth for each country from 2015 to 2019. 
   This plot provides a visual comparison of urban growth rates across countries.

2. Line plot showing the annual urban population growth over the years for various countries. 
   The plot helps in understanding the trend of urban population growth from 2015 to 2019.

3. Pie chart depicting the percentage distribution of population in the largest city for the top countries in 2019. 
   This chart visually represents the concentration of urban population in the largest cities of selected countries.

4. Histogram representing the distribution of rural population across countries for the years 2015 to 2019. 
   This plot illustrates the frequency distribution of rural population across different countries.
"""

plt.figtext(0.92, 0.5, 
            combined_description, 
            ha='left', va='center',
            fontsize=18, 
            bbox=dict(facecolor='white',
                      alpha=0.8, boxstyle='round,pad=0.5'),weight='bold')

# Save the entire canvas as a single image
plt.savefig("22077669.png", dpi=300, bbox_inches='tight')

# Display the infographic
plt.show()
