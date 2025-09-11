# Seasonal-Forecast-Agriculture-Advisory-System-




---

# 🌾 Seasonal Weather Forecasting & Agriculture Advisory System

A **Python CLI-based simulation project** for seasonal weather forecasting and agricultural advisory.
This system provides two roles: **Admin** and **Farmer**. Admins can manage forecasts, advisories, and farmer queries, while Farmers can access weather data, receive crop advisories, and request personalized guidance.

Data is stored in **JSON** with full **CRUD (Create, Read, Update, Delete)** functionality.

---

## 🚀 Features

### 👨‍💼 Admin Functionalities

* Login as Admin
* Manage **Seasonal Forecasts** (Add / Update / Delete)
* Upload bulk climate datasets (**CSV/JSON**)
* Manage **Crop Advisories** (crop type, season, practices, fertilizer use, precautions)
* Generate **Reports** (forecast summaries, advisories by region/crop)
* Respond to **Farmer Queries** (approve/reject advisory requests)

### 👩‍🌾 Farmer Functionalities

* Register as a new Farmer (name, age, location, contact, crops grown)
* Login with Farmer ID
* View **Seasonal Weather Forecasts** (region-wise)
* Access **Crop Advisories** (crop-specific recommendations)
* Search **Historical Forecast/Advisory Data**
* Submit a query/request for personalized advisory
* Manage Profile (update details, crops grown)
* Logout

---

## 📂 Data Storage

Data is persisted in **JSON/CSV files**:

| File              | Fields                                                                                |
| ----------------- | ------------------------------------------------------------------------------------- |
| `forecasts.json`  | forecast\_id, region, season, rainfall\_mm, avg\_temp, expected\_events, issued\_date |
| `advisories.json` | advisory\_id, crop, season, practices, fertilizer, precautions                        |
| `farmers.json`    | farmer\_id, name, age, location, contact, crops                                       |
| `queries.json`    | query\_id, farmer\_id, crop, issue, status, response                                  |
| `reports.json`    | report\_id, admin\_id, type, parameters, generated\_on                                |

---

## 🛠 Tech Stack

* **Python 3.x**
* Libraries:

  * `json` → storage
  * `tabulate` → table display
  * `datetime` → dates & seasonal calculations
 

---

## 🖥 Sample CLI Flow

```text
=== Seasonal Forecast & Agriculture Advisory System ===
1. Admin Login
2. Farmer Login
3. Register as New Farmer
4. Exit
```

### Admin Menu

```text
--- Admin Menu ---
1. Add Seasonal Forecast
2. Update/Delete Forecast
3. Manage Crop Advisories
4. Upload Bulk Forecast Data
5. Generate Reports
6. Manage Farmer Queries
7. Logout
```

### Farmer Menu

```text
--- Farmer Menu ---
1. View Seasonal Forecast
2. Access Crop Advisories
3. Search Historical Data
4. Submit Query/Request Advisory
5. Manage Profile
6. Logout
```

---


🔗 Public sources:

* [IMD (Indian Meteorological Department)](https://mausam.imd.gov.in/)
* [FAO crop advisory datasets](https://www.fao.org/)
* [Kaggle agriculture & climate datasets](https://www.kaggle.com/datasets)


---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ojasjog/seasonal-forecast-advisory.git
cd seasonal-forecast-advisory
```

### 2. Install Dependencies

```bash
pip install tabulate 
```

### 3. Run the Program

```bash
python main.py
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.



---


