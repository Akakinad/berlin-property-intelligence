
# 🏙️ Berlin Property Intelligence

**End-to-end data analytics and machine learning project analyzing Berlin's property market through the lens of crime statistics, demographics, and pricing data.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![ML](https://img.shields.io/badge/ML-Scikit--learn-yellow.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

---

## 📊 Project Overview

This project demonstrates a complete data science workflow, from data integration to machine learning deployment, answering the critical question: **"How do crime rates influence property prices in Berlin, and where are the best investment opportunities?"**

### 🎯 Business Problem

Real estate investors need comprehensive intelligence combining:
- **Safety metrics** (crime rates, trends, severity)
- **Property valuations** (land prices by district)
- **Market segmentation** (identifying similar neighborhoods)
- **Predictive analytics** (price forecasting)

### 💡 Key Findings

1. **Location > Safety**: Central location (45% importance) outweighs safety (25%) in Berlin pricing
2. **Weak correlation**: Crime and price show only -0.128 correlation (other factors dominate)
3. **Best value cluster**: 7 middle-market districts offer €606/sqm with moderate safety (STRONG BUY)
4. **Premium justified**: Mitte (72/100 safety score) commands €2,585/sqm premium
5. **Urban prestige paradox**: Friedrichshain expensive (€2,380/sqm) despite high crime

---

## 🗂️ Project Structure
```
berlin-property-intelligence/
├── database/
│   ├── berlin_intelligence.db       # Integrated SQLite database
│   ├── crime_statistics.csv         # 28,390 crime records (2015-2024)
│   ├── district_population.csv      # Demographics for 12 districts
│   └── land_prices.csv              # 16,826 residential land valuations
├── notebooks/
│   ├── 01_Crime_Statistics_EDA.ipynb
│   ├── 02_Crime_Per_Capita_Analysis.ipynb
│   ├── 03_Crime_vs_Property_Price_Correlation.ipynb
│   ├── 04_ML_Property_Price_Prediction.ipynb
│   ├── 05_Safety_Scoring_System.ipynb
│   └── 06_ML_Neighborhood_Clustering.ipynb
└── README.md
```

---

## 📚 Analysis Pipeline (6 Notebooks)

### **Phase 1: Exploratory Data Analysis**

#### 📓 Notebook 01: Crime Statistics EDA
**Objective**: Understand Berlin's crime landscape

- **Techniques**: Data profiling, distribution analysis, temporal trends
- **Key Findings**:
  - 28,390 crime incidents across 12 districts (2015-2024)
  - Top crime types: Damage to property, theft, fraud
  - Temporal patterns: Higher crime in summer months
- **Skills**: Pandas, data cleaning, visualization

#### 📓 Notebook 02: Per Capita Analysis (Critical Thinking Showcase)
**Objective**: Normalize crime by population (avoid misleading absolute numbers)

- **Techniques**: Per capita calculation, population weighting
- **Key Findings**:
  - **Mitte**: Lowest rate (170K per 100k) - Safest ✅
  - **Marzahn**: Highest rate (964K per 100k) - Most dangerous ❌
  - 8.1x variance between safest and most dangerous
- **Skills**: Statistical normalization, critical analysis

#### 📓 Notebook 03: Crime vs Property Price Correlation
**Objective**: Test hypothesis "Higher crime = Lower prices"

- **Techniques**: Pearson correlation, scatter plots, district-level aggregation
- **Key Finding**: 
  - Correlation: **-0.128 (weak negative)**
  - Conclusion: Crime explains only 1.6% of price variance
  - Other factors (location, prestige) dominate
- **Skills**: Correlation analysis, hypothesis testing

---

### **Phase 2: Machine Learning - Supervised Learning**

#### 🤖 Notebook 04: ML Property Price Prediction
**Objective**: Predict land prices using crime + demographics

**Models**:
- **Random Forest Regressor** (100 trees, max_depth=10)
- **XGBoost Regressor** (100 estimators, learning_rate=0.1)

**Features Engineered**:
1. `population_density` - Urban vs suburban indicator
2. `crime_category` - Low/Medium/High bins
3. `is_central` - Binary flag for premium districts
4. `safety_rank` - 1-12 ranking by crime rate
5. `gender_ratio` - Male/female demographic balance

**Results**:
| Model | Training R² | Test R² | RMSE | MAE |
|-------|------------|---------|------|-----|
| Random Forest | 0.95 | 0.85 | €150/sqm | €120/sqm |
| XGBoost | 0.92 | 0.87 | €140/sqm | €115/sqm |

**Feature Importance** (Random Forest):
1. `is_central`: 45% ⭐ Most important!
2. `safety_rank`: 25%
3. `crime_per_100k`: 15%
4. `population_density`: 10%

**Key Insight**: Central location is **1.8x more important** than safety in Berlin pricing!

**Skills**: Supervised ML, feature engineering, model comparison, cross-validation

---

### **Phase 3: Advanced Analytics**

#### 🎯 Notebook 05: Safety Scoring System
**Objective**: Create comprehensive 0-100 safety scores

**Methodology**: Multi-component scoring algorithm (40-30-20-10 weighting)

**Components**:
1. **Crime Rate (40%)**: Volume per 100k residents
2. **Crime Severity (30%)**: Average seriousness (1-5 scale)
3. **Crime Trend (20%)**: 2015→2024 improvement/worsening
4. **Crime Distribution (10%)**: Evenly spread vs concentrated

**Results**:
| District | Safety Score | Tier | Interpretation |
|----------|-------------|------|----------------|
| Mitte | 72/100 | ⭐⭐⭐ Safe | Excellent rate, perfect distribution |
| Steglitz-Zehlendorf | 66/100 | ⭐⭐ Moderate | Good overall, solid trend |
| Pankow | 64/100 | ⭐⭐ Moderate | Great trend (-20% crime) |
| Marzahn-Hellersdorf | 26/100 | ⭐ High Risk | Worst rate, poor distribution |

**Safety vs Price Correlation**: 0.298 (weak positive)
- Confirms: Location/prestige > safety in pricing

**Skills**: Algorithm design, feature engineering, normalization, business logic

---

#### 🤖 Notebook 06: ML Neighborhood Clustering
**Objective**: Automatically group similar districts using unsupervised ML

**Algorithm**: K-Means Clustering
- **Optimal K**: 3 (determined by Elbow Method + Silhouette Score)
- **Features**: crime_per_100k, avg_price, population, density
- **Preprocessing**: StandardScaler normalization

**Model Evaluation**:
- **Silhouette Score**: 0.298 (acceptable for overlapping real-world data)
- **Inertia**: 18.19
- **PCA Variance**: 83.8% explained in 2D (62.0% PC1 + 21.8% PC2)

**Clusters Discovered**:

| Cluster | Districts | Crime | Price | Strategy |
|---------|-----------|-------|-------|----------|
| **0: Affordable Suburbs** | 7 districts (58%) | 485K | €606/sqm | 🟢 STRONG BUY |
| **1: Premium Safe Core** | Mitte, Pankow | 292K | €1,724/sqm | 💎 HOLD/PREMIUM |
| **2: Urban Prestige Outliers** | Friedrichshain, Charlottenburg, Marzahn | 817K | €1,503/sqm | ⚠️ SPECULATIVE HOLD |

**Cluster Insights**:
- **Cluster 0** (BEST VALUE): 7 middle-market districts with moderate crime, affordable prices
- **Cluster 1** (PREMIUM): Mitte + Pankow justify high prices with safety (lowest crime)
- **Cluster 2** (OUTLIERS): Mixed group showing urban prestige premium (pay for location despite crime)

**Visualization**: PCA reduces 4D to 2D, showing clear cluster separation

**Skills**: Unsupervised ML, K-Means, hyperparameter tuning, PCA, silhouette analysis, heatmaps

---

## 🛠️ Technical Stack

**Languages & Tools**:
- **Python 3.11**: Core language
- **Jupyter Notebook**: Interactive analysis
- **SQLite**: Data integration and storage

**Data Science Libraries**:
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Visualization

**Machine Learning**:
- **Scikit-learn**: ML models, preprocessing, evaluation
  - RandomForestRegressor, XGBoostRegressor
  - KMeans, StandardScaler, PCA
  - train_test_split, cross_val_score, silhouette_score
- **XGBoost**: Gradient boosting

**Statistical Analysis**:
- **SciPy**: Statistical tests, coefficient of variation

---

## 🎓 Skills Demonstrated

### Data Engineering
- ✅ Multi-source data integration (crime, demographics, prices)
- ✅ SQL database design and querying
- ✅ Data cleaning and validation
- ✅ ETL pipeline implementation

### Exploratory Analysis
- ✅ Statistical profiling and normalization
- ✅ Per capita calculations
- ✅ Correlation analysis
- ✅ Critical thinking (questioning misleading metrics)

### Machine Learning
- ✅ **Supervised learning**: Random Forest, XGBoost regression
- ✅ **Unsupervised learning**: K-Means clustering
- ✅ Feature engineering (created 5 new features)
- ✅ Model evaluation (R², RMSE, MAE, silhouette score)
- ✅ Hyperparameter tuning (optimal K selection)
- ✅ Dimensionality reduction (PCA)
- ✅ Cross-validation for robustness

### Data Visualization
- ✅ Distribution plots, scatter plots, heatmaps
- ✅ PCA 2D cluster visualization
- ✅ Feature importance charts
- ✅ Multi-panel dashboards

### Business Translation
- ✅ Converting technical findings to actionable insights
- ✅ Investment strategy recommendations
- ✅ Risk-reward profiling by cluster
- ✅ Value vs premium market identification

---

## 💼 Business Impact & Recommendations

### Investment Strategy by Cluster

**🟢 STRONG BUY: Cluster 0 (Middle Market Suburbs)**
- **Districts**: Lichtenberg, Neukölln, Reinickendorf, Spandau, Steglitz-Zehlendorf, Tempelhof-Schöneberg, Treptow-Köpenick
- **Profile**: €606/sqm, 485K crime rate (moderate)
- **Rationale**: Best value for money - affordable with acceptable safety
- **Target**: First-time buyers, value investors, rental properties

**💎 HOLD/PREMIUM: Cluster 1 (Premium Safe Core)**
- **Districts**: Mitte, Pankow
- **Profile**: €1,724/sqm, 292K crime rate (lowest!)
- **Rationale**: Premium justified by safety and centrality
- **Target**: High net worth, risk-averse, wealth preservation

**⚠️ SPECULATIVE HOLD: Cluster 2 (Urban Prestige Outliers)**
- **Districts**: Friedrichshain-Kreuzberg, Charlottenburg-Wilmersdorf
- **Profile**: €2,095/sqm avg, high crime
- **Rationale**: Paying for location/culture/nightlife, NOT safety - volatile
- **Target**: Risk-tolerant, urban lifestyle enthusiasts, short-term rental

**🔴 AVOID: Marzahn-Hellersdorf**
- **Profile**: €319/sqm, 964K crime rate (EXTREME)
- **Rationale**: Value trap - cheapest for a reason
- **Risk**: Extreme crime risk not compensated by low prices

---

## 🚀 Future Enhancements

1. **Neighborhood-level clustering**: Extend from 12 districts to 166 neighborhoods
2. **Time-series forecasting**: Predict future crime and price trends
3. **Additional features**: Schools quality, transport accessibility, amenities
4. **Alternative algorithms**: DBSCAN, Hierarchical clustering comparison
5. **Interactive dashboard**: Streamlit deployment for real-time exploration
6. **API deployment**: REST API for programmatic access to predictions

---

## 📈 Project Metrics

- **Data Points**: 57,216 total records
  - Crime: 28,390 incidents
  - Prices: 16,826 land valuations
  - Demographics: 12 districts
- **Time Span**: 2015-2024 (9 years)
- **Geographic Coverage**: 12 Berlin districts, 166 neighborhoods
- **Analysis Notebooks**: 6 comprehensive notebooks
- **ML Models**: 3 (Random Forest, XGBoost, K-Means)
- **Lines of Code**: ~2,500+ across all notebooks

---

## 🎯 Key Takeaways for Investors

1. **Location dominates**: Central districts (Mitte, Friedrichshain) command premiums regardless of crime
2. **Safety premium exists**: But only 0.298 correlation with price (other factors matter more)
3. **Best value**: Middle-market suburbs (Cluster 0) offer €606/sqm with moderate safety
4. **Urban prestige effect**: Friedrichshain/Charlottenburg expensive despite high crime (lifestyle > safety)
5. **Avoid value traps**: Marzahn's low price (€319/sqm) doesn't compensate for extreme crime (964K rate)

---

## 📝 Documentation & Reproducibility

All analysis is fully reproducible:
- ✅ Complete data files included
- ✅ SQLite database with integration logic
- ✅ Step-by-step notebook execution
- ✅ Detailed markdown explanations
- ✅ Code comments and docstrings
- ✅ Visualizations embedded

---

## 👤 Author

**[Your Name]**
- GitHub: [@Akakinad](https://github.com/Akakinad)
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

---

## 📄 License

This project is open source and available for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- Berlin Open Data Portal for crime statistics
- Berlin Senate Department for demographics
- OpenStreetMap contributors for geographic data

---

*Last Updated: December 2024*

**⭐ If you found this project valuable, please consider starring the repository!**

