# pyRevit Glue Calculator

A Python-based pyRevit automation tool for calculating solvent glue requirements
for piping systems directly from Autodesk Revit models.

The tool reads relevant pipe and fitting information from the Revit model,
groups compatible elements, calculates connection glue requirements, and
generates a summarized glue quantity report.

---

## Overview

The Glue Calculator was developed to automate the manual calculation of
solvent glue requirements for piping installations.

Instead of manually reviewing pipes, fittings, reducers, sockets, caps and
other piping components, the tool extracts the required information directly
from the Revit model.

The calculated results are presented in a structured table containing:

- System Type
- Description
- Diameter 1
- Diameter 2
- Diameter 3
- Glue per Connection 1
- Glue per Connection 2
- Glue per Connection 3
- Total Length
- Count
- Total Glue 1
- Total Glue 2
- Total Glue 3
- Total Net Glue

The report also calculates:

- Total glue required
- Additional 10% allowance
- Gross total glue required

---

## Key Features

### 1. Automatic Revit Model Extraction

The tool reads piping elements directly from the active Revit model.

It can process relevant:

- Pipes
- Pipe fittings
- Reducers
- Sockets
- Caps
- Bends
- Other supported piping components

---

### 2. Diameter-Based Glue Calculation

The calculator identifies pipe/fitting diameters and applies the
corresponding glue quantity.

Multiple diameter values can be handled for fittings such as reducers.

Example:

```text
Dia 1
Dia 2
Dia 3
