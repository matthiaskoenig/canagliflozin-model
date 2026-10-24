#set page(paper: "a4", margin: 2cm)
#set text(size: 10pt)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")
// a table longer than a page continues on the next page, its
// caption above it and its header repeated
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)

#align(center, text(size: 16pt, weight: "bold")[Canagliflozin PBPK\/PD model: fit PD])

= Methods: Canagliflozin PBPK\/PD model: fit PD

== Parameters and data

4 parameters were optimized: EC50 reduction in RTG (#raw("KI__RTG_E50")), baseline RTG (#raw("KI__RTG_base")), FPG effect on RTG (#raw("KI__RTG_m_fpg")) and maximal relative reduction of the RTG (#raw("KI__RTG_max_inhibition")). The parameters of the adopted fit PK\_20261019\_103422\_\_858e3 were fixed at their fitted values.

A fit mapping is a curve of a study, the data and the observable of the model it is compared with. The fit has 67 fit mappings of training data with 227 data points, whose residuals enter the objective; and 36 fit mappings of validation data with 174 data points, which were simulated and evaluated with the fitted parameters but not fitted. The fit was set up and run with sbmlsim #cite(<Koenig2026_sbmlsim>).

== Objective function

The parameters were estimated by minimizing the objective function

$ F(arrow(p)) = 1/2 sum_k sum_i rho(w_(i,k) r_(i,k)(arrow(p))^2) $

where $k$ runs over the fit mappings of the training data and $i$ over their data points, $r_(i,k)$ is the residual, $w_(i,k) = w_k w^p_(i,k)$ the weight of the data point and $rho$ the loss function, applied to the squared weighted residual $z = w_(i,k) r_(i,k)^2$. The loss function is linear, $rho(z) = z$, i.e. a standard least squares problem.

The residuals are normalized by the mean $overline(y)_k$ of the data of their curve, which makes curves of different quantities and magnitudes comparable:

$ r_(i,k) = (y_(i,k) - f_k(x_(i,k), arrow(p))) / overline(y)_k $

The weight of curve $k$ is $w_k = n_k / N_k$, the weight $n_k$ of its fit mapping (the weight its fit mapping collection assigns, 1 by default, or, for a collection which uses the weights of its mappings, the weight of the mapping, by default the number of subjects of its data) divided by the number $N_k$ of its data points.

A data point is weighted with the inverse of its coefficient of variation, $w^p_(i,k) = |y_(i,k)| / sigma_(i,k)$, with $sigma_(i,k)$ the standard deviation of the data point, or its standard error for data without a standard deviation. An error of zero is missing, a missing error of a curve with errors is replaced by the largest error of the curve, and the data points of a curve without errors have the weight $w^p_(i,k) = 2$, the weight of a coefficient of variation of 0.5.

== Optimization

The optimizer searched the parameters in log10 space within their bounds; bounds, values and intervals are given in the units of the fit parameters, the units of the table of the parameters.

The objective was minimized in 3 runs with differential evolution #cite(<Storn1997>) of SciPy #cite(<Virtanen2020>) within the bounds of the parameters, with the strategy #raw("best1bin"), a population of 15 times the number of parameters, at most 1000 generations, the relative tolerance 0.01 of convergence, the recombination constant 0.7 and a mutation dithered between 0.5 and 1. The initial population of a run was drawn by latin hypercube sampling #cite(<McKay1979>), with a seed of every run derived from the seed 1234 of the fit. The best member of the final population was polished with the L-BFGS-B method of SciPy.

The convergence of the runs was assessed from the traces of their cost and the waterfall plot of their final costs, and the parameter set with the lowest cost was used.

The models were simulated with libRoadRunner #cite(<Welsh2023>) and its integrator CVODE #cite(<Hindmarsh2005>) with the relative tolerance $10^(-6)$ and the absolute tolerances $10^(-12)$ of an amount, $10^(-12)$ of a concentration and $10^(-6)$ of the other states, which for a species in a concentration is multiplied by the initial volume of its compartment. It ran with the variable step size of libRoadRunner, i.e. with an output at every step of the integrator. A data point at the time of a change after the start of a simulation, e.g. a dose or the reset of a collection, was compared with the state before the change, except the first data point of a curve with data at later times, which starts a collection and was compared with the state after the change.

== Goodness of fit

The goodness of fit is given per kind of data (training data and validation data) by metrics over its $n$ data points with the residuals $e_i = y_i - f(x_i, hat(arrow(p)))$ at the fitted parameters $hat(arrow(p))$, the mean squared error, its root and the root mean squared error normalized by the mean $overline(y)_(k(i))$ of the data of the curve of a point:

$ "MSE" = 1/n sum_(i=1)^n e_i^2, quad "RMSE" = sqrt("MSE"), quad "NRMSE" = sqrt(1/n sum_(i=1)^n (e_i / overline(y)_(k(i)))^2) $

The root mean square of the residuals of the objective, i.e. what the fit minimizes, and the coefficient of determination:

$ "RMSE"_w = sqrt(1/n sum_(i=1)^n rho(w_i r_i^2)), quad R^2 = 1 - (sum_i e_i^2) / (sum_i (y_i - overline(y))^2) $

The predictions of a non-linear model are no linear regression of the data, so $R^2$ can be negative: the prediction is worse than the mean of the data. The information criteria of Akaike #cite(<Akaike1974>) and Schwarz #cite(<Schwarz1978>) with the number $n_p$ of fitted parameters are those of a least squares fit with normally distributed residuals, up to an additive constant, so only differences between models fitted to the same data are meaningful:

$ "AIC" = n ln("MSE") + 2 n_p, quad "BIC" = n ln("MSE") + n_p ln(n) $

The percentage of the data points whose prediction $f_i = f(x_i, hat(arrow(p)))$ lies within twofold of the data is taken over the $n_(+)$ data points with positive data $y_i > 0$ and a positive prediction $f_i > 0$; the others have no ratio and are not counted, and a kind of data without such a point has no percentage:

$ P_2 = 100 / n_(+) abs(\{ i : 1/2 <= f_i / y_i <= 2 \}) $

The goodness of fit plot shows the predictions against the data on logarithmic axes, with the lines of twofold $f = 2y$ and $f = y/2$. The Bland-Altman plot #cite(<Bland1986>) shows the ratio of prediction and data as $d_i = log_10(f_i / y_i)$ against the geometric mean $sqrt(f_i y_i)$ for the data points with positive values, with the bias $overline(d)$ and the limits of agreement $overline(d) plus.minus 1.96 s_d$, with the sample standard deviation $s_d$ of $d_i$, of the training data; they are read as the fold factors $10^(overline(d))$ and $10^(overline(d) plus.minus 1.96 s_d)$.

== Identifiability

The identifiability of the parameters was analysed with the profile likelihood #cite(<Raue2009>) #cite(<Kreutz2013>). The profile of a parameter is the lowest objective with the parameter fixed:

$ "PL"(p_j) = min_(p_(l != j)) F(arrow(p)) $

At every point of a scan the other parameters were re-optimized from the previous point with the least squares optimizer of SciPy with the relative step 0.05. A scan ran from the optimum in both directions in the space of the optimizer, with steps in decades of the parameter, starting at 0.1. A step which raised the objective by more than 0.2 of the distance between the objective at the optimum and the threshold was reduced by the factor 2 and repeated, down to 0.01, and the step after one which raised it by less than that divided by the factor was enlarged by the factor, up to 1. A scan stopped at the threshold, at the bound of the parameter, at a point which failed or after 50 points.

The confidence intervals are the values at which the profile crosses the threshold of the likelihood ratio test

$ F_"thr" = F_"min" + chi^2_alpha ("df") / 2 $

with $F_"min"$ the lowest objective of the fit and of all profiles and $chi^2_alpha ("df")$ the quantile of the $chi^2$ distribution at the confidence level $alpha = 0.95$ with df \= 1 degrees of freedom, i.e. 1.92 above the lowest objective. The threshold has this confidence level if $F$ is the negative log-likelihood of the data up to a constant, i.e. if the weighted residuals are independent and normally distributed with unit variance; otherwise the level is approximate. A crossing is interpolated between two points of the profile, on the logarithm of a parameter on a logarithmic scale. A parameter is identifiable if its profile reaches the threshold within the scan on both sides of the optimum, i.e. its confidence interval is finite; practically non-identifiable towards the lower bound if its profile reaches the threshold above the optimum but not below it within the scan, which ends at the lower bound or after 50 points; practically non-identifiable towards the upper bound if its profile reaches the threshold below the optimum but not above it within the scan, which ends at the upper bound or after 50 points; practically non-identifiable if its profile reaches the threshold on neither side within the scans, which end at the bounds or after 50 points, and is not flat; and structurally non-identifiable if its profile is flat on both sides. A side of a profile is flat if it rises by less than 0.05 of the distance between the lowest objective and the threshold, and a profile with a point which failed or did not converge is not classified. The profile likelihood is preferred over the intervals of the Fisher information, its intervals are invariant under a transformation of the parameters and can be asymmetric #cite(<Wieland2021>).

The Fisher information is the local alternative to the profiles: it is the Gauss-Newton approximation of the curvature of the objective at the optimum, from the Jacobian $J$ of the weighted residuals of the training data with respect to the parameters $arrow(p)$ in the space of the optimizer, computed by central finite differences with the step $h_j = epsilon max(|p_j|, 1), space epsilon = 10^(-6)$ of the parameter $p_j$:

$ I = J^top J, quad "cov" = sigma^2 I^(-1), quad sigma^2 = (2 F) / (n - n_p) $

with the number $n$ of data points of the training data and the number $n_p$ of parameters. The information has rank 4 of 4, the number of its eigenvalues above $10^(-8)$ of the largest one, and the condition number 377; the covariance of an information of a lower rank is computed with the pseudo-inverse. The Wald intervals are $hat(p)_j plus.minus t_((1+alpha)/2, n-n_p) "SE"_j$ with the standard errors $"SE"_j = sqrt("cov"_(j j))$ at the confidence level $alpha = 0.95$, transformed back into the units of the fit parameters.

== Provenance

The fit PD\_20261019\_201254\_\_61546 was run on 2026-10-19 18:13:02 UTC with sbmlsim 0.10.0 #cite(<Koenig2026_sbmlsim>), libRoadRunner 2.10.0 #cite(<Welsh2023>), SciPy 1.18.1 #cite(<Virtanen2020>), NumPy 2.5.3 #cite(<Harris2020>) and Python 3.14.4 (seed 1234). The models and data were those of commit #raw("e2644f489b973f8d28b845906e093e3af1870fe1") of #raw("/home/mkoenig/git/pkdb_models-canagliflozin"); their SHA-256 checksums are listed in #ref(<tab:checksums:PD_20261019_201254__61546>). The fit kept the values #raw("ftissue_can") \= 1.08931, #raw("Kp_can") \= 0.685123, #raw("ftissue_deep_can") \= 0.00663007, #raw("Kp_deep_can") \= 9.54277, #raw("GU__CANABS_k") \= 0.0152774, #raw("GU__F_can_abs") \= 0.66566, #raw("LI__CAN2M5_k") \= 0.0254215, #raw("LI__CAN2M7_k") \= 0.0351472, #raw("LI__CAN2M9_k") \= 0.016767, #raw("LI__M5BIEX_k") \= 0.0281205, #raw("LI__M7BIEX_k") \= 0.0569284, #raw("GU__GLUHYD_k") \= 0.00697926, #raw("KI__CANEX_f") \= 1.27294, #raw("KI__M5EX_f") \= 0.551072 and #raw("KI__M7EX_f") \= 0.801255 of the model fixed.

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([File], [SHA-256]),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_Fig1.tsv"),
  raw("11309517d87d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_Fig2.tsv"),
  raw("ac40152c7c3e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_Tab2.tsv"),
  raw("dbf8674d6ca0..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_Tab2A.tsv"),
  raw("0d692d95ddf4..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_Tab3.tsv"),
  raw("474fc25c69c2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_TabGroups.tsv"),
  raw("7df0b6e2b74b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Chen2015/.Chen2015_TabInterventions.tsv"),
  raw("caa47749503b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Fig1.tsv"),
  raw("99cbb98d385c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Fig2.tsv"),
  raw("17ddd3ee74e9..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Fig3.tsv"),
  raw("a9788d138f8e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Tab2.tsv"),
  raw("de641741be66..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Tab3.tsv"),
  raw("003083a994f7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_Tab3A.tsv"),
  raw("4ab4230cd24c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_TabGroups.tsv"),
  raw("fcbd9926a0bc..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2012/.Devineni2012_TabInterventions.tsv"),
  raw("cc994c72c23e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Fig1.tsv"),
  raw("d3151c60e782..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Fig2.tsv"),
  raw("d54b41c9d9f3..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Tab2.tsv"),
  raw("a6e88864f675..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Tab2A.tsv"),
  raw("3f08200106ae..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Tab3.tsv"),
  raw("f10df8a57a2c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_Tab3A.tsv"),
  raw("9877e8bf611b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_TabGroups.tsv"),
  raw("5ca1502e81fc..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2013/.Devineni2013_TabInterventions.tsv"),
  raw("cb41feee3128..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_Fig2.tsv"),
  raw("04b9e40bb1dc..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_Fig3.tsv"),
  raw("ba3c236103c1..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_Tab1.tsv"),
  raw("096cbdc6db9e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_Tab2.tsv"),
  raw("c5d09da767d6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_Tab2A.tsv"),
  raw("c6dda93b2bbf..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_TabGroups.tsv"),
  raw("7b29e1f269b4..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2014/.Devineni2014_TabInterventions.tsv"),
  raw("e0063bf738d2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig2.tsv"),
  raw("c1a175827351..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig3.tsv"),
  raw("088ab9028590..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig4.tsv"),
  raw("b424a9f15e15..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig5.tsv"),
  raw("ddfbd5c57f48..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig6.tsv"),
  raw("5976a606bf1f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Fig7.tsv"),
  raw("188d2acb983d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Tab1.tsv"),
  raw("071331a4faa2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Tab2A.tsv"),
  raw("f4135efe551d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Tab2B.tsv"),
  raw("292e0ef0a05b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_Tab3.tsv"),
  raw("1f36409e81fd..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_TabGroups.tsv"),
  raw("f83495e58cf1..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015/.Devineni2015_TabInterventions.tsv"),
  raw("78abd7831e94..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_Fig1.tsv"),
  raw("3d3fbde8968b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_Tab1.tsv"),
  raw("ec81b99e0ca6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_Tab1A.tsv"),
  raw("6a4903dd4e4f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_Tab2.tsv"),
  raw("04b43205a186..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_Tab2A.tsv"),
  raw("844240dc5dc6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_TabGroups.tsv"),
  raw("4f4c51134a10..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015a/.Devineni2015a_TabInterventions.tsv"),
  raw("4331918feabe..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_Fig2.tsv"),
  raw("8635c6b62220..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_Tab1.tsv"),
  raw("3293450f44b2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_Tab1A.tsv"),
  raw("e157aa24d566..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_Tab2.tsv"),
  raw("8fd0702a9085..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_TabGroups.tsv"),
  raw("2c50e3e696b0..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015b/.Devineni2015b_TabInterventions.tsv"),
  raw("f13ca85bf9c7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Fig2.tsv"),
  raw("306cecb5e301..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Fig3.tsv"),
  raw("afda21ad9861..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Fig4.tsv"),
  raw("f008c659cdb0..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Fig5.tsv"),
  raw("5401fabf3340..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab2.tsv"),
  raw("b9496b829298..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab2A.tsv"),
  raw("c5f0a0b8b56c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab3.tsv"),
  raw("023b75ee6d50..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab3A.tsv"),
  raw("c6090bb491e7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab5.tsv"),
  raw("a119dc77b0c6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_Tab5A.tsv"),
  raw("1b57262d6247..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_TabGroups.tsv"),
  raw("4beb338545d4..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015c/.Devineni2015c_TabInterventions.tsv"),
  raw("f37f547ca7ba..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Fig2.tsv"),
  raw("bcda389be253..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Fig3.tsv"),
  raw("e5050775f881..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Fig4.tsv"),
  raw("b757d7034480..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Tab2.tsv"),
  raw("4b7347040170..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Tab2A.tsv"),
  raw("a0342074e785..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Tab3.tsv"),
  raw("71c08387ea36..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Tab3A.tsv"),
  raw("496033a5bd0b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_Tab4.tsv"),
  raw("dc77a141fa4a..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_TabGroups.tsv"),
  raw("a4556016f856..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015d/.Devineni2015d_TabInterventions.tsv"),
  raw("3b735ad4f8cf..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_Fig1.tsv"),
  raw("1baed35b0680..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_Fig2.tsv"),
  raw("5ad4836b7e41..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_Tab1.tsv"),
  raw("f93e791bfcd7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_Tab2.tsv"),
  raw("cb889fba805d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_Tab3.tsv"),
  raw("96ff9591e565..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_TabGroups.tsv"),
  raw("57bd46aaa7a8..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2015e/.Devineni2015e_TabInterventions.tsv"),
  raw("8ece422a882b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_Fig2.tsv"),
  raw("84245d2ba2bf..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_Fig3.tsv"),
  raw("b9328fee4365..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_Tab2.tsv"),
  raw("5ea0640764b6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_Tab3.tsv"),
  raw("e02222b8d262..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_Tab3A.tsv"),
  raw("98c55b823920..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_TabGroups.tsv"),
  raw("2dee9dc252e2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Devineni2016/.Devineni2016_TabInterventions.tsv"),
  raw("ffda46d473f9..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Fig2.tsv"),
  raw("91ee6b63d891..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Fig3.tsv"),
  raw("8333b049b72c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Fig4.tsv"),
  raw("a64350254d61..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Fig5.tsv"),
  raw("da49dae531f0..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Fig6.tsv"),
  raw("f85056a3fc84..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Tab2.tsv"),
  raw("6c281cbfdb3b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_Tab2A.tsv"),
  raw("c606b0fb2fa3..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_TabGroups.tsv"),
  raw("c0595c0aae4f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Iijima2015/.Iijima2015_TabInterventions.tsv"),
  raw("9cb67d9d726c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Fig1.tsv"),
  raw("e5060ccd6762..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Fig2.tsv"),
  raw("88ac0a7f691b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Fig4.tsv"),
  raw("d26a2084dfda..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Tab3.tsv"),
  raw("d1cbc8c27327..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Tab3A.tsv"),
  raw("23f0511c9c1a..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_Tab4.tsv"),
  raw("1e0705ae5817..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_TabGroups.tsv"),
  raw("1bf0d899848b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Inagaki2014/.Inagaki2014_TabInterventions.tsv"),
  raw("89b6e7ded71c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Fig2.tsv"),
  raw("0131c0f0b1ac..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Fig3.tsv"),
  raw("483cf8f95e92..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Fig4.tsv"),
  raw("bb43f00e42d6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Tab1.tsv"),
  raw("0dfa5cb6b43f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Tab2.tsv"),
  raw("442a8708b838..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_Tab3.tsv"),
  raw("d410ffe2a7ff..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_TabGroups.tsv"),
  raw("d345e2dc019f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Kinoshita2015/.Kinoshita2015_TabInterventions.tsv"),
  raw("fb9adf4562f1..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Fig3.tsv"),
  raw("cd8a21860345..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab1.tsv"),
  raw("d24d6386dba1..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab1A.tsv"),
  raw("6c0db0ec5eae..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab2.tsv"),
  raw("2fb24299329d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab3.tsv"),
  raw("95f5dc03d10b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab4.tsv"),
  raw("aa5a15782060..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab5.tsv"),
  raw("aab8440e3e6e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab5A.tsv"),
  raw("6bd2a5f313cf..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab6.tsv"),
  raw("1c8f1853c13b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_Tab6A.tsv"),
  raw("21d10f2b200f..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_TabGroups.tsv"),
  raw("d6a0315899cd..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mamidi2014/.Mamidi2014_TabInterventions.tsv"),
  raw("1df63c1b445c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mohamed2019/.Mohamed2019_Fig4.tsv"),
  raw("dab10af787e0..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mohamed2019/.Mohamed2019_Tab5.tsv"),
  raw("85e7d382c1ed..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mohamed2019/.Mohamed2019_TabGroups.tsv"),
  raw("ed0881ef74b8..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Mohamed2019/.Mohamed2019_TabInterventions.tsv"),
  raw("41528e011971..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Murphy2015/.Murphy2015_Fig1.tsv"),
  raw("3cc61caa2896..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Murphy2015/.Murphy2015_Tab1.tsv"),
  raw("ecaea8f10002..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Murphy2015/.Murphy2015_Tab2.tsv"),
  raw("5fabd2ff3788..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Murphy2015/.Murphy2015_TabGroups.tsv"),
  raw("675eac9484fa..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Murphy2015/.Murphy2015_TabInterventions.tsv"),
  raw("f93a05f0c73c..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2011/.Sha2011_Fig1.tsv"),
  raw("b42af877b45a..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2011/.Sha2011_Fig2.tsv"),
  raw("3bcd3329fb92..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2011/.Sha2011_TabGroups.tsv"),
  raw("e408392ed910..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2011/.Sha2011_TabInterventions.tsv"),
  raw("984b740a83a7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Fig2.tsv"),
  raw("d3e08cc01af2..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Fig4.tsv"),
  raw("b4933da0e2d6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Fig5.tsv"),
  raw("637494be2da3..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Fig6.tsv"),
  raw("2fcf7d202af6..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Fig7.tsv"),
  raw("5b7ac8dec783..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Tab2.tsv"),
  raw("6b6e3a4b6df8..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Tab2A.tsv"),
  raw("ddd07c215259..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_Tab3.tsv"),
  raw("60ed6fab26bc..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_TabGroups.tsv"),
  raw("93df6598e18b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2014/.Sha2014_TabInterventions.tsv"),
  raw("bde1cbe4c5f4..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2015/.Sha2015_Fig2.tsv"),
  raw("f709539e223d..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2015/.Sha2015_Fig3.tsv"),
  raw("76562e87e8de..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2015/.Sha2015_TabGroups.tsv"),
  raw("1c17a90fc63e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Sha2015/.Sha2015_TabInterventions.tsv"),
  raw("866a70d1f6a7..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_Fig1.tsv"),
  raw("ab52656d80c1..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_Fig3.tsv"),
  raw("83dbb1d0aa58..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_Fig4.tsv"),
  raw("2faf49857570..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_Fig5.tsv"),
  raw("2d0425030e0b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_Tab2.tsv"),
  raw("ed117f76c761..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_TabGroups.tsv"),
  raw("ffe3ccbea06e..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Tamborlane2018/.Tamborlane2018_TabInterventions.tsv"),
  raw("34993d1baf72..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Wattamwar2020/.Wattamwar2020_Fig4.tsv"),
  raw("d42dadbff52b..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Wattamwar2020/.Wattamwar2020_Tab8.tsv"),
  raw("a5c6664ba403..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Wattamwar2020/.Wattamwar2020_TabGroups.tsv"),
  raw("ee43c63765d3..."),
  raw("pkdb_models/models/canagliflozin/data/canagliflozin/Wattamwar2020/.Wattamwar2020_TabInterventions.tsv"),
  raw("da66713c7ae7..."),
  raw("pkdb_models/models/canagliflozin/models/output/models/canagliflozin_body_flat.xml"),
  raw("ed17cbd80655..."),
  ),
  caption: [SHA-256 checksums of the models and data of the fit PD\_20261019\_201254\_\_61546, their first 12 characters; the full checksums are in the provenance of the result (optimization\_result.json).],
) <tab:checksums:PD_20261019_201254__61546>

= Results: Canagliflozin PBPK\/PD model: fit PD

== Parameters

#figure(
  table(
  columns: 6,
  align: (left, left, right, left, right, left,),
  table.header([Parameter], [Description], [Value \[95% CI\]], [Unit], [Bounds], [Identifiable]),
  raw("KI__RTG_E50"),
  [EC50 reduction in RTG],
  [7.59e-05 \[5.86e-05, 9.61e-05\]],
  [mmol\/l],
  [\[1e-06, 0.0002\]],
  [yes],
  raw("KI__RTG_base"),
  [baseline RTG],
  [8.93 \[8.46, 9.46\]],
  [mmol\/l],
  [\[6, 13\]],
  [yes],
  raw("KI__RTG_m_fpg"),
  [FPG effect on RTG],
  [0.667 \[0.604, 0.749\]],
  [dimensionless],
  [\[0.05, 2\]],
  [yes],
  raw("KI__RTG_max_inhibition"),
  [maximal relative reduction of the RTG],
  [0.645 \[0.624, 0.664\]],
  [dimensionless],
  [\[0.3, 0.9\]],
  [yes],
  ),
  caption: [Parameters of the fit PD\_20261019\_201254\_\_61546, the parameter set PD\_20261019\_201254\_\_61546\_0, cost 169, with their bounds in the optimization. The 95% confidence intervals are those of the profile likelihood, LB and UB an interval which is open towards the lower or the upper bound, and the Wald intervals of the Fisher information for a parameter without a profile. Identifiable is the classification of the profile: yes, no (LB) or no (UB) if the profile does not reach the threshold towards the lower or the upper bound, no if it reaches it on neither side, structural if it is flat.],
) <tab:parameters:PD_20261019_201254__61546>

== Data

#figure(
  table(
  columns: 5,
  align: (left, right, right, right, right,),
  table.header([Study], [Training], [Validation], [Outlier], [Total]),
  [Chen2015],
  [4 (6)],
  [1 (2)],
  [-],
  [5 (8)],
  [Devineni2012],
  [5 (11)],
  [1 (1)],
  [-],
  [6 (12)],
  [Devineni2013],
  [7 (24)],
  [1 (4)],
  [-],
  [8 (28)],
  [Devineni2014],
  [2 (2)],
  [2 (2)],
  [-],
  [4 (4)],
  [Devineni2015a],
  [6 (18)],
  [-],
  [-],
  [6 (18)],
  [Devineni2015c],
  [2 (5)],
  [6 (15)],
  [-],
  [8 (20)],
  [Devineni2016],
  [4 (20)],
  [-],
  [-],
  [4 (20)],
  [Iijima2015],
  [5 (10)],
  [4 (40)],
  [-],
  [9 (50)],
  [Inagaki2014],
  [2 (6)],
  [2 (6)],
  [-],
  [4 (12)],
  [Sha2011],
  [14 (21)],
  [3 (5)],
  [-],
  [17 (26)],
  [Sha2014],
  [14 (95)],
  [10 (87)],
  [-],
  [24 (182)],
  [Sha2015],
  [2 (9)],
  [-],
  [-],
  [2 (9)],
  [Tamborlane2018],
  [-],
  [6 (12)],
  [-],
  [6 (12)],
  [Total],
  [67 (227)],
  [36 (174)],
  [-],
  [103 (401)],
  ),
  caption: [Data of the fit PD\_20261019\_201254\_\_61546: the number of fit mappings and, in parentheses, of data points per study and kind. The training data enters the cost, the validation data and the outliers are evaluated only.],
) <tab:data:PD_20261019_201254__61546>

== Goodness of fit

#figure(
  table(
  columns: 11,
  align: (left, right, right, right, right, right, right, right, right, right, right,),
  table.header([Kind], [n], [cost], [MSE], [RMSE], [NRMSE], [RMSE\_w], [R²], [2-fold \[%\]], [AIC], [BIC]),
  [training],
  [227],
  [169],
  [404],
  [20.1],
  [0.322],
  [1.22],
  [0.852],
  [95.1],
  [1370.1],
  [1383.8],
  [validation],
  [174],
  [-],
  [770],
  [27.7],
  [12.3],
  [30.7],
  [0.4],
  [71.3],
  [1164.5],
  [1177.1],
  ),
  caption: [Goodness of fit of the fit PD\_20261019\_201254\_\_61546 per kind of data, the parameter set PD\_20261019\_201254\_\_61546\_0. The cost is defined on the training data only, 2-fold is the percentage of the data points with a positive value and prediction whose prediction is within twofold of the data.],
) <tab:metrics:PD_20261019_201254__61546>

== Figures

#figure(
  image("plots/traces.svg", width: 100%),
  caption: [Cost of the optimizers over their steps, fit PD\_20261019\_201254\_\_61546. The cost of every optimization run over its steps. Runs which end at the same cost found the same optimum; a run which stops much higher is stuck in a local minimum.],
) <fig:traces:PD_20261019_201254__61546>

#figure(
  image("plots/waterfall.svg", width: 100%),
  caption: [Cost of the optimization runs, ordered, fit PD\_20261019\_201254\_\_61546. The final cost of the runs, ordered. A flat plateau at the left is the global optimum found repeatedly, which is the evidence that the multistart converged; steps to the right are local minima.],
) <fig:waterfall:PD_20261019_201254__61546>

#figure(
  image("plots/goodness_of_fit.svg", width: 100%),
  caption: [Prediction against the measured data points, per kind of fit mapping, with the agreement of the training data, the lines of twofold and the metrics of the panel, fit PD\_20261019\_201254\_\_61546. Within twofold of the data are 193 of the 203 training data points (95.1%) and 112 of the 157 validation data points (71.3%); only the data points with a positive value and prediction are counted. Prediction against measurement, one point per data point, with a panel per kind of fit mapping. The points scatter around the diagonal when the model describes the data; a systematic deviation from it is a systematic error of the model. The band is the agreement of the training data, i.e. the same band the Bland-Altman plot draws, here as lines parallel to the diagonal. The dark red dotted lines are twofold, prediction \= 2 x measurement and prediction \= measurement \/ 2; the caption states the points between them of every kind. A point which is zero or negative is not drawn on the logarithmic axes and not counted, the title of a panel then states the points drawn of all. The validation panel shows how the fit describes data it was not fitted on, the outlier panel the data the fit dropped. The box of a panel carries its R², its normalized RMSE, the RMSE of the residuals of the cost, its fold errors GMFE and AFE and the percentages of its points within twofold and within two standard deviations of the data.],
) <fig:goodness_of_fit:PD_20261019_201254__61546>

#figure(
  image("plots/bland_altman.svg", width: 100%),
  caption: [Agreement of prediction and measurement as a ratio, per kind of fit mapping, with the agreement of the training data and the agreement of the panel, fit PD\_20261019\_201254\_\_61546. The ratio of prediction and measurement over the geometric mean of the two, i.e. the goodness of fit with the diagonal turned into the horizontal. The band is the same, the bias and the limits of agreement #raw("bias ± 1.96 SD") of the training data as fold factors. A bias away from 1 is a systematic over- or underprediction, wide limits are a large scatter, and a trend over the mean is a model which describes the large or the small values better. The box of a panel carries the bias and the SD of its own points as fold factors and the share of them inside the limits of agreement of the training data.],
) <fig:bland_altman:PD_20261019_201254__61546>

#figure(
  image("plots/profiles.svg", width: 100%),
  caption: [Profile likelihood of every parameter: the cost with the parameter fixed and the other parameters optimized, the threshold of the confidence level and the confidence interval, fit PD\_20261019\_201254\_\_61546. One profile per parameter. A profile which crosses the dashed threshold on both sides gives a finite confidence interval; one which stays below it up to a bound is practically non-identifiable; a flat profile is structurally non-identifiable, the parameter is compensated by the others.],
) <fig:profiles:PD_20261019_201254__61546>

== Provenance

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([Item], [Value]),
  [Fit],
  raw("PD_20261019_201254__61546"),
  [Created],
  [2026-10-19 18:13:02 UTC],
  [Seed],
  [1234],
  [Python],
  [3.14.4],
  [sbmlsim],
  [0.10.0],
  [libRoadRunner],
  [2.10.0],
  [SciPy],
  [1.18.1],
  [NumPy],
  [2.5.3],
  [Repository],
  raw("/home/mkoenig/git/pkdb_models-canagliflozin"),
  [Commit],
  raw("e2644f489b973f8d28b845906e093e3af1870fe1"),
  [Uncommitted changes],
  [no],
  ),
  caption: [Provenance of the fit PD\_20261019\_201254\_\_61546: the versions it ran with and the revision of its models and data; the SHA-256 checksums of the models and data are listed in #ref(<tab:checksums:PD_20261019_201254__61546>).],
) <tab:provenance:PD_20261019_201254__61546>

#bibliography("references.bib", style: "references.csl")
