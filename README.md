# Sustain-table

## About
Sustain-table is a web application to help you decarbonize your diet while simplifying the process of grocery shopping. The application is currently under development.

***

## The Data Incubator
This project is my capstone project for [The Data Incubator](https://www.thedataincubator.com/programs/data-science-bootcamp/). Below I outline how the project fulfills the capstone requirements.

### 1. A clear business objective.
Sustain-table aims at to reduce global carbon emissions by providing its users with intelligent ingredient substitutions options. It would be possible to monitize the platform through ingredient, cooking-product, and recipe promotions.

The platform is for anyone who regularly cooks and wants to reduce their carbon footprint. Cooking at home has been on the rise in recent years, amongst both men and women ([reference](https://nutritionj.biomedcentral.com/articles/10.1186/s12937-018-0347-9)). While climate change is personally important to a broad swathe of Americans, interest is more pronounced in younger generations ([reference](https://climatecommunication.yale.edu/publications/do-younger-generations-care-more-about-global-warming/)). Therefore, the intetend audience of Sustain-table is broad, but key interest group is young professionals.

### 2. Data ingestion.

Sustain-table makes use of numerous datasets:
* **Expert substitution dataset.** The ingredient substition model (still under development) is a hybrid expert-ML model. The expert recommendations come from data scraped from [The Cook's Thesaurus](http://www.foodsubs.com/). I scrapped and processed the data, as shown in the [expert_substitutions](https://github.com/DJRdatascience/sustain-table/tree/main/expert_substitutions) folder.
*  **Recipe dataset.** The machine learning component of the ingredient substition model is currently under development. Initially, I have been working with the [Recipe1M+ dataset](http://pic2recipe.csail.mit.edu/), and I am currently evaluating whether this needs to be modified or expanded upon.
*  **Carbon equivalents.** In order to calculate carbon emissions of recipes, I have taken estimated carbon equivalents of common food products from the academic literature. For further information on the data sources and how I prepared the data, see the [carbon_equivalents](https://github.com/DJRdatascience/sustain-table/tree/main/carbon_equivalents) folder.
*  **Mass converstion.** Most (American) recipes give ingredient measuremets by volume. Volume-to-mass converstions were carried out using estimated densities of common food products, see the [mass_conversion](https://github.com/DJRdatascience/sustain-table/tree/main/mass_conversion) folder.

### 3. A demonstration of the following:

#### 3a. Machine learning

A key component of Sustain-table is an ingredient substitution model that provides users with intelligent ingredient substitution options in order to lower the carbon emissions of their grocery shopping lists. The current implementation of this model is an expert model, which provides recommended food substitutions for >1k ingredients using expert recommendations from [The Cook's Thesaurus](http://www.foodsubs.com/). I am actively working to incorporate  a machine learning model (word2vec) that provides substitution options for ingredients not in the expert database. Further information on the model can be folder in the [ml-substitutions](https://github.com/DJRdatascience/sustain-table/tree/main/ml_substitutions) folder.

#### 3b. An interactive website

Sustain-table is an interative website built using Flask and SQLAlchemy. The website has not yet launched online. You can find the web application, which can be run locally, in the [app](https://github.com/DJRdatascience/sustain-table/tree/main/app) folder.

### 4. A deliverable
The final deliverable for this project will be this GitHub repository and a live website.
