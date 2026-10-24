# Model for the renal excretion of canagliflozin, M5 and M7 and the urinary glucose excretion.

Model `canagliflozin_kidney`, SBML Level 3 Version 2, read from canagliflozin\_kidney.xml, written by sbmlode 0.3.0.

Model for the renal excretion of canagliflozin, M5 and M7, the renal glucuronidation of canagliflozin to M7 and the urinary glucose excretion.

About 33 % of an oral dose is excreted in the urine, mainly as the O-glucuronides M5 (13.7 %) and M7 (18.2 %), unchanged canagliflozin &lt; 0.5 % \[Mamidi2014, Devineni2015b\].

The renal excretion is relative to the glomerular filtration rate (GFR), canagliflozin is 99 % bound to plasma proteins, its renal clearance of 0.8-1.4 ml/min is the filtration of its unbound fraction \[Devineni2015c, Inagaki2014\].

UGT1A9 of the kidney forms M7 \[Francke2015\]; the renal glucuronidation scales with the renal function, which makes the exposure of canagliflozin increase in renal impairment \[Devineni2015c\].

Canagliflozin lowers the renal threshold of glucose (RTG) by the inhibition of SGLT2; glucose above the RTG is excreted with the GFR.

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vext}$ | `Vext` | plasma | $1.5$ | l | ✓ |
| $\mathrm{Vki}$ | `Vki` | kidney | $0.3$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{can}_{\mathrm{ext}}$ | `can_ext` | canagliflozin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{can}_{\mathrm{urine}}$ | `can_urine` | canagliflozin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{m5}_{\mathrm{ext}}$ | `m5_ext` | M5 (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{m5}_{\mathrm{urine}}$ | `m5_urine` | M5 (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{m7}_{\mathrm{ext}}$ | `m7_ext` | M7 (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{m7}_{\mathrm{urine}}$ | `m7_urine` | M7 (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{cantot}_{\mathrm{urine}}$ | `cantot_urine` | total canagliflozin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{fpg}$ | `fpg` | fasting plasma glucose (FPG) | $\mathrm{Vext}$ | $5$ | mmol/l | concentration, boundary |
| $\mathrm{glc}_{\mathrm{urine}}$ | `glc_urine` | glucose (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $f_{\mathrm{ugt1a9}}$ | `f_ugt1a9` | scaling factor UGT1A9 activity | $1$ | \- | ✓ |
| $f_{\mathrm{oat}}$ | `f_oat` | scaling factor renal anion transport of the glucuronides | $1$ | \- | ✓ |
| $\mathrm{fu}_{\mathrm{can}}$ | `fu_can` | fraction unbound in plasma canagliflozin | $0.01$ | \- | ✓ |
| $\mathrm{CANEX}_{\mathrm{f}}$ | `CANEX_f` | renal clearance of unbound canagliflozin relative to the GFR | $1.27293622415953$ | \- | ✓ |
| $\mathrm{M5EX}_{\mathrm{f}}$ | `M5EX_f` | renal clearance of M5 relative to the GFR | $0.551071893208109$ | \- | ✓ |
| $\mathrm{M7EX}_{\mathrm{f}}$ | `M7EX_f` | renal clearance of M7 relative to the GFR | $0.801255192259492$ | \- | ✓ |
| $\mathrm{CAN2M7}_{\mathrm{k}}$ | `CAN2M7_k` | rate of the renal glucuronidation of canagliflozin to M7 (UGT1A9) | $0.133$ | 1/min | ✓ |
| $\mathrm{Mr}_{\mathrm{glc}}$ | `Mr_glc` | molecular weight glucose | $180.16$ | g/mol | ✓ |
| $\mathrm{cf}_{\mathrm{mg\_per\_g}}$ | `cf_mg_per_g` | conversion factor mg per g | $1000$ | mg/g | ✓ |
| $\mathrm{fpg}_{\mathrm{healthy}}$ | `fpg_healthy` | fasting plasma glucose (healthy) | $5$ | mmol/l | ✓ |
| $\mathrm{PG}_{\mathrm{delta}}$ | `PG_delta` | mean plasma glucose of the day minus the fasting plasma glucose | $0.85$ | mmol/l | ✓ |
| $\mathrm{RTG}_{\mathrm{E50}}$ | `RTG_E50` | EC50 reduction in RTG | $7.58654838673793 \times 10^{-5}$ | mmol/l | ✓ |
| $\mathrm{RTG}_{\mathrm{gamma}}$ | `RTG_gamma` | hill coefficient reduction in RTG | $1$ | \- | ✓ |
| $\mathrm{RTG}_{\mathrm{base}}$ | `RTG_base` | baseline RTG | $8.93271199710849$ | mmol/l | ✓ |
| $\mathrm{RTG}_{\mathrm{m\_fpg}}$ | `RTG_m_fpg` | FPG effect on RTG | $0.667145959612092$ | \- | ✓ |
| $\mathrm{RTG}_{\mathrm{max\_inhibition}}$ | `RTG_max_inhibition` | maximal relative reduction of the RTG | $0.64508284571308$ | \- | ✓ |
| $\mathrm{RTG}_{\mathrm{splay}}$ | `RTG_splay` | splay of the glucose excretion around the RTG | $1$ | mmol/l | ✓ |
| $\mathrm{RTG}_{\mathrm{int}}$ | `RTG_int` | integral of the RTG over the collection interval | $0$ | mmol·min/l |  |
| $\mathrm{RTG}_{\mathrm{time}}$ | `RTG_time` | duration of the collection interval of the RTG | $0$ | min |  |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{pg}$ | `pg` | mean plasma glucose of the day |  | mmol/l |  |
| $\mathrm{RTG}_{\mathrm{fpg}}$ | `RTG_fpg` | RTG without SGLT2 inhibition |  | mmol/l |  |
| $\mathrm{RTG}_{\mathrm{delta}}$ | `RTG_delta` | maximal reduction of the RTG |  | mmol/l |  |
| $\mathrm{RTG}$ | `RTG` | renal threshold glucose (RTG) |  | mmol/l |  |
| $\mathrm{RTG}_{\mathrm{mean}}$ | `RTG_mean` | mean RTG of the collection interval |  | mmol/l |  |
| $\mathrm{UGE}$ | `UGE` | urinary glucose excretion (UGE) |  | gram |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{can}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{m5}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{m7}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{glc}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{cantot}_{\mathrm{urine}} &= \mathrm{can}_{\mathrm{urine}} + \mathrm{m5}_{\mathrm{urine}} + \mathrm{m7}_{\mathrm{urine}} \\[1ex]
\mathrm{pg} &= \mathrm{fpg} + \mathrm{PG}_{\mathrm{delta}} \\[1ex]
\mathrm{RTG}_{\mathrm{fpg}} &= \mathrm{RTG}_{\mathrm{base}} + \mathrm{RTG}_{\mathrm{m\_fpg}} \cdot \mathopen{}\left(\mathrm{fpg} - \mathrm{fpg}_{\mathrm{healthy}}\right) \\[1ex]
\mathrm{RTG}_{\mathrm{delta}} &= \mathrm{RTG}_{\mathrm{fpg}} \cdot \mathrm{RTG}_{\mathrm{max\_inhibition}} \\[1ex]
\mathrm{RTG} &= \mathrm{RTG}_{\mathrm{fpg}} - \frac{\mathrm{RTG}_{\mathrm{delta}} \cdot \mathrm{can}_{\mathrm{ext}}^{\mathrm{RTG}_{\mathrm{gamma}}}}{\mathrm{RTG}_{\mathrm{E50}}^{\mathrm{RTG}_{\mathrm{gamma}}} + \mathrm{can}_{\mathrm{ext}}^{\mathrm{RTG}_{\mathrm{gamma}}}} \\[1ex]
\mathrm{RTG}_{\mathrm{mean}} &= \begin{cases} \frac{\mathrm{RTG}_{\mathrm{int}}}{\mathrm{RTG}_{\mathrm{time}}} & \text{if } \mathrm{RTG}_{\mathrm{time}} > 0 \\ \mathrm{RTG} & \text{otherwise} \end{cases} \\[1ex]
\mathrm{UGE} &= \frac{\mathrm{glc}_{\mathrm{urine}} \cdot \mathrm{Mr}_{\mathrm{glc}}}{\mathrm{cf}_{\mathrm{mg\_per\_g}}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{CAN2M7}}$ | `CAN2M7` | UGT1A9 (can -&gt; m7) | $\mathrm{can}_{\mathrm{ext}} \longrightarrow \mathrm{m7}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{CANEX}}$ | `CANEX` | canagliflozin excretion (CANEX) | $\mathrm{can}_{\mathrm{ext}} \longrightarrow \mathrm{can}_{\mathrm{urine}}$ |  |
| $v_{\mathrm{M5EX}}$ | `M5EX` | M5 excretion (M5EX) | $\mathrm{m5}_{\mathrm{ext}} \longrightarrow \mathrm{m5}_{\mathrm{urine}}$ |  |
| $v_{\mathrm{M7EX}}$ | `M7EX` | M7 excretion (M7EX) | $\mathrm{m7}_{\mathrm{ext}} \longrightarrow \mathrm{m7}_{\mathrm{urine}}$ |  |
| $v_{\mathrm{GLCEX}}$ | `GLCEX` | glucose excretion (GLCEX) | $\mathrm{fpg} \longrightarrow \mathrm{glc}_{\mathrm{urine}}$ | $\mathrm{can}_{\mathrm{ext}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CAN2M7}} &= f_{\mathrm{renal\_function}} \cdot f_{\mathrm{ugt1a9}} \cdot \mathrm{CAN2M7}_{\mathrm{k}} \cdot \mathrm{Vki} \cdot \mathrm{can}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{CANEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{can}} \cdot \mathrm{CANEX}_{\mathrm{f}} \cdot \mathrm{can}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{M5EX}} &= \mathrm{GFR} \cdot 0.001 \cdot f_{\mathrm{oat}} \cdot \mathrm{M5EX}_{\mathrm{f}} \cdot \mathrm{m5}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{M7EX}} &= \mathrm{GFR} \cdot 0.001 \cdot f_{\mathrm{oat}} \cdot \mathrm{M7EX}_{\mathrm{f}} \cdot \mathrm{m7}_{\mathrm{ext}} \\[1ex]
v_{\mathrm{GLCEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{RTG}_{\mathrm{splay}} \cdot \ln\mathopen{}\left(1 + \exp\mathopen{}\left(\frac{\mathrm{pg} - \mathrm{RTG}}{\mathrm{RTG}_{\mathrm{splay}}}\right)\right)
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CAN2M7}} - v_{\mathrm{CANEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{CANEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{M5EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{M5EX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CAN2M7}} - v_{\mathrm{M7EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{M7EX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{glc}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{GLCEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{RTG}_{\mathrm{int}}}{\mathrm{d} t} &= \mathrm{RTG} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{RTG}_{\mathrm{time}}}{\mathrm{d} t} &= 1 \qquad \text{(rate rule)}
\end{aligned}
$$
