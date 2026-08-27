# -*- coding: utf-8 -*-
__doc__     = """Version = 2.0
Date    = 08.08.2025
________________________________________________________________
Description:

Use it for Glue Calculation
________________________________________________________________
How-To:

1. Press Glue Calculator
2. Select whether you want glue calculation for all model elements or required system.
3. For system-Wise you can select more than one system at a time for glue amount.
4. To filter out any systems use search bar and then unselect those systems.
________________________________________________________________
Last Updates:
- [08.12.2025] v2.0 Count for Pipes Wasnt right but now its corrected 
- [08.08.2025] v1.5 Added Checkmarks to select required system types
- [08.08.2025] v1.0 Added extra 10 % in net glue calculation
- [08.07.2025] v0.5 Total model elements with System vise elements
- [08.06.2025] v0.1 Basic Tool
________________________________________________________________
Author: Akshay Pawar

import re
import math
from math import ceil
from collections import OrderedDict
from pyrevit import revit, forms, script
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ElementCategoryFilter,
    LogicalOrFilter,
    BuiltInCategory,
    UnitUtils,
    BuiltInParameter,
    SpecTypeId,
    UnitTypeId
)

doc = revit.doc
output = script.get_output()

# --- Glue consumption per diameter (mm -> grams) ---
glue_table = {
    '25': 4, '32': 6, '40': 7, '50': 9, '63': 11, '75': 17, '90': 23,
    '110': 31, '125': 35, '160': 62, '200': 91, '250': 128, '315': 182, '400': 308
}

# Helper: get diameter string from a parameter
def get_dia_str_from_param(param):
    if not param:
        return ""
    try:
        val = param.AsDouble()
        if val is not None:
            mm = int(round(UnitUtils.ConvertFromInternalUnits(val, UnitTypeId.Millimeters)))
            return str(mm)
    except Exception:
        pass
    try:
        vs = param.AsValueString()
        if vs:
            m = re.search(r'\d+', vs)
            if m:
                return m.group(0)
    except Exception:
        pass
    return ""

# Helper: get numeric length in mm
def get_length_mm(elem):
    try:
        p = elem.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)
        if p and p.AsDouble() is not None:
            return UnitUtils.ConvertFromInternalUnits(p.AsDouble(), UnitTypeId.Millimeters)
    except Exception:
        pass
    try:
        p2 = elem.LookupParameter("Length")
        if p2 and p2.AsDouble() is not None:
            return UnitUtils.ConvertFromInternalUnits(p2.AsDouble(), UnitTypeId.Millimeters)
    except Exception:
        pass
    return 0.0

# Collect fittings, accessories, and pipes
filters = [
    ElementCategoryFilter(BuiltInCategory.OST_PipeFitting),
    ElementCategoryFilter(BuiltInCategory.OST_PipeAccessory),
    ElementCategoryFilter(BuiltInCategory.OST_PipeCurves)
]
collector = FilteredElementCollector(doc).WhereElementIsNotElementType().WherePasses(LogicalOrFilter(filters))

# Ask mode
mode = forms.alert(
    "What do you want to calculate?",
    options=["Overall Material Glue Calculation", "System-wise Glue Calculation"]
)
if not mode:
    script.exit()

# Gather system types
system_types = set()
for el in collector:
    sp = el.LookupParameter("System Type")
    if sp and sp.HasValue:
        system_types.add(sp.AsValueString())

if not system_types:
    forms.alert("No system types found. Exiting.")
    script.exit()

# Filter by selected systems if user chose system-wise
if mode == "System-wise Glue Calculation":
    selected_systems = forms.SelectFromList.show(
        sorted(system_types),
        title="Select System Type(s) to Calculate Glue",
        button_name="Calculate",
        multiselect=True
    )
    if not selected_systems:
        script.exit()
    filtered_elements = [el for el in collector if el.LookupParameter("System Type") and el.LookupParameter("System Type").AsValueString() in selected_systems]
else:
    selected_systems = None
    filtered_elements = list(collector)

# Grouping dictionary
grouped = OrderedDict()

for el in filtered_elements:
    cat_name = el.Category.Name if el.Category else ""
    sys_param = el.LookupParameter("System Type")
    sys_type = sys_param.AsValueString() if sys_param and sys_param.HasValue else "N/A"

    # Description: for pipes, read from type
    desc = "N/A"
    try:
        if cat_name == "Pipes":
            type_el = doc.GetElement(el.GetTypeId())
            if type_el:
                dp = type_el.LookupParameter("Description (English)")
                if dp and dp.HasValue:
                    desc = dp.AsString()
        else:
            dp = el.LookupParameter("Description (English)")
            if dp and dp.HasValue:
                desc = dp.AsString()
    except Exception:
        desc = "N/A"

    dia1 = dia2 = dia3 = ""
    glue1 = glue2 = glue3 = 0
    total_length_mm = 0.0
    elem_count_for_group = 0  # will be updated later for Pipes

    # Pipes logic
    if cat_name == "Pipes":
        dia_param = el.LookupParameter("Diameter") or el.get_Parameter(BuiltInParameter.RBS_PIPE_DIAMETER_PARAM)
        dia1 = get_dia_str_from_param(dia_param) if dia_param else ""
        if dia1:
            glue1 = glue_table.get(dia1, 0)
        length_mm = get_length_mm(el)
        total_length_mm = length_mm if length_mm else 0.0
        # ⬇️ Do NOT set count here — will calculate later after grouping total length
        elem_count_for_group = 0
    else:
        d1p = el.LookupParameter("d1")
        d2p = el.LookupParameter("d2")
        if d1p and d1p.HasValue and d2p and d2p.HasValue:
            dia1 = get_dia_str_from_param(d1p)
            dia2 = dia1
            dia3 = get_dia_str_from_param(d2p)
            glue1 = glue_table.get(dia1, 0)
            glue2 = glue_table.get(dia2, 0)
            glue3 = glue_table.get(dia3, 0)
            elem_count_for_group = 1
        else:
            p1 = el.LookupParameter("NLRS_P_c01_diameter")
            p2 = el.LookupParameter("NLRS_P_c02_diameter")
            dia1 = get_dia_str_from_param(p1) if p1 else ""
            dia2 = get_dia_str_from_param(p2) if p2 else ""
            glue1 = glue_table.get(dia1, 0)
            glue2 = glue_table.get(dia2, 0)
            elem_count_for_group = 1

    if not (glue1 or glue2 or glue3):
        continue

    key = (sys_type, desc, dia1, dia2, dia3)
    if key not in grouped:
        grouped[key] = {
            "system": sys_type,
            "desc": desc,
            "dia1": dia1,
            "dia2": dia2,
            "dia3": dia3,
            "glue1_per_unit": glue1,
            "glue2_per_unit": glue2,
            "glue3_per_unit": glue3,
            "count": 0,
            "total_length_mm": 0.0,
            "is_pipe": (cat_name == "Pipes")
        }

    grouped[key]["count"] += elem_count_for_group
    grouped[key]["total_length_mm"] += total_length_mm

# Sort
def safe_int_val(v):
    try:
        return int(v) if v != "" else 99999
    except Exception:
        return 99999

sorted_items = sorted(grouped.values(), key=lambda x: (x["system"], x["desc"], safe_int_val(x["dia1"])))

header = [
    "System Type", "Description", "Dia 1", "Dia 2", "Dia 3",
    "Glue per Connection 1", "Glue per Connection 2", "Glue per Connection 3",
    "Total Length (mm)", "Count",
    "Total Glue for Dia1", "Total Glue for Dia2", "Total Glue for Dia3",
    "Total Net Glue (g)"
]

table = []
grand_total = 0

for rec in sorted_items:
    # ⬇️ Calculate count for pipes now based on total length
    if rec["is_pipe"]:
        rec["count"] = int(ceil(rec["total_length_mm"] / 5000.0)) if rec["total_length_mm"] > 0 else 0

    count = rec["count"]
    glue1_total = rec["glue1_per_unit"] * count if rec["glue1_per_unit"] else 0
    glue2_total = rec["glue2_per_unit"] * count if rec["glue2_per_unit"] else 0
    glue3_total = rec["glue3_per_unit"] * count if rec["glue3_per_unit"] else 0
    total_net = glue1_total + glue2_total + glue3_total
    grand_total += total_net

    table.append([
        rec["system"],
        rec["desc"],
        rec["dia1"],
        rec["dia2"],
        rec["dia3"],
        rec["glue1_per_unit"] if rec["glue1_per_unit"] else "",
        rec["glue2_per_unit"] if rec["glue2_per_unit"] else "",
        rec["glue3_per_unit"] if rec["glue3_per_unit"] else "",
        int(round(rec["total_length_mm"])) if rec["total_length_mm"] > 0 else "",
        count,
        glue1_total if glue1_total else "",
        glue2_total if glue2_total else "",
        glue3_total if glue3_total else "",
        total_net
    ])

if not table:
    forms.alert("No valid elements found.")
    script.exit()

# Add TOTAL summary row inside the table
table.append([
    "**TOTAL**", "", "", "", "",
    "", "", "",
    "", "", "", "", "",
    grand_total
])

# Print Table
output.print_table(table, columns=header)

# Glue totals
additional_glue = round(grand_total * 0.10, 2)
gross_total = round(grand_total + additional_glue, 2)

output.print_md("**TOTAL GLUE REQUIRED:** {} grams".format(grand_total))
output.print_md("**10% Additional Glue:** {} grams".format(additional_glue))
output.print_md("**GROSS TOTAL GLUE REQUIRED:** {} grams".format(gross_total))
