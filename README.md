# cold_start_energy
This repository contains separate files for the algorithm and UI for Cold Start Energy Prediction

Energy forecasting is a very critical problem with both economic and environmental ramifications. A recurring problem with energy prediction for commercial buildings is that they need significant data to make accurate predictions.

The goal of this project is cold start prediction of energy consumption for commercial buildings.

The dataset contains data of ~700 buildings collected over 4 weeks at different time intervals. The product uses this data to train several models and come up with a prediction model for predicting the consumption of new buildings with as little as 1 week's worth of data.

The algorithm leverages on the fact that several buildings perform similarly due to similar factors such as having similar work schedules and general characteristics. These buildings are grouped together and customized models are run on these specific buildings in order to get best results.

The clustering removes the time series element of the data to a certain extent and hence, allows for traditional machine learning models to be applied on it.
