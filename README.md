# 🧮 pyRevit Glue Calculator

> 🚀 Automated piping glue quantity calculation directly from Autodesk Revit using Python and pyRevit.

---

## 📌 Overview

The **pyRevit Glue Calculator** is a BIM automation tool developed to automate the calculation of solvent glue requirements for piping installations.

Instead of manually checking pipes, fittings, reducers, sockets, caps and other piping components, the tool extracts relevant information directly from the Revit model and calculates the required glue quantity.

This helps reduce manual quantity take-off work and improves consistency in material estimation.

---

## ✨ Features

- 🔍 Extracts piping elements directly from the Revit model
- 📏 Reads pipe and fitting diameters
- 🔗 Calculates glue requirements based on connections
- 📐 Calculates total pipe length
- 🧩 Handles multiple diameters for fittings and reducers
- 📊 Groups similar piping components
- 🏗️ Supports system-wise calculations
- 🌎 Supports overall model calculations
- 🧮 Calculates total net glue requirement
- ➕ Adds 10% additional glue allowance
- 📋 Generates a structured calculation table

---

## 🏗️ Calculation Modes

### 🌎 Overall Model Calculation

Processes all supported piping elements in the Revit model and generates the overall glue requirement.

### 🔧 System-wise Calculation

Allows the user to select specific Revit system types and calculates glue requirements only for the selected systems.

This is useful when material quantities are required separately for different building services or systems.

---

## 📊 Output Data

The calculation table includes:

| Parameter | Description |
|---|---|
| System Type | Revit piping system type |
| Description | Element description |
| Dia 1 | Primary connection diameter |
| Dia 2 | Secondary connection diameter |
| Dia 3 | Third connection diameter |
| Glue / Conn 1 | Glue required for connection 1 |
| Glue / Conn 2 | Glue required for connection 2 |
| Glue / Conn 3 | Glue required for connection 3 |
| Total Length | Total pipe length in mm |
| Count | Number of elements |
| Total Glue 1 | Total glue for connection 1 |
| Total Glue 2 | Total glue for connection 2 |
| Total Glue 3 | Total glue for connection 3 |
| Total Net Glue | Total calculated glue requirement |

---

## 🧮 Calculation Logic

The basic workflow is:

```text
Revit Model
     ↓
Extract Piping Elements
     ↓
Identify Pipes & Fittings
     ↓
Read Diameters
     ↓
Identify Connections
     ↓
Apply Glue Quantity
     ↓
Calculate Element Total
     ↓
Group Similar Elements
     ↓
Generate Summary
     ↓
Calculate 10% Allowance
     ↓
Gross Glue Requirement

📐 Glue Calculation

For applicable connections, the tool calculates:

Glue per Connection × Number of Connections

The resulting quantities are accumulated to determine the total net glue requirement.

An additional 10% allowance is then applied:

Total Net Glue
      +
10% Additional Glue
      =
Gross Total Glue Required
🏢 BIM Automation Use Case

This project demonstrates how information already available inside a BIM model can be used for automated construction quantity calculations.

Instead of performing a manual take-off:

Revit Model
     ↓
BIM Data
     ↓
Python Automation
     ↓
Quantity Calculation
     ↓
Material Requirement
🛠️ Technologies
🏗️ Autodesk Revit
🐍 Python
⚙️ pyRevit
🔌 Revit API
📊 BIM Automation
📋 Requirements

Before using the tool, make sure you have:

Autodesk Revit
pyRevit
A Revit model containing the required piping information
🚀 Installation
Install pyRevit.
Clone or download this repository.
Add the pyRevit extension to your pyRevit extensions location.
Reload pyRevit.
Open the Glue Calculator from the Revit ribbon.
▶️ Usage
🌎 Overall Model
Open your Revit project.
Launch Glue Calculator.
Select Overall Model Glue Calculation.
Review the calculated quantities.
🔧 System-wise
Launch Glue Calculator.
Select System-wise Glue Calculation.
Select the required Revit system type.
Run the calculation.
Review the filtered results.
📸 Example

Add screenshots of the tool here.

📷 Revit Glue Calculator
📷 System Selection
📷 Calculation Results
🎯 Project Goals

The main goals of this project are:

🚀 Reduce manual BIM quantity take-off
⏱️ Save calculation time
📊 Improve quantity consistency
🏗️ Use Revit model data more effectively
🤖 Demonstrate practical BIM automation using Python
🔮 Future Improvements

Possible future enhancements include:

📊 Excel export
📄 PDF reporting
⚙️ User-configurable glue values
🎨 Improved UI
🔍 Advanced filtering
📈 Calculation history
🧩 Support for additional fitting types
⚡ Performance improvements for large Revit models
⚠️ Disclaimer

This tool is intended to assist with BIM-based quantity calculations.

Final quantities should always be checked against the project's approved specifications, manufacturer recommendations and construction requirements before procurement or site use.

👨‍💻 Author

Akshay
BIM Engineer | BIM Automation
