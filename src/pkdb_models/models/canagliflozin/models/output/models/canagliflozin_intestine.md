# Model for canagliflozin absorption in the small intestine

Model `canagliflozin_intestine`, SBML Level 3 Version 2, read from canagliflozin\_intestine.xml, written by sbmlode 0.3.0.

Model for canagliflozin absorption

Dissolution of the oral dose and absorption of canagliflozin; the fraction absorbed F\_can\_abs of the canagliflozin of the lumen is absorbed, the rest is excreted in the feces. The absolute bioavailability is 65 % (90 % CI 55-76 %) \[Devineni2015b\].

The glucuronides M5 and M7 of the bile are hydrolysed to canagliflozin in the lumen (enterohepatic circulation), the source of most of the canagliflozin of the feces (39-41.5 % of the dose). M7 which is not hydrolysed is excreted in the feces (2-3 % of the dose), M5 is not found in the feces \[Mamidi2014, Devineni2015b\]. M9 of the bile is excreted in the feces (7-8 %).

The absorption of canagliflozin is not changed by food: a high fat breakfast changes neither the AUC (+8 %) nor Cmax (+0.5 %) \[Devineni2015e\], so the model has no food effect.

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vapical}$ | `Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{can}_{\mathrm{stomach}}$ | `can_stomach` | canagliflozin (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |
| $\mathrm{can}_{\mathrm{lumen}}$ | `can_lumen` | canagliflozin (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{can}_{\mathrm{ext}}$ | `can_ext` | canagliflozin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{can}_{\mathrm{feces}}$ | `can_feces` | canagliflozin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{m5}_{\mathrm{lumen}}$ | `m5_lumen` | M5 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{m7}_{\mathrm{lumen}}$ | `m7_lumen` | M7 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{m9}_{\mathrm{lumen}}$ | `m9_lumen` | M9 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{m7}_{\mathrm{feces}}$ | `m7_feces` | M7 (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{m9}_{\mathrm{feces}}$ | `m9_feces` | M9 (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{cantot}_{\mathrm{feces}}$ | `cantot_feces` | total canagliflozin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $F_{\mathrm{can\_abs}}$ | `F_can_abs` | fraction absorbed canagliflozin | $0.665659728244104$ | \- | ✓ |
| $\mathrm{CANABS}_{\mathrm{k}}$ | `CANABS_k` | rate of canagliflozin absorption | $0.0152774444477217$ | 1/min | ✓ |
| $\mathrm{GLUHYD}_{\mathrm{k}}$ | `GLUHYD_k` | rate of the hydrolysis of the glucuronides in the lumen | $0.006979255151286$ | 1/min | ✓ |
| $\mathrm{METEXC}_{\mathrm{k}}$ | `METEXC_k` | rate of the fecal excretion of the metabolites | $0.001$ | 1/min | ✓ |
| $\mathrm{PODOSE}_{\mathrm{can}}$ | `PODOSE_can` | oral dose canagliflozin \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{dis\_can}}$ | `Ka_dis_can` | dissolution rate canagliflozin | $2$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{can}}$ | `Mr_can` | Molecular weight canagliflozin \[g/mole\] | $444.518$ | g/mol | ✓ |
| $\mathrm{absorption}$ | `absorption` | absorption canagliflozin |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{can}_{\mathrm{stomach}} &= 0 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{can}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{m7}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{m9}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{absorption} &= \mathrm{CANABS}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{can}_{\mathrm{lumen}} \\[1ex]
\mathrm{cantot}_{\mathrm{feces}} &= \mathrm{can}_{\mathrm{feces}} + \mathrm{m7}_{\mathrm{feces}} + \mathrm{m9}_{\mathrm{feces}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{CANABS}}$ | `CANABS` | CANABS | $\mathrm{can}_{\mathrm{lumen}} \longrightarrow \mathrm{can}_{\mathrm{ext}}$ |
| $v_{\mathrm{CANEXC}}$ | `CANEXC` | CANEXC (feces) | $\mathrm{can}_{\mathrm{lumen}} \longrightarrow \mathrm{can}_{\mathrm{feces}}$ |
| $v_{\mathrm{M5HYD}}$ | `M5HYD` | M5 hydrolysis (M5HYD) | $\mathrm{m5}_{\mathrm{lumen}} \longrightarrow \mathrm{can}_{\mathrm{lumen}}$ |
| $v_{\mathrm{M7HYD}}$ | `M7HYD` | M7 hydrolysis (M7HYD) | $\mathrm{m7}_{\mathrm{lumen}} \longrightarrow \mathrm{can}_{\mathrm{lumen}}$ |
| $v_{\mathrm{M5EXC}}$ | `M5EXC` | M5 excretion (M5EXC, feces, hydrolysed to canagliflozin) | $\mathrm{m5}_{\mathrm{lumen}} \longrightarrow \mathrm{can}_{\mathrm{feces}}$ |
| $v_{\mathrm{M7EXC}}$ | `M7EXC` | M7 excretion (M7EXC, feces) | $\mathrm{m7}_{\mathrm{lumen}} \longrightarrow \mathrm{m7}_{\mathrm{feces}}$ |
| $v_{\mathrm{M9EXC}}$ | `M9EXC` | M9 excretion (M9EXC, feces) | $\mathrm{m9}_{\mathrm{lumen}} \longrightarrow \mathrm{m9}_{\mathrm{feces}}$ |
| $v_{\mathrm{dissolution\_can}}$ | `dissolution_can` | dissolution canagliflozin | $\mathrm{can}_{\mathrm{stomach}} \longrightarrow \mathrm{can}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CANABS}} &= F_{\mathrm{can\_abs}} \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{CANEXC}} &= \mathopen{}\left(1 - F_{\mathrm{can\_abs}}\right) \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{M5HYD}} &= \mathrm{GLUHYD}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{m5}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{M7HYD}} &= \mathrm{GLUHYD}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{m7}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{M5EXC}} &= \mathrm{METEXC}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{m5}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{M7EXC}} &= \mathrm{METEXC}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{m7}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{M9EXC}} &= \mathrm{METEXC}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{m9}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{dissolution\_can}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{dis\_can}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{can}}}{\mathrm{Mr}_{\mathrm{can}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vlumen}} \Bigl( -v_{\mathrm{CANABS}} - v_{\mathrm{CANEXC}} + v_{\mathrm{M5HYD}} + v_{\mathrm{M7HYD}} \\
&\quad {} + v_{\mathrm{dissolution\_can}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CANABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{can}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{CANEXC}} + v_{\mathrm{M5EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m5}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{M5HYD}} - v_{\mathrm{M5EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{M7HYD}} - v_{\mathrm{M7EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m9}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{M9EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m7}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{M7EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{m9}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{M9EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{can}}}{\mathrm{d} t} &= -v_{\mathrm{dissolution\_can}} \cdot \mathrm{Mr}_{\mathrm{can}} \qquad \text{(rate rule)}
\end{aligned}
$$
