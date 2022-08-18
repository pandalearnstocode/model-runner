```python
env:str = "dev"
country: str = "us"
brand: str = "skol" # "skol","all"
rc_level: str = "brand" # "imp", "portfolio"
year: int = 2020
period: str = "monthly" # "monthly", "quarterly"
period_value: int = 1 # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
```



* Check if data is present in local use local data.
* If data is not present, download it from blob.
* With parameter run model. Save model object. With hash upload in blob.
* Generate RC curve upload in blob and DB.
* Generate other outputs upload in blob and DB.

```bash
python app.py run-modelling --env develop --country us --brand skol --rc-level brand --year 2020 --period monthly --period-value 1 --commit-id 1
python app.py run-optimization --rc-id 1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1 --env develop
python app.py run-simulation --rc-id 1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1 --env develop
```
inputs:
country:
    description: 'Country for which model will be executed'
    required: true
brand:
    description: 'Brand from the above country: skol, all'
    required: true
rc_level:
    description: 'RC levels: brand, imp, portfolio'
    required: true
year:
    description: 'Model year'
    required: true
period:
    description: 'Model period: monthly, quarterly'
    required: true
period_value:
    description: 'Model period value: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12'
    required: true