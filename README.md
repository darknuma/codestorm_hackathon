# CODESTORM ELITE'S HACKATHON on AgriFinance: Data-Driven Access to Finance for Young Agripreneurs

## Overview

This project aims to bridge the finance gap in Nigerian agriculture by developing data-driven solutions to help young agripreneurs obtain access to affordable finance. By leveraging data analysis and predictive modeling, we create tools that help financial institutions assess the creditworthiness of young farmers and make informed lending decisions.

## Problem Statement

- Only 27% of rural adults in Nigeria have access to formal financial services
- Only 6% of young people (18-25) have access to business loans
- Agriculture employs 35% of Nigeria's workforce but contributes less than 25% to GDP
- Commercial banks consider agriculture "too risky" due to climate variability, land tenure issues, and lack of credit history

## Solution

Our solution combines data analysis, predictive modeling, and visualization to:

1. Identify creditworthy farmers through data-driven profiling
2. Predict repayment behavior and business success
3. Create tools for financial institutions to assess risk and make informed lending decisions

## Thoughts Process

For a more granular thinking towards the approach there are three markdowns (`CL.md`, `DS.md` and `GC.md`) that shows the thought to generating the data we needed in the master data, which incorporated different researches and macro/micro economic data from Nigeria Bureau Statistics their ***LSMS Integrated Surveys on Agriculture Nigeria General Household SurveyPanel*** report to generate a synthetic simulated data from existing data, the documentation shown in `MasterTD.md` you would find this files in `technical_docs/` directory

Check out `streamlit_app/model/model_report.md` for information on our credit-score worthiness model

## Project Structure

```.
├── data_assets/           # Raw and processed data files, data generated
├── data/                  # Data (contains master data, and other data)
├── streamlit_app/          # Streamlit app for Data Science and ML models 
├── main.py                # Main script
├── requirements.txt       # Project dependencies
├── technical_docs/        # Technical Documentation for generating data, focus on `MasterTD.md`
└── README.md             # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- UV package manager

### Installation and Running the Project

1; Install UV:

```bash
    pip install uv
```

2; Create and activate virtual environment:

```bash
    uv venv
    source .venv/bin/activate  # On Windows:.venv\Scripts\activate 
```

3; Install dependencies:

```bash
    uv pip install -r requirements.txt
```

4; Run the Generator Script

```bash
    uv run main.py  
    # or run
    uv run data_assets/data_gen.py
```

5; Run the Credit_Score Model

```bash
    streamlit run streamlit_app/app.py
```

## Data Strategy

Our analysis leverages multiple data sources to build comprehensive farmer profiles:

- Agricultural production data
- Climate and weather patterns
- Market price trends
- Farmer demographic information
- Historical loan repayment data

## Credit Scoring Model

We developed a predictive model that assesses:

- Farmer creditworthiness
- Business success probability or Farmer Business Viability
- Risk factors and mitigation strategies

## Analysis and Insights

Key findings from our data analysis:

1. [Insert key insights about farmer creditworthiness]
2. [Insert findings about successful farming practices]
3. [Insert risk assessment patterns]

## Architecture

The solution is built on a modular architecture:

1. Data Collection and Processing Layer
2. Analysis and Modeling Layer
3. Visualization and Reporting Layer
4. API and Integration Layer

## Future Enhancements

- Integration with mobile banking platforms
- Real-time market price tracking
- Weather prediction integration
- Blockchain-based smart contracts for loan management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Format your code with `ruff format .` and check `ruff check .`
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the APACHE License - see the LICENSE file for details.

## Related References

1. [Zolawest](https://techcabal.com/2024/02/20/zowasel-releases-alternative-credit-evaluation-scoring-system-to-link-smallholder-farmers-with-financial-institutions/): A Credit evaluation company
2. Scientific Papers:

   - [Agricultural credit constraints in smallholder farming in developing countries: Evidence from Nigeria](https://www.sciencedirect.com/science/article/pii/S2772655X2200012X#tbl0002)
   - Credit Worthiness and Loan Repayment Performance Among Farmer Cooperators In Owerri Agricultural Zone of Imo State, Nigeria by `Osondu, Charles Kelechi and Obike, Kingsley Chukwuemeka`.
   - [Credits seeking and sourcing for agribusiness firms in developing countries: An empirical review of Nigerian experience]( https://doi.org/10.30574/gscarr.2023.17.2.0432 )
   - Assessment of creditworthiness and repayment among bank of agriculture loan beneficiaries in Cross River State, Nigeria by `Nkem H. Justice, Atturo E O. and Nwagbo Kingsley`.

## Acknowledgments

- EFInA Access to Financial Services in Nigeria 2020 survey
- DataFest Africa
- RedTech Africa
