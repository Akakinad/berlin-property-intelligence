
# 🏙️ Berlin Property Intelligence System

> A comprehensive data analysis project integrating crime statistics, demographics, and real estate data to provide intelligent property investment insights for Berlin.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

This project analyzes **45,000+ data points** across multiple Berlin datasets to answer critical questions for property investors:

- 🔍 **Which districts are safest?**
- 💰 **Does safety correlate with property prices?**
- 🏠 **Where are the best value investment opportunities?**
- 📈 **How have crime trends evolved over 10 years?**

### Key Achievement: The Per Capita Discovery

Through rigorous analysis, this project uncovered that **absolute crime numbers were misleading** - proper statistical normalization revealed Mitte as Berlin's safest district, not the most dangerous as raw numbers suggested. This demonstrates critical thinking and proper data methodology.

---

## 📊 Key Findings

### 🚨 Crime Analysis
- **28,390 crime records** analyzed (2015-2024)
- **12 Berlin districts** comprehensively evaluated
- **166 neighborhoods** mapped for granular insights
- **5.7x crime rate variance** between safest and most dangerous districts

### 💡 Major Insights

| Finding | Impact |
|---------|--------|
| **Mitte is Safest** | 170,247 crimes per 100k residents (despite appearing dangerous in raw numbers) |
| **Marzahn-Hellersdorf Most Dangerous** | 964,332 crimes per 100k residents |
| **Location > Safety in Pricing** | Weak correlation (-0.128) shows prestige trumps crime in Berlin real estate |
| **8.1x Price Variance** | €319/sqm (Marzahn) to €2,585/sqm (Mitte) |

### 💰 Investment Intelligence

**Best Value Opportunities** (Safe + Affordable):
- 🟢 **Treptow-Köpenick**: €462/sqm + 376K crime rate per 100k
- 🟢 **Spandau**: €484/sqm + 424K crime rate per 100k

**Premium Districts** (Safe + Expensive - Justified):
- 💎 **Mitte**: €2,585/sqm + 170K crime rate per 100k
- 💎 **Steglitz-Zehlendorf**: €877/sqm + 341K crime rate per 100k

**Surprising Finding**:
- ⚠️ **Friedrichshain-Kreuzberg**: 2nd most expensive (€2,380/sqm) BUT 2nd most dangerous (847K per 100k)
- **Insight**: Urban center prestige and culture override safety concerns in pricing

---

## 🗂️ Data Sources & Scale

| Dataset | Records | Coverage | Source |
|---------|---------|----------|--------|
| **Crime Statistics** | 28,390 | 2015-2024, 12 districts | Berlin Police Department |
| **Population Data** | 12 districts | 3.9M residents | Berlin Statistical Office |
| **Land Prices** | 16,826 zones | Residential valuations | Official Bodenrichtwert |

**Total Integrated Data Points**: 45,000+

---

## 📓 Analysis Notebooks

### 1️⃣ [Crime Statistics EDA](notebooks/01_Crime_Statistics_EDA.ipynb)
**Exploratory analysis of Berlin crime patterns**
- Crime distribution by district and neighborhood
- Temporal trends (2015-2024)
- Crime type analysis
- Geographic hotspot identification

### 2️⃣ [Crime Per Capita Analysis](notebooks/02_Crime_Per_Capita_Analysis.ipynb) ⭐
**The critical insight that changed everything**
- Absolute numbers vs per capita comparison
- Statistical normalization methodology
- Reveals Mitte as actually safest (not most dangerous)
- Demonstrates critical thinking and data quality awareness

**Key Visualization**:
> Before: Mitte had lowest absolute crime (675K) → Appeared safest ❌  
> After: Mitte had lowest per capita rate (170K per 100k) → Actually safest ✅

### 3️⃣ [Crime vs Property Price Correlation](notebooks/03_Crime_Property_Price_Analysis.ipynb) ⭐
**Comprehensive investment intelligence analysis**
- Scatter plots with regression analysis
- Investment quadrant matrix (4-quadrant risk/value analysis)
- Statistical correlation testing (Pearson r = -0.128)
- Business insights and recommendations

**Correlation Finding**: Weak negative correlation suggests **location and prestige dominate safety** in Berlin real estate pricing decisions.

---

## 🛠️ Technical Stack

### Core Technologies
```python
Python 3.11          # Primary language
SQLite               # Database management
Pandas               # Data manipulation
NumPy                # Numerical computing
Matplotlib/Seaborn   # Data visualization
Scipy                # Statistical analysis
Jupyter              # Interactive analysis
```

### Database Schema
```
berlin_intelligence.db
├── crime_statistics (28,390 records)
│   ├── district, district_id, neighborhood
│   ├── year, crime_type, category
│   └── total_cases, frequency_100k, severity
├── district_population (12 districts)
│   ├── district_id, total_population
│   └── demographics (age, gender, nationality)
└── land_prices (16,826 zones)
    ├── district_name, standard_land_value
    └── land_use_type, reference_date
```

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.11+
pip
virtualenv
```

### Installation
```bash
# Clone repository
git clone git@github.com:Akakinad/berlin-property-intelligence.git
cd berlin-property-intelligence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Set up database
python scripts/setup_database.py

# Load population data
python scripts/load_population_data.py

# Load real estate data
python scripts/load_real_estate_data.py
```

### Run Analysis
```bash
# Launch Jupyter
jupyter notebook

# Open any notebook in notebooks/ directory
# Run cells sequentially
```

---

## 📂 Project Structure
```
berlin-property-intelligence/
├── data/                           # Raw datasets (9 sources)
│   ├── crime_statistics/           # 28,390 crime records
│   ├── population_statistics/      # District demographics
│   ├── real_estate/               # 16,826 land valuations
│   ├── schools/                   # Educational facilities
│   ├── hospitals/                 # Healthcare facilities
│   ├── public_transport/          # Transit data
│   ├── recreational_zones/        # Parks & playgrounds
│   ├── districts_neighborhoods/   # Geographic boundaries
│   └── milieuschutz/             # Urban protection zones
├── database/                      # SQLite database
│   └── berlin_intelligence.db    # Integrated data
├── notebooks/                     # Analysis notebooks
│   ├── 01_Crime_Statistics_EDA.ipynb
│   ├── 02_Crime_Per_Capita_Analysis.ipynb
│   └── 03_Crime_Property_Price_Analysis.ipynb
├── scripts/                       # Automation scripts
│   ├── setup_database.py         # Database initialization
│   ├── load_population_data.py   # Population ETL
│   └── load_real_estate_data.py  # Real estate ETL
├── models/                        # ML models (planned)
├── docs/                          # Documentation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🎯 Methodology Highlights

### Statistical Rigor
- **Per Capita Normalization**: Crime rates calculated per 100,000 residents for fair comparison
- **Correlation Analysis**: Pearson correlation with p-value testing
- **Data Quality**: Identified and fixed SQL join bug (Cartesian product)

### Key Methodological Decisions
1. **Why Per Capita?** Absolute numbers favor smaller districts unfairly
2. **Residential Zones Only**: Focused on W-type land use for investment relevance
3. **District-Level Analysis**: Balanced granularity with statistical power
4. **10-Year Timeframe**: Captures long-term trends, not short-term fluctuations

---

## 📈 Business Insights & Recommendations

### For Property Investors

**🟢 Strong Buy - Best Value**
- Treptow-Köpenick, Spandau, Pankow
- **Strategy**: Safe neighborhoods with affordable entry points

**💎 Hold - Premium Justified**
- Mitte, Steglitz-Zehlendorf
- **Strategy**: Safety premium is justified, good long-term hold

**⚠️ Caution - Urban Risk Premium**
- Friedrichshain-Kreuzberg, Charlottenburg-Wilmersdorf
- **Strategy**: High prices despite crime - for risk-tolerant urban lifestyle seekers

**🔴 Avoid - High Risk, Low Value**
- Marzahn-Hellersdorf, Lichtenberg
- **Strategy**: Low prices don't compensate for high crime rates

### Key Takeaway
> **In Berlin, location and cultural prestige often trump safety in property pricing decisions.**

---

## 🚀 Future Roadmap

### Phase 3: Machine Learning (Next)
- [ ] Property price prediction model (Random Forest/XGBoost)
- [ ] Safety scoring algorithm (0-100 scale)
- [ ] Neighborhood recommendation engine
- [ ] Time series forecasting (crime trends)

### Phase 4: Additional Data Integration
- [ ] Schools quality and density
- [ ] Hospital accessibility
- [ ] Public transport connectivity
- [ ] Geospatial visualization (maps)

### Phase 5: Deployment
- [ ] Interactive dashboard (Streamlit/Plotly Dash)
- [ ] REST API for predictions
- [ ] Deploy to cloud (Heroku/AWS)

---

## 🎓 Skills Demonstrated

This project showcases:

✅ **Data Engineering**
- Database design and management (SQLite)
- ETL pipelines for multiple data sources
- Data cleaning and validation

✅ **Statistical Analysis**
- Per capita normalization
- Correlation analysis
- Hypothesis testing (p-values)

✅ **Critical Thinking**
- Questioned misleading initial results
- Identified need for population normalization
- Diagnosed SQL join bug (Cartesian product)

✅ **Data Visualization**
- Matplotlib, Seaborn for static plots
- Multi-panel comparative visualizations
- Investment quadrant matrices

✅ **Software Engineering**
- Git version control
- Virtual environments
- Modular, reusable code
- Documentation

✅ **Business Intelligence**
- Translating data insights to actionable recommendations
- Investment strategy formulation
- Risk-value trade-off analysis

---

## 📊 Sample Visualizations

### Crime Per Capita Rankings
Shows proper statistical comparison reveals true safety rankings.

### Crime vs Price Scatter Plot
Demonstrates weak correlation - location trumps safety in pricing.

### Investment Quadrant Matrix
4-quadrant risk/value analysis for investment decision-making.

*Full visualizations available in notebooks with outputs on GitHub*

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Shola Akinade**

- GitHub: [@Akakinad](https://github.com/Akakinad)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/your-profile) *(update with your LinkedIn)*
- Portfolio: Data Science & Analytics

---

## 🙏 Acknowledgments

- Berlin Police Department for crime statistics
- Berlin Statistical Office for population data
- Official Bodenrichtwert portal for land valuations
- Open Data Berlin initiative

---

## 📧 Contact

For questions, opportunities, or collaborations:
- Email: your.email@example.com *(update with your email)*
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

---

**⭐ If you found this project interesting, please star the repository!**

---

*Last Updated: December 2024 | Status: Active Development*
