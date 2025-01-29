# Politicians doing business: Evidence from Mozambique


Politically exposed persons are linked to private firms in Mozambique since Independence. Through a generalized event study, it is shown that significant gains in company ownership and structural power are achieved by political officeholders, especially in joint-stock firms in business services, mining, and finance, indicating wealth accumulation as rentier-brokers.



## How to Run This Project on Your Personal Machine

To run this project on your personal machine, follow these steps:

1. **Clone this repository**:
    ```sh
    git clone https://github.com/yourusername/MozPolBiz.git
    cd MozPolBiz
    ```

2. **Store all data files in the `data` folder**:
    - Note: Proprietary files are not included in this repository. Ensure you have the necessary data files and place them in the appropriate subdirectories within the `data` folder.

3. **Create a Conda or virtual environment**:
    - Using Conda:
        ```sh
        conda create --name mozpolbiz python=3.12.3
        conda activate mozpolbiz
        ```
    - Using virtualenv:
        ```sh
        python -m venv mozpolbiz
        source mozpolbiz/bin/activate  # On Windows use `mozpolbiz\Scripts\activate`
        ```

4. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the necessary scripts**:
    - Execute the following scripts in order:
        ```sh
        python MozPolBiz/1_html_2_register.py
        python MozPolBiz/2_indie_vars_DBWHO.py
        python MozPolBiz/3_outcome_vars_DBWHO.py
        ```

By following these steps, you should be able to set up and run the project on your personal machine successfully.




## Project Organization

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>


```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         MozPolBiz and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── MozPolBiz   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes MozPolBiz a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

