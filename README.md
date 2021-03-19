# ZwiftPower Power Meter vs. Smart Trainer analyzer

Jupyter Notebook for analyzing the power reading difference between power meters and smart trainers. 

My specific use case is to compare Tacx Neo generation 1 vs Wahoo Kickr smart trainers, but the script can be "easily" modified to investigate other correlations.

A live, interactive version is available at Binder ↓. Just follow the link, wait for the instace to load and open `zwiftpower-webscraping.ipynb`.  

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stalegjelsten/zwiftpower-power-data-analyzer/main)


# Results

The table below shows the average 300 second power for riders riding with the Tacx Neo gen 1 and any Wahoo Kickr smart trainer.

|  ST brand   | PM avg. 300s | ST avg. 300s | avg. diff. | samples |
|-------------|-------------:|-------------:|-----------:|--------:|
| Tacx Neo 1  |       328.30 |       324.96 |       3.34 |    3234 |
| Wahoo Kickr |       340.37 |       339.34 |       1.03 |   19886 |
| Total       |        338.7 |        337.3 |       1.35 |   23100 |

The table below is grouped by power meter brands. The data is 300 seconds max average power measured at both the power meter (PM) and smart trainer (ST). 

|  pm_brand  |  p300s_pm  |  p300s_st  |   delta   |
|------------|-----------:|-----------:|----------:|
|  4iiii     | 339.289683 | 338.875000 |  0.414683 |
|  favero    | 326.360698 | 324.983005 |  1.377693 |
|  power2max | 340.707384 | 339.694962 |  1.012422 |
|  powertap  | 338.682836 | 340.483209 | -1.800373 |
|  quarq     | 359.088099 | 354.360124 |  4.727975 |
|  rotor     | 371.545455 | 369.742657 |  1.802797 |
|  srm       | 351.996694 | 350.795041 |  1.201653 |
|  stages    | 336.225434 | 337.524360 | -1.298927 |
|  vector    | 335.530079 | 335.556892 | -0.026813 |


## Discussion

Analyzing the 300s average power of every Zwiftpower rider with a rank of less than 500 indicates that both the Tacx Neo gen 1 and the Wahoo Kickr series of smart bike trainers underestimate the power output by a very small amount. Because of friction losses in the drivetrain, the power measured at the back wheel (or the smart trainer in our case) *should* be less than the power measured at the cranks or pedals. 

The Tacx Neo generation 1 underestimate the power by 3.34 W, while the Wahoo Kickr line underestimate the power by 1.03 W.

