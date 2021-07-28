![CDL Hackaton](img/CDL_logo.png)

# Business Pitch
<img src="./logo.jpg" width="100">

<table align="center">
     <tr>
        <td><img src="./Aviation.jpg" width="400"></td>
        <td><img src="./WeatherForecast.jpg" width="450"></td>
    </tr>
</table>



The chaotic nature of our atmosphere seriously limits our ability to model it — and therefore to predict what it will do next. A single weather model run more than once with even the most subtle differences in starting conditions can produce very different predictions. Since no measurement is perfect - every observation has an associated uncertainty - these small imperfections can cause big changes in what a model predicts. These changes get bigger and bigger the further ahead you try to predict. Because of this, the potential predictability limit of weather is about two weeks. For hurricanes and winter storms, which are much bigger and therefore easier to spot in advance, the theoretical limit is two to three weeks. 

Today’s five-day forecast is accurate about 90 percent of the time, the seven-day - about 80 percent, and a 10-day forecast - about 50 percent. Forecasts have become very accurate - today’s five-day hurricane forecast is more reliable than the four-day forecast in the early 2000s, and more reliable than a three-day forecast in the 1990s. Three- to 10-day forecasts have been improving by about a day per decade - meaning a modern six-day forecast is as accurate as a five-day forecast 10 years ago. As we see there is still potential to further improve accuracy in extending the forecast period [1].

Weather forecasts can be divided into three types: short term weather forecast (2-3 days), medium-term weather forecast (4–9 days), and long-term weather forecast (more than 10–15 days). According to the coverage area, the weather forecast can be divided into large-scale forecast (generally referring to the forecast of a continent or country), medium-scale forecast (usually referring to the forecast of a province (region), state, and region), and small scale forecast (such as the forecast of a county, city, etc.) [2]. 

## The problem
Despite the increased accuracy of weather forecasts over the years, weather and climate change related natural disasters are on the rise and cause deaths and substantial economic loss. The U.S. alone has sustained 298 weather and climate disasters since 1980 where overall damages/costs exceed $1.975 trillion. Since 1980 there have been 7 disaster events per year, costs were 48 billion $US/year, deaths - 353/year. In 2020 alone 22 events have resulted in ca. 100 billion $US damage and 262 deaths [3].

## The solution
1QPoint’s weather forecast platform takes advantage of hybrid algorithms and NISQ devices to extend the weather forecast day period and increase  accuracy. We start with a medium-scale forecast and medium-term weather forecast products. With proven results using proprietary algorithms we were able to classify wildfires, storms and demonstrate potential quantum advantages in weather anomaly detection. Given our expertise in QML (Quantum Machine Learning) our algorithms provide NISQ (Noisy Intermediate Scale Quantum) solutions as a Saas platform via techniques such as QSVM (Quantum Support Vector Machines) and QNN (Quantum Neural Networks). 

## The current state
To do weather forecasting we need observational data, mathematical modeling, and computation. Various sources, such as weather stations, satellites, sea buoys, commercial airliners and ships gather data from all around the world. Billions of observations are made every single day. Most weather agencies use supercomputers with amazing computational prowess. The supercomputers at the National Oceanic and Atmospheric Administration (NOAA), for example, can complete 2.8 quadrillion calculations every second. These supercomputers have now become crucial to generating global forecasts. The observational data used are temperature, pressure, wind humidity and clouds.

Researchers have used parameterizations to model the relationships underlying small-scale atmospheric processes and their interactions with large-scale atmospheric processes. Stochastic parameterizations have become popular for representing the uncertainty in subgrid-scale processes and they produce accurate weather forecasts and climate projections. It’s still a mathematically challenging method. Now researchers are turning to machine learning to provide more efficiency to mathematical models. 

Generative adversarial networks (GANs) have been used with a toy model of the extratropical atmosphere known as the L96 system, frequently used as a test bed for stochastic parameterization schemes. The GANs that provided the most accurate weather forecasts also performed best for climate simulations, but they did not perform as well in offline evaluations. The authors conclude that GANs are a promising approach for the parameterization of small-scale but uncertain processes in weather and climate models [5].

Many machine learning models have been implemented such as Extra Tree Regression, Random Forest Regression, Support Vector Regression and Ridge Regression for weather forecasting. They have found Random Forest Regressor to be a better regressor as it ensembles multiple decision trees while making decisions. Their evaluation results have shown that machine learning models can give accurate results comparable to the traditional models. Comparison has been made among Convolutional Networks, Conditional Restricted Boltzmann Machine, Recurrent Neural Network. RNN method was found to give adequate accuracy when compared to the other models. Different combinations of weather parameters such as pressure, temperature, dewpoints, wind speed, precipitation and many other weather parameters were used to train LSTM. The LSTM algorithm has given  substantial results accuracy wise, among other weather prediction techniques [6].

## Why now
We believe the true representation and description of a chaotic system as the weather can be achieved with quantum computing and algorithms due to the underlying similarity of both systems. Quantum is at the beginning of its realisation potential. We are aware of the limitations the current devices have and this helps us build better solutions by incorporating technology advancements as soon as they are achieved. We grow our platform together with quantum technology as the future belongs to quantum especially in predicting inherently complex systems.

## Business model
We offer our forecast products in a SaaS subscription model.

## Verticals
The platform assists following industries to optimize weather risk:
* The global aviation weather forecasting services market is projected to reach US$ 447.6 million in 2024 [7].
* Energy and utilities: From causing outages to affecting energy consumption rates, the weather can have a significant impact on energy and utilities.
* Ground transportations: If drivers aren’t prepared, harsh conditions such as icy roads, poor visibility and violent storms may lead to delays, accidents or serious injuries. Applying AI and analytics to weather and traffic data helps transportation companies and their drivers make better decisions about impending conditions. 
* Insurance: Innovative insurers use data and analytics to discover innovative ways to improve policyholder satisfaction, manage risk, reduce claims and prevent fraud. 
* Retail: The correlation between weather and consumer buying patterns is rarely utilized when predicting retail trends. But even more often overlooked is weather's impact on supply chain management, product demand and pricing. 

## Global weather forecast market
The weather forecasting systems market is estimated to be USD 2.3 billion in 2019 and is projected to reach USD 3.3 billion by 2025, at a CAGR of 5.7% from 2019 to 2025 [8]. Increasing demand for weather forecasting using big data analytics and rise in climate change patterns resulting in uncertainties related to rainfall are major factors expected to drive the growth of the weather forecasting systems market, globally. The software solution segment is projected to grow at the highest CAGR during the forecast period with North America to lead the weather forecasting systems market from 2019 to 2025.

Market growth in North America is driven majorly by the increased demand for highly accurate weather forecasting systems from the aviation and commercial industries. The region is considered to be the largest developer, operator, and exporter of weather forecasting systems, globally. The US and Canadian governments are investing increasingly for the enhancement of their respective weather forecasting agencies.

## Product roadmap and platform strategy

**Products:** Our first product CloudQ has big potential in the aviation weather forecast market. We are proud of our SolarPowerQ that predicts solar electricity generation less than a few hours in advance. Instead of working out what the weather will be in a given area, to get precise solar forecasts, we build on our CloudQ product. SolarPowerQ precisely locates where each cloud will be located relative to a solar array, and how the size and shape of the clouds influence how much sunlight gets through to the solar panels. By maximizing the solar panel output, fossil fuel power stations are run less, and by doing so we reduce CO2 emissions and their impact on climate change [9].

Our next products are TemperatureQ and PrecipitationQ, the latter being more challenging to forecast than temperature. Temperature is a continuous field, precipitation is a discontinuous field, meaning there’s a lot of places where there is none, and then some places where it can be raining or snowing very hard [10].

Our weather forecast platform can extend to other markets such as emotion recognition and predictions due to the similarity of the problem as they belong to multi-class classification problems. They both can be modeled using recurrent neural networks due to their temporal interactions.

## Competitors and competitive advantage
**Key players:** The Weather Company (US), Vaisala (Finland), Sutron Corporation (US), Campbell Scientific (US), Airmar Technology Corporation (US), All Weather, Inc. (US), Morcom International (US), Columbia Weather Systems (US), G. Lufft Mess-und Regeltechnik (Germany), and Skye Instruments (UK), among others.

<table align="center">
    <tr >
        <td> <b>Company name</b> </td>
        <td> <b>Headquarter</b> </td>
        <td> <b>Profit in USD</b></td>
    </tr>
    <tr>
        <td>The Weather Company/IBM Parent Company</td>
        <td>USA</td>
        <td>N/A</td>
    </tr>
    <tr>
        <td>Vaisala</td>
        <td>Finland</td>        
        <td>447.85 million</td>
    </tr>
    <tr>
        <td>Sutron Corporation </td>
        <td>USA</td>        
        <td>26 million</td>
     </tr>    
     </tr>          
</table>

**The market:** Increase in number of natural disasters due to undesired climatic changes drives the growth of the global market. Reliable weather forecasting can lead to reduction in operational & maintenance costs for business operations, reduce disaster recovery cost and lead to flexible insurance policies. On the supply side, increasing the accuracy of machine learning techniques and improvement in data fusion methods leads to increasing accuracy of predictions. Our vision is to become the weather forecast partner for governments and universities.

**Value proposition:** more efficient representations of the underlying physics is expected due to the shared quantum nature of programmable qubits and the weather systems being simulated. 

**Our advantage:** agile, scalable platform focused solely on weather forecasting using hybrid machine learning algorithms and methods across relevant verticals. Our biggest strength is our highly skilled team of PhDs, (quantum) machine learning engineers and architecture design experts with combined academia research, industry and corporate consulting experience of 35 years.

## Potential customers
A single public weather service is typically the only source available for forecasts, warnings and alerts. These meteorologists work for public (government) organizations or universities. By contrast, the United States has strong public, private (commercial) and university-based weather observation and forecasting programs.
Commercial weather providers typically have some weather modeling capabilities. and fills a different niche like, surfing conditions, fire conditions or transportation concerns, based on specific observations and models that refine the broad public-sector data.

Clients: National Oceanic and Atmospheric Administration (NOAA)/USA, Government of Canada Weather Information Service, University of Oklahoma

## Conclusion
1QPoint aims to leverage current NISQ devices to deploy classical, hybrid and quantum inspired algorithms and machine learning to model weather forecast-relevant data points and deliver more accurate medium-term and medium-scale weather forecasts. Our products help industries such as aviation, insurance, energy and utilities, retail to optimize operation and maintenance cost, optimize weather risks and increase value provided to their customers. We help governments to reduce disaster recovery costs and save people’s lives due to severe natural events with timely and accurate weather predictions. 

Our advantage lies in an agile and scalable platform tuned to address weather complexity using cutting edge techniques. Our strength is our team of PhDs and (quantum)  machine learning engineers with a combined expertise of 35 years in academia research, management of machine learning teams  and consulting. We envision ourselves as the go to partner for accurate weather predictions that save people’s lives and help business thrive.

## References

[1] [How Weather Forecasts Are Made](https://www.discovermagazine.com/planet-earth/how-weather-forecasts-are-made). Accessed July 26, 2021.

[2] [Zhang, J. et al.. 2021. Support Vector Machine Weather Prediction Technology Based on the Improved Quantum Optimization Algorithm](https://www.hindawi.com/journals/cin/2021/6653659/)

[3] [Billion-Dollar Weather and Climate Disasters: Overview | National Centers for Environmental Information (NCEI)](https://www.ncdc.noaa.gov/billions/). Accessed July 26, 2021 

[4] [How Does Weather Forecasting Work?](https://www.scienceabc.com/innovation/how-does-weather-forecasting-work.html#how-does-weather-forecasting-work). Accessed July 26, 2021

[5] [Machine Learning Improves Weather and Climate Models](https://eos.org/research-spotlights/machine-learning-improves-weather-and-climate-models). Accessed July 27, 2021

[6] [Kashyap, P. et al. 2020. Intelligent Weather Forecasting using Machine Learning Techniques](https://www.irjet.net/archives/V7/i3/IRJET-V7I3499.pdf)

[7] [Aviation Weather Forecast Market](https://www.stratviewresearch.com/367/Aviation-Weather-Forecasting-Services-Market.html). Accessed July 26, 2021

[8] [Weather Forecast Systems Market](https://www.marketsandmarkets.com/Market-Reports/meteorological-weather-forecasting-systems-market-29645152.html).  Accessed July 26, 2021

[9] [Faulty Weather Forecasts Are a Climate Crisis Disaster](https://www.wired.com/story/bad-weather-forecasts-climate-crisis-disaster/ ). Accessed July 26, 2021

[10] [How Weather Forecasts Are Made](https://www.discovermagazine.com/planet-earth/how-weather-forecasts-are-made). Accessed July 26, 2021


![CDL Hackaton](img/cml_qml.PNG)
