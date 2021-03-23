# ZwiftPower Power Meter vs. Smart Trainer analyzer

This is a Jupyter Notebook and python script for calculating the power reading difference between power meters and smart trainers. 

The script scrapes the [ZwiftPower](https://zwiftpower.com) for Power Analysis data. On this web page, users can upload dual-recorded data from their power meters (usually connected to their GPS head unit) and data recorded from their smart trainer (usually connected to a platform like [Zwift](https://zwift.com). For race that has been uploaded the script compares the best 300 seconds power from the two sources and calculates the difference.

I have chosen to run this script only selecting riders with a ZwiftPower Rank of less than 500 and, using the 300 second avg. power and only accepting data where the two sources are within 15 % of each other. The script will also only download data matching the regex dictionaries I have created, so a lot of data is discarded – feel free to improve the regexes (this is my first time writing a regex).

All data from my specific use case for this is available in the `.csv` and `.xslx` files. 

A live, interactive version is available at Binder ↓. Just follow the link, wait for the instace to load and open `zwiftpower-webscraping.ipynb`.  

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stalegjelsten/zwiftpower-power-data-analyzer/main)


# Results

I ran the script on March 23rd 2021, with a rider list downloaded on 2021-03-17. 

The table below shows the average diffrence between the 300 second power measured by the power meter and the smart trainer. A negeative number means that the smart trainer is reporting a higher power than the power meter. A positive number means that the power meter is reporting a higher value than the smart trainer. 

|     Smart trainer     | count | avg. diff. PM-ST 300sec pwr |
|-----------------------|-------|-----------------------------|
| bkool_classic         |     2 |                      -38.50 |
| bkool_smart_pro       |    17 |                      -21.29 |
| elite_direto          |  1808 |                       -3.01 |
| elite_direto_2        |   128 |                        0.78 |
| elite_direto_x        |   873 |                       -1.51 |
| elite_direto_xr       |   772 |                       -1.97 |
| elite_drivo           |   647 |                       -0.90 |
| elite_drivo_2         |   703 |                        2.03 |
| elite_muin            |    22 |                        1.73 |
| elite_suito           |   561 |                       -1.13 |
| kinetic_rock_and_roll |     2 |                        0.50 |
| saris_h2              |   428 |                       -2.10 |
| saris_h3              |  3001 |                        3.16 |
| saris_hammer          |   550 |                        2.22 |
| saris_m2              |     5 |                        0.20 |
| saris_magnus          |    43 |                       -1.79 |
| tacx_bushido          |     1 |                       24.00 |
| tacx_flux             |   255 |                        5.99 |
| tacx_flux_2           |   198 |                        6.17 |
| tacx_flux_s           |   570 |                        1.55 |
| tacx_genius           |   113 |                      -17.72 |
| tacx_neo              |  2847 |                        3.53 |
| tacx_neo_2            |   229 |                        4.97 |
| tacx_neo_2t           |  2654 |                        6.17 |
| tacx_satori           |     3 |                        1.33 |
| tacx_vortex           |    94 |                       -4.57 |
| wahoo_kickr           | 12796 |                        2.23 |
| wahoo_kickr_bike      |  1052 |                       -2.83 |
| wahoo_kickr_core      |  4953 |                       -2.55 |
| wahoo_kickr_snap      |   124 |                        1.82 |
| wattbike_atom         |   293 |                        1.48 |
| Total	                | 35744 |                        1.22 |

The table below is grouped by power meter brands. The data is 300 seconds max average power measured at both the power meter (PM) and smart trainer (ST). 


| Power meter brand | count | avg. diff. PM-ST 300sec pwr |
|-------------------|-------|-----------------------------|
| 4iiii             |  2165 |                        0.50 |
| dura_ace          |   186 |                       -1.01 |
| favero            | 11731 |                        1.16 |
| giant_power       |   161 |                        5.68 |
| infocrank         |   508 |                        4.14 |
| pioneer           |   431 |                       -2.96 |
| power2max         |  2252 |                        1.94 |
| powertap          |  1147 |                       -2.66 |
| quarq             |  6537 |                        4.79 |
| rotor             |  1037 |                        3.30 |
| sram_axs          |    49 |                       18.10 |
| srm               |   976 |                        0.32 |
| stages            |  3657 |                       -1.99 |
| vector            |  4836 |                       -0.50 |
| xcadey            |    71 |                       -0.96 |
| Total             | 35744 |                        1.22 |


## Discussion


Both the power meter and smart trainer can give incorrect power values, but comparing the differences between the two, using a large enough sample size, could give us some insight as to which smart trainers overestimate and underestimate the effort.

Almost every smart trainer and power meter are (on average) in quite close agreement. The average power measured by the power meters is 337 W for the data set, and the majority of the smart trainers are within 1 % of that power. 
Because of friction losses in the drivetrain, the power measured at the back wheel (or the smart trainer) *should* be less than the power measured at the cranks or pedals. A couple of notes:

- The Kickr Core, Kickr Bike and Elite Direto seem to overestimate the effort. In the case of the Kickr Core, we even have quite a large sample size to verify this fact.
- The Tacx Neo-line, the Saris H-line and Wahoo Kickr-line all seem to underestimate the effort by approx. 1–2 %. These are premium trainers and we expect them to read a bit lower than the power meters. It is also possible to speculate that riders using these trainers have invested in good quality power meters as well.
- The Tacx Genius, Tacx Vortex and the Bkool line of trainers all seem to be quite inaccurate. 

## Conclusion

Using group averages, different models of smart trainers (especially direct drive smart trainers) seem to be within 1-2 % of the actual power. Using a specific type of smart trainer (or even better: The Kickr Bike) might earn you about 5 W FTP.
