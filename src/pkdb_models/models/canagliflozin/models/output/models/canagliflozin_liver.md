# Model for hepatic canagliflozin metabolism.

Model `canagliflozin_liver`, SBML Level 3 Version 2, read from canagliflozin\_liver.xml, written by sbmlode 0.3.0.

Model for the hepatic metabolism of canagliflozin.

Canagliflozin is mainly glucuronidated to the inactive O-glucuronides M7 (UGT1A9) and M5 (UGT2B4); the oxidation to M9 by CYP3A4 is minor (about 7 % of the dose) \[Mamidi2014, Francke2015\].

The metabolism is first order: canagliflozin is far below the Km of the enzymes, its pharmacokinetics are dose proportional from 50 to 300 mg \[Devineni2015e\].

The glucuronides are exported into the plasma and the bile; the glucuronides of the bile are hydrolysed to canagliflozin in the intestine, the source of most of the canagliflozin of the feces \[Mamidi2014, Devineni2015b\]. M9 is excreted into the bile.

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
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |
| $\mathrm{Vmem}$ | `Vmem` | plasma membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vbi}$ | `Vbi` | bile | $1$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{can}_{\mathrm{ext}}$ | `can_ext` | canagliflozin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{m5}_{\mathrm{ext}}$ | `m5_ext` | M5 (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{m7}_{\mathrm{ext}}$ | `m7_ext` | M7 (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{can}$ | `can` | canagliflozin (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $m_{5}$ | `m5` | M5 (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $m_{7}$ | `m7` | M7 (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $m_{9}$ | `m9` | M9 (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{m5}_{\mathrm{bi}}$ | `m5_bi` | M5 (bile) | $\mathrm{Vbi}$ |  | mmol | amount |
| $\mathrm{m5}_{\mathrm{lumen}}$ | `m5_lumen` | M5 (lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{m7}_{\mathrm{bi}}$ | `m7_bi` | M7 (bile) | $\mathrm{Vbi}$ |  | mmol | amount |
| $\mathrm{m7}_{\mathrm{lumen}}$ | `m7_lumen` | M7 (lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{m9}_{\mathrm{bi}}$ | `m9_bi` | M9 (bile) | $\mathrm{Vbi}$ |  | mmol | amount |
| $\mathrm{m9}_{\mathrm{lumen}}$ | `m9_lumen` | M9 (lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{ugt1a9}}$ | `f_ugt1a9` | scaling factor UGT1A9 activity | $1$ | \- | ✓ |
| $f_{\mathrm{ugt2b4}}$ | `f_ugt2b4` | scaling factor UGT2B4 activity | $1$ | \- | ✓ |
| $f_{\mathrm{cyp3a4}}$ | `f_cyp3a4` | scaling factor CYP3A4 activity | $1$ | \- | ✓ |
| $\mathrm{CANIM}_{\mathrm{k}}$ | `CANIM_k` | rate of the canagliflozin exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{CAN2M5}_{\mathrm{k}}$ | `CAN2M5_k` | rate of the glucuronidation of canagliflozin to M5 (UGT2B4) | $0.0254214589232899$ | 1/min | ✓ |
| $\mathrm{CAN2M7}_{\mathrm{k}}$ | `CAN2M7_k` | rate of the glucuronidation of canagliflozin to M7 (UGT1A9) | $0.035147180170869$ | 1/min | ✓ |
| $\mathrm{CAN2M9}_{\mathrm{k}}$ | `CAN2M9_k` | rate of the oxidation of canagliflozin to M9 (CYP3A4) | $0.0167669796160069$ | 1/min | ✓ |
| $\mathrm{M5EX}_{\mathrm{k}}$ | `M5EX_k` | rate of the M5 exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{M7EX}_{\mathrm{k}}$ | `M7EX_k` | rate of the M7 exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{M5BIEX}_{\mathrm{k}}$ | `M5BIEX_k` | rate of the biliary excretion of M5 | $0.0281205406918407$ | 1/min | ✓ |
| $\mathrm{M7BIEX}_{\mathrm{k}}$ | `M7BIEX_k` | rate of the biliary excretion of M7 | $0.0569283930226851$ | 1/min | ✓ |
| $\mathrm{M9BIEX}_{\mathrm{k}}$ | `M9BIEX_k` | rate of the biliary excretion of M9 | $0.1$ | 1/min | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{m5}_{\mathrm{bi}} &= 0 \cdot \mathrm{Vbi} \\[1ex]
\mathrm{m7}_{\mathrm{bi}} &= 0 \cdot \mathrm{Vbi} \\[1ex]
\mathrm{m9}_{\mathrm{bi}} &= 0 \cdot \mathrm{Vbi}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{CANIM}}$ | `CANIM` | canagliflozin import (CANIM) | $\mathrm{can}_{\mathrm{ext}} \rightleftharpoons \mathrm{can}$ |
| $v_{\mathrm{CAN2M5}}$ | `CAN2M5` | CAN2M5 (UGT2B4) | $\mathrm{can} \longrightarrow m_{5}$ |
| $v_{\mathrm{CAN2M7}}$ | `CAN2M7` | CAN2M7 (UGT1A9) | $\mathrm{can} \longrightarrow m_{7}$ |
| $v_{\mathrm{CAN2M9}}$ | `CAN2M9` | CAN2M9 (CYP3A4) | $\mathrm{can} \longrightarrow m_{9}$ |
| $v_{\mathrm{M5EX}}$ | `M5EX` | M5 export (M5EX) | $m_{5} \rightleftharpoons \mathrm{m5}_{\mathrm{ext}}$ |
| $v_{\mathrm{M7EX}}$ | `M7EX` | M7 export (M7EX) | $m_{7} \rightleftharpoons \mathrm{m7}_{\mathrm{ext}}$ |
| $v_{\mathrm{M5BIEX}}$ | `M5BIEX` | M5 biliary excretion (M5BIEX) | $m_{5} \longrightarrow \mathrm{m5}_{\mathrm{bi}}$ |
| $v_{\mathrm{M7BIEX}}$ | `M7BIEX` | M7 biliary excretion (M7BIEX) | $m_{7} \longrightarrow \mathrm{m7}_{\mathrm{bi}}$ |
| $v_{\mathrm{M9BIEX}}$ | `M9BIEX` | M9 biliary excretion (M9BIEX) | $m_{9} \longrightarrow \mathrm{m9}_{\mathrm{bi}}$ |
| $v_{\mathrm{M5EHC}}$ | `M5EHC` | M5 bile flow into the intestine | $\mathrm{m5}_{\mathrm{bi}} \longrightarrow \mathrm{m5}_{\mathrm{lumen}}$ |
| $v_{\mathrm{M7EHC}}$ | `M7EHC` | M7 bile flow into the intestine | $\mathrm{m7}_{\mathrm{bi}} \longrightarrow \mathrm{m7}_{\mathrm{lumen}}$ |
| $v_{\mathrm{M9EHC}}$ | `M9EHC` | M9 bile flow into the intestine | $\mathrm{m9}_{\mathrm{bi}} \longrightarrow \mathrm{m9}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CANIM}} &= \mathrm{CANIM}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{can}_{\mathrm{ext}} - \mathrm{can}\right) \\[1ex]
v_{\mathrm{CAN2M5}} &= f_{\mathrm{ugt2b4}} \cdot \mathrm{CAN2M5}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{can} \\[1ex]
v_{\mathrm{CAN2M7}} &= f_{\mathrm{ugt1a9}} \cdot \mathrm{CAN2M7}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{can} \\[1ex]
v_{\mathrm{CAN2M9}} &= f_{\mathrm{cyp3a4}} \cdot \mathrm{CAN2M9}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{can} \\[1ex]
v_{\mathrm{M5EX}} &= \mathrm{M5EX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(m_{5} - \mathrm{m5}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{M7EX}} &= \mathrm{M7EX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(m_{7} - \mathrm{m7}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{M5BIEX}} &= \mathrm{M5BIEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot m_{5} \\[1ex]
v_{\mathrm{M7BIEX}} &= \mathrm{M7BIEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot m_{7} \\[1ex]
v_{\mathrm{M9BIEX}} &= \mathrm{M9BIEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot m_{9} \\[1ex]
v_{\mathrm{M5EHC}} &= v_{\mathrm{M5BIEX}} \\[1ex]
v_{\mathrm{M7EHC}} &= v_{\mathrm{M7BIEX}} \\[1ex]
v_{\mathrm{M9EHC}} &= v_{\mathrm{M9BIEX}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CANIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{M5EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{M7EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{can}}{\mathrm{d} t} &= \frac{v_{\mathrm{CANIM}} - v_{\mathrm{CAN2M5}} - v_{\mathrm{CAN2M7}} - v_{\mathrm{CAN2M9}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} m_{5}}{\mathrm{d} t} &= \frac{v_{\mathrm{CAN2M5}} - v_{\mathrm{M5EX}} - v_{\mathrm{M5BIEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} m_{7}}{\mathrm{d} t} &= \frac{v_{\mathrm{CAN2M7}} - v_{\mathrm{M7EX}} - v_{\mathrm{M7BIEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} m_{9}}{\mathrm{d} t} &= \frac{v_{\mathrm{CAN2M9}} - v_{\mathrm{M9BIEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{bi}}}{\mathrm{d} t} &= v_{\mathrm{M5BIEX}} - v_{\mathrm{M5EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{M5EHC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{bi}}}{\mathrm{d} t} &= v_{\mathrm{M7BIEX}} - v_{\mathrm{M7EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{M7EHC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m9}_{\mathrm{bi}}}{\mathrm{d} t} &= v_{\mathrm{M9BIEX}} - v_{\mathrm{M9EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m9}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{M9EHC}}}{\mathrm{Vlumen}}
\end{aligned}
$$
