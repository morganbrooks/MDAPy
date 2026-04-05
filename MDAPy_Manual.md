# MDAPy User Manual

MDAPy is a free, open-source Python application for calculating and comparing Maximum Depositional Ages (MDAs) from detrital zircon U-Pb geochronology data. This manual covers everything you need to get started and make the most of MDAPy's features.

For installation instructions, see the [README](README.md).

---

## Table of Contents

1. [Overview](#overview)
2. [Preparing Your Data](#preparing-your-data)
3. [Importing Data](#importing-data)
4. [Customizing Settings](#customizing-settings)
5. [Running Calculations](#running-calculations)
6. [Understanding Your Outputs](#understanding-your-outputs)
7. [MDA Method Reference](#mda-method-reference)
8. [Exporting Results](#exporting-results)
9. [Limitations](#limitations)

---

## Overview

MDAPy calculates 10 of the most commonly applied MDA methods simultaneously or individually for an unlimited number of samples. It accepts two types of detrital zircon U-Pb datasets and provides customized plots and summary tables for each calculation method.

**The 10 MDA methods available in MDAPy:**

| Method | Abbreviation |
|---|---|
| Youngest Single Grain | YSG |
| Youngest Grain Cluster at 1σ | YC1σ (2+) |
| Youngest Grain Cluster at 2σ | YC2σ (3+) |
| Youngest Three Zircons at 2σ | Y3Zo |
| Youngest Three Zircons | Y3Za |
| Youngest Statistical Population | YSP |
| Youngest Detrital Zircon | YDZ |
| Youngest Graphical Peak | YPP |
| Tau Method | τ |
| Maximum Likelihood Age | MLA |

---

## Preparing Your Data

MDAPy accepts two dataset types:

- **Ratio-based:** Measured ratios of ²³⁸U/²⁰⁶Pb and ²⁰⁷Pb/²⁰⁶Pb with associated uncertainties
- **Age-based:** Pre-calculated detrital zircon ages with associated uncertainties

### Download the Import Template

Before importing data, download the Excel import template directly from the **Input Data** panel within the application. There are two templates — one for ratio-based datasets and one for age-based datasets. Select the one that matches your data type.

### Fill in the Template

The import template contains two worksheets that must both be populated: **Samples** and **Data**.

**Samples worksheet:**
- List all unique sample names in your dataset
- Sample names must be alphanumeric (e.g., `A27`, `AB01`)
- Each sample name must be unique

**Data worksheet:**
- Enter the `Sample_ID` for each measurement — this must match exactly the names in the Samples worksheet
- Enter the associated ratios or ages and uncertainties for each grain measurement
- An unlimited number of samples and grain measurements can be included

---

## Importing Data

Once your template is filled in, open MDAPy in your browser at `http://localhost:8080` and navigate to the **Input Data** panel.

Before uploading, configure the following settings:

### Dataset Type
Select whether your data contains measured **ratios** (²³⁸U/²⁰⁶Pb, ²⁰⁷Pb/²⁰⁶Pb) or **pre-calculated ages**.

### Uncertainty Format
- Select **1σ or 2σ** to match the uncertainty level used in your dataset
- Select **percent (%)** or **absolute (ABS)** to match the uncertainty format

### Best Age Cut Off *(ratio datasets only)*
This setting determines the age at which MDAPy switches from using ²³⁸U/²⁰⁶Pb to ²⁰⁷Pb/²⁰⁶Pb ages. The default is **1.5 Ga**, which is appropriate for most datasets. ²⁰⁷Pb/²⁰⁶Pb dates are more reliable for older zircons (>1.5 Ga).

### Decay Constants *(ratio datasets only)*
Default values are pre-set from published standards. These can be edited if your dataset requires different values.

### Systematic Uncertainty *(ratio datasets only)*
Systematic uncertainty can be included in MDA calculations for seven methods (YSG, YC1σ, YC2σ, Y3Zo, Y3Za, YSP, τ). User inputs include:
- Long-term excess variance for ²³⁸U/²⁰⁶Pb and ²⁰⁷Pb/²⁰⁶Pb
- Calibration uncertainty for ²³⁸U/²⁰⁶Pb and ²⁰⁷Pb/²⁰⁶Pb
- Decay constant uncertainty for ²³⁸U and ²³⁵U

To exclude systematic uncertainty, enter zeros for all fields. Note: systematic uncertainty is not applied to MLA, YPP, or YDZ regardless of inputs.

### Upload Your File
Once all settings are configured, click **Import Data**. After importing, navigate to the **Inspect Dataset** tab to review your uploaded data and confirm it has loaded correctly before running calculations.

---

## Running Calculations

The **Run Analysis** panel displays a summary of your uploaded data including each sample name and sample size. From here you can select samples and choose one of three calculation options.

### Selecting Samples
- Use **Select All** to run all samples at once
- Or select individual samples from the list
- There is no maximum on the number of samples or individual sample size

### Calculation Options

#### Option 1: Calculate All MDA Methods and Plot
Calculates all 10 MDA methods simultaneously for each selected sample. Use this option to quickly compare all methods side by side.

**Outputs:**
- A summary table of all 10 calculated MDAs with 1σ absolute uncertainty, exportable as Excel
- A comparison plot for each sample showing all MDA results with 1σ/2σ uncertainty bars

#### Option 2: Calculate One MDA Method and Plot
Calculates a single MDA method, selected from the **Input Data** tab. Use this option for a detailed view of one method across your dataset.

**Outputs:**
- A summary table with the MDA, uncertainty, MSWD (where applicable), and number of grains used
- A customized plot for each sample specific to that MDA method

#### Option 3: Plot All Samples With One MDA Method
Plots the calculated MDAs for all samples using the selected method on a single stratigraphic plot. Use this option to visualize trends across your dataset.

**Outputs:**
- A stratigraphic plot with samples sorted ascendingly on a descending age scale

### Age Plotting Dimensions
Before running calculations, set the maximum age for plots in the **Age Plotting Dimensions** tab. This controls the age range displayed on output plots and prevents crowding when samples contain a wide range of grain ages.

---

## Understanding Your Outputs

### Summary Tables
All summary tables are exportable as Microsoft Excel files. Depending on the method, tables include:
- **MDA** — the calculated maximum depositional age in Ma
- **1σ uncertainty** — absolute uncertainty on the MDA
- **MSWD** — mean square weighted deviation (where applicable; see below)
- **n grains** — number of grains included in the MDA calculation (where applicable)

### MSWD
The MSWD is a measure of whether the scatter in a sub-sample of grains can be explained by measurement uncertainty alone.

- **MSWD < 1** — the dispersion of dates is consistent with measurement uncertainty; grains are likely the same true age
- **MSWD > 1** — the dispersion exceeds what measurement uncertainty would predict; grains may not be the same true age

The MSWD is reported for methods that calculate MDAs from a sub-sample of grains: YC1σ, YC2σ, Y3Zo, Y3Za, YSP, and τ.

### Plot Types
MDAPy generates four types of plots depending on the MDA method:

**Age plots** (YSG, YC1σ, YC2σ, Y3Zo, Y3Za, YSP) — detrital zircon dates sorted ascendingly with 1σ/2σ uncertainty bars. Grains selected for the MDA calculation are highlighted in red. The calculated MDA is shown as a horizontal dashed line.

**Frequency histogram** (YDZ) — displays the distribution of 10,000 youngest grains from the Monte Carlo simulation. The MDA (mode) is highlighted in red; upper and lower 2σ uncertainties are shown as black dashed lines.

**Probability density plots** (YPP, τ) — shows the probability density of the sample age distribution. The MDA is indicated by a vertical red line (YPP) or black dashed line (τ), with grains used in the τ calculation highlighted in red.

**Radial plot** (MLA) — displays ages versus measurement precision. The angular position of each point represents the date; horizontal distance from the origin represents precision. Useful for identifying younger and older age populations within the dataset.

### Stratigraphic Plot
The stratigraphic plot (Calculation Option 3) displays MDAs for all samples sorted in ascending order on a descending age scale, providing a stratigraphic representation of the dataset.

---

## MDA Method Reference

### YSG — Youngest Single Grain
Uses the single youngest detrital zircon grain and its uncertainty as the MDA. If the youngest grain has a 1σ uncertainty >10 Ma and overlaps within 1σ of the second-youngest grain, the second-youngest is substituted. Grains are sorted by their age plus 1σ uncertainty, so older, more precise grains may be selected over younger, less precise grains.

*Output: summary table + age plot*

---

### YC1σ (2+) — Youngest Grain Cluster at 1σ
Calculates the weighted mean age of the youngest two or more grains that overlap within 1σ uncertainty. The grain cluster is identified using the youngest grain cluster algorithm.

*Output: summary table (MDA, 1σ uncertainty, MSWD, n grains) + age plot*

---

### YC2σ (3+) — Youngest Grain Cluster at 2σ
Calculates the weighted mean age of the youngest three or more grains that overlap within 2σ uncertainty. The grain cluster is identified using the youngest grain cluster algorithm.

*Output: summary table (MDA, 1σ uncertainty, MSWD, n grains) + age plot*

---

### Y3Zo — Youngest Three Zircons at 2σ
Calculates the weighted mean age of the youngest three grains that overlap within 2σ uncertainty. The grain cluster is identified using the youngest grain cluster algorithm.

*Output: summary table (MDA, 1σ uncertainty, MSWD) + age plot*

---

### Y3Za — Youngest Three Zircons
Calculates the weighted mean age of the three youngest grains, regardless of overlap. Grains are sorted ascendingly and the three youngest are selected directly.

*Output: summary table (MDA, 1σ uncertainty, MSWD) + age plot*

---

### YSP — Youngest Statistical Population
Calculates the weighted mean age of the youngest group of two or more grains that produces an MSWD of ~1. Grains are added to the sub-sample in ascending order until the MSWD exceeds 1, indicating the grains are statistically consistent with being the same true age.

*Output: summary table (MDA, 1σ uncertainty, MSWD, n grains) + age plot*

---

### YDZ — Youngest Detrital Zircon
Applies a Monte Carlo simulation to all grains within 5σ of the youngest grain. Each of 10,000 iterations takes the sub-sample and adjusts each grain by a random variation of its uncertainty, then selects the youngest grain. The mode of the 10,000 youngest grains is the MDA. Upper (P97.5) and lower (P2.5) limits define the 2σ uncertainties. Systematic uncertainty is not included.

*Output: summary table (MDA, 2σ upper and lower uncertainty) + frequency histogram*

---

### YPP — Youngest Graphical Peak
Uses the youngest peak (mode) on the age probability density plot (PDP) that consists of two or more grains overlapping within 2σ of the MDA. No uncertainty is reported for this method.

*Output: summary table (MDA only) + probability density plot*

---

### τ — Tau Method
Calculates the weighted mean age of all grains that fall between the probability minima of the youngest peak composed of three or more grains on the PDP.

*Output: summary table (MDA, 1σ uncertainty, MSWD, n grains) + probability density plot*

---

### MLA — Maximum Likelihood Age
Uses a maximum likelihood model that assumes two age populations exist in the sample: a discrete younger population centered around a minimum age peak, and a continuous older population. Four parameters are estimated iteratively (minimum age peak, mean and spread of the older population, fraction of young grains) until the most probable combination is found. The minimum age peak of the young population is the MDA. Systematic uncertainty is not included. Radial plots are used to visualize results as they effectively display the two-population structure of the data.

*Output: summary table (MDA, 1σ uncertainty) + radial plot*

---

## Exporting Results

All plots can be exported in the following formats: **TIFF, EPS, JPEG, PDF, PNG, SVG**

All summary tables can be exported as **Microsoft Excel (.xlsx)** files.

---

## Limitations

- MDAPy calculates the 10 most commonly applied MDA methods. Some newer or less common methods — such as the Youngest Gaussian Fit (YGF), TuffZirc, or the weighted average of the youngest 4 zircons (Y4Z) — are not currently available.
- MDAPy does not recommend which MDA method is optimal for a given dataset. Researcher expertise and knowledge of the geologic setting are required to interpret results and select the most appropriate method.
- For guidance on method selection, see: Coutts et al. (2019), Herriott et al. (2019), and Brooks (2025).

---

## Citation

If you use MDAPy in your research, please cite:

> Brooks, M. (2025). An evaluation of the accuracy of maximum depositional age algorithms in a variety of tectonic settings using MDAPy: a new Python based application (Master's thesis, University of Calgary, Calgary, Canada). https://doi.org/10.11575/PRISM/49790

---

## References

Brooks, M. (2025). An evaluation of the accuracy of maximum depositional age algorithms in a variety of tectonic settings using MDAPy: a new Python based application (Master's thesis, University of Calgary). https://doi.org/10.11575/PRISM/49790

Coutts, D.S., Matthews, W.A., and Hubbard, S.M. (2019). Assessment of widely used methods to derive depositional ages from detrital zircon populations. *Geoscience Frontiers*, 10(4), 1421–1435.

Sharman, G.R., Sharman, J.P., and Sylvester, Z. (2018). detritalPy: A Python-based toolset for visualizing and analysing detrital geo- and thermochronologic data. *The Depositional Record*, 4(2), 202–215. https://doi.org/10.1002/dep2.45

Vermeesch, P. (2018). IsoplotR: A free and open toolbox for geochronology. *Geoscience Frontiers*, 9(5), 1479–1493. https://doi.org/10.1016/j.gsf.2018.04.001

Vermeesch, P. (2021). Corrigendum to "IsoplotR: A free and open toolbox for geochronology." *Geoscience Frontiers*, 12(2), 1227. https://doi.org/10.1016/j.gsf.2020.12.027
