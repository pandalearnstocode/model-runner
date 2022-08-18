```python
env:str = "develop"
country: str = "us"
brand: str = "skol" # "skol","all"
rc_level: str = "brand" # "imp", "portfolio"
year: int = 2020
period: str = "monthly" # "monthly", "quarterly"
period_value: int = 1 # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
```

# __Model trigger using GitHub actions workflow dispatcher + API__

Here we will run model in github action using two methods,

* Workflow dispatcher
* GitHub API

While executing the model following things will happen,

* Check if data is present in local (File share attached to the AKS used as github action runner) use local data.
* If data is not present, download it from blob in attached file share.
* With parameter from API payload or workflow dispatcher run model using a typer cli app. Pass all the required parameters in the CLI app.
* Save model object in file share after training `model.pickle`. Upload the same in blob.
* Generate RC and other output files. Save them in attached file share. Upload them in blob.
* Update a DB table with all the unique identifiers.
* Once RC & other files are validated someone needs to get info from the DB related to the model. Write a azure functions which will take these parameters and will update the application DB. Someone needs to trigger the function and DB will be updated from Blob.
* Rest of the flow of the application remains as is.

## __Parameters:__

```yaml
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
```

Other two parameters are:

* branch name/ env name
* commit hash/commit id

__Note:__ `data_hash/data_id` has to be derived using all the datasets.

## __Workflow Trigger:__

* [Model Trigger](https://github.com/pandalearnstocode/model-runner/actions/workflows/model-trigger.yml)

## __Running the CI application:__

Runt the below commands to execute `model`, `optimization` and `simulation`.

```bash
python app.py run-modelling --env develop --country us --brand skol --rc-level brand --year 2020 --period monthly --period-value 1 --commit-id 1
python app.py run-optimization --rc-id 1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1 --env develop
python app.py run-simulation --rc-id 1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1 --env develop
```

__Note:__ `1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1` this value refers a unique identifier for the model or a response curve.