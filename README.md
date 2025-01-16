This repository contains scripts that automatically retrieve information from the most recent sources for the Sustainable Wage Tool.

Read the project's documentation [here](https://angelfebles.github.io/Sustainable-Wage-Tool-APIs/en/index.html).


Sources:

Housing Cost API: https://www.huduser.gov/portal/dataset/fmr-api.html

Food Plan List: https://www.fns.usda.gov/cnpp/usda-food-plans-cost-food-monthly-reports

Self Sufficiency Standard: https://selfsufficiencystandard.org/Wisconsin/

Job Salary Data: https://download.bls.gov/pub/time.series/oe/

Job Educational Requirements: https://www.bls.gov/emp/tables/education-and-training-by-occupation.htm


The project expects a file named "credentials.py" under the root directory of the project. 

This file should have the string variable APIKEYHOUSING, which contains your Huduser API key. This is used to retrieve housing cost data. Refer to the [Housing Cost API](https://www.huduser.gov/portal/dataset/fmr-api.html) source mentioned above to learn how to create an API key.



Before running the project, make sure to install the required dependecies. Run this command in the project's root folder:

```
pip install -r requirements.txt
```

This project uses argparse for county lookup. To initialize project, run from the command line in the root directory:

```
python src/sustainable_wage_tool_data "county name"
```

Example: 

```
python src/sustainable_wage_tool_data "racine"
```



Upon execution, project will output two files:

1) dataOutput.xlsx contains the following sheets:

    Housing_lookup  --- Costs for each housing plan\
    Self_Sufficiency_Standard --- Self Sufficiency Standard data\
    Food_lookup --- Costs for each food plan, divided by age and gender\
    Food_means --- Average costs for each food plan, divided by age\ group (Adult, Infant, Preschooler, School Age, Teenager)\
    Monthly Budget --- Addition of all the previous costs to determine the monthly budget according to family size\


2) jobData.xlsx contains the following sheets:

    Job_Data --- Misc data for each job (annual wage, hourly wage, number of jobs available, ...)\
    Education_Requirements --- Educational requirements for each job