# Food Diversity in Major US Cities
## An analysis of ethnic cuisines based on Yelp data
Written by Willa Hua as an assignment from Urban Informatics, a course taught by Anthony Vanky at the University of Michigan.

## Overview
Introduce your question
Cite the data
List key accomplishments and findings

## Data Collection and Preparation
Method: Param setting + Yelp API + Join Country Code
Attributes: time scale, filters (what cities, what categories and how many), columns (business count, avg review count, avg rating), rationale, error rate

Data sets:
- Yelp businesses
- Yelp categories
- M49 Country Code
- Geo Json
with credits

## Popularity of Ethnic Cuisine Categories
How many ethnic cuisines do top 50 US cities have?
median count total restarants, median count categories, 
Define popularity as percentage of total, Sort by mean popularity

### Intuitive measure: the case of NYC
Following the definition above, what ethnic cuisines are most popular in New York? What are the available options? Introduce Viz

> viz title

![Placeholder Viz](https://via.placeholder.com/800x400)

### How does the ethnic cuisine landscape look like for your city, compares to NYC?
Intro to viz: drop-down filter, interactivity, zooming, panning and hover

> viz title & Dropdown Box

![Placeholder Viz](https://via.placeholder.com/800x400)


### Popular ethnic cuisines in major US cities, mapped!
Where does the ethnic cuisines in major US cities come from, and how popular are they?
Intro to measurement
Intro to viz
> viz title

![Placeholder Viz](https://via.placeholder.com/800x400)

## Modeling Food Diversity
What is food diversity? We consider ... as a diverse food scene.
### Measuring food diversity with the Shannon entropy
What is entropy

### Other diversity measures
Other metrices evaluated: The Simpson Index and the Kullback–Leibler divergence. 
Why entropy is a superior measure than simpson index and relative entropy
Cities with top food diversity
> Details on how the Simpson Index and the Kullback–Leibler divergence ranked the US food scene and details on why we prefer the Shannon entropy

### Top ranked cities with a diverse food scene
List top cities
Find out the rank of your city
![Dropdown Box](https://via.placeholder.com/800x20)

## Discussion
Limitations
    Data accuracy is ambiguous, inherently biased sample
    Sample for average rating and review count is small
    Ethnic food != Nationality
        Losses in mapping
    Modeling food diversity
        More could have been taken into consideration
Future works
    Include more cities
    Request a list of businesses
        to get accurate business count
        to analyze rating, price and review_count
Impacts