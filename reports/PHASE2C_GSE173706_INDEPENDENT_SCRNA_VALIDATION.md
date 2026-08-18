# PHASE 2C GSE173706 Independent scRNA Validation

## 结论

NO-GO / SHRINK. GSE173706 作为独立 scRNA 验证集完成 donor-level marker/reference 定位。分析未使用作者整合注释，采用透明 marker mapping；cell 只作为打分单位，统计解释基于 donor summary。

## 数据概况

- QC-passing cells scored: 90609
- Donors with recoverable IDs: 23
- Tissue states: {'lesional': 43880, 'nonlesional': 33936, 'healthy': 12793}

## Final independent scRNA localization

| axis   | dominant_refined_state_paired   | parent_cell_type   | score_localization    |   n_paired_donors |   paired_LS_minus_NL |   paired_ci_low |   paired_ci_high |   paired_fdr | lesional_vs_healthy_top_state   |   lesional_vs_healthy_effect |   core_extended_spearman | independent_scrna_confidence   |
|:-------|:--------------------------------|:-------------------|:----------------------|------------------:|---------------------:|----------------:|-----------------:|-------------:|:--------------------------------|-----------------------------:|-------------------------:|:-------------------------------|
| F1     | keratinocyte_inflammatory_T17   | keratinocyte       | melanocyte_unresolved |                10 |            0.0647195 |       0.0213119 |        0.10989   |     0.278363 | keratinocyte_inflammatory_T17   |                    0.0839643 |                 0.953799 | LOW                            |
| F2     | keratinocyte_stress_hypoxia     | keratinocyte       | melanocyte_unresolved |                 8 |            0.0372059 |       0.0100311 |        0.0658886 |     0.312439 | keratinocyte_inflammatory_T17   |                    0.050746  |                 0.982464 | LOW                            |
| F6     | keratinocyte_stress_hypoxia     | keratinocyte       | melanocyte_unresolved |                 8 |            0.0935218 |       0.0173958 |        0.169671  |     0.312439 | keratinocyte_inflammatory_T17   |                    0.111487  |                 0.9634   | LOW                            |
| F7     | B_cell_unresolved               | B_cell             | keratinocyte_basal    |                 9 |            0.128239  |      -0.0114021 |        0.328622  |     0.622222 | dendritic_LAMP3_CCR7            |                    0.470784  |                 0.943936 | LOW                            |

## Paired PsO LS-vs-NL donor statistics

| axis   | program_type   | refined_state                   | parent_cell_type   |   n_paired_donors |   mean_LS_minus_NL |   bootstrap_ci_low |   bootstrap_ci_high |   signflip_p |   fdr_by_program_type |
|:-------|:---------------|:--------------------------------|:-------------------|------------------:|-------------------:|-------------------:|--------------------:|-------------:|----------------------:|
| F1     | CORE           | keratinocyte_basal              | keratinocyte       |                10 |        0.0410837   |        0.0193061   |         0.0611722   |   0.00878049 |              0.22924  |
| F1     | CORE           | endothelial_vascular            | endothelial        |                 9 |        0.0261039   |        0.00973368  |         0.0438558   |   0.0292398  |              0.278363 |
| F1     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.0647195   |        0.0213119   |         0.10989     |   0.0243902  |              0.278363 |
| F1     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0248188   |       -0.0431069   |        -0.00294023  |   0.0565302  |              0.312439 |
| F1     | CORE           | cytotoxic_NK_T                  | NK_cell            |                 8 |       -0.012895    |       -0.0219884   |        -0.0033622   |   0.0505837  |              0.312439 |
| F1     | CORE           | melanocyte_unresolved           | melanocyte         |                10 |        0.0315958   |        0.00518837  |         0.0560313   |   0.057561   |              0.312439 |
| F1     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0554632   |        0.00627766  |         0.103218    |   0.07393    |              0.319298 |
| F1     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.0104558   |       -0.000229913 |         0.0192307   |   0.0955166  |              0.352747 |
| F1     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |       -0.013456    |       -0.0297287   |         0.0012023   |   0.143415   |              0.490272 |
| F1     | CORE           | endothelial_activated           | endothelial        |                 9 |        0.0342238   |       -0.0125033   |         0.0782351   |   0.196881   |              0.570276 |
| F1     | CORE           | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.0601928   |       -0.0249121   |         0.15918     |   0.411765   |              0.786096 |
| F1     | CORE           | T_cell_TRM_T17_like             | T_cell             |                 9 |        0.00937923  |       -0.0178468   |         0.0366073   |   0.528265   |              0.915033 |
| F1     | CORE           | unassigned_unresolved           | unassigned         |                 3 |        0.0181126   |       -0.00620424  |         0.0386595   |   0.555556   |              0.915033 |
| F1     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                 4 |       -0.020433    |       -0.0562714   |         0.0350669   |   0.647059   |              0.952368 |
| F1     | CORE           | B_cell_plasma                   | B_cell             |                 7 |       -0.0110101   |       -0.062192    |         0.0398653   |   0.736434   |              0.961981 |
| F1     | CORE           | fibroblast_inflammatory         | fibroblast         |                 7 |        0.00949732  |       -0.0344979   |         0.0556824   |   0.72093    |              0.961981 |
| F1     | CORE           | T_cell_unresolved               | T_cell             |                 1 |       -0.0184169   |       -0.0184169   |        -0.0184169   |   1          |              1        |
| F1     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.00458958  |       -0.0393127   |         0.0249803   |   0.845854   |              1        |
| F1     | CORE           | B_cell_unresolved               | B_cell             |                 9 |       -0.00330334  |       -0.043224    |         0.0403949   |   0.88694    |              1        |
| F1     | CORE           | mast_cell                       | mast_cell          |                 8 |        0.000118988 |       -0.0267973   |         0.0354402   |   1          |              1        |
| F1     | CORE           | dendritic_unresolved            | dendritic          |                 1 |        0.00557962  |        0.00557962  |         0.00557962  |   1          |              1        |
| F1     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                10 |        0.0320489   |        0.0169577   |         0.0451219   |   0.00878049 |              0.36878  |
| F1     | EXTENDED       | endothelial_vascular            | endothelial        |                 9 |        0.0174652   |        0.00514557  |         0.0316975   |   0.0487329  |              0.404634 |
| F1     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                10 |        0.028378    |        0.00477939  |         0.0510914   |   0.057561   |              0.404634 |
| F1     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0452853   |        0.00674616  |         0.0825719   |   0.0661479  |              0.404634 |
| F1     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.0479477   |        0.015164    |         0.082447    |   0.0439024  |              0.404634 |
| F1     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.00761886  |       -0.000263628 |         0.0157763   |   0.134503   |              0.513557 |
| F1     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0159047   |       -0.0354149   |         0.00488159  |   0.189084   |              0.661793 |
| F1     | EXTENDED       | endothelial_activated           | endothelial        |                 9 |        0.0204664   |       -0.0172179   |         0.0495109   |   0.282651   |              0.847953 |
| F1     | EXTENDED       | mast_cell                       | mast_cell          |                 8 |       -0.0123689   |       -0.0329731   |         0.0107944   |   0.307393   |              0.848485 |
| F1     | EXTENDED       | B_cell_plasma                   | B_cell             |                 7 |       -0.0148339   |       -0.0501707   |         0.0248177   |   0.472868   |              0.918605 |
| F1     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                 9 |        0.00735166  |       -0.0178953   |         0.0337384   |   0.610136   |              0.918605 |
| F1     | EXTENDED       | B_cell_unresolved               | B_cell             |                 9 |        0.0107325   |       -0.0181295   |         0.0432737   |   0.563353   |              0.918605 |
| F1     | EXTENDED       | unassigned_unresolved           | unassigned         |                 3 |        0.0139367   |       -0.00738237  |         0.0259227   |   0.555556   |              0.918605 |
| F1     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.045409    |       -0.0189016   |         0.106738    |   0.411765   |              0.918605 |
| F1     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.00949418  |       -0.0412248   |         0.0165677   |   0.676098   |              0.970914 |
| F1     | EXTENDED       | cytotoxic_NK_T                  | NK_cell            |                 8 |       -0.00259047  |       -0.011799    |         0.00863301  |   0.673152   |              0.970914 |
| F1     | EXTENDED       | T_cell_unresolved               | T_cell             |                 1 |       -0.00210093  |       -0.00210093  |        -0.00210093  |   1          |              1        |
| F1     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |       -0.00128423  |       -0.0126423   |         0.00937731  |   0.851707   |              1        |
| F1     | EXTENDED       | fibroblast_inflammatory         | fibroblast         |                 7 |        0.00357368  |       -0.0260949   |         0.0349924   |   0.875969   |              1        |
| F1     | EXTENDED       | keratinocyte_IFN_response       | keratinocyte       |                 4 |        0.00558658  |       -0.0339273   |         0.0679983   |   1          |              1        |
| F1     | EXTENDED       | dendritic_unresolved            | dendritic          |                 1 |        0.0142627   |        0.0142627   |         0.0142627   |   1          |              1        |
| F2     | CORE           | keratinocyte_basal              | keratinocyte       |                10 |        0.0218451   |        0.0119737   |         0.0321096   |   0.00878049 |              0.22924  |
| F2     | CORE           | endothelial_vascular            | endothelial        |                 9 |        0.0181125   |        0.00717927  |         0.0315836   |   0.0175439  |              0.245614 |
| F2     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.027286    |        0.00559446  |         0.0503907   |   0.0595122  |              0.312439 |
| F2     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0372059   |        0.0100311   |         0.0658886   |   0.0505837  |              0.312439 |
| F2     | CORE           | melanocyte_unresolved           | melanocyte         |                10 |        0.0197777   |        0.00254444  |         0.0367607   |   0.0731707  |              0.319298 |
| F2     | CORE           | B_cell_unresolved               | B_cell             |                 9 |        0.0178046   |       -0.00290309  |         0.0401373   |   0.173489   |              0.532164 |
| F2     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0148992   |       -0.0370081   |         0.00838455  |   0.239766   |              0.592363 |
| F2     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.00819186  |       -0.00180385  |         0.020404    |   0.216374   |              0.592363 |
| F2     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |        0.00707442  |       -0.00597164  |         0.0224128   |   0.404878   |              0.786096 |
| F2     | CORE           | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.0233609   |       -0.00626887  |         0.0529907   |   0.411765   |              0.786096 |
| F2     | CORE           | endothelial_activated           | endothelial        |                 9 |        0.0109258   |       -0.0196998   |         0.0333824   |   0.512671   |              0.915033 |
| F2     | CORE           | unassigned_unresolved           | unassigned         |                 3 |        0.01187     |       -0.000970474 |         0.0313591   |   0.555556   |              0.915033 |
| F2     | CORE           | B_cell_plasma                   | B_cell             |                 7 |       -0.0101633   |       -0.0403783   |         0.022408    |   0.581395   |              0.939177 |
| F2     | CORE           | mast_cell                       | mast_cell          |                 8 |       -0.00467377  |       -0.0210931   |         0.00859207  |   0.618677   |              0.952368 |
| F2     | CORE           | cytotoxic_NK_T                  | NK_cell            |                 8 |        0.00390568  |       -0.0104013   |         0.0196347   |   0.657588   |              0.952368 |
| F2     | CORE           | T_cell_TRM_T17_like             | T_cell             |                 9 |        0.00505781  |       -0.0100501   |         0.0225347   |   0.610136   |              0.952368 |
| F2     | CORE           | fibroblast_inflammatory         | fibroblast         |                 7 |        0.00561823  |       -0.0129598   |         0.0294394   |   0.689922   |              0.961981 |
| F2     | CORE           | dendritic_unresolved            | dendritic          |                 1 |       -0.0228531   |       -0.0228531   |        -0.0228531   |   1          |              1        |
| F2     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.00351742  |       -0.0261339   |         0.0143352   |   0.849756   |              1        |
| F2     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                 4 |       -0.0018983   |       -0.0192241   |         0.0264648   |   1          |              1        |
| F2     | CORE           | T_cell_unresolved               | T_cell             |                 1 |        0.00886196  |        0.00886196  |         0.00886196  |   1          |              1        |
| F2     | EXTENDED       | endothelial_vascular            | endothelial        |                 9 |        0.0166619   |        0.00399101  |         0.0306619   |   0.037037   |              0.404634 |
| F2     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                10 |        0.020017    |        0.00824448  |         0.0308949   |   0.0185366  |              0.404634 |
| F2     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.029337    |        0.00818696  |         0.0527098   |   0.04       |              0.404634 |
| F2     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0320444   |        0.00486115  |         0.0604142   |   0.07393    |              0.404634 |
| F2     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0165839   |       -0.0325284   |         0.000438024 |   0.103314   |              0.456585 |
| F2     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                10 |        0.0159647   |       -0.00123652  |         0.0328042   |   0.114146   |              0.456585 |
| F2     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.00693196  |       -0.0026146   |         0.0183516   |   0.267057   |              0.847953 |
| F2     | EXTENDED       | B_cell_plasma                   | B_cell             |                 7 |       -0.015961    |       -0.0438875   |         0.0137276   |   0.348837   |              0.861833 |
| F2     | EXTENDED       | mast_cell                       | mast_cell          |                 8 |       -0.00629498  |       -0.0214925   |         0.00760902  |   0.486381   |              0.918605 |
| F2     | EXTENDED       | fibroblast_inflammatory         | fibroblast         |                 7 |        0.00571516  |       -0.00887576  |         0.0235524   |   0.565891   |              0.918605 |
| F2     | EXTENDED       | unassigned_unresolved           | unassigned         |                 3 |        0.00718718  |       -0.00117818  |         0.0195677   |   0.555556   |              0.918605 |
| F2     | EXTENDED       | endothelial_activated           | endothelial        |                 9 |        0.0107179   |       -0.0186236   |         0.0334572   |   0.497076   |              0.918605 |
| F2     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.0188091   |       -0.00737581  |         0.0449941   |   0.529412   |              0.918605 |
| F2     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.00658986  |       -0.0285327   |         0.0109603   |   0.701463   |              0.982049 |
| F2     | EXTENDED       | B_cell_unresolved               | B_cell             |                 9 |        0.00422858  |       -0.0166003   |         0.0262898   |   0.734893   |              0.995661 |
| F2     | EXTENDED       | T_cell_unresolved               | T_cell             |                 1 |       -0.00552425  |       -0.00552425  |        -0.00552425  |   1          |              1        |
| F2     | EXTENDED       | keratinocyte_IFN_response       | keratinocyte       |                 4 |       -0.00473934  |       -0.0262067   |         0.0323184   |   0.882353   |              1        |
| F2     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                 9 |       -0.000336497 |       -0.0150044   |         0.0163156   |   0.97271    |              1        |
| F2     | EXTENDED       | dendritic_unresolved            | dendritic          |                 1 |        5.1118e-06  |        5.1118e-06  |         5.1118e-06  |   1          |              1        |
| F2     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |        0.00114898  |       -0.0107778   |         0.0138985   |   0.85561    |              1        |
| F2     | EXTENDED       | cytotoxic_NK_T                  | NK_cell            |                 8 |        0.0013996   |       -0.0107905   |         0.0149425   |   0.859922   |              1        |
| F6     | CORE           | endothelial_vascular            | endothelial        |                 9 |        0.027228    |        0.0110489   |         0.0464731   |   0.0136452  |              0.22924  |
| F6     | CORE           | keratinocyte_basal              | keratinocyte       |                10 |        0.0517853   |        0.0280422   |         0.0729627   |   0.00682927 |              0.22924  |
| F6     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.0164222   |        0.005423    |         0.0277886   |   0.0331384  |              0.278363 |
| F6     | CORE           | melanocyte_unresolved           | melanocyte         |                10 |        0.0575472   |        0.0170465   |         0.0945982   |   0.0302439  |              0.278363 |
| F6     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0935218   |        0.0173958   |         0.169671    |   0.0505837  |              0.312439 |
| F6     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.0579723   |        0.00149384  |         0.115963    |   0.0965854  |              0.352747 |
| F6     | CORE           | B_cell_unresolved               | B_cell             |                 9 |        0.0470912   |       -0.00284188  |         0.106823    |   0.150097   |              0.490272 |
| F6     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0385432   |       -0.0917002   |         0.0167307   |   0.177388   |              0.532164 |
| F6     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |        0.014129    |       -0.00611573  |         0.0354366   |   0.235122   |              0.592363 |
| F6     | CORE           | T_cell_TRM_T17_like             | T_cell             |                 9 |        0.0257896   |       -0.0124177   |         0.063806    |   0.235867   |              0.592363 |
| F6     | CORE           | cytotoxic_NK_T                  | NK_cell            |                 8 |        0.0126166   |       -0.0080958   |         0.0314767   |   0.291829   |              0.680934 |
| F6     | CORE           | unassigned_unresolved           | unassigned         |                 3 |        0.0459585   |        0.021128    |         0.0867499   |   0.333333   |              0.736842 |
| F6     | CORE           | fibroblast_inflammatory         | fibroblast         |                 7 |        0.0358459   |       -0.0255628   |         0.103067    |   0.364341   |              0.784735 |
| F6     | CORE           | endothelial_activated           | endothelial        |                 9 |        0.0324617   |       -0.0410498   |         0.0856061   |   0.387914   |              0.786096 |
| F6     | CORE           | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.0708717   |       -0.0477075   |         0.157026    |   0.411765   |              0.786096 |
| F6     | CORE           | mast_cell                       | mast_cell          |                 8 |       -0.0108811   |       -0.0500561   |         0.0274763   |   0.634241   |              0.952368 |
| F6     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.0088652   |       -0.0518163   |         0.0285316   |   0.74439    |              0.961981 |
| F6     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                 4 |       -0.0198679   |       -0.0900231   |         0.0895678   |   0.764706   |              0.973262 |
| F6     | CORE           | B_cell_plasma                   | B_cell             |                 7 |       -0.00521437  |       -0.0957425   |         0.0835544   |   0.906977   |              1        |
| F6     | CORE           | T_cell_unresolved               | T_cell             |                 1 |        0.029415    |        0.029415    |         0.029415    |   1          |              1        |
| F6     | CORE           | dendritic_unresolved            | dendritic          |                 1 |        0.0534023   |        0.0534023   |         0.0534023   |   1          |              1        |
| F6     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                10 |        0.047045    |        0.0241242   |         0.0678868   |   0.00878049 |              0.36878  |
| F6     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                10 |        0.0448252   |        0.0129003   |         0.0740824   |   0.0341463  |              0.404634 |
| F6     | EXTENDED       | B_cell_unresolved               | B_cell             |                 9 |        0.0519559   |        0.00670982  |         0.10809     |   0.0721248  |              0.404634 |
| F6     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                10 |        0.0631817   |        0.0113612   |         0.114406    |   0.057561   |              0.404634 |
| F6     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                 8 |        0.0646031   |        0.0139417   |         0.113234    |   0.0661479  |              0.404634 |
| F6     | EXTENDED       | endothelial_vascular            | endothelial        |                 9 |        0.0136916   |       -0.00194162  |         0.0318594   |   0.204678   |              0.687719 |
| F6     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                 9 |       -0.0265724   |       -0.0737066   |         0.0256284   |   0.325536   |              0.848485 |
| F6     | EXTENDED       | unassigned_unresolved           | unassigned         |                 3 |        0.0410188   |        0.010137    |         0.0809465   |   0.333333   |              0.848485 |
| F6     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                 4 |        0.0831938   |       -0.0383761   |         0.158287    |   0.294118   |              0.848485 |
| F6     | EXTENDED       | B_cell_plasma                   | B_cell             |                 7 |       -0.021966    |       -0.0952652   |         0.0515587   |   0.596899   |              0.918605 |
| F6     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                10 |       -0.0206024   |       -0.0634818   |         0.0161632   |   0.434146   |              0.918605 |
| F6     | EXTENDED       | mast_cell                       | mast_cell          |                 8 |       -0.00898432  |       -0.048421    |         0.0328367   |   0.595331   |              0.918605 |
| F6     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                 9 |        0.00468985  |       -0.00684672  |         0.0167342   |   0.481481   |              0.918605 |
| F6     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                10 |        0.00728063  |       -0.0144784   |         0.0283897   |   0.545366   |              0.918605 |
| F6     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                 9 |        0.0145979   |       -0.0140228   |         0.045406    |   0.391813   |              0.918605 |

## Lesional-vs-healthy donor support

| axis   | program_type   | refined_state                   | parent_cell_type   |   n_lesional_donors |   n_healthy_donors |   mean_lesional_minus_healthy |   mannwhitney_p |   fdr_by_program_type |
|:-------|:---------------|:--------------------------------|:-------------------|--------------------:|-------------------:|------------------------------:|----------------:|----------------------:|
| F1     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.159031    |     0.00879121  |             0.175824  |
| F1     | CORE           | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.0508698   |     0.0158583   |             0.177861  |
| F1     | CORE           | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0458198   |     0.0159427   |             0.177861  |
| F1     | CORE           | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.0428252   |     0.0128467   |             0.177861  |
| F1     | CORE           | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0501516   |     0.0476729   |             0.227537  |
| F1     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.0430038   |     0.083064    |             0.27688   |
| F1     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.0839643   |     0.0757482   |             0.27688   |
| F1     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                  -0.0233153   |     0.15743     |             0.420044  |
| F1     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.0205616   |     0.211852    |             0.498476  |
| F1     | CORE           | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.0346453   |     0.20202     |             0.498476  |
| F1     | CORE           | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.0721178   |     0.228571    |             0.507937  |
| F1     | CORE           | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.0472949   |     0.246292    |             0.532523  |
| F1     | CORE           | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.0162904   |     0.437797    |             0.735226  |
| F1     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                   0.013263    |     0.525171    |             0.778985  |
| F1     | CORE           | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.0216848   |     0.525171    |             0.778985  |
| F1     | CORE           | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.0168436   |     0.742674    |             0.91406   |
| F1     | CORE           | endothelial_activated           | endothelial        |                  13 |                  7 |                  -0.00347144  |     0.642647    |             0.91406   |
| F1     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                  -0.0167322   |     0.798039    |             0.945055  |
| F1     | CORE           | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.0023311   |     1           |             1         |
| F1     | CORE           | B_cell_plasma                   | B_cell             |                  14 |                  6 |                   0.0118815   |     0.967957    |             1         |
| F1     | EXTENDED       | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0418248   |     0.00193924  |             0.0491273 |
| F1     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0361765   |     0.0102511   |             0.117156  |
| F1     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.0603285   |     0.0244559   |             0.177861  |
| F1     | EXTENDED       | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.118158    |     0.0307692   |             0.189349  |
| F1     | EXTENDED       | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.098448    |     0.0571429   |             0.228571  |
| F1     | EXTENDED       | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.0396233   |     0.0555556   |             0.228571  |
| F1     | EXTENDED       | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.0354554   |     0.0460956   |             0.228571  |
| F1     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.0729403   |     0.0506708   |             0.228571  |
| F1     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                  -0.0251003   |     0.0674923   |             0.234432  |
| F1     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.022725    |     0.109979    |             0.277887  |
| F1     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.0167202   |     0.187597    |             0.349018  |
| F1     | EXTENDED       | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.0153442   |     0.241357    |             0.438831  |
| F1     | EXTENDED       | endothelial_activated           | endothelial        |                  13 |                  7 |                  -0.0120116   |     0.350697    |             0.553795  |
| F1     | EXTENDED       | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.0168232   |     0.437797    |             0.619138  |
| F1     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.025205    |     0.509615    |             0.679487  |
| F1     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                  -0.00754303  |     0.616343    |             0.762852  |
| F1     | EXTENDED       | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.0221813   |     0.638889    |             0.762852  |
| F1     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.0150262   |     0.867555    |             0.948428  |
| F1     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                  -0.0135593   |     0.958824    |             0.992776  |
| F1     | EXTENDED       | B_cell_plasma                   | B_cell             |                  14 |                  6 |                  -0.0133563   |     0.967957    |             0.992776  |
| F2     | CORE           | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0359398   |     0.00113122  |             0.0452489 |
| F2     | CORE           | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0259983   |     0.00812459  |             0.175824  |
| F2     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.045206    |     0.0244559   |             0.177861  |
| F2     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.050746    |     0.0200206   |             0.177861  |
| F2     | CORE           | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.0171263   |     0.0369453   |             0.211116  |
| F2     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.0679735   |     0.0483516   |             0.227537  |
| F2     | CORE           | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.0777611   |     0.0571429   |             0.240602  |
| F2     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                  -0.0215694   |     0.055676    |             0.240602  |
| F2     | CORE           | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.0175066   |     0.0793258   |             0.27688   |
| F2     | CORE           | endothelial_activated           | endothelial        |                  13 |                  7 |                  -0.00993187  |     0.15743     |             0.420044  |
| F2     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                  -0.0119884   |     0.266692    |             0.561456  |
| F2     | CORE           | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.0247835   |     0.285445    |             0.585528  |
| F2     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.00549878  |     0.297345    |             0.59469   |
| F2     | CORE           | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.0198446   |     0.437797    |             0.735226  |
| F2     | CORE           | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.0034686   |     0.525171    |             0.778985  |
| F2     | CORE           | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.0217739   |     0.530303    |             0.778985  |
| F2     | CORE           | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.0181952   |     0.742674    |             0.91406   |
| F2     | CORE           | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.00971621  |     0.920336    |             0.981692  |
| F2     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                  -0.00669431  |     1           |             1         |
| F2     | CORE           | B_cell_plasma                   | B_cell             |                  14 |                  6 |                  -0.00532117  |     1           |             1         |
| F2     | EXTENDED       | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0327596   |     0.00307046  |             0.0491273 |
| F2     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0278482   |     0.0102511   |             0.117156  |
| F2     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.0520037   |     0.0200206   |             0.160165  |
| F2     | EXTENDED       | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.0759644   |     0.0571429   |             0.228571  |
| F2     | EXTENDED       | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.0750808   |     0.0483516   |             0.228571  |
| F2     | EXTENDED       | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.024281    |     0.0556244   |             0.228571  |
| F2     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.0375965   |     0.0667959   |             0.234432  |
| F2     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                  -0.0249675   |     0.0811146   |             0.249583  |
| F2     | EXTENDED       | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.0173872   |     0.0968008   |             0.276574  |
| F2     | EXTENDED       | endothelial_activated           | endothelial        |                  13 |                  7 |                  -0.0127235   |     0.134804    |             0.291468  |
| F2     | EXTENDED       | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.0248193   |     0.17911     |             0.341162  |
| F2     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.0128029   |     0.266692    |             0.453943  |
| F2     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                  -0.0125676   |     0.266692    |             0.453943  |
| F2     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.018884    |     0.440934    |             0.619138  |
| F2     | EXTENDED       | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.00644931  |     0.485423    |             0.669347  |
| F2     | EXTENDED       | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.021533    |     0.530303    |             0.695479  |
| F2     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.010194    |     0.569891    |             0.735343  |
| F2     | EXTENDED       | B_cell_plasma                   | B_cell             |                  14 |                  6 |                  -0.0106333   |     0.601548    |             0.762852  |
| F2     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                  -0.0203642   |     0.720915    |             0.812299  |
| F2     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.00123699  |     0.713544    |             0.812299  |
| F6     | CORE           | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.111487    |     0.0200206   |             0.177861  |
| F6     | CORE           | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.0951431   |     0.0369453   |             0.211116  |
| F6     | CORE           | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.115992    |     0.0703297   |             0.27688   |
| F6     | CORE           | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.052173    |     0.083064    |             0.27688   |
| F6     | CORE           | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0336595   |     0.0950183   |             0.292364  |
| F6     | CORE           | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.0546941   |     0.0950183   |             0.292364  |
| F6     | CORE           | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                   0.0617366   |     0.157516    |             0.420044  |
| F6     | CORE           | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.0437798   |     0.211852    |             0.498476  |
| F6     | CORE           | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.122424    |     0.228571    |             0.507937  |
| F6     | CORE           | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.0357808   |     0.328306    |             0.640596  |
| F6     | CORE           | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                  -0.00938586  |     0.441136    |             0.735226  |
| F6     | CORE           | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.0493399   |     0.431818    |             0.735226  |
| F6     | CORE           | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.00730037  |     0.48796     |             0.778985  |
| F6     | CORE           | endothelial_activated           | endothelial        |                  13 |                  7 |                   0.000224505 |     0.535552    |             0.778985  |
| F6     | CORE           | B_cell_plasma                   | B_cell             |                  14 |                  6 |                   0.0406069   |     0.493963    |             0.778985  |
| F6     | CORE           | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0231128   |     0.732547    |             0.91406   |
| F6     | CORE           | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.00143873  |     0.713544    |             0.91406   |
| F6     | CORE           | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.000659844 |     0.826923    |             0.945055  |
| F6     | CORE           | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                   0.00485029  |     0.816796    |             0.945055  |
| F6     | CORE           | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.00398441  |     0.877296    |             0.96142   |
| F6     | EXTENDED       | fibroblast_inflammatory         | fibroblast         |                  11 |                  6 |                  -0.0553652   |     0.000161603 |             0.0129282 |
| F6     | EXTENDED       | T_cell_TRM_T17_like             | T_cell             |                  14 |                  8 |                  -0.0472763   |     0.00289583  |             0.0491273 |
| F6     | EXTENDED       | keratinocyte_inflammatory_T17   | keratinocyte       |                  14 |                  6 |                   0.111068    |     0.0200206   |             0.160165  |
| F6     | EXTENDED       | keratinocyte_IFN_response       | keratinocyte       |                  12 |                  3 |                  -0.123065    |     0.0307692   |             0.189349  |
| F6     | EXTENDED       | endothelial_vascular            | endothelial        |                  13 |                  7 |                  -0.0242133   |     0.0811146   |             0.249583  |
| F6     | EXTENDED       | B_cell_unresolved               | B_cell             |                  13 |                  7 |                   0.0705628   |     0.0968008   |             0.276574  |
| F6     | EXTENDED       | T_cell_unresolved               | T_cell             |                   3 |                  4 |                  -0.104558    |     0.114286    |             0.277887  |
| F6     | EXTENDED       | mast_cell                       | mast_cell          |                  11 |                  7 |                  -0.054525    |     0.104198    |             0.277887  |
| F6     | EXTENDED       | fibroblast_homeostatic_matrix   | fibroblast         |                  13 |                  7 |                  -0.0207213   |     0.114628    |             0.277887  |
| F6     | EXTENDED       | keratinocyte_stress_hypoxia     | keratinocyte       |                  12 |                  6 |                  -0.0462104   |     0.12465     |             0.288155  |
| F6     | EXTENDED       | cytotoxic_NK_T                  | NK_cell            |                  14 |                  7 |                  -0.0243026   |     0.148951    |             0.313581  |
| F6     | EXTENDED       | dendritic_LAMP3_CCR7            | myeloid_monocyte   |                  14 |                  4 |                   0.0624928   |     0.157516    |             0.315033  |
| F6     | EXTENDED       | keratinocyte_basal              | keratinocyte       |                  14 |                  8 |                   0.0374387   |     0.165313    |             0.322561  |
| F6     | EXTENDED       | endothelial_activated           | endothelial        |                  13 |                  7 |                  -0.0185296   |     0.350697    |             0.553795  |
| F6     | EXTENDED       | myeloid_monocyte_macrophage     | myeloid_monocyte   |                  14 |                  8 |                  -0.0046909   |     0.40202     |             0.595585  |
| F6     | EXTENDED       | B_cell_plasma                   | B_cell             |                  14 |                  6 |                   0.00984206  |     0.397007    |             0.595585  |
| F6     | EXTENDED       | keratinocyte_spinous_suprabasal | keratinocyte       |                  14 |                  8 |                  -0.0138062   |     0.441136    |             0.619138  |
| F6     | EXTENDED       | unassigned_unresolved           | unassigned         |                   5 |                  7 |                   0.0246147   |     0.638889    |             0.762852  |
| F6     | EXTENDED       | melanocyte_unresolved           | melanocyte         |                  14 |                  8 |                   0.0210929   |     0.713544    |             0.812299  |
| F6     | EXTENDED       | keratinocyte_proliferative      | keratinocyte       |                  11 |                  5 |                  -0.00913832  |     0.913004    |             0.968775  |

## Score localization

| axis   | program_type   | dominant_refined_state        | dominant_parent_cell_type   |   dominant_mean_score |   n_refined_states_observed |
|:-------|:---------------|:------------------------------|:----------------------------|----------------------:|----------------------------:|
| F1     | CORE           | melanocyte_unresolved         | melanocyte                  |              0.439636 |                          25 |
| F1     | EXTENDED       | melanocyte_unresolved         | melanocyte                  |              0.335987 |                          25 |
| F2     | CORE           | melanocyte_unresolved         | melanocyte                  |              0.218409 |                          25 |
| F2     | EXTENDED       | fibroblast_homeostatic_matrix | fibroblast                  |              0.239077 |                          25 |
| F6     | CORE           | melanocyte_unresolved         | melanocyte                  |              0.518251 |                          25 |
| F6     | EXTENDED       | keratinocyte_proliferative    | keratinocyte                |              0.470865 |                          25 |
| F7     | CORE           | keratinocyte_basal            | keratinocyte                |              1.48435  |                          25 |
| F7     | EXTENDED       | keratinocyte_basal            | keratinocyte                |              0.845047 |                          25 |

## Interpretation boundary

This is independent single-cell support, but marker-derived annotations are still less strong than curated author cell-state labels. A mechanism name should be upgraded only if GSE173706 converges with Phase 2B-R and later spatial evidence.
