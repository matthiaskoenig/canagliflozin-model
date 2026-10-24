# Canagliflozin body model

Model `canagliflozin_body`, SBML Level 3 Version 2, read from canagliflozin\_body.xml, written by sbmlode 0.3.0.

Canagliflozin body model

Distribution of canagliflozin and its glucuronides M5 and M7 with the blood flow, the tissue distribution of canagliflozin, the hepatic and renal metabolism, the biliary excretion of the metabolites with the hydrolysis of the glucuronides in the intestine, and the renal excretion.

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
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{LI}_{\mathrm{\_Vmem}}$ | `LI__Vmem` | plasma membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vapical}}$ | `LI__Vapical` | apical membrane | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |
| $\mathrm{LI}_{\mathrm{\_Vbi}}$ | `LI__Vbi` | bile | $1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vapical}}$ | `GU__Vapical` | apical membrane (intestinal membrane enterocytes) | $\mathrm{NaN}$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cki}_{\mathrm{plasma\_can}}$ | `Cki_plasma_can` | canagliflozin (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_can}}$ | `Cli_plasma_can` | canagliflozin (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_can}}$ | `Clu_plasma_can` | canagliflozin (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_can}}$ | `Cgu_plasma_can` | canagliflozin (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_can}}$ | `Cre_plasma_can` | canagliflozin (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{can}}$ | `Car_can` | canagliflozin (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{can}}$ | `Cve_can` | canagliflozin (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{can}}$ | `Cpo_can` | canagliflozin (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{can}}$ | `Chv_can` | canagliflozin (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{can}}$ | `Clu_can` | canagliflozin (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{can}}$ | `Cre_can` | canagliflozin (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{deep\_can}}$ | `Cre_deep_can` | canagliflozin (rest, deep tissue) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{can}}$ | `Aurine_can` | canagliflozin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_m5}}$ | `Cki_plasma_m5` | M5 (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_m5}}$ | `Cli_plasma_m5` | M5 (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_m5}}$ | `Clu_plasma_m5` | M5 (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_m5}}$ | `Cgu_plasma_m5` | M5 (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_m5}}$ | `Cre_plasma_m5` | M5 (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{m5}}$ | `Car_m5` | M5 (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{m5}}$ | `Cve_m5` | M5 (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{m5}}$ | `Cpo_m5` | M5 (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{m5}}$ | `Chv_m5` | M5 (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{m5}}$ | `Aurine_m5` | M5 (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cki}_{\mathrm{plasma\_m7}}$ | `Cki_plasma_m7` | M7 (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_m7}}$ | `Cli_plasma_m7` | M7 (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_m7}}$ | `Clu_plasma_m7` | M7 (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_m7}}$ | `Cgu_plasma_m7` | M7 (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_m7}}$ | `Cre_plasma_m7` | M7 (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{m7}}$ | `Car_m7` | M7 (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{m7}}$ | `Cve_m7` | M7 (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{m7}}$ | `Cpo_m7` | M7 (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{m7}}$ | `Chv_m7` | M7 (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{m7}}$ | `Aurine_m7` | M7 (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Cgu}_{\mathrm{can}}$ | `Cgu_can` | canagliflozin (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Afeces}_{\mathrm{can}}$ | `Afeces_can` | canagliflozin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgu}_{\mathrm{m5}}$ | `Cgu_m5` | M5 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{m7}}$ | `Cgu_m7` | M7 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Afeces}_{\mathrm{m7}}$ | `Afeces_m7` | M7 (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgu}_{\mathrm{m9}}$ | `Cgu_m9` | M9 (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Afeces}_{\mathrm{m9}}$ | `Afeces_m9` | M9 (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cve}_{\mathrm{cantot}}$ | `Cve_cantot` | total canagliflozin (plasma) | $\mathrm{Vve}$ |  | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{cantot}}$ | `Aurine_cantot` | total canagliflozin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{cantot}}$ | `Afeces_cantot` | total canagliflozin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{KI}_{\mathrm{\_fpg}}$ | `KI__fpg` | fasting plasma glucose (FPG) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $5$ | mmol/l | concentration, boundary |
| $\mathrm{KI}_{\mathrm{\_glc\_urine}}$ | `KI__glc_urine` | glucose (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{LI}_{\mathrm{\_can}}$ | `LI__can` | canagliflozin (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_m5}}$ | `LI__m5` | M5 (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_m7}}$ | `LI__m7` | M7 (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_m9}}$ | `LI__m9` | M9 (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_m5\_bi}}$ | `LI__m5_bi` | M5 (bile) | $\mathrm{LI}_{\mathrm{\_Vbi}}$ |  | mmol | amount |
| $\mathrm{LI}_{\mathrm{\_m7\_bi}}$ | `LI__m7_bi` | M7 (bile) | $\mathrm{LI}_{\mathrm{\_Vbi}}$ |  | mmol | amount |
| $\mathrm{LI}_{\mathrm{\_m9\_bi}}$ | `LI__m9_bi` | M9 (bile) | $\mathrm{LI}_{\mathrm{\_Vbi}}$ |  | mmol | amount |
| $\mathrm{GU}_{\mathrm{\_can\_stomach}}$ | `GU__can_stomach` | canagliflozin (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{BW}$ | `BW` | body weight | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight | $1.548$ | ml/s/kg | ✓ |
| $f_{\mathrm{cardiac\_function}}$ | `f_cardiac_function` | heart function | $1$ | \- |  |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[l/min\] |  | l/min |  |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- |  |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $76.3105006271061$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) |  | ml/min |  |
| $f_{\mathrm{ugt1a9}}$ | `f_ugt1a9` | scaling factor UGT1A9 activity | $1$ | \- | ✓ |
| $\mathrm{PODOSE}_{\mathrm{can}}$ | `PODOSE_can` | oral dose can \[mg\] | $0$ | mg |  |
| $\mathrm{Mr}_{\mathrm{can}}$ | `Mr_can` | Molecular weight can \[g/mole\] | $444.518$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{can}}$ | `ftissue_can` | tissue distribution can | $1.08930588990549$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{can}}$ | `Kp_can` | tissue/plasma partition coefficient can | $0.685123325515857$ | \- | ✓ |
| $\mathrm{ftissue}_{\mathrm{deep\_can}}$ | `ftissue_deep_can` | deep tissue distribution can | $0.00663006706318984$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{deep\_can}}$ | `Kp_deep_can` | deep tissue/plasma partition coefficient can | $9.54277408691065$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{can}}$ | `IVDOSE_can` | IV bolus dose can \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{can}}$ | `ti_can` | injection time can \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{can}}$ | `Ki_can` | Ki \[1/min\] injection can |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{can}}$ | `Ri_can` | Ri \[mg/min\] rate of infusion can | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_can}}$ | `cum_dose_can` | Cumulative dose due to infusion can | $0$ | mg |  |
| $\mathrm{Mr}_{\mathrm{m5}}$ | `Mr_m5` | Molecular weight m5 \[g/mole\] | $620.6$ | g/mol | ✓ |
| $\mathrm{Mr}_{\mathrm{m7}}$ | `Mr_m7` | Molecular weight m7 \[g/mole\] | $620.6$ | g/mol | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_f\_oat}}$ | `KI__f_oat` | scaling factor renal anion transport of the glucuronides | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_fu\_can}}$ | `KI__fu_can` | fraction unbound in plasma canagliflozin | $0.01$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_CANEX\_f}}$ | `KI__CANEX_f` | renal clearance of unbound canagliflozin relative to the GFR | $1.27293622415953$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_M5EX\_f}}$ | `KI__M5EX_f` | renal clearance of M5 relative to the GFR | $0.551071893208109$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_M7EX\_f}}$ | `KI__M7EX_f` | renal clearance of M7 relative to the GFR | $0.801255192259492$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_CAN2M7\_k}}$ | `KI__CAN2M7_k` | rate of the renal glucuronidation of canagliflozin to M7 (UGT1A9) | $0.133$ | 1/min | ✓ |
| $\mathrm{KI}_{\mathrm{\_Mr\_glc}}$ | `KI__Mr_glc` | molecular weight glucose | $180.16$ | g/mol | ✓ |
| $\mathrm{KI}_{\mathrm{\_cf\_mg\_per\_g}}$ | `KI__cf_mg_per_g` | conversion factor mg per g | $1000$ | mg/g | ✓ |
| $\mathrm{KI}_{\mathrm{\_fpg\_healthy}}$ | `KI__fpg_healthy` | fasting plasma glucose (healthy) | $5$ | mmol/l | ✓ |
| $\mathrm{KI}_{\mathrm{\_PG\_delta}}$ | `KI__PG_delta` | mean plasma glucose of the day minus the fasting plasma glucose | $0.85$ | mmol/l | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_E50}}$ | `KI__RTG_E50` | EC50 reduction in RTG | $7.58654838673793 \times 10^{-5}$ | mmol/l | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_gamma}}$ | `KI__RTG_gamma` | hill coefficient reduction in RTG | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_base}}$ | `KI__RTG_base` | baseline RTG | $8.93271199710849$ | mmol/l | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_m\_fpg}}$ | `KI__RTG_m_fpg` | FPG effect on RTG | $0.667145959612092$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_max\_inhibition}}$ | `KI__RTG_max_inhibition` | maximal relative reduction of the RTG | $0.64508284571308$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_splay}}$ | `KI__RTG_splay` | splay of the glucose excretion around the RTG | $1$ | mmol/l | ✓ |
| $\mathrm{KI}_{\mathrm{\_RTG\_int}}$ | `KI__RTG_int` | integral of the RTG over the collection interval | $0$ | mmol·min/l |  |
| $\mathrm{KI}_{\mathrm{\_RTG\_time}}$ | `KI__RTG_time` | duration of the collection interval of the RTG | $0$ | min |  |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{KI}_{\mathrm{\_pg}}$ | `KI__pg` | mean plasma glucose of the day |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_RTG\_fpg}}$ | `KI__RTG_fpg` | RTG without SGLT2 inhibition |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_RTG\_delta}}$ | `KI__RTG_delta` | maximal reduction of the RTG |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_RTG}}$ | `KI__RTG` | renal threshold glucose (RTG) |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_RTG\_mean}}$ | `KI__RTG_mean` | mean RTG of the collection interval |  | mmol/l |  |
| $\mathrm{KI}_{\mathrm{\_UGE}}$ | `KI__UGE` | urinary glucose excretion (UGE) |  | gram |  |
| $\mathrm{LI}_{\mathrm{\_f\_ugt2b4}}$ | `LI__f_ugt2b4` | scaling factor UGT2B4 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_cyp3a4}}$ | `LI__f_cyp3a4` | scaling factor CYP3A4 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_CANIM\_k}}$ | `LI__CANIM_k` | rate of the canagliflozin exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CAN2M5\_k}}$ | `LI__CAN2M5_k` | rate of the glucuronidation of canagliflozin to M5 (UGT2B4) | $0.0254214589232899$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CAN2M7\_k}}$ | `LI__CAN2M7_k` | rate of the glucuronidation of canagliflozin to M7 (UGT1A9) | $0.035147180170869$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_CAN2M9\_k}}$ | `LI__CAN2M9_k` | rate of the oxidation of canagliflozin to M9 (CYP3A4) | $0.0167669796160069$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_M5EX\_k}}$ | `LI__M5EX_k` | rate of the M5 exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_M7EX\_k}}$ | `LI__M7EX_k` | rate of the M7 exchange of the liver | $10$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_M5BIEX\_k}}$ | `LI__M5BIEX_k` | rate of the biliary excretion of M5 | $0.0281205406918407$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_M7BIEX\_k}}$ | `LI__M7BIEX_k` | rate of the biliary excretion of M7 | $0.0569283930226851$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_M9BIEX\_k}}$ | `LI__M9BIEX_k` | rate of the biliary excretion of M9 | $0.1$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_F\_can\_abs}}$ | `GU__F_can_abs` | fraction absorbed canagliflozin | $0.665659728244104$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_CANABS\_k}}$ | `GU__CANABS_k` | rate of canagliflozin absorption | $0.0152774444477217$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_GLUHYD\_k}}$ | `GU__GLUHYD_k` | rate of the hydrolysis of the glucuronides in the lumen | $0.006979255151286$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_METEXC\_k}}$ | `GU__METEXC_k` | rate of the fecal excretion of the metabolites | $0.001$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ka\_dis\_can}}$ | `GU__Ka_dis_can` | dissolution rate canagliflozin | $2$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_absorption}}$ | `GU__absorption` | absorption canagliflozin |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Aurine}_{\mathrm{can}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Aurine}_{\mathrm{m5}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Aurine}_{\mathrm{m7}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{can}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{Afeces}_{\mathrm{m7}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{Afeces}_{\mathrm{m9}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{KI}_{\mathrm{\_glc\_urine}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{LI}_{\mathrm{\_m5\_bi}} &= 0 \cdot \mathrm{LI}_{\mathrm{\_Vbi}} \\[1ex]
\mathrm{LI}_{\mathrm{\_m7\_bi}} &= 0 \cdot \mathrm{LI}_{\mathrm{\_Vbi}} \\[1ex]
\mathrm{LI}_{\mathrm{\_m9\_bi}} &= 0 \cdot \mathrm{LI}_{\mathrm{\_Vbi}} \\[1ex]
\mathrm{GU}_{\mathrm{\_can\_stomach}} &= 0 \cdot \mathrm{Vstomach}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{Cve}_{\mathrm{cantot}} &= \mathrm{Cve}_{\mathrm{can}} + \mathrm{Cve}_{\mathrm{m5}} + \mathrm{Cve}_{\mathrm{m7}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{CO} &= f_{\mathrm{cardiac\_function}} \cdot \mathrm{BW} \cdot \mathrm{COBW} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{Vlumen} &= 0.9 \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{can}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{can}}} \cdot 60 \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{Aurine}_{\mathrm{cantot}} &= \mathrm{Aurine}_{\mathrm{can}} + \mathrm{Aurine}_{\mathrm{m5}} + \mathrm{Aurine}_{\mathrm{m7}} \\[1ex]
\mathrm{KI}_{\mathrm{\_pg}} &= \mathrm{KI}_{\mathrm{\_fpg}} + \mathrm{KI}_{\mathrm{\_PG\_delta}} \\[1ex]
\mathrm{KI}_{\mathrm{\_RTG\_fpg}} &= \mathrm{KI}_{\mathrm{\_RTG\_base}} + \mathrm{KI}_{\mathrm{\_RTG\_m\_fpg}} \cdot \mathopen{}\left(\mathrm{KI}_{\mathrm{\_fpg}} - \mathrm{KI}_{\mathrm{\_fpg\_healthy}}\right) \\[1ex]
\mathrm{KI}_{\mathrm{\_RTG\_delta}} &= \mathrm{KI}_{\mathrm{\_RTG\_fpg}} \cdot \mathrm{KI}_{\mathrm{\_RTG\_max\_inhibition}} \\[1ex]
\mathrm{KI}_{\mathrm{\_RTG}} &= \mathrm{KI}_{\mathrm{\_RTG\_fpg}} - \frac{\mathrm{KI}_{\mathrm{\_RTG\_delta}} \cdot \mathrm{Cki}_{\mathrm{plasma\_can}}^{\mathrm{KI}_{\mathrm{\_RTG\_gamma}}}}{\mathrm{KI}_{\mathrm{\_RTG\_E50}}^{\mathrm{KI}_{\mathrm{\_RTG\_gamma}}} + \mathrm{Cki}_{\mathrm{plasma\_can}}^{\mathrm{KI}_{\mathrm{\_RTG\_gamma}}}} \\[1ex]
\mathrm{KI}_{\mathrm{\_RTG\_mean}} &= \begin{cases} \frac{\mathrm{KI}_{\mathrm{\_RTG\_int}}}{\mathrm{KI}_{\mathrm{\_RTG\_time}}} & \text{if } \mathrm{KI}_{\mathrm{\_RTG\_time}} > 0 \\ \mathrm{KI}_{\mathrm{\_RTG}} & \text{otherwise} \end{cases} \\[1ex]
\mathrm{KI}_{\mathrm{\_UGE}} &= \frac{\mathrm{KI}_{\mathrm{\_glc\_urine}} \cdot \mathrm{KI}_{\mathrm{\_Mr\_glc}}}{\mathrm{KI}_{\mathrm{\_cf\_mg\_per\_g}}} \\[1ex]
\mathrm{GU}_{\mathrm{\_absorption}} &= \mathrm{GU}_{\mathrm{\_CANABS\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{can}} \\[1ex]
\mathrm{Afeces}_{\mathrm{cantot}} &= \mathrm{Afeces}_{\mathrm{can}} + \mathrm{Afeces}_{\mathrm{m7}} + \mathrm{Afeces}_{\mathrm{m9}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{transport\_lu\_can}}$ | `transport_lu_can` | transport canagliflozin | $\mathrm{Clu}_{\mathrm{plasma\_can}} \rightleftharpoons \mathrm{Clu}_{\mathrm{can}}$ |  |
| $v_{\mathrm{transport\_re\_can}}$ | `transport_re_can` | transport canagliflozin | $\mathrm{Cre}_{\mathrm{plasma\_can}} \rightleftharpoons \mathrm{Cre}_{\mathrm{can}}$ |  |
| $v_{\mathrm{transport\_re\_deep\_can}}$ | `transport_re_deep_can` | transport canagliflozin (deep tissue) | $\mathrm{Cre}_{\mathrm{plasma\_can}} \rightleftharpoons \mathrm{Cre}_{\mathrm{deep\_can}}$ |  |
| $v_{\mathrm{iv\_can}}$ | `iv_can` | iv canagliflozin | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_can}}$ | `Flow_ar_ki_can` | inflow kidney canagliflozin | $\mathrm{Car}_{\mathrm{can}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_can}}$ | `Flow_ki_ve_can` | outflow kidney canagliflozin | $\mathrm{Cki}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Cve}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_can}}$ | `Flow_arli_li_can` | arterial inflow liver canagliflozin | $\mathrm{Car}_{\mathrm{can}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_can}}$ | `Flow_arli_hv_can` | flow arterial shunts | $\mathrm{Car}_{\mathrm{can}} \longrightarrow \mathrm{Chv}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_can}}$ | `Flow_po_li_can` | outflow po canagliflozin | $\mathrm{Cpo}_{\mathrm{can}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_can}}$ | `Flow_po_hv_can` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{can}} \longrightarrow \mathrm{Chv}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_can}}$ | `Flow_li_hv_can` | outflow liver canagliflozin | $\mathrm{Cli}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Chv}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_can}}$ | `Flow_hv_ve_can` | outflow hepatic vein canagliflozin | $\mathrm{Chv}_{\mathrm{can}} \longrightarrow \mathrm{Cve}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_can}}$ | `Flow_ve_lu_can` | inflow lung canagliflozin | $\mathrm{Cve}_{\mathrm{can}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_can}}$ | `Flow_lu_ar_can` | outflow lung canagliflozin | $\mathrm{Clu}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Car}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_can}}$ | `Flow_ar_gu_can` | inflow gut canagliflozin | $\mathrm{Car}_{\mathrm{can}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_can}}$ | `Flow_gu_po_can` | outflow gut canagliflozin | $\mathrm{Cgu}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Cpo}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_can}}$ | `Flow_ar_re_can` | inflow rest canagliflozin | $\mathrm{Car}_{\mathrm{can}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_can}}$ | `Flow_re_ve_can` | outflow rest canagliflozin | $\mathrm{Cre}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Cve}_{\mathrm{can}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_m5}}$ | `Flow_ar_ki_m5` | inflow kidney M5 | $\mathrm{Car}_{\mathrm{m5}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_m5}}$ | `Flow_ki_ve_m5` | outflow kidney M5 | $\mathrm{Cki}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Cve}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_m5}}$ | `Flow_arli_li_m5` | arterial inflow liver M5 | $\mathrm{Car}_{\mathrm{m5}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_m5}}$ | `Flow_arli_hv_m5` | flow arterial shunts | $\mathrm{Car}_{\mathrm{m5}} \longrightarrow \mathrm{Chv}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_m5}}$ | `Flow_po_li_m5` | outflow po M5 | $\mathrm{Cpo}_{\mathrm{m5}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_m5}}$ | `Flow_po_hv_m5` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{m5}} \longrightarrow \mathrm{Chv}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_m5}}$ | `Flow_li_hv_m5` | outflow liver M5 | $\mathrm{Cli}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Chv}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_m5}}$ | `Flow_hv_ve_m5` | outflow hepatic vein M5 | $\mathrm{Chv}_{\mathrm{m5}} \longrightarrow \mathrm{Cve}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_m5}}$ | `Flow_ve_lu_m5` | inflow lung M5 | $\mathrm{Cve}_{\mathrm{m5}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_m5}}$ | `Flow_lu_ar_m5` | outflow lung M5 | $\mathrm{Clu}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Car}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_m5}}$ | `Flow_ar_gu_m5` | inflow gut M5 | $\mathrm{Car}_{\mathrm{m5}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_m5}}$ | `Flow_gu_po_m5` | outflow gut M5 | $\mathrm{Cgu}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Cpo}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_m5}}$ | `Flow_ar_re_m5` | inflow rest M5 | $\mathrm{Car}_{\mathrm{m5}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_m5}}$ | `Flow_re_ve_m5` | outflow rest M5 | $\mathrm{Cre}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Cve}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_m7}}$ | `Flow_ar_ki_m7` | inflow kidney M7 | $\mathrm{Car}_{\mathrm{m7}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_m7}}$ | `Flow_ki_ve_m7` | outflow kidney M7 | $\mathrm{Cki}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Cve}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_m7}}$ | `Flow_arli_li_m7` | arterial inflow liver M7 | $\mathrm{Car}_{\mathrm{m7}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_m7}}$ | `Flow_arli_hv_m7` | flow arterial shunts | $\mathrm{Car}_{\mathrm{m7}} \longrightarrow \mathrm{Chv}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_m7}}$ | `Flow_po_li_m7` | outflow po M7 | $\mathrm{Cpo}_{\mathrm{m7}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_m7}}$ | `Flow_po_hv_m7` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{m7}} \longrightarrow \mathrm{Chv}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_m7}}$ | `Flow_li_hv_m7` | outflow liver M7 | $\mathrm{Cli}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Chv}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_m7}}$ | `Flow_hv_ve_m7` | outflow hepatic vein M7 | $\mathrm{Chv}_{\mathrm{m7}} \longrightarrow \mathrm{Cve}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_m7}}$ | `Flow_ve_lu_m7` | inflow lung M7 | $\mathrm{Cve}_{\mathrm{m7}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_m7}}$ | `Flow_lu_ar_m7` | outflow lung M7 | $\mathrm{Clu}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Car}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_m7}}$ | `Flow_ar_gu_m7` | inflow gut M7 | $\mathrm{Car}_{\mathrm{m7}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_m7}}$ | `Flow_gu_po_m7` | outflow gut M7 | $\mathrm{Cgu}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Cpo}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_m7}}$ | `Flow_ar_re_m7` | inflow rest M7 | $\mathrm{Car}_{\mathrm{m7}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_m7}}$ | `Flow_re_ve_m7` | outflow rest M7 | $\mathrm{Cre}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Cve}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{KI\_\_CAN2M7}}$ | `KI__CAN2M7` | UGT1A9 (can -&gt; m7) | $\mathrm{Cki}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{KI\_\_CANEX}}$ | `KI__CANEX` | canagliflozin excretion (CANEX) | $\mathrm{Cki}_{\mathrm{plasma\_can}} \longrightarrow \mathrm{Aurine}_{\mathrm{can}}$ |  |
| $v_{\mathrm{KI\_\_M5EX}}$ | `KI__M5EX` | M5 excretion (M5EX) | $\mathrm{Cki}_{\mathrm{plasma\_m5}} \longrightarrow \mathrm{Aurine}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{KI\_\_M7EX}}$ | `KI__M7EX` | M7 excretion (M7EX) | $\mathrm{Cki}_{\mathrm{plasma\_m7}} \longrightarrow \mathrm{Aurine}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{KI\_\_GLCEX}}$ | `KI__GLCEX` | glucose excretion (GLCEX) | $\mathrm{KI}_{\mathrm{\_fpg}} \longrightarrow \mathrm{KI}_{\mathrm{\_glc\_urine}}$ | $\mathrm{Cki}_{\mathrm{plasma\_can}}$ |
| $v_{\mathrm{LI\_\_CANIM}}$ | `LI__CANIM` | canagliflozin import (CANIM) | $\mathrm{Cli}_{\mathrm{plasma\_can}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_can}}$ |  |
| $v_{\mathrm{LI\_\_CAN2M5}}$ | `LI__CAN2M5` | CAN2M5 (UGT2B4) | $\mathrm{LI}_{\mathrm{\_can}} \longrightarrow \mathrm{LI}_{\mathrm{\_m5}}$ |  |
| $v_{\mathrm{LI\_\_CAN2M7}}$ | `LI__CAN2M7` | CAN2M7 (UGT1A9) | $\mathrm{LI}_{\mathrm{\_can}} \longrightarrow \mathrm{LI}_{\mathrm{\_m7}}$ |  |
| $v_{\mathrm{LI\_\_CAN2M9}}$ | `LI__CAN2M9` | CAN2M9 (CYP3A4) | $\mathrm{LI}_{\mathrm{\_can}} \longrightarrow \mathrm{LI}_{\mathrm{\_m9}}$ |  |
| $v_{\mathrm{LI\_\_M5EX}}$ | `LI__M5EX` | M5 export (M5EX) | $\mathrm{LI}_{\mathrm{\_m5}} \rightleftharpoons \mathrm{Cli}_{\mathrm{plasma\_m5}}$ |  |
| $v_{\mathrm{LI\_\_M7EX}}$ | `LI__M7EX` | M7 export (M7EX) | $\mathrm{LI}_{\mathrm{\_m7}} \rightleftharpoons \mathrm{Cli}_{\mathrm{plasma\_m7}}$ |  |
| $v_{\mathrm{LI\_\_M5BIEX}}$ | `LI__M5BIEX` | M5 biliary excretion (M5BIEX) | $\mathrm{LI}_{\mathrm{\_m5}} \longrightarrow \mathrm{LI}_{\mathrm{\_m5\_bi}}$ |  |
| $v_{\mathrm{LI\_\_M7BIEX}}$ | `LI__M7BIEX` | M7 biliary excretion (M7BIEX) | $\mathrm{LI}_{\mathrm{\_m7}} \longrightarrow \mathrm{LI}_{\mathrm{\_m7\_bi}}$ |  |
| $v_{\mathrm{LI\_\_M9BIEX}}$ | `LI__M9BIEX` | M9 biliary excretion (M9BIEX) | $\mathrm{LI}_{\mathrm{\_m9}} \longrightarrow \mathrm{LI}_{\mathrm{\_m9\_bi}}$ |  |
| $v_{\mathrm{LI\_\_M5EHC}}$ | `LI__M5EHC` | M5 bile flow into the intestine | $\mathrm{LI}_{\mathrm{\_m5\_bi}} \longrightarrow \mathrm{Cgu}_{\mathrm{m5}}$ |  |
| $v_{\mathrm{LI\_\_M7EHC}}$ | `LI__M7EHC` | M7 bile flow into the intestine | $\mathrm{LI}_{\mathrm{\_m7\_bi}} \longrightarrow \mathrm{Cgu}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{LI\_\_M9EHC}}$ | `LI__M9EHC` | M9 bile flow into the intestine | $\mathrm{LI}_{\mathrm{\_m9\_bi}} \longrightarrow \mathrm{Cgu}_{\mathrm{m9}}$ |  |
| $v_{\mathrm{GU\_\_CANABS}}$ | `GU__CANABS` | CANABS | $\mathrm{Cgu}_{\mathrm{can}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_can}}$ |  |
| $v_{\mathrm{GU\_\_CANEXC}}$ | `GU__CANEXC` | CANEXC (feces) | $\mathrm{Cgu}_{\mathrm{can}} \longrightarrow \mathrm{Afeces}_{\mathrm{can}}$ |  |
| $v_{\mathrm{GU\_\_M5HYD}}$ | `GU__M5HYD` | M5 hydrolysis (M5HYD) | $\mathrm{Cgu}_{\mathrm{m5}} \longrightarrow \mathrm{Cgu}_{\mathrm{can}}$ |  |
| $v_{\mathrm{GU\_\_M7HYD}}$ | `GU__M7HYD` | M7 hydrolysis (M7HYD) | $\mathrm{Cgu}_{\mathrm{m7}} \longrightarrow \mathrm{Cgu}_{\mathrm{can}}$ |  |
| $v_{\mathrm{GU\_\_M5EXC}}$ | `GU__M5EXC` | M5 excretion (M5EXC, feces, hydrolysed to canagliflozin) | $\mathrm{Cgu}_{\mathrm{m5}} \longrightarrow \mathrm{Afeces}_{\mathrm{can}}$ |  |
| $v_{\mathrm{GU\_\_M7EXC}}$ | `GU__M7EXC` | M7 excretion (M7EXC, feces) | $\mathrm{Cgu}_{\mathrm{m7}} \longrightarrow \mathrm{Afeces}_{\mathrm{m7}}$ |  |
| $v_{\mathrm{GU\_\_M9EXC}}$ | `GU__M9EXC` | M9 excretion (M9EXC, feces) | $\mathrm{Cgu}_{\mathrm{m9}} \longrightarrow \mathrm{Afeces}_{\mathrm{m9}}$ |  |
| $v_{\mathrm{GU\_\_dissolution\_can}}$ | `GU__dissolution_can` | dissolution canagliflozin | $\mathrm{GU}_{\mathrm{\_can\_stomach}} \longrightarrow \mathrm{Cgu}_{\mathrm{can}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_lu\_can}} &= \frac{\mathrm{ftissue}_{\mathrm{can}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_can}} \cdot \mathrm{Kp}_{\mathrm{can}} - \mathrm{Clu}_{\mathrm{can}}\right) \\[1ex]
v_{\mathrm{transport\_re\_can}} &= \frac{\mathrm{ftissue}_{\mathrm{can}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_can}} \cdot \mathrm{Kp}_{\mathrm{can}} - \mathrm{Cre}_{\mathrm{can}}\right) \\[1ex]
v_{\mathrm{transport\_re\_deep\_can}} &= \frac{\mathrm{ftissue}_{\mathrm{deep\_can}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_can}} \cdot \mathrm{Kp}_{\mathrm{deep\_can}} - \mathrm{Cre}_{\mathrm{deep\_can}}\right) \\[1ex]
v_{\mathrm{iv\_can}} &= \frac{\mathrm{Ki}_{\mathrm{can}} \cdot \mathrm{IVDOSE}_{\mathrm{can}}}{\mathrm{Mr}_{\mathrm{can}}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_can}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_can}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_can}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_can}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_can}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_can}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_can}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_can}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_can}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_can}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_can}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_can}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_can}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{can}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_can}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_m5}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_m5}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_m5}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_m5}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_m5}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_m5}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_m5}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_m5}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_m5}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_m5}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_m5}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_m5}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_m5}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_m5}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_m7}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_m7}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_m7}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_m7}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_m7}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_m7}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_m7}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_m7}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_m7}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_m7}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_m7}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_m7}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_m7}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_m7}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{KI\_\_CAN2M7}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot f_{\mathrm{ugt1a9}} \cdot \mathrm{KI}_{\mathrm{\_CAN2M7\_k}} \cdot \mathrm{Vki}_{\mathrm{tissue}} \cdot \mathrm{Cki}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{KI\_\_CANEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_fu\_can}} \cdot \mathrm{KI}_{\mathrm{\_CANEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_can}} \\[1ex]
v_{\mathrm{KI\_\_M5EX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_f\_oat}} \cdot \mathrm{KI}_{\mathrm{\_M5EX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_m5}} \\[1ex]
v_{\mathrm{KI\_\_M7EX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_f\_oat}} \cdot \mathrm{KI}_{\mathrm{\_M7EX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_m7}} \\[1ex]
v_{\mathrm{KI\_\_GLCEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_RTG\_splay}} \cdot \ln\mathopen{}\left(1 + \exp\mathopen{}\left(\frac{\mathrm{KI}_{\mathrm{\_pg}} - \mathrm{KI}_{\mathrm{\_RTG}}}{\mathrm{KI}_{\mathrm{\_RTG\_splay}}}\right)\right) \\[1ex]
v_{\mathrm{LI\_\_CANIM}} &= \mathrm{LI}_{\mathrm{\_CANIM\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{Cli}_{\mathrm{plasma\_can}} - \mathrm{LI}_{\mathrm{\_can}}\right) \\[1ex]
v_{\mathrm{LI\_\_CAN2M5}} &= \mathrm{LI}_{\mathrm{\_f\_ugt2b4}} \cdot \mathrm{LI}_{\mathrm{\_CAN2M5\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_can}} \\[1ex]
v_{\mathrm{LI\_\_CAN2M7}} &= f_{\mathrm{ugt1a9}} \cdot \mathrm{LI}_{\mathrm{\_CAN2M7\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_can}} \\[1ex]
v_{\mathrm{LI\_\_CAN2M9}} &= \mathrm{LI}_{\mathrm{\_f\_cyp3a4}} \cdot \mathrm{LI}_{\mathrm{\_CAN2M9\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_can}} \\[1ex]
v_{\mathrm{LI\_\_M5EX}} &= \mathrm{LI}_{\mathrm{\_M5EX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_m5}} - \mathrm{Cli}_{\mathrm{plasma\_m5}}\right) \\[1ex]
v_{\mathrm{LI\_\_M7EX}} &= \mathrm{LI}_{\mathrm{\_M7EX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_m7}} - \mathrm{Cli}_{\mathrm{plasma\_m7}}\right) \\[1ex]
v_{\mathrm{LI\_\_M5BIEX}} &= \mathrm{LI}_{\mathrm{\_M5BIEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_m5}} \\[1ex]
v_{\mathrm{LI\_\_M7BIEX}} &= \mathrm{LI}_{\mathrm{\_M7BIEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_m7}} \\[1ex]
v_{\mathrm{LI\_\_M9BIEX}} &= \mathrm{LI}_{\mathrm{\_M9BIEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_m9}} \\[1ex]
v_{\mathrm{LI\_\_M5EHC}} &= v_{\mathrm{LI\_\_M5BIEX}} \\[1ex]
v_{\mathrm{LI\_\_M7EHC}} &= v_{\mathrm{LI\_\_M7BIEX}} \\[1ex]
v_{\mathrm{LI\_\_M9EHC}} &= v_{\mathrm{LI\_\_M9BIEX}} \\[1ex]
v_{\mathrm{GU\_\_CANABS}} &= \mathrm{GU}_{\mathrm{\_F\_can\_abs}} \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_CANEXC}} &= \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_can\_abs}}\right) \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_M5HYD}} &= \mathrm{GU}_{\mathrm{\_GLUHYD\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{GU\_\_M7HYD}} &= \mathrm{GU}_{\mathrm{\_GLUHYD\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{GU\_\_M5EXC}} &= \mathrm{GU}_{\mathrm{\_METEXC\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{m5}} \\[1ex]
v_{\mathrm{GU\_\_M7EXC}} &= \mathrm{GU}_{\mathrm{\_METEXC\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{m7}} \\[1ex]
v_{\mathrm{GU\_\_M9EXC}} &= \mathrm{GU}_{\mathrm{\_METEXC\_k}} \cdot \mathrm{Vlumen} \cdot \mathrm{Cgu}_{\mathrm{m9}} \\[1ex]
v_{\mathrm{GU\_\_dissolution\_can}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_Ka\_dis\_can}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{can}}}{\mathrm{Mr}_{\mathrm{can}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_can}} - v_{\mathrm{Flow\_ki\_ve\_can}} - v_{\mathrm{KI\_\_CAN2M7}} - v_{\mathrm{KI\_\_CANEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_can}} + v_{\mathrm{Flow\_po\_li\_can}} - v_{\mathrm{Flow\_li\_hv\_can}} - v_{\mathrm{LI\_\_CANIM}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_can}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_can}} + v_{\mathrm{Flow\_ve\_lu\_can}} - v_{\mathrm{Flow\_lu\_ar\_can}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_can}} - v_{\mathrm{Flow\_gu\_po\_can}} + v_{\mathrm{GU\_\_CANABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_can}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_can}} - v_{\mathrm{transport\_re\_deep\_can}} + v_{\mathrm{Flow\_ar\_re\_can}} - v_{\mathrm{Flow\_re\_ve\_can}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_can}} - v_{\mathrm{Flow\_arli\_li\_can}} - v_{\mathrm{Flow\_arli\_hv\_can}} + v_{\mathrm{Flow\_lu\_ar\_can}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_can}} - v_{\mathrm{Flow\_ar\_re\_can}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_can}} + v_{\mathrm{Flow\_ki\_ve\_can}} + v_{\mathrm{Flow\_hv\_ve\_can}} - v_{\mathrm{Flow\_ve\_lu\_can}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_can}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_can}} - v_{\mathrm{Flow\_po\_hv\_can}} + v_{\mathrm{Flow\_gu\_po\_can}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_can}} + v_{\mathrm{Flow\_po\_hv\_can}} + v_{\mathrm{Flow\_li\_hv\_can}} - v_{\mathrm{Flow\_hv\_ve\_can}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_can}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_can}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{deep\_can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_deep\_can}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{can}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_CANEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_m5}} - v_{\mathrm{Flow\_ki\_ve\_m5}} - v_{\mathrm{KI\_\_M5EX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_m5}} + v_{\mathrm{Flow\_po\_li\_m5}} - v_{\mathrm{Flow\_li\_hv\_m5}} + v_{\mathrm{LI\_\_M5EX}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_m5}} - v_{\mathrm{Flow\_lu\_ar\_m5}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_m5}} - v_{\mathrm{Flow\_gu\_po\_m5}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_m5}} - v_{\mathrm{Flow\_re\_ve\_m5}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{m5}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_m5}} - v_{\mathrm{Flow\_arli\_li\_m5}} - v_{\mathrm{Flow\_arli\_hv\_m5}} + v_{\mathrm{Flow\_lu\_ar\_m5}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_m5}} - v_{\mathrm{Flow\_ar\_re\_m5}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_m5}} + v_{\mathrm{Flow\_hv\_ve\_m5}} - v_{\mathrm{Flow\_ve\_lu\_m5}} + v_{\mathrm{Flow\_re\_ve\_m5}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{m5}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_m5}} - v_{\mathrm{Flow\_po\_hv\_m5}} + v_{\mathrm{Flow\_gu\_po\_m5}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_m5}} + v_{\mathrm{Flow\_po\_hv\_m5}} + v_{\mathrm{Flow\_li\_hv\_m5}} - v_{\mathrm{Flow\_hv\_ve\_m5}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{m5}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_M5EX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_m7}} - v_{\mathrm{Flow\_ki\_ve\_m7}} + v_{\mathrm{KI\_\_CAN2M7}} - v_{\mathrm{KI\_\_M7EX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_m7}} + v_{\mathrm{Flow\_po\_li\_m7}} - v_{\mathrm{Flow\_li\_hv\_m7}} + v_{\mathrm{LI\_\_M7EX}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_m7}} - v_{\mathrm{Flow\_lu\_ar\_m7}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_m7}} - v_{\mathrm{Flow\_gu\_po\_m7}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_m7}} - v_{\mathrm{Flow\_re\_ve\_m7}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{m7}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_m7}} - v_{\mathrm{Flow\_arli\_li\_m7}} - v_{\mathrm{Flow\_arli\_hv\_m7}} + v_{\mathrm{Flow\_lu\_ar\_m7}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_m7}} - v_{\mathrm{Flow\_ar\_re\_m7}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ki\_ve\_m7}} + v_{\mathrm{Flow\_hv\_ve\_m7}} - v_{\mathrm{Flow\_ve\_lu\_m7}} + v_{\mathrm{Flow\_re\_ve\_m7}}}{\mathrm{Vve}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{m7}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_m7}} - v_{\mathrm{Flow\_po\_hv\_m7}} + v_{\mathrm{Flow\_gu\_po\_m7}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_m7}} + v_{\mathrm{Flow\_po\_hv\_m7}} + v_{\mathrm{Flow\_li\_hv\_m7}} - v_{\mathrm{Flow\_hv\_ve\_m7}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{m7}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_M7EX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{can}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vlumen}} \Bigl( -v_{\mathrm{GU\_\_CANABS}} - v_{\mathrm{GU\_\_CANEXC}} + v_{\mathrm{GU\_\_M5HYD}} + v_{\mathrm{GU\_\_M7HYD}} \\
&\quad {} + v_{\mathrm{GU\_\_dissolution\_can}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{can}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_CANEXC}} + v_{\mathrm{GU\_\_M5EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_M5EHC}} - v_{\mathrm{GU\_\_M5HYD}} - v_{\mathrm{GU\_\_M5EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_M7EHC}} - v_{\mathrm{GU\_\_M7HYD}} - v_{\mathrm{GU\_\_M7EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{m7}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_M7EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{m9}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_M9EHC}} - v_{\mathrm{GU\_\_M9EXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{m9}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_M9EXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_glc\_urine}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_GLCEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_can}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_CANIM}} - v_{\mathrm{LI\_\_CAN2M5}} - v_{\mathrm{LI\_\_CAN2M7}} - v_{\mathrm{LI\_\_CAN2M9}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m5}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_CAN2M5}} - v_{\mathrm{LI\_\_M5EX}} - v_{\mathrm{LI\_\_M5BIEX}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m7}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_CAN2M7}} - v_{\mathrm{LI\_\_M7EX}} - v_{\mathrm{LI\_\_M7BIEX}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m9}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_CAN2M9}} - v_{\mathrm{LI\_\_M9BIEX}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m5\_bi}}}{\mathrm{d} t} &= v_{\mathrm{LI\_\_M5BIEX}} - v_{\mathrm{LI\_\_M5EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m7\_bi}}}{\mathrm{d} t} &= v_{\mathrm{LI\_\_M7BIEX}} - v_{\mathrm{LI\_\_M7EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_m9\_bi}}}{\mathrm{d} t} &= v_{\mathrm{LI\_\_M9BIEX}} - v_{\mathrm{LI\_\_M9EHC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{can}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_dissolution\_can}} \cdot \mathrm{Mr}_{\mathrm{can}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{can}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_can}} \cdot \mathrm{Mr}_{\mathrm{can}} + \mathrm{Ri}_{\mathrm{can}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_can}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{can}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_RTG\_int}}}{\mathrm{d} t} &= \mathrm{KI}_{\mathrm{\_RTG}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{KI}_{\mathrm{\_RTG\_time}}}{\mathrm{d} t} &= 1 \qquad \text{(rate rule)}
\end{aligned}
$$
