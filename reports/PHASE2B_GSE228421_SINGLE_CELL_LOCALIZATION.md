# PHASE 2B GSE228421 Single-Cell Localization

## Executive conclusion

NO-GO / SHRINK. Frozen F1/F2/F6/F7 programs were scored in GSE228421 single-cell skin data using donor-level summaries. CORE programs are primary; EXTENDED programs are sensitivity.

## Dataset and lock

- GSE228421 samples parsed: 20.
- Donors detected: 5.
- Raw cells/barcodes: 97320587; QC-passing cells: 244432.
- Primary analysis: baseline lesional versus baseline nonlesional, paired by donor.
- Treatment day 3/day 14 lesional samples are sensitivity only.
- Inference unit: donor/patient, not cell.

## Final localization table

| axis   | dominant_cell   | secondary_cell   | LS_NL_context                                                      |   donor_effect |   bootstrap_ci_low |   bootstrap_ci_high |      fdr |   core_extended_spearman | replication   | final_name   | confidence   | phase2b_status                  |
|:-------|:----------------|:-----------------|:-------------------------------------------------------------------|---------------:|-------------------:|--------------------:|---------:|-------------------------:|:--------------|:-------------|:-------------|:--------------------------------|
| F1     | keratinocyte    | T_cell           | skin baseline paired LS-vs-NL                                      |      0.0353959 |         0.0245615  |           0.0462304 | 0.363636 |                 0.9553   | yes           | F1           | LOW          | directional_not_fdr_significant |
| F2     | keratinocyte    | NK_cell          | skin baseline paired LS-vs-NL                                      |      0.0152069 |         0.0101339  |           0.0202798 | 0.363636 |                 0.972925 | yes           | F2           | LOW          | directional_not_fdr_significant |
| F6     | keratinocyte    | NK_cell          | skin baseline paired LS-vs-NL                                      |      0.0493425 |         0.0386122  |           0.0620077 | 0.363636 |                 0.946499 | yes           | F6           | LOW          | directional_not_fdr_significant |
| F7     | NK_cell         | B_cell           | skin immune localization; systemic support remains from bulk blood |      0.120505  |         0.00885095 |           0.259251  | 0.424242 |                 0.976219 | support       | F7           | LOW          | directional_not_fdr_significant |

## Cell-type localization

| axis   | program_type   | dominant_cell_type     |   dominant_mean_score | secondary_cell_type    |   secondary_mean_score |   specificity_delta_vs_second |   n_cell_types_observed |
|:-------|:---------------|:-----------------------|----------------------:|:-----------------------|-----------------------:|------------------------------:|------------------------:|
| F1     | CORE           | melanocyte             |              0.374263 | keratinocyte           |               0.308269 |                   0.0659936   |                      12 |
| F1     | EXTENDED       | melanocyte             |              0.26205  | fibroblast             |               0.227693 |                   0.0343576   |                      12 |
| F2     | CORE           | fibroblast             |              0.158427 | melanocyte             |               0.157359 |                   0.00106842  |                      12 |
| F2     | EXTENDED       | fibroblast             |              0.189364 | melanocyte             |               0.177689 |                   0.0116746   |                      12 |
| F6     | CORE           | melanocyte             |              0.374288 | dendritic              |               0.353287 |                   0.0210012   |                      12 |
| F6     | EXTENDED       | dendritic              |              0.33716  | pericyte_smooth_muscle |               0.333408 |                   0.00375229  |                      12 |
| F7     | CORE           | pericyte_smooth_muscle |              1.22474  | NK_cell                |               1.22432  |                   0.000416422 |                      12 |
| F7     | EXTENDED       | dendritic              |              0.707272 | NK_cell                |               0.691057 |                   0.0162144   |                      12 |

## Baseline paired donor statistics

| axis   | program_type   | cell_type              |   n_donors |   mean_LS_minus_NL |   bootstrap_ci_low |   bootstrap_ci_high |   signflip_p |   fdr_by_program_type |
|:-------|:---------------|:-----------------------|-----------:|-------------------:|-------------------:|--------------------:|-------------:|----------------------:|
| F1     | CORE           | B_cell                 |          5 |       -0.0328632   |       -0.0441876   |        -0.0218685   |    0.0909091 |              0.363636 |
| F1     | CORE           | keratinocyte           |          5 |        0.0353959   |        0.0245615   |         0.0462304   |    0.0909091 |              0.363636 |
| F1     | CORE           | mast_cell              |          5 |       -0.0455331   |       -0.0553104   |        -0.0356041   |    0.0909091 |              0.363636 |
| F1     | CORE           | dendritic              |          5 |       -0.0219871   |       -0.0322121   |        -0.00673433  |    0.151515  |              0.424242 |
| F1     | CORE           | fibroblast             |          5 |       -0.0162625   |       -0.0297951   |        -0.00314449  |    0.151515  |              0.424242 |
| F1     | CORE           | melanocyte             |          5 |       -0.0171623   |       -0.0292182   |        -0.00491154  |    0.151515  |              0.424242 |
| F1     | CORE           | myeloid_monocyte       |          5 |       -0.0300242   |       -0.0465553   |        -0.00757696  |    0.151515  |              0.424242 |
| F1     | CORE           | endothelial            |          5 |       -0.00934568  |       -0.0206469   |         0.00545282  |    0.272727  |              0.467532 |
| F1     | CORE           | unassigned             |          3 |       -0.0779574   |       -0.140162    |         0.000869853 |    0.555556  |              0.78961  |
| F1     | CORE           | T_cell                 |          5 |        0.008815    |       -0.0176913   |         0.0404364   |    0.69697   |              0.857809 |
| F1     | CORE           | NK_cell                |          5 |       -0.0103785   |       -0.0519386   |         0.0311815   |    0.757576  |              0.865801 |
| F1     | CORE           | pericyte_smooth_muscle |          5 |       -0.000313483 |       -0.0128723   |         0.0129453   |    1         |              1        |
| F1     | EXTENDED       | B_cell                 |          5 |       -0.0221246   |       -0.0329436   |        -0.0119873   |    0.0909091 |              0.363636 |
| F1     | EXTENDED       | keratinocyte           |          5 |        0.0251948   |        0.0164709   |         0.0339187   |    0.0909091 |              0.363636 |
| F1     | EXTENDED       | mast_cell              |          5 |       -0.0338617   |       -0.0368033   |        -0.0308546   |    0.0909091 |              0.363636 |
| F1     | EXTENDED       | dendritic              |          5 |       -0.0160854   |       -0.0236826   |        -0.00386952  |    0.151515  |              0.382775 |
| F1     | EXTENDED       | melanocyte             |          5 |       -0.011668    |       -0.0200443   |        -0.00199034  |    0.151515  |              0.382775 |
| F1     | EXTENDED       | myeloid_monocyte       |          5 |       -0.0227102   |       -0.036607    |        -0.00280995  |    0.151515  |              0.382775 |
| F1     | EXTENDED       | fibroblast             |          5 |       -0.0112702   |       -0.0236162   |         0.00107586  |    0.212121  |              0.424242 |
| F1     | EXTENDED       | endothelial            |          5 |       -0.00582595  |       -0.0140892   |         0.00319017  |    0.333333  |              0.484848 |
| F1     | EXTENDED       | unassigned             |          3 |       -0.049521    |       -0.0680479   |        -0.0240871   |    0.333333  |              0.484848 |
| F1     | EXTENDED       | NK_cell                |          5 |        0.0068721   |       -0.0165714   |         0.0350924   |    0.757576  |              0.808081 |
| F1     | EXTENDED       | T_cell                 |          5 |        0.00600751  |       -0.0147351   |         0.0287136   |    0.69697   |              0.808081 |
| F1     | EXTENDED       | pericyte_smooth_muscle |          5 |       -0.00213159  |       -0.0113076   |         0.00718933  |    0.878788  |              0.897485 |
| F2     | CORE           | B_cell                 |          5 |       -0.0174231   |       -0.0297292   |        -0.00561761  |    0.0909091 |              0.363636 |
| F2     | CORE           | keratinocyte           |          5 |        0.0152069   |        0.0101339   |         0.0202798   |    0.0909091 |              0.363636 |
| F2     | CORE           | mast_cell              |          5 |       -0.025092    |       -0.032677    |        -0.0186932   |    0.0909091 |              0.363636 |
| F2     | CORE           | NK_cell                |          5 |        0.0148333   |        0.000312972 |         0.0315916   |    0.212121  |              0.424242 |
| F2     | CORE           | dendritic              |          5 |       -0.00953293  |       -0.0174468   |        -0.000317179 |    0.212121  |              0.424242 |
| F2     | CORE           | melanocyte             |          5 |       -0.00722186  |       -0.0132516   |        -0.000243711 |    0.212121  |              0.424242 |
| F2     | CORE           | myeloid_monocyte       |          5 |       -0.0162776   |       -0.027085    |        -0.000182572 |    0.151515  |              0.424242 |
| F2     | CORE           | pericyte_smooth_muscle |          5 |        0.00889042  |        0.000296502 |         0.0174843   |    0.272727  |              0.467532 |
| F2     | CORE           | unassigned             |          3 |       -0.0247199   |       -0.0316136   |        -0.0204299   |    0.333333  |              0.516129 |
| F2     | CORE           | fibroblast             |          5 |       -0.00325801  |       -0.0129532   |         0.00706272  |    0.575758  |              0.78961  |
| F2     | CORE           | T_cell                 |          5 |        0.00615334  |       -0.0112276   |         0.0245934   |    0.636364  |              0.803828 |
| F2     | CORE           | endothelial            |          5 |        0.00247498  |       -0.00404191  |         0.00914624  |    0.636364  |              0.803828 |
| F2     | EXTENDED       | B_cell                 |          5 |       -0.0257939   |       -0.0382421   |        -0.0133457   |    0.0909091 |              0.363636 |
| F2     | EXTENDED       | keratinocyte           |          5 |        0.013554    |        0.00766321  |         0.0187845   |    0.0909091 |              0.363636 |
| F2     | EXTENDED       | mast_cell              |          5 |       -0.0257064   |       -0.0285511   |        -0.0228431   |    0.0909091 |              0.363636 |
| F2     | EXTENDED       | dendritic              |          5 |       -0.0116716   |       -0.0163955   |        -0.00500584  |    0.151515  |              0.382775 |
| F2     | EXTENDED       | melanocyte             |          5 |       -0.0116576   |       -0.0180629   |        -0.00338084  |    0.151515  |              0.382775 |
| F2     | EXTENDED       | myeloid_monocyte       |          5 |       -0.0200189   |       -0.0285111   |        -0.00690636  |    0.151515  |              0.382775 |
| F2     | EXTENDED       | unassigned             |          3 |       -0.0317211   |       -0.0448152   |        -0.0183705   |    0.333333  |              0.484848 |
| F2     | EXTENDED       | fibroblast             |          5 |       -0.00682591  |       -0.0180284   |         0.00437656  |    0.393939  |              0.525253 |
| F2     | EXTENDED       | pericyte_smooth_muscle |          5 |        0.00331558  |       -0.00397243  |         0.0106036   |    0.454545  |              0.589681 |
| F2     | EXTENDED       | NK_cell                |          5 |        0.00404236  |       -0.00961661  |         0.0212237   |    0.757576  |              0.808081 |
| F2     | EXTENDED       | T_cell                 |          5 |        0.00362234  |       -0.0101215   |         0.0191965   |    0.69697   |              0.808081 |
| F2     | EXTENDED       | endothelial            |          5 |       -0.00101377  |       -0.00657364  |         0.00503425  |    0.757576  |              0.808081 |
| F6     | CORE           | keratinocyte           |          5 |        0.0493425   |        0.0386122   |         0.0620077   |    0.0909091 |              0.363636 |
| F6     | CORE           | mast_cell              |          5 |       -0.0650293   |       -0.0829707   |        -0.0491664   |    0.0909091 |              0.363636 |
| F6     | CORE           | NK_cell                |          5 |        0.0484264   |        0.00756602  |         0.0877382   |    0.212121  |              0.424242 |
| F6     | CORE           | dendritic              |          5 |       -0.0282296   |       -0.0550457   |         0.00602645  |    0.212121  |              0.424242 |
| F6     | CORE           | myeloid_monocyte       |          5 |       -0.0250491   |       -0.0594411   |         0.0196649   |    0.333333  |              0.516129 |
| F6     | CORE           | unassigned             |          3 |       -0.0487301   |       -0.0748494   |        -0.0116676   |    0.333333  |              0.516129 |
| F6     | CORE           | T_cell                 |          5 |        0.0177101   |       -0.0175429   |         0.0591019   |    0.575758  |              0.78961  |
| F6     | CORE           | fibroblast             |          5 |       -0.00647221  |       -0.0304371   |         0.019662    |    0.636364  |              0.803828 |
| F6     | CORE           | melanocyte             |          5 |        0.00160479  |       -0.00854789  |         0.0123444   |    0.757576  |              0.865801 |
| F6     | CORE           | pericyte_smooth_muscle |          5 |        0.00691459  |       -0.0135513   |         0.0326664   |    0.757576  |              0.865801 |
| F6     | CORE           | endothelial            |          5 |       -0.00194367  |       -0.0187092   |         0.0163438   |    0.878788  |              0.958678 |
| F6     | CORE           | B_cell                 |          5 |       -0.00238619  |       -0.0210561   |         0.0162838   |    0.939394  |              0.980237 |
| F6     | EXTENDED       | keratinocyte           |          5 |        0.0445161   |        0.0373436   |         0.0538554   |    0.0909091 |              0.363636 |
| F6     | EXTENDED       | mast_cell              |          5 |       -0.0671947   |       -0.0791154   |        -0.0577368   |    0.0909091 |              0.363636 |
| F6     | EXTENDED       | melanocyte             |          5 |       -0.0135248   |       -0.0213738   |        -0.00567577  |    0.0909091 |              0.363636 |
| F6     | EXTENDED       | dendritic              |          5 |       -0.0178332   |       -0.0370698   |         0.00658643  |    0.212121  |              0.424242 |
| F6     | EXTENDED       | endothelial            |          5 |       -0.0146241   |       -0.0264443   |        -0.00221449  |    0.212121  |              0.424242 |
| F6     | EXTENDED       | NK_cell                |          5 |        0.0336874   |       -0.00139607  |         0.0687709   |    0.272727  |              0.484848 |
| F6     | EXTENDED       | fibroblast             |          5 |       -0.0217961   |       -0.0431775   |         0.00123789  |    0.272727  |              0.484848 |
| F6     | EXTENDED       | myeloid_monocyte       |          5 |       -0.0258483   |       -0.0526026   |         0.0053237   |    0.272727  |              0.484848 |
| F6     | EXTENDED       | pericyte_smooth_muscle |          5 |       -0.00943617  |       -0.0252019   |         0.00908948  |    0.333333  |              0.484848 |
| F6     | EXTENDED       | unassigned             |          3 |       -0.0422827   |       -0.0676695   |        -0.0111956   |    0.333333  |              0.484848 |
| F6     | EXTENDED       | B_cell                 |          5 |        0.00311431  |       -0.00817169  |         0.0138474   |    0.636364  |              0.783217 |
| F6     | EXTENDED       | T_cell                 |          5 |        0.00689854  |       -0.0236305   |         0.0408701   |    0.757576  |              0.808081 |
| F7     | CORE           | B_cell                 |          5 |        0.108511    |        0.0306509   |         0.191018    |    0.0909091 |              0.363636 |
| F7     | CORE           | endothelial            |          5 |       -0.104702    |       -0.143337    |        -0.0495917   |    0.0909091 |              0.363636 |
| F7     | CORE           | mast_cell              |          5 |       -0.278623    |       -0.308654    |        -0.239491    |    0.0909091 |              0.363636 |
| F7     | CORE           | melanocyte             |          5 |       -0.12718     |       -0.163679    |        -0.0957117   |    0.0909091 |              0.363636 |
| F7     | CORE           | NK_cell                |          5 |        0.120505    |        0.00885095  |         0.259251    |    0.212121  |              0.424242 |
| F7     | CORE           | fibroblast             |          5 |       -0.096919    |       -0.185225    |        -0.00861291  |    0.212121  |              0.424242 |
| F7     | CORE           | T_cell                 |          5 |       -0.0790564   |       -0.165821    |         0.00770794  |    0.272727  |              0.467532 |
| F7     | CORE           | pericyte_smooth_muscle |          5 |       -0.0456389   |       -0.0982382   |         0.00696043  |    0.272727  |              0.467532 |

## CORE versus EXTENDED robustness

| axis   |   core_extended_pseudobulk_spearman |   n_donor_celltype_units |
|:-------|------------------------------------:|-------------------------:|
| F1     |                            0.9553   |                      236 |
| F2     |                            0.972925 |                      236 |
| F6     |                            0.946499 |                      236 |
| F7     |                            0.976219 |                      236 |

## Treatment sensitivity

| axis   | program_type   | cell_type              | contrast                      |   n_donors |   mean_treatment_shift |   bootstrap_ci_low |   bootstrap_ci_high |   signflip_p |   fdr_by_program_type |
|:-------|:---------------|:-----------------------|:------------------------------|-----------:|-----------------------:|-------------------:|--------------------:|-------------:|----------------------:|
| F1     | CORE           | B_cell                 | day3_minus_baseline_lesional  |          5 |            0.0131802   |        0.00169852  |          0.0257731  |    0.212121  |              0.969697 |
| F1     | CORE           | B_cell                 | day14_minus_baseline_lesional |          5 |            0.0484702   |        0.031787    |          0.0651263  |    0.0909091 |              0.969697 |
| F1     | CORE           | NK_cell                | day3_minus_baseline_lesional  |          5 |           -0.0112614   |       -0.0398212   |          0.0172984  |    0.575758  |              0.969697 |
| F1     | CORE           | NK_cell                | day14_minus_baseline_lesional |          5 |            0.0330493   |        0.00230919  |          0.0674598  |    0.151515  |              0.969697 |
| F1     | CORE           | T_cell                 | day3_minus_baseline_lesional  |          5 |           -0.00876944  |       -0.0305962   |          0.0130574  |    0.575758  |              0.969697 |
| F1     | CORE           | T_cell                 | day14_minus_baseline_lesional |          5 |            0.0178097   |       -0.0109788   |          0.0519419  |    0.454545  |              0.969697 |
| F1     | CORE           | dendritic              | day14_minus_baseline_lesional |          5 |            0.0416753   |        0.015736    |          0.0789332  |    0.0909091 |              0.969697 |
| F1     | CORE           | endothelial            | day3_minus_baseline_lesional  |          5 |            0.0208837   |       -0.0003457   |          0.044407   |    0.272727  |              0.969697 |
| F1     | CORE           | endothelial            | day14_minus_baseline_lesional |          5 |            0.0296875   |       -0.00755095  |          0.0688418  |    0.393939  |              0.969697 |
| F1     | CORE           | fibroblast             | day3_minus_baseline_lesional  |          5 |            0.0247838   |       -0.00333805  |          0.057559   |    0.454545  |              0.969697 |
| F1     | CORE           | fibroblast             | day14_minus_baseline_lesional |          5 |            0.0334412   |       -0.0166695   |          0.0888743  |    0.393939  |              0.969697 |
| F1     | CORE           | keratinocyte           | day3_minus_baseline_lesional  |          5 |            0.0255813   |       -0.0320146   |          0.0676543  |    0.454545  |              0.969697 |
| F1     | CORE           | keratinocyte           | day14_minus_baseline_lesional |          5 |            0.039258    |       -0.0273738   |          0.0888702  |    0.333333  |              0.969697 |
| F1     | CORE           | mast_cell              | day14_minus_baseline_lesional |          5 |            0.0431893   |        0.0158276   |          0.0700093  |    0.151515  |              0.969697 |
| F1     | CORE           | melanocyte             | day3_minus_baseline_lesional  |          5 |            0.0116326   |       -0.0126923   |          0.0349722  |    0.515152  |              0.969697 |
| F1     | CORE           | melanocyte             | day14_minus_baseline_lesional |          5 |            0.0399714   |        0.0159924   |          0.0651776  |    0.0909091 |              0.969697 |
| F1     | CORE           | myeloid_monocyte       | day3_minus_baseline_lesional  |          5 |            0.0167512   |       -0.00929729  |          0.0486742  |    0.515152  |              0.969697 |
| F1     | CORE           | myeloid_monocyte       | day14_minus_baseline_lesional |          5 |            0.0498308   |        0.0234329   |          0.0842949  |    0.0909091 |              0.969697 |
| F1     | CORE           | pericyte_smooth_muscle | day3_minus_baseline_lesional  |          5 |            0.0109529   |       -0.00435288  |          0.0262587  |    0.333333  |              0.969697 |
| F1     | CORE           | pericyte_smooth_muscle | day14_minus_baseline_lesional |          5 |            0.0320937   |        0.00158284  |          0.0703867  |    0.212121  |              0.969697 |
| F1     | CORE           | unassigned             | day3_minus_baseline_lesional  |          2 |            0.0925176   |        0.0367891   |          0.148246   |    0.6       |              0.969697 |
| F1     | CORE           | unassigned             | day14_minus_baseline_lesional |          2 |            0.0593728   |        0.0361523   |          0.0825933  |    0.6       |              0.969697 |
| F1     | CORE           | dendritic              | day3_minus_baseline_lesional  |          5 |            0.00121116  |       -0.0187591   |          0.0225554  |    0.878788  |              0.992513 |
| F1     | CORE           | mast_cell              | day3_minus_baseline_lesional  |          5 |            0.000689806 |       -0.0157128   |          0.0173476  |    1         |              1        |
| F1     | EXTENDED       | B_cell                 | day3_minus_baseline_lesional  |          5 |            0.00976867  |       -0.00349324  |          0.0239317  |    0.272727  |              0.932401 |
| F1     | EXTENDED       | B_cell                 | day14_minus_baseline_lesional |          5 |            0.0283334   |        0.0137157   |          0.0429512  |    0.0909091 |              0.932401 |
| F1     | EXTENDED       | NK_cell                | day3_minus_baseline_lesional  |          5 |           -0.00552368  |       -0.0327432   |          0.0250504  |    0.757576  |              0.932401 |
| F1     | EXTENDED       | NK_cell                | day14_minus_baseline_lesional |          5 |            0.0230091   |       -0.00752342  |          0.0575714  |    0.272727  |              0.932401 |
| F1     | EXTENDED       | T_cell                 | day14_minus_baseline_lesional |          5 |            0.0107409   |       -0.0100966   |          0.0343812  |    0.515152  |              0.932401 |
| F1     | EXTENDED       | dendritic              | day3_minus_baseline_lesional  |          5 |            0.00745148  |       -0.00763865  |          0.0284166  |    0.757576  |              0.932401 |
| F1     | EXTENDED       | dendritic              | day14_minus_baseline_lesional |          5 |            0.0270769   |        0.00870096  |          0.0554974  |    0.0909091 |              0.932401 |
| F1     | EXTENDED       | endothelial            | day3_minus_baseline_lesional  |          5 |            0.0110239   |       -0.00989657  |          0.0359868  |    0.636364  |              0.932401 |
| F1     | EXTENDED       | endothelial            | day14_minus_baseline_lesional |          5 |            0.0139701   |       -0.0160558   |          0.0490389  |    0.575758  |              0.932401 |
| F1     | EXTENDED       | fibroblast             | day3_minus_baseline_lesional  |          5 |            0.0147989   |       -0.0121369   |          0.045875   |    0.454545  |              0.932401 |
| F1     | EXTENDED       | fibroblast             | day14_minus_baseline_lesional |          5 |            0.0150625   |       -0.0355897   |          0.0662438  |    0.636364  |              0.932401 |
| F1     | EXTENDED       | keratinocyte           | day3_minus_baseline_lesional  |          5 |            0.0162416   |       -0.0258205   |          0.0475835  |    0.454545  |              0.932401 |
| F1     | EXTENDED       | keratinocyte           | day14_minus_baseline_lesional |          5 |            0.0248387   |       -0.0246939   |          0.0616841  |    0.333333  |              0.932401 |
| F1     | EXTENDED       | mast_cell              | day14_minus_baseline_lesional |          5 |            0.0242214   |        0.00679313  |          0.0414203  |    0.151515  |              0.932401 |
| F1     | EXTENDED       | melanocyte             | day14_minus_baseline_lesional |          5 |            0.025275    |        0.00834729  |          0.0422027  |    0.0909091 |              0.932401 |
| F1     | EXTENDED       | myeloid_monocyte       | day3_minus_baseline_lesional  |          5 |            0.014795    |       -0.0086204   |          0.0436043  |    0.515152  |              0.932401 |
| F1     | EXTENDED       | myeloid_monocyte       | day14_minus_baseline_lesional |          5 |            0.0337404   |        0.00792049  |          0.0631601  |    0.0909091 |              0.932401 |
| F1     | EXTENDED       | pericyte_smooth_muscle | day3_minus_baseline_lesional  |          5 |            0.00902949  |       -0.00661011  |          0.0249979  |    0.333333  |              0.932401 |
| F1     | EXTENDED       | pericyte_smooth_muscle | day14_minus_baseline_lesional |          5 |            0.0188766   |       -0.00776318  |          0.0528059  |    0.454545  |              0.932401 |
| F1     | EXTENDED       | unassigned             | day3_minus_baseline_lesional  |          2 |            0.0366589   |        0.013975    |          0.0593428  |    0.6       |              0.932401 |
| F1     | EXTENDED       | unassigned             | day14_minus_baseline_lesional |          2 |            0.0303133   |        0.0186782   |          0.0419484  |    0.6       |              0.932401 |
| F1     | EXTENDED       | mast_cell              | day3_minus_baseline_lesional  |          5 |            0.00215578  |       -0.0129625   |          0.0143539  |    0.818182  |              0.935065 |
| F1     | EXTENDED       | melanocyte             | day3_minus_baseline_lesional  |          5 |            0.00316957  |       -0.0137428   |          0.0197155  |    0.818182  |              0.935065 |
| F1     | EXTENDED       | T_cell                 | day3_minus_baseline_lesional  |          5 |           -0.00243173  |       -0.0198114   |          0.0165522  |    0.878788  |              0.937374 |
| F2     | CORE           | B_cell                 | day3_minus_baseline_lesional  |          5 |            0.00612415  |       -0.00557891  |          0.0183762  |    0.454545  |              0.969697 |
| F2     | CORE           | B_cell                 | day14_minus_baseline_lesional |          5 |            0.0146781   |        0.00232273  |          0.0270335  |    0.212121  |              0.969697 |
| F2     | CORE           | NK_cell                | day14_minus_baseline_lesional |          5 |            0.0116009   |       -0.00547304  |          0.0341827  |    0.454545  |              0.969697 |
| F2     | CORE           | dendritic              | day14_minus_baseline_lesional |          5 |            0.0143646   |       -0.00275437  |          0.0340438  |    0.333333  |              0.969697 |
| F2     | CORE           | keratinocyte           | day3_minus_baseline_lesional  |          5 |            0.00793132  |       -0.0154604   |          0.027049   |    0.515152  |              0.969697 |
| F2     | CORE           | keratinocyte           | day14_minus_baseline_lesional |          5 |            0.0124477   |       -0.0158514   |          0.0337253  |    0.454545  |              0.969697 |
| F2     | CORE           | mast_cell              | day14_minus_baseline_lesional |          5 |            0.0113755   |        0.00131579  |          0.0243547  |    0.151515  |              0.969697 |
| F2     | CORE           | melanocyte             | day14_minus_baseline_lesional |          5 |            0.01271     |        0.00386481  |          0.0223927  |    0.151515  |              0.969697 |
| F2     | CORE           | myeloid_monocyte       | day14_minus_baseline_lesional |          5 |            0.0216353   |       -0.00114866  |          0.0439809  |    0.272727  |              0.969697 |
| F2     | CORE           | unassigned             | day3_minus_baseline_lesional  |          2 |            0.00534327  |        0.00258476  |          0.00810177 |    0.6       |              0.969697 |
| F2     | CORE           | NK_cell                | day3_minus_baseline_lesional  |          5 |           -0.00550683  |       -0.0271224   |          0.0206106  |    0.757576  |              0.992513 |
| F2     | CORE           | dendritic              | day3_minus_baseline_lesional  |          5 |            0.00793935  |       -0.00738048  |          0.0280193  |    0.69697   |              0.992513 |
| F2     | CORE           | endothelial            | day3_minus_baseline_lesional  |          5 |            0.00231175  |       -0.0169779   |          0.0249374  |    0.878788  |              0.992513 |
| F2     | CORE           | endothelial            | day14_minus_baseline_lesional |          5 |            0.00166473  |       -0.0234689   |          0.0293684  |    0.878788  |              0.992513 |
| F2     | CORE           | fibroblast             | day3_minus_baseline_lesional  |          5 |            0.00624865  |       -0.0170867   |          0.0317855  |    0.757576  |              0.992513 |
| F2     | CORE           | fibroblast             | day14_minus_baseline_lesional |          5 |            0.00236001  |       -0.0367247   |          0.0409262  |    0.878788  |              0.992513 |
| F2     | CORE           | mast_cell              | day3_minus_baseline_lesional  |          5 |            0.00144506  |       -0.0109892   |          0.0127957  |    0.818182  |              0.992513 |
| F2     | CORE           | melanocyte             | day3_minus_baseline_lesional  |          5 |           -0.00202235  |       -0.0132417   |          0.00857155 |    0.757576  |              0.992513 |
| F2     | CORE           | myeloid_monocyte       | day3_minus_baseline_lesional  |          5 |            0.0104906   |       -0.00983377  |          0.0345595  |    0.757576  |              0.992513 |
| F2     | CORE           | pericyte_smooth_muscle | day3_minus_baseline_lesional  |          5 |            0.00308189  |       -0.0120736   |          0.0177585  |    0.69697   |              0.992513 |
| F2     | CORE           | pericyte_smooth_muscle | day14_minus_baseline_lesional |          5 |            0.00553574  |       -0.0143233   |          0.0300675  |    0.818182  |              0.992513 |
| F2     | CORE           | T_cell                 | day3_minus_baseline_lesional  |          5 |            0.000726559 |       -0.0149137   |          0.0207277  |    1         |              1        |
| F2     | CORE           | T_cell                 | day14_minus_baseline_lesional |          5 |            0.00185008  |       -0.0150033   |          0.0211431  |    0.939394  |              1        |
| F2     | CORE           | unassigned             | day14_minus_baseline_lesional |          2 |            0.00609768  |       -0.00951198  |          0.0217073  |    1         |              1        |
| F2     | EXTENDED       | B_cell                 | day3_minus_baseline_lesional  |          5 |            0.00596101  |       -0.00261242  |          0.016033   |    0.515152  |              0.932401 |
| F2     | EXTENDED       | B_cell                 | day14_minus_baseline_lesional |          5 |            0.0225486   |        0.0137082   |          0.0313889  |    0.0909091 |              0.932401 |
| F2     | EXTENDED       | NK_cell                | day3_minus_baseline_lesional  |          5 |           -0.00530838  |       -0.0251681   |          0.0163988  |    0.69697   |              0.932401 |
| F2     | EXTENDED       | NK_cell                | day14_minus_baseline_lesional |          5 |            0.017063    |        0.000874608 |          0.0396436  |    0.212121  |              0.932401 |
| F2     | EXTENDED       | T_cell                 | day14_minus_baseline_lesional |          5 |            0.00708847  |       -0.00621641  |          0.0234789  |    0.515152  |              0.932401 |
| F2     | EXTENDED       | dendritic              | day14_minus_baseline_lesional |          5 |            0.0182805   |        0.00530428  |          0.0370479  |    0.0909091 |              0.932401 |
| F2     | EXTENDED       | endothelial            | day3_minus_baseline_lesional  |          5 |            0.00338172  |       -0.015534    |          0.0242933  |    0.757576  |              0.932401 |
| F2     | EXTENDED       | endothelial            | day14_minus_baseline_lesional |          5 |            0.00860821  |       -0.0144677   |          0.0360585  |    0.69697   |              0.932401 |

## Reviewer attack points

- Donor count is 5, so p values are low-power and confidence intervals should drive interpretation.
- Cell-type annotation is marker-based and coarse; Phase 2B conclusions should be treated as localization candidates until refined annotation or reference mapping.
- F7 is a systemic/supportive axis; skin single-cell localization can identify immune-state plausibility but cannot replace blood/PBMC validation.
- CORE programs are primary. EXTENDED concordance supports robustness but cannot rescue failed CORE localization.

## GO / CONDITIONAL GO / NO-GO

NO-GO / SHRINK

## Next recommendation

If at least two axes show MODERATE/HIGH localization confidence, proceed to refined annotation and then spatial validation. Do not start GWAS/MR until Phase 2B localization and Phase 2C spatial/perturbation boundaries are accepted.
