# Popularity and Diversity of Food in Major US Cities
## An analysis of ethnic cuisines based on Yelp data
Written by Willa Hua as an assignment from Urban Informatics, a course taught by Anthony Vanky at the University of Michigan.

## Overview
I'm interested in investigating the popularity and diversity of ethnic cuisines running in the US by pulling Yelp data. In this article, I report on my methods and answer the following questions:
1. What ethnic cuisines are popular in NYC, and in your city? 
2. Where does the food we enjoy come from? 
3. What cities have top diverse food scenes in the US?

<br/>

## Data Collection and Preparation
The data consists of the count of restaurants and food businesses for 76 ethnic food categories in the top 50 US major cities (ranked by population) and Ann Arbor, where the author is located. More specifically, each row of data consists of the city (e.g. NYC), the ethnic food category (e.g. Chinese), the country corresponding to the category, if applicable, and the count of total businesses. To download the data, access [my Github page](https://github.com/wiiilla/Food_Diversity_In_US_Cities).

<br/>

#### Table: Underlying data sources
| Dataset | Description | Source | Credit |
| ----------- | ----------- | ----------- | ----------- |
| US Ethnic Food Categories | A list of 76 Yelp categories that're available in the US and relevant to a broad culture and ethnicity | Yelp | [Yelp Fusion API Documentation](https://www.yelp.com/developers/documentation/v3/all_category_list) |
| Top 50 US cities | A list of top 50 US cities ranked by popularity | GitHub | [Github User Miserlou's Shared file](https://gist.github.com/Miserlou/c5cd8364bf9b2420bb29) |
| Count of Businesses | A total count of businesses for each of the combination of 51 cities and 76 categories | Yelp | [the Business Endpoint of the Yelp Fusion API](https://www.yelp.com/developers/documentation/v3/business_search) |
| M49 country codes and nationality | Used to map the ethnic food categories to nationalities; 57 categories successfully matched | Wikipedia | [Github User Dinuk's Shared File](https://github.com/Dinuks/country-nationality-list)

<br/>

## Popularity of Ethnic Cuisine Categories
Based on the data described above, the average US major city has ~2,000 restaurants captured in our sample. On average, US cities have 53 generic ethnic food categories, with New York City hitting the maximum of 74 categories. For each city, we define the popularity of an ethnic cuisine intuitively as the percentage of the given ethnic cuisine in all restaurants. To estimate the popularity of an ethnic cuisine across the US, we define its popularity as the average percentage of total across all cities. 

<br/>

### Intuitive measure: the case of NYC

Following the definition above, what ethnic cuisines are most popular in New York City? What are some delicious options that you haven't tried? Chinese food dominates the food scene Big Apple with a 13% percentage, followed by Italian and Mexican. Our beloved American Traditional lies on the fourth rank and Japanese food the fifth. In the interactive visualization below, you can explore the ethnic cuisines in NYC ranked by popularity. Zoom and pan to dive into the niche cuisines, and hover to read its details.

> Food Popularity in NYC by Ethnic Cuisine Categories

![Placeholder Viz](https://via.placeholder.com/800x400)

<br/>

### How about my city? You asked.
If you wonder how the ethnic cuisine landscape looks like for your city, compares to NYC, I got you covered. Use the drop-down filter for the visualization below to find your own city, and don't forget to zoom in! The visualization defaults to a comparison between NYC and Ann Arbor, and I'll demonstrate later how Ann Arbor has a higher food diversity than NYC under my model.

> Paired Food Popularity of NYC and your City of Choice

![Placeholder Viz](https://via.placeholder.com/800x400)

<br/>

### Popular ethnic cuisines in the US, mapped!
Where does the ethnic cuisines we love here in the US come from? To answer the question, I linked the applicable ethnic food categories to their corresponding countries and mapped the result. The deeper the color, the more popularity the cuisine from that country has in the US.

> Map of Origins for Ethnic Cuisines Popular in Major US Cities

![Placeholder Viz](https://via.placeholder.com/800x400)

<br/>

## Diversity of US City Food Landscape
Now that we've looked at the popularity of ethnic cuisines, how about diversity? A food diversity metric provides a helpful lense to the Diversity of demographics and tastes in cities and communities. To devise such a metric, let's consider a city with abundant and well-balanced ethnic food categories as having a diverse food scene. A good diversity metric captures both the number of ethnic food categories and the extent to which these categories are equally distributed. 

<br/>

### Measuring food diversity with the Shannon entropy
The diversity metric most useful for our context is the [Shannon entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)), also known as Shannon's diversity index in the ecological literature. The idea is first proposed to quantifies the uncertainty in predicting the letter that's taken at random from a string. As a generalization, given a distribution of categories, the more different categories there are and the more equal their frequency, the higher its entropy and hence, its diversity. 

<br/>

### Cities with best food diversity
What are the top cities with a diverse food scene? As a Wolverine I'm happy to report that Ann Arbor, Michigan, with 57 ethnic cuisine categories, ranked the top in terms of food diversity. NYC only ranked the fifth, despite that it has nearly all the ethnic cuisines available. This is likely because the frequency of ethnic cuisines in NYC are more unevenly distributed than that in Ann Arbor.  

#### Table: Cities with top 10 food diversity
| Rank | City | # Ethnic Cuisine Categories | Food diversity in Shannon entropy |
| ----------- | ----------- | ----------- | ----------- |
| 1 | Ann Arbor, Michigan | 57 | 3.47 |
| 2 | Seattle, Washington | 68 | 3.08 |
| 3 | Washington, District of Columbia | 62 | 3.05 |
| 4 | San Francisco, California | 70 | 3.03 |
| 5 | New York, New York | 73 | 3.03 |
| 6 | Baltimore, Maryland | 63 | 3.00 |
| 7 | San Jose, California | 70 | 2.99 |
| 8 | Detroit, Michigan | 56 | 2.97 |
| 9 | Oakland, California | 72 | 2.97 |
| 10 | Miami, Florida | 58 | 2.95 |

<br/>

## Discussion
The goal of this analysis is to preliminarily explore the popularity of each ethnic food categories in the US and model food diversity. The later is particularly useful given that we've validated that modeling food diversity with Shannon Entropy provides a robust ranking that echos our intuition. Meanwhile, the analysis is constrained by the dataset: the sample is inherently biased and lacks validation given that Yelp is the sole data source. Some future next steps would be requesting data for more cities and more business details, as well as building a more informed model of food diversity that takes into account the new data.
