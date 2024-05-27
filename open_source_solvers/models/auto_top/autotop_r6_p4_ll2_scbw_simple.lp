\ Model auto_top_gurobi
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  0 bi_bw + sc_bw
Subject To
 reflex_rmap_r0: map_r0_r0 = 0
 reflex_rdist_r0: dist_r0_r0 = 0
 reflex_onehop_r0: onehop_r0_r0 = 0
 reflex_rmap_r1: map_r1_r1 = 0
 reflex_rdist_r1: dist_r1_r1 = 0
 reflex_onehop_r1: onehop_r1_r1 = 0
 reflex_rmap_r2: map_r2_r2 = 0
 reflex_rdist_r2: dist_r2_r2 = 0
 reflex_onehop_r2: onehop_r2_r2 = 0
 reflex_rmap_r3: map_r3_r3 = 0
 reflex_rdist_r3: dist_r3_r3 = 0
 reflex_onehop_r3: onehop_r3_r3 = 0
 reflex_rmap_r4: map_r4_r4 = 0
 reflex_rdist_r4: dist_r4_r4 = 0
 reflex_onehop_r4: onehop_r4_r4 = 0
 reflex_rmap_r5: map_r5_r5 = 0
 reflex_rdist_r5: dist_r5_r5 = 0
 reflex_onehop_r5: onehop_r5_r5 = 0
 radix_out_r0: map_r0_r1 + map_r0_r2 + map_r0_r3 + map_r0_r4 + map_r0_r5
   <= 4
 radix_in_r0: map_r1_r0 + map_r2_r0 + map_r3_r0 + map_r4_r0 + map_r5_r0
   <= 4
 radix_out_r1: map_r1_r0 + map_r1_r2 + map_r1_r3 + map_r1_r4 + map_r1_r5
   <= 4
 radix_in_r1: map_r0_r1 + map_r2_r1 + map_r3_r1 + map_r4_r1 + map_r5_r1
   <= 4
 radix_out_r2: map_r2_r0 + map_r2_r1 + map_r2_r3 + map_r2_r4 + map_r2_r5
   <= 4
 radix_in_r2: map_r0_r2 + map_r1_r2 + map_r3_r2 + map_r4_r2 + map_r5_r2
   <= 4
 radix_out_r3: map_r3_r0 + map_r3_r1 + map_r3_r2 + map_r3_r4 + map_r3_r5
   <= 4
 radix_in_r3: map_r0_r3 + map_r1_r3 + map_r2_r3 + map_r4_r3 + map_r5_r3
   <= 4
 radix_out_r4: map_r4_r0 + map_r4_r1 + map_r4_r2 + map_r4_r3 + map_r4_r5
   <= 4
 radix_in_r4: map_r0_r4 + map_r1_r4 + map_r2_r4 + map_r3_r4 + map_r5_r4
   <= 4
 radix_out_r5: map_r5_r0 + map_r5_r1 + map_r5_r2 + map_r5_r3 + map_r5_r4
   <= 4
 radix_in_r5: map_r0_r5 + map_r1_r5 + map_r2_r5 + map_r3_r5 + map_r4_r5
   <= 4
 map2onehop_r0_r1: - 6 map_r0_r1 - onehop_r0_r1 = -7
 map2onehop_r0_r2: - 6 map_r0_r2 - onehop_r0_r2 = -7
 map2onehop_r0_r3: - 6 map_r0_r3 - onehop_r0_r3 = -7
 map2onehop_r0_r4: - 6 map_r0_r4 - onehop_r0_r4 = -7
 map2onehop_r0_r5: - 6 map_r0_r5 - onehop_r0_r5 = -7
 map2onehop_r1_r0: - 6 map_r1_r0 - onehop_r1_r0 = -7
 map2onehop_r1_r2: - 6 map_r1_r2 - onehop_r1_r2 = -7
 map2onehop_r1_r3: - 6 map_r1_r3 - onehop_r1_r3 = -7
 map2onehop_r1_r4: - 6 map_r1_r4 - onehop_r1_r4 = -7
 map2onehop_r1_r5: - 6 map_r1_r5 - onehop_r1_r5 = -7
 map2onehop_r2_r0: - 6 map_r2_r0 - onehop_r2_r0 = -7
 map2onehop_r2_r1: - 6 map_r2_r1 - onehop_r2_r1 = -7
 map2onehop_r2_r3: - 6 map_r2_r3 - onehop_r2_r3 = -7
 map2onehop_r2_r4: - 6 map_r2_r4 - onehop_r2_r4 = -7
 map2onehop_r2_r5: - 6 map_r2_r5 - onehop_r2_r5 = -7
 map2onehop_r3_r0: - 6 map_r3_r0 - onehop_r3_r0 = -7
 map2onehop_r3_r1: - 6 map_r3_r1 - onehop_r3_r1 = -7
 map2onehop_r3_r2: - 6 map_r3_r2 - onehop_r3_r2 = -7
 map2onehop_r3_r4: - 6 map_r3_r4 - onehop_r3_r4 = -7
 map2onehop_r3_r5: - 6 map_r3_r5 - onehop_r3_r5 = -7
 map2onehop_r4_r0: - 6 map_r4_r0 - onehop_r4_r0 = -7
 map2onehop_r4_r1: - 6 map_r4_r1 - onehop_r4_r1 = -7
 map2onehop_r4_r2: - 6 map_r4_r2 - onehop_r4_r2 = -7
 map2onehop_r4_r3: - 6 map_r4_r3 - onehop_r4_r3 = -7
 map2onehop_r4_r5: - 6 map_r4_r5 - onehop_r4_r5 = -7
 map2onehop_r5_r0: - 6 map_r5_r0 - onehop_r5_r0 = -7
 map2onehop_r5_r1: - 6 map_r5_r1 - onehop_r5_r1 = -7
 map2onehop_r5_r2: - 6 map_r5_r2 - onehop_r5_r2 = -7
 map2onehop_r5_r3: - 6 map_r5_r3 - onehop_r5_r3 = -7
 map2onehop_r5_r4: - 6 map_r5_r4 - onehop_r5_r4 = -7
 k_route_r0_r1_k0: C110 = 6
 k_route_r0_r1_k1: onehop_r0_r1 + dist_r1_r1 - k_route_i0_k1_j1 = 0
 k_route_r0_r1_k2: onehop_r0_r2 + dist_r2_r1 - k_route_i0_k2_j1 = 0
 k_route_r0_r1_k3: onehop_r0_r3 + dist_r3_r1 - k_route_i0_k3_j1 = 0
 k_route_r0_r1_k4: onehop_r0_r4 + dist_r4_r1 - k_route_i0_k4_j1 = 0
 k_route_r0_r1_k5: onehop_r0_r5 + dist_r5_r1 - k_route_i0_k5_j1 = 0
 R66: C116 >= 0
 R67: C117 >= 0
 R68: C118 >= 0
 R69: C119 >= 0
 R70: C120 >= 0
 R71: C121 >= 0
 R72: C122 >= 0
 min_kroute_zatmost_r0_r1: C123 + C124 + C125 + C126 + C127 + C128 + C129
   >= 1
 min_kroute_res_r0_r1_r0: - dist_r0_r1 + C110 - C116 = 0
 min_kroute_res_r0_r1_r1: - dist_r0_r1 + k_route_i0_k1_j1 - C117 = 0
 min_kroute_res_r0_r1_r2: - dist_r0_r1 + k_route_i0_k2_j1 - C118 = 0
 min_kroute_res_r0_r1_r3: - dist_r0_r1 + k_route_i0_k3_j1 - C119 = 0
 min_kroute_res_r0_r1_r4: - dist_r0_r1 + k_route_i0_k4_j1 - C120 = 0
 min_kroute_res_r0_r1_r5: - dist_r0_r1 + k_route_i0_k5_j1 - C121 = 0
 min_kroute_res_r0_r1_r6: - dist_r0_r1 - C122 = -12
 R81: - C116 - 0.001 C123 <= -0.001
 R82: - C116 - 12 C123 >= -12
 R83: - C117 - 0.001 C124 <= -0.001
 R84: - C117 - 12 C124 >= -12
 R85: - C118 - 0.001 C125 <= -0.001
 R86: - C118 - 12 C125 >= -12
 R87: - C119 - 0.001 C126 <= -0.001
 R88: - C119 - 12 C126 >= -12
 R89: - C120 - 0.001 C127 <= -0.001
 R90: - C120 - 12 C127 >= -12
 R91: - C121 - 0.001 C128 <= -0.001
 R92: - C121 - 12 C128 >= -12
 R93: - C122 - 0.001 C129 <= -0.001
 R94: - C122 - 12 C129 >= -12
 k_route_r0_r2_k0: C130 = 6
 k_route_r0_r2_k1: onehop_r0_r1 + dist_r1_r2 - k_route_i0_k1_j2 = 0
 k_route_r0_r2_k2: onehop_r0_r2 + dist_r2_r2 - k_route_i0_k2_j2 = 0
 k_route_r0_r2_k3: onehop_r0_r3 + dist_r3_r2 - k_route_i0_k3_j2 = 0
 k_route_r0_r2_k4: onehop_r0_r4 + dist_r4_r2 - k_route_i0_k4_j2 = 0
 k_route_r0_r2_k5: onehop_r0_r5 + dist_r5_r2 - k_route_i0_k5_j2 = 0
 R101: C136 >= 0
 R102: C137 >= 0
 R103: C138 >= 0
 R104: C139 >= 0
 R105: C140 >= 0
 R106: C141 >= 0
 R107: C142 >= 0
 min_kroute_zatmost_r0_r2: C143 + C144 + C145 + C146 + C147 + C148 + C149
   >= 1
 min_kroute_res_r0_r2_r0: - dist_r0_r2 + C130 - C136 = 0
 min_kroute_res_r0_r2_r1: - dist_r0_r2 + k_route_i0_k1_j2 - C137 = 0
 min_kroute_res_r0_r2_r2: - dist_r0_r2 + k_route_i0_k2_j2 - C138 = 0
 min_kroute_res_r0_r2_r3: - dist_r0_r2 + k_route_i0_k3_j2 - C139 = 0
 min_kroute_res_r0_r2_r4: - dist_r0_r2 + k_route_i0_k4_j2 - C140 = 0
 min_kroute_res_r0_r2_r5: - dist_r0_r2 + k_route_i0_k5_j2 - C141 = 0
 min_kroute_res_r0_r2_r6: - dist_r0_r2 - C142 = -12
 R116: - C136 - 0.001 C143 <= -0.001
 R117: - C136 - 12 C143 >= -12
 R118: - C137 - 0.001 C144 <= -0.001
 R119: - C137 - 12 C144 >= -12
 R120: - C138 - 0.001 C145 <= -0.001
 R121: - C138 - 12 C145 >= -12
 R122: - C139 - 0.001 C146 <= -0.001
 R123: - C139 - 12 C146 >= -12
 R124: - C140 - 0.001 C147 <= -0.001
 R125: - C140 - 12 C147 >= -12
 R126: - C141 - 0.001 C148 <= -0.001
 R127: - C141 - 12 C148 >= -12
 R128: - C142 - 0.001 C149 <= -0.001
 R129: - C142 - 12 C149 >= -12
 k_route_r0_r3_k0: C150 = 6
 k_route_r0_r3_k1: onehop_r0_r1 + dist_r1_r3 - k_route_i0_k1_j3 = 0
 k_route_r0_r3_k2: onehop_r0_r2 + dist_r2_r3 - k_route_i0_k2_j3 = 0
 k_route_r0_r3_k3: onehop_r0_r3 + dist_r3_r3 - k_route_i0_k3_j3 = 0
 k_route_r0_r3_k4: onehop_r0_r4 + dist_r4_r3 - k_route_i0_k4_j3 = 0
 k_route_r0_r3_k5: onehop_r0_r5 + dist_r5_r3 - k_route_i0_k5_j3 = 0
 R136: C156 >= 0
 R137: C157 >= 0
 R138: C158 >= 0
 R139: C159 >= 0
 R140: C160 >= 0
 R141: C161 >= 0
 R142: C162 >= 0
 min_kroute_zatmost_r0_r3: C163 + C164 + C165 + C166 + C167 + C168 + C169
   >= 1
 min_kroute_res_r0_r3_r0: - dist_r0_r3 + C150 - C156 = 0
 min_kroute_res_r0_r3_r1: - dist_r0_r3 + k_route_i0_k1_j3 - C157 = 0
 min_kroute_res_r0_r3_r2: - dist_r0_r3 + k_route_i0_k2_j3 - C158 = 0
 min_kroute_res_r0_r3_r3: - dist_r0_r3 + k_route_i0_k3_j3 - C159 = 0
 min_kroute_res_r0_r3_r4: - dist_r0_r3 + k_route_i0_k4_j3 - C160 = 0
 min_kroute_res_r0_r3_r5: - dist_r0_r3 + k_route_i0_k5_j3 - C161 = 0
 min_kroute_res_r0_r3_r6: - dist_r0_r3 - C162 = -12
 R151: - C156 - 0.001 C163 <= -0.001
 R152: - C156 - 12 C163 >= -12
 R153: - C157 - 0.001 C164 <= -0.001
 R154: - C157 - 12 C164 >= -12
 R155: - C158 - 0.001 C165 <= -0.001
 R156: - C158 - 12 C165 >= -12
 R157: - C159 - 0.001 C166 <= -0.001
 R158: - C159 - 12 C166 >= -12
 R159: - C160 - 0.001 C167 <= -0.001
 R160: - C160 - 12 C167 >= -12
 R161: - C161 - 0.001 C168 <= -0.001
 R162: - C161 - 12 C168 >= -12
 R163: - C162 - 0.001 C169 <= -0.001
 R164: - C162 - 12 C169 >= -12
 k_route_r0_r4_k0: C170 = 6
 k_route_r0_r4_k1: onehop_r0_r1 + dist_r1_r4 - k_route_i0_k1_j4 = 0
 k_route_r0_r4_k2: onehop_r0_r2 + dist_r2_r4 - k_route_i0_k2_j4 = 0
 k_route_r0_r4_k3: onehop_r0_r3 + dist_r3_r4 - k_route_i0_k3_j4 = 0
 k_route_r0_r4_k4: onehop_r0_r4 + dist_r4_r4 - k_route_i0_k4_j4 = 0
 k_route_r0_r4_k5: onehop_r0_r5 + dist_r5_r4 - k_route_i0_k5_j4 = 0
 R171: C176 >= 0
 R172: C177 >= 0
 R173: C178 >= 0
 R174: C179 >= 0
 R175: C180 >= 0
 R176: C181 >= 0
 R177: C182 >= 0
 min_kroute_zatmost_r0_r4: C183 + C184 + C185 + C186 + C187 + C188 + C189
   >= 1
 min_kroute_res_r0_r4_r0: - dist_r0_r4 + C170 - C176 = 0
 min_kroute_res_r0_r4_r1: - dist_r0_r4 + k_route_i0_k1_j4 - C177 = 0
 min_kroute_res_r0_r4_r2: - dist_r0_r4 + k_route_i0_k2_j4 - C178 = 0
 min_kroute_res_r0_r4_r3: - dist_r0_r4 + k_route_i0_k3_j4 - C179 = 0
 min_kroute_res_r0_r4_r4: - dist_r0_r4 + k_route_i0_k4_j4 - C180 = 0
 min_kroute_res_r0_r4_r5: - dist_r0_r4 + k_route_i0_k5_j4 - C181 = 0
 min_kroute_res_r0_r4_r6: - dist_r0_r4 - C182 = -12
 R186: - C176 - 0.001 C183 <= -0.001
 R187: - C176 - 12 C183 >= -12
 R188: - C177 - 0.001 C184 <= -0.001
 R189: - C177 - 12 C184 >= -12
 R190: - C178 - 0.001 C185 <= -0.001
 R191: - C178 - 12 C185 >= -12
 R192: - C179 - 0.001 C186 <= -0.001
 R193: - C179 - 12 C186 >= -12
 R194: - C180 - 0.001 C187 <= -0.001
 R195: - C180 - 12 C187 >= -12
 R196: - C181 - 0.001 C188 <= -0.001
 R197: - C181 - 12 C188 >= -12
 R198: - C182 - 0.001 C189 <= -0.001
 R199: - C182 - 12 C189 >= -12
 k_route_r0_r5_k0: C190 = 6
 k_route_r0_r5_k1: onehop_r0_r1 + dist_r1_r5 - k_route_i0_k1_j5 = 0
 k_route_r0_r5_k2: onehop_r0_r2 + dist_r2_r5 - k_route_i0_k2_j5 = 0
 k_route_r0_r5_k3: onehop_r0_r3 + dist_r3_r5 - k_route_i0_k3_j5 = 0
 k_route_r0_r5_k4: onehop_r0_r4 + dist_r4_r5 - k_route_i0_k4_j5 = 0
 k_route_r0_r5_k5: onehop_r0_r5 + dist_r5_r5 - k_route_i0_k5_j5 = 0
 R206: C196 >= 0
 R207: C197 >= 0
 R208: C198 >= 0
 R209: C199 >= 0
 R210: C200 >= 0
 R211: C201 >= 0
 R212: C202 >= 0
 min_kroute_zatmost_r0_r5: C203 + C204 + C205 + C206 + C207 + C208 + C209
   >= 1
 min_kroute_res_r0_r5_r0: - dist_r0_r5 + C190 - C196 = 0
 min_kroute_res_r0_r5_r1: - dist_r0_r5 + k_route_i0_k1_j5 - C197 = 0
 min_kroute_res_r0_r5_r2: - dist_r0_r5 + k_route_i0_k2_j5 - C198 = 0
 min_kroute_res_r0_r5_r3: - dist_r0_r5 + k_route_i0_k3_j5 - C199 = 0
 min_kroute_res_r0_r5_r4: - dist_r0_r5 + k_route_i0_k4_j5 - C200 = 0
 min_kroute_res_r0_r5_r5: - dist_r0_r5 + k_route_i0_k5_j5 - C201 = 0
 min_kroute_res_r0_r5_r6: - dist_r0_r5 - C202 = -12
 R221: - C196 - 0.001 C203 <= -0.001
 R222: - C196 - 12 C203 >= -12
 R223: - C197 - 0.001 C204 <= -0.001
 R224: - C197 - 12 C204 >= -12
 R225: - C198 - 0.001 C205 <= -0.001
 R226: - C198 - 12 C205 >= -12
 R227: - C199 - 0.001 C206 <= -0.001
 R228: - C199 - 12 C206 >= -12
 R229: - C200 - 0.001 C207 <= -0.001
 R230: - C200 - 12 C207 >= -12
 R231: - C201 - 0.001 C208 <= -0.001
 R232: - C201 - 12 C208 >= -12
 R233: - C202 - 0.001 C209 <= -0.001
 R234: - C202 - 12 C209 >= -12
 k_route_r1_r0_k0: dist_r0_r0 + onehop_r1_r0 - k_route_i1_k0_j0 = 0
 k_route_r1_r0_k1: C211 = 6
 k_route_r1_r0_k2: onehop_r1_r2 + dist_r2_r0 - k_route_i1_k2_j0 = 0
 k_route_r1_r0_k3: onehop_r1_r3 + dist_r3_r0 - k_route_i1_k3_j0 = 0
 k_route_r1_r0_k4: onehop_r1_r4 + dist_r4_r0 - k_route_i1_k4_j0 = 0
 k_route_r1_r0_k5: onehop_r1_r5 + dist_r5_r0 - k_route_i1_k5_j0 = 0
 R241: C216 >= 0
 R242: C217 >= 0
 R243: C218 >= 0
 R244: C219 >= 0
 R245: C220 >= 0
 R246: C221 >= 0
 R247: C222 >= 0
 min_kroute_zatmost_r1_r0: C223 + C224 + C225 + C226 + C227 + C228 + C229
   >= 1
 min_kroute_res_r1_r0_r0: - dist_r1_r0 + k_route_i1_k0_j0 - C216 = 0
 min_kroute_res_r1_r0_r1: - dist_r1_r0 + C211 - C217 = 0
 min_kroute_res_r1_r0_r2: - dist_r1_r0 + k_route_i1_k2_j0 - C218 = 0
 min_kroute_res_r1_r0_r3: - dist_r1_r0 + k_route_i1_k3_j0 - C219 = 0
 min_kroute_res_r1_r0_r4: - dist_r1_r0 + k_route_i1_k4_j0 - C220 = 0
 min_kroute_res_r1_r0_r5: - dist_r1_r0 + k_route_i1_k5_j0 - C221 = 0
 min_kroute_res_r1_r0_r6: - dist_r1_r0 - C222 = -12
 R256: - C216 - 0.001 C223 <= -0.001
 R257: - C216 - 12 C223 >= -12
 R258: - C217 - 0.001 C224 <= -0.001
 R259: - C217 - 12 C224 >= -12
 R260: - C218 - 0.001 C225 <= -0.001
 R261: - C218 - 12 C225 >= -12
 R262: - C219 - 0.001 C226 <= -0.001
 R263: - C219 - 12 C226 >= -12
 R264: - C220 - 0.001 C227 <= -0.001
 R265: - C220 - 12 C227 >= -12
 R266: - C221 - 0.001 C228 <= -0.001
 R267: - C221 - 12 C228 >= -12
 R268: - C222 - 0.001 C229 <= -0.001
 R269: - C222 - 12 C229 >= -12
 k_route_r1_r2_k0: dist_r0_r2 + onehop_r1_r0 - k_route_i1_k0_j2 = 0
 k_route_r1_r2_k1: C231 = 6
 k_route_r1_r2_k2: onehop_r1_r2 + dist_r2_r2 - k_route_i1_k2_j2 = 0
 k_route_r1_r2_k3: onehop_r1_r3 + dist_r3_r2 - k_route_i1_k3_j2 = 0
 k_route_r1_r2_k4: onehop_r1_r4 + dist_r4_r2 - k_route_i1_k4_j2 = 0
 k_route_r1_r2_k5: onehop_r1_r5 + dist_r5_r2 - k_route_i1_k5_j2 = 0
 R276: C236 >= 0
 R277: C237 >= 0
 R278: C238 >= 0
 R279: C239 >= 0
 R280: C240 >= 0
 R281: C241 >= 0
 R282: C242 >= 0
 min_kroute_zatmost_r1_r2: C243 + C244 + C245 + C246 + C247 + C248 + C249
   >= 1
 min_kroute_res_r1_r2_r0: - dist_r1_r2 + k_route_i1_k0_j2 - C236 = 0
 min_kroute_res_r1_r2_r1: - dist_r1_r2 + C231 - C237 = 0
 min_kroute_res_r1_r2_r2: - dist_r1_r2 + k_route_i1_k2_j2 - C238 = 0
 min_kroute_res_r1_r2_r3: - dist_r1_r2 + k_route_i1_k3_j2 - C239 = 0
 min_kroute_res_r1_r2_r4: - dist_r1_r2 + k_route_i1_k4_j2 - C240 = 0
 min_kroute_res_r1_r2_r5: - dist_r1_r2 + k_route_i1_k5_j2 - C241 = 0
 min_kroute_res_r1_r2_r6: - dist_r1_r2 - C242 = -12
 R291: - C236 - 0.001 C243 <= -0.001
 R292: - C236 - 12 C243 >= -12
 R293: - C237 - 0.001 C244 <= -0.001
 R294: - C237 - 12 C244 >= -12
 R295: - C238 - 0.001 C245 <= -0.001
 R296: - C238 - 12 C245 >= -12
 R297: - C239 - 0.001 C246 <= -0.001
 R298: - C239 - 12 C246 >= -12
 R299: - C240 - 0.001 C247 <= -0.001
 R300: - C240 - 12 C247 >= -12
 R301: - C241 - 0.001 C248 <= -0.001
 R302: - C241 - 12 C248 >= -12
 R303: - C242 - 0.001 C249 <= -0.001
 R304: - C242 - 12 C249 >= -12
 k_route_r1_r3_k0: dist_r0_r3 + onehop_r1_r0 - k_route_i1_k0_j3 = 0
 k_route_r1_r3_k1: C251 = 6
 k_route_r1_r3_k2: onehop_r1_r2 + dist_r2_r3 - k_route_i1_k2_j3 = 0
 k_route_r1_r3_k3: onehop_r1_r3 + dist_r3_r3 - k_route_i1_k3_j3 = 0
 k_route_r1_r3_k4: onehop_r1_r4 + dist_r4_r3 - k_route_i1_k4_j3 = 0
 k_route_r1_r3_k5: onehop_r1_r5 + dist_r5_r3 - k_route_i1_k5_j3 = 0
 R311: C256 >= 0
 R312: C257 >= 0
 R313: C258 >= 0
 R314: C259 >= 0
 R315: C260 >= 0
 R316: C261 >= 0
 R317: C262 >= 0
 min_kroute_zatmost_r1_r3: C263 + C264 + C265 + C266 + C267 + C268 + C269
   >= 1
 min_kroute_res_r1_r3_r0: - dist_r1_r3 + k_route_i1_k0_j3 - C256 = 0
 min_kroute_res_r1_r3_r1: - dist_r1_r3 + C251 - C257 = 0
 min_kroute_res_r1_r3_r2: - dist_r1_r3 + k_route_i1_k2_j3 - C258 = 0
 min_kroute_res_r1_r3_r3: - dist_r1_r3 + k_route_i1_k3_j3 - C259 = 0
 min_kroute_res_r1_r3_r4: - dist_r1_r3 + k_route_i1_k4_j3 - C260 = 0
 min_kroute_res_r1_r3_r5: - dist_r1_r3 + k_route_i1_k5_j3 - C261 = 0
 min_kroute_res_r1_r3_r6: - dist_r1_r3 - C262 = -12
 R326: - C256 - 0.001 C263 <= -0.001
 R327: - C256 - 12 C263 >= -12
 R328: - C257 - 0.001 C264 <= -0.001
 R329: - C257 - 12 C264 >= -12
 R330: - C258 - 0.001 C265 <= -0.001
 R331: - C258 - 12 C265 >= -12
 R332: - C259 - 0.001 C266 <= -0.001
 R333: - C259 - 12 C266 >= -12
 R334: - C260 - 0.001 C267 <= -0.001
 R335: - C260 - 12 C267 >= -12
 R336: - C261 - 0.001 C268 <= -0.001
 R337: - C261 - 12 C268 >= -12
 R338: - C262 - 0.001 C269 <= -0.001
 R339: - C262 - 12 C269 >= -12
 k_route_r1_r4_k0: dist_r0_r4 + onehop_r1_r0 - k_route_i1_k0_j4 = 0
 k_route_r1_r4_k1: C271 = 6
 k_route_r1_r4_k2: onehop_r1_r2 + dist_r2_r4 - k_route_i1_k2_j4 = 0
 k_route_r1_r4_k3: onehop_r1_r3 + dist_r3_r4 - k_route_i1_k3_j4 = 0
 k_route_r1_r4_k4: onehop_r1_r4 + dist_r4_r4 - k_route_i1_k4_j4 = 0
 k_route_r1_r4_k5: onehop_r1_r5 + dist_r5_r4 - k_route_i1_k5_j4 = 0
 R346: C276 >= 0
 R347: C277 >= 0
 R348: C278 >= 0
 R349: C279 >= 0
 R350: C280 >= 0
 R351: C281 >= 0
 R352: C282 >= 0
 min_kroute_zatmost_r1_r4: C283 + C284 + C285 + C286 + C287 + C288 + C289
   >= 1
 min_kroute_res_r1_r4_r0: - dist_r1_r4 + k_route_i1_k0_j4 - C276 = 0
 min_kroute_res_r1_r4_r1: - dist_r1_r4 + C271 - C277 = 0
 min_kroute_res_r1_r4_r2: - dist_r1_r4 + k_route_i1_k2_j4 - C278 = 0
 min_kroute_res_r1_r4_r3: - dist_r1_r4 + k_route_i1_k3_j4 - C279 = 0
 min_kroute_res_r1_r4_r4: - dist_r1_r4 + k_route_i1_k4_j4 - C280 = 0
 min_kroute_res_r1_r4_r5: - dist_r1_r4 + k_route_i1_k5_j4 - C281 = 0
 min_kroute_res_r1_r4_r6: - dist_r1_r4 - C282 = -12
 R361: - C276 - 0.001 C283 <= -0.001
 R362: - C276 - 12 C283 >= -12
 R363: - C277 - 0.001 C284 <= -0.001
 R364: - C277 - 12 C284 >= -12
 R365: - C278 - 0.001 C285 <= -0.001
 R366: - C278 - 12 C285 >= -12
 R367: - C279 - 0.001 C286 <= -0.001
 R368: - C279 - 12 C286 >= -12
 R369: - C280 - 0.001 C287 <= -0.001
 R370: - C280 - 12 C287 >= -12
 R371: - C281 - 0.001 C288 <= -0.001
 R372: - C281 - 12 C288 >= -12
 R373: - C282 - 0.001 C289 <= -0.001
 R374: - C282 - 12 C289 >= -12
 k_route_r1_r5_k0: dist_r0_r5 + onehop_r1_r0 - k_route_i1_k0_j5 = 0
 k_route_r1_r5_k1: C291 = 6
 k_route_r1_r5_k2: onehop_r1_r2 + dist_r2_r5 - k_route_i1_k2_j5 = 0
 k_route_r1_r5_k3: onehop_r1_r3 + dist_r3_r5 - k_route_i1_k3_j5 = 0
 k_route_r1_r5_k4: onehop_r1_r4 + dist_r4_r5 - k_route_i1_k4_j5 = 0
 k_route_r1_r5_k5: onehop_r1_r5 + dist_r5_r5 - k_route_i1_k5_j5 = 0
 R381: C296 >= 0
 R382: C297 >= 0
 R383: C298 >= 0
 R384: C299 >= 0
 R385: C300 >= 0
 R386: C301 >= 0
 R387: C302 >= 0
 min_kroute_zatmost_r1_r5: C303 + C304 + C305 + C306 + C307 + C308 + C309
   >= 1
 min_kroute_res_r1_r5_r0: - dist_r1_r5 + k_route_i1_k0_j5 - C296 = 0
 min_kroute_res_r1_r5_r1: - dist_r1_r5 + C291 - C297 = 0
 min_kroute_res_r1_r5_r2: - dist_r1_r5 + k_route_i1_k2_j5 - C298 = 0
 min_kroute_res_r1_r5_r3: - dist_r1_r5 + k_route_i1_k3_j5 - C299 = 0
 min_kroute_res_r1_r5_r4: - dist_r1_r5 + k_route_i1_k4_j5 - C300 = 0
 min_kroute_res_r1_r5_r5: - dist_r1_r5 + k_route_i1_k5_j5 - C301 = 0
 min_kroute_res_r1_r5_r6: - dist_r1_r5 - C302 = -12
 R396: - C296 - 0.001 C303 <= -0.001
 R397: - C296 - 12 C303 >= -12
 R398: - C297 - 0.001 C304 <= -0.001
 R399: - C297 - 12 C304 >= -12
 R400: - C298 - 0.001 C305 <= -0.001
 R401: - C298 - 12 C305 >= -12
 R402: - C299 - 0.001 C306 <= -0.001
 R403: - C299 - 12 C306 >= -12
 R404: - C300 - 0.001 C307 <= -0.001
 R405: - C300 - 12 C307 >= -12
 R406: - C301 - 0.001 C308 <= -0.001
 R407: - C301 - 12 C308 >= -12
 R408: - C302 - 0.001 C309 <= -0.001
 R409: - C302 - 12 C309 >= -12
 k_route_r2_r0_k0: dist_r0_r0 + onehop_r2_r0 - k_route_i2_k0_j0 = 0
 k_route_r2_r0_k1: dist_r1_r0 + onehop_r2_r1 - k_route_i2_k1_j0 = 0
 k_route_r2_r0_k2: C312 = 6
 k_route_r2_r0_k3: onehop_r2_r3 + dist_r3_r0 - k_route_i2_k3_j0 = 0
 k_route_r2_r0_k4: onehop_r2_r4 + dist_r4_r0 - k_route_i2_k4_j0 = 0
 k_route_r2_r0_k5: onehop_r2_r5 + dist_r5_r0 - k_route_i2_k5_j0 = 0
 R416: C316 >= 0
 R417: C317 >= 0
 R418: C318 >= 0
 R419: C319 >= 0
 R420: C320 >= 0
 R421: C321 >= 0
 R422: C322 >= 0
 min_kroute_zatmost_r2_r0: C323 + C324 + C325 + C326 + C327 + C328 + C329
   >= 1
 min_kroute_res_r2_r0_r0: - dist_r2_r0 + k_route_i2_k0_j0 - C316 = 0
 min_kroute_res_r2_r0_r1: - dist_r2_r0 + k_route_i2_k1_j0 - C317 = 0
 min_kroute_res_r2_r0_r2: - dist_r2_r0 + C312 - C318 = 0
 min_kroute_res_r2_r0_r3: - dist_r2_r0 + k_route_i2_k3_j0 - C319 = 0
 min_kroute_res_r2_r0_r4: - dist_r2_r0 + k_route_i2_k4_j0 - C320 = 0
 min_kroute_res_r2_r0_r5: - dist_r2_r0 + k_route_i2_k5_j0 - C321 = 0
 min_kroute_res_r2_r0_r6: - dist_r2_r0 - C322 = -12
 R431: - C316 - 0.001 C323 <= -0.001
 R432: - C316 - 12 C323 >= -12
 R433: - C317 - 0.001 C324 <= -0.001
 R434: - C317 - 12 C324 >= -12
 R435: - C318 - 0.001 C325 <= -0.001
 R436: - C318 - 12 C325 >= -12
 R437: - C319 - 0.001 C326 <= -0.001
 R438: - C319 - 12 C326 >= -12
 R439: - C320 - 0.001 C327 <= -0.001
 R440: - C320 - 12 C327 >= -12
 R441: - C321 - 0.001 C328 <= -0.001
 R442: - C321 - 12 C328 >= -12
 R443: - C322 - 0.001 C329 <= -0.001
 R444: - C322 - 12 C329 >= -12
 k_route_r2_r1_k0: dist_r0_r1 + onehop_r2_r0 - k_route_i2_k0_j1 = 0
 k_route_r2_r1_k1: dist_r1_r1 + onehop_r2_r1 - k_route_i2_k1_j1 = 0
 k_route_r2_r1_k2: C332 = 6
 k_route_r2_r1_k3: onehop_r2_r3 + dist_r3_r1 - k_route_i2_k3_j1 = 0
 k_route_r2_r1_k4: onehop_r2_r4 + dist_r4_r1 - k_route_i2_k4_j1 = 0
 k_route_r2_r1_k5: onehop_r2_r5 + dist_r5_r1 - k_route_i2_k5_j1 = 0
 R451: C336 >= 0
 R452: C337 >= 0
 R453: C338 >= 0
 R454: C339 >= 0
 R455: C340 >= 0
 R456: C341 >= 0
 R457: C342 >= 0
 min_kroute_zatmost_r2_r1: C343 + C344 + C345 + C346 + C347 + C348 + C349
   >= 1
 min_kroute_res_r2_r1_r0: - dist_r2_r1 + k_route_i2_k0_j1 - C336 = 0
 min_kroute_res_r2_r1_r1: - dist_r2_r1 + k_route_i2_k1_j1 - C337 = 0
 min_kroute_res_r2_r1_r2: - dist_r2_r1 + C332 - C338 = 0
 min_kroute_res_r2_r1_r3: - dist_r2_r1 + k_route_i2_k3_j1 - C339 = 0
 min_kroute_res_r2_r1_r4: - dist_r2_r1 + k_route_i2_k4_j1 - C340 = 0
 min_kroute_res_r2_r1_r5: - dist_r2_r1 + k_route_i2_k5_j1 - C341 = 0
 min_kroute_res_r2_r1_r6: - dist_r2_r1 - C342 = -12
 R466: - C336 - 0.001 C343 <= -0.001
 R467: - C336 - 12 C343 >= -12
 R468: - C337 - 0.001 C344 <= -0.001
 R469: - C337 - 12 C344 >= -12
 R470: - C338 - 0.001 C345 <= -0.001
 R471: - C338 - 12 C345 >= -12
 R472: - C339 - 0.001 C346 <= -0.001
 R473: - C339 - 12 C346 >= -12
 R474: - C340 - 0.001 C347 <= -0.001
 R475: - C340 - 12 C347 >= -12
 R476: - C341 - 0.001 C348 <= -0.001
 R477: - C341 - 12 C348 >= -12
 R478: - C342 - 0.001 C349 <= -0.001
 R479: - C342 - 12 C349 >= -12
 k_route_r2_r3_k0: dist_r0_r3 + onehop_r2_r0 - k_route_i2_k0_j3 = 0
 k_route_r2_r3_k1: dist_r1_r3 + onehop_r2_r1 - k_route_i2_k1_j3 = 0
 k_route_r2_r3_k2: C352 = 6
 k_route_r2_r3_k3: onehop_r2_r3 + dist_r3_r3 - k_route_i2_k3_j3 = 0
 k_route_r2_r3_k4: onehop_r2_r4 + dist_r4_r3 - k_route_i2_k4_j3 = 0
 k_route_r2_r3_k5: onehop_r2_r5 + dist_r5_r3 - k_route_i2_k5_j3 = 0
 R486: C356 >= 0
 R487: C357 >= 0
 R488: C358 >= 0
 R489: C359 >= 0
 R490: C360 >= 0
 R491: C361 >= 0
 R492: C362 >= 0
 min_kroute_zatmost_r2_r3: C363 + C364 + C365 + C366 + C367 + C368 + C369
   >= 1
 min_kroute_res_r2_r3_r0: - dist_r2_r3 + k_route_i2_k0_j3 - C356 = 0
 min_kroute_res_r2_r3_r1: - dist_r2_r3 + k_route_i2_k1_j3 - C357 = 0
 min_kroute_res_r2_r3_r2: - dist_r2_r3 + C352 - C358 = 0
 min_kroute_res_r2_r3_r3: - dist_r2_r3 + k_route_i2_k3_j3 - C359 = 0
 min_kroute_res_r2_r3_r4: - dist_r2_r3 + k_route_i2_k4_j3 - C360 = 0
 min_kroute_res_r2_r3_r5: - dist_r2_r3 + k_route_i2_k5_j3 - C361 = 0
 min_kroute_res_r2_r3_r6: - dist_r2_r3 - C362 = -12
 R501: - C356 - 0.001 C363 <= -0.001
 R502: - C356 - 12 C363 >= -12
 R503: - C357 - 0.001 C364 <= -0.001
 R504: - C357 - 12 C364 >= -12
 R505: - C358 - 0.001 C365 <= -0.001
 R506: - C358 - 12 C365 >= -12
 R507: - C359 - 0.001 C366 <= -0.001
 R508: - C359 - 12 C366 >= -12
 R509: - C360 - 0.001 C367 <= -0.001
 R510: - C360 - 12 C367 >= -12
 R511: - C361 - 0.001 C368 <= -0.001
 R512: - C361 - 12 C368 >= -12
 R513: - C362 - 0.001 C369 <= -0.001
 R514: - C362 - 12 C369 >= -12
 k_route_r2_r4_k0: dist_r0_r4 + onehop_r2_r0 - k_route_i2_k0_j4 = 0
 k_route_r2_r4_k1: dist_r1_r4 + onehop_r2_r1 - k_route_i2_k1_j4 = 0
 k_route_r2_r4_k2: C372 = 6
 k_route_r2_r4_k3: onehop_r2_r3 + dist_r3_r4 - k_route_i2_k3_j4 = 0
 k_route_r2_r4_k4: onehop_r2_r4 + dist_r4_r4 - k_route_i2_k4_j4 = 0
 k_route_r2_r4_k5: onehop_r2_r5 + dist_r5_r4 - k_route_i2_k5_j4 = 0
 R521: C376 >= 0
 R522: C377 >= 0
 R523: C378 >= 0
 R524: C379 >= 0
 R525: C380 >= 0
 R526: C381 >= 0
 R527: C382 >= 0
 min_kroute_zatmost_r2_r4: C383 + C384 + C385 + C386 + C387 + C388 + C389
   >= 1
 min_kroute_res_r2_r4_r0: - dist_r2_r4 + k_route_i2_k0_j4 - C376 = 0
 min_kroute_res_r2_r4_r1: - dist_r2_r4 + k_route_i2_k1_j4 - C377 = 0
 min_kroute_res_r2_r4_r2: - dist_r2_r4 + C372 - C378 = 0
 min_kroute_res_r2_r4_r3: - dist_r2_r4 + k_route_i2_k3_j4 - C379 = 0
 min_kroute_res_r2_r4_r4: - dist_r2_r4 + k_route_i2_k4_j4 - C380 = 0
 min_kroute_res_r2_r4_r5: - dist_r2_r4 + k_route_i2_k5_j4 - C381 = 0
 min_kroute_res_r2_r4_r6: - dist_r2_r4 - C382 = -12
 R536: - C376 - 0.001 C383 <= -0.001
 R537: - C376 - 12 C383 >= -12
 R538: - C377 - 0.001 C384 <= -0.001
 R539: - C377 - 12 C384 >= -12
 R540: - C378 - 0.001 C385 <= -0.001
 R541: - C378 - 12 C385 >= -12
 R542: - C379 - 0.001 C386 <= -0.001
 R543: - C379 - 12 C386 >= -12
 R544: - C380 - 0.001 C387 <= -0.001
 R545: - C380 - 12 C387 >= -12
 R546: - C381 - 0.001 C388 <= -0.001
 R547: - C381 - 12 C388 >= -12
 R548: - C382 - 0.001 C389 <= -0.001
 R549: - C382 - 12 C389 >= -12
 k_route_r2_r5_k0: dist_r0_r5 + onehop_r2_r0 - k_route_i2_k0_j5 = 0
 k_route_r2_r5_k1: dist_r1_r5 + onehop_r2_r1 - k_route_i2_k1_j5 = 0
 k_route_r2_r5_k2: C392 = 6
 k_route_r2_r5_k3: onehop_r2_r3 + dist_r3_r5 - k_route_i2_k3_j5 = 0
 k_route_r2_r5_k4: onehop_r2_r4 + dist_r4_r5 - k_route_i2_k4_j5 = 0
 k_route_r2_r5_k5: onehop_r2_r5 + dist_r5_r5 - k_route_i2_k5_j5 = 0
 R556: C396 >= 0
 R557: C397 >= 0
 R558: C398 >= 0
 R559: C399 >= 0
 R560: C400 >= 0
 R561: C401 >= 0
 R562: C402 >= 0
 min_kroute_zatmost_r2_r5: C403 + C404 + C405 + C406 + C407 + C408 + C409
   >= 1
 min_kroute_res_r2_r5_r0: - dist_r2_r5 + k_route_i2_k0_j5 - C396 = 0
 min_kroute_res_r2_r5_r1: - dist_r2_r5 + k_route_i2_k1_j5 - C397 = 0
 min_kroute_res_r2_r5_r2: - dist_r2_r5 + C392 - C398 = 0
 min_kroute_res_r2_r5_r3: - dist_r2_r5 + k_route_i2_k3_j5 - C399 = 0
 min_kroute_res_r2_r5_r4: - dist_r2_r5 + k_route_i2_k4_j5 - C400 = 0
 min_kroute_res_r2_r5_r5: - dist_r2_r5 + k_route_i2_k5_j5 - C401 = 0
 min_kroute_res_r2_r5_r6: - dist_r2_r5 - C402 = -12
 R571: - C396 - 0.001 C403 <= -0.001
 R572: - C396 - 12 C403 >= -12
 R573: - C397 - 0.001 C404 <= -0.001
 R574: - C397 - 12 C404 >= -12
 R575: - C398 - 0.001 C405 <= -0.001
 R576: - C398 - 12 C405 >= -12
 R577: - C399 - 0.001 C406 <= -0.001
 R578: - C399 - 12 C406 >= -12
 R579: - C400 - 0.001 C407 <= -0.001
 R580: - C400 - 12 C407 >= -12
 R581: - C401 - 0.001 C408 <= -0.001
 R582: - C401 - 12 C408 >= -12
 R583: - C402 - 0.001 C409 <= -0.001
 R584: - C402 - 12 C409 >= -12
 k_route_r3_r0_k0: dist_r0_r0 + onehop_r3_r0 - k_route_i3_k0_j0 = 0
 k_route_r3_r0_k1: dist_r1_r0 + onehop_r3_r1 - k_route_i3_k1_j0 = 0
 k_route_r3_r0_k2: dist_r2_r0 + onehop_r3_r2 - k_route_i3_k2_j0 = 0
 k_route_r3_r0_k3: C413 = 6
 k_route_r3_r0_k4: onehop_r3_r4 + dist_r4_r0 - k_route_i3_k4_j0 = 0
 k_route_r3_r0_k5: onehop_r3_r5 + dist_r5_r0 - k_route_i3_k5_j0 = 0
 R591: C416 >= 0
 R592: C417 >= 0
 R593: C418 >= 0
 R594: C419 >= 0
 R595: C420 >= 0
 R596: C421 >= 0
 R597: C422 >= 0
 min_kroute_zatmost_r3_r0: C423 + C424 + C425 + C426 + C427 + C428 + C429
   >= 1
 min_kroute_res_r3_r0_r0: - dist_r3_r0 + k_route_i3_k0_j0 - C416 = 0
 min_kroute_res_r3_r0_r1: - dist_r3_r0 + k_route_i3_k1_j0 - C417 = 0
 min_kroute_res_r3_r0_r2: - dist_r3_r0 + k_route_i3_k2_j0 - C418 = 0
 min_kroute_res_r3_r0_r3: - dist_r3_r0 + C413 - C419 = 0
 min_kroute_res_r3_r0_r4: - dist_r3_r0 + k_route_i3_k4_j0 - C420 = 0
 min_kroute_res_r3_r0_r5: - dist_r3_r0 + k_route_i3_k5_j0 - C421 = 0
 min_kroute_res_r3_r0_r6: - dist_r3_r0 - C422 = -12
 R606: - C416 - 0.001 C423 <= -0.001
 R607: - C416 - 12 C423 >= -12
 R608: - C417 - 0.001 C424 <= -0.001
 R609: - C417 - 12 C424 >= -12
 R610: - C418 - 0.001 C425 <= -0.001
 R611: - C418 - 12 C425 >= -12
 R612: - C419 - 0.001 C426 <= -0.001
 R613: - C419 - 12 C426 >= -12
 R614: - C420 - 0.001 C427 <= -0.001
 R615: - C420 - 12 C427 >= -12
 R616: - C421 - 0.001 C428 <= -0.001
 R617: - C421 - 12 C428 >= -12
 R618: - C422 - 0.001 C429 <= -0.001
 R619: - C422 - 12 C429 >= -12
 k_route_r3_r1_k0: dist_r0_r1 + onehop_r3_r0 - k_route_i3_k0_j1 = 0
 k_route_r3_r1_k1: dist_r1_r1 + onehop_r3_r1 - k_route_i3_k1_j1 = 0
 k_route_r3_r1_k2: dist_r2_r1 + onehop_r3_r2 - k_route_i3_k2_j1 = 0
 k_route_r3_r1_k3: C433 = 6
 k_route_r3_r1_k4: onehop_r3_r4 + dist_r4_r1 - k_route_i3_k4_j1 = 0
 k_route_r3_r1_k5: onehop_r3_r5 + dist_r5_r1 - k_route_i3_k5_j1 = 0
 R626: C436 >= 0
 R627: C437 >= 0
 R628: C438 >= 0
 R629: C439 >= 0
 R630: C440 >= 0
 R631: C441 >= 0
 R632: C442 >= 0
 min_kroute_zatmost_r3_r1: C443 + C444 + C445 + C446 + C447 + C448 + C449
   >= 1
 min_kroute_res_r3_r1_r0: - dist_r3_r1 + k_route_i3_k0_j1 - C436 = 0
 min_kroute_res_r3_r1_r1: - dist_r3_r1 + k_route_i3_k1_j1 - C437 = 0
 min_kroute_res_r3_r1_r2: - dist_r3_r1 + k_route_i3_k2_j1 - C438 = 0
 min_kroute_res_r3_r1_r3: - dist_r3_r1 + C433 - C439 = 0
 min_kroute_res_r3_r1_r4: - dist_r3_r1 + k_route_i3_k4_j1 - C440 = 0
 min_kroute_res_r3_r1_r5: - dist_r3_r1 + k_route_i3_k5_j1 - C441 = 0
 min_kroute_res_r3_r1_r6: - dist_r3_r1 - C442 = -12
 R641: - C436 - 0.001 C443 <= -0.001
 R642: - C436 - 12 C443 >= -12
 R643: - C437 - 0.001 C444 <= -0.001
 R644: - C437 - 12 C444 >= -12
 R645: - C438 - 0.001 C445 <= -0.001
 R646: - C438 - 12 C445 >= -12
 R647: - C439 - 0.001 C446 <= -0.001
 R648: - C439 - 12 C446 >= -12
 R649: - C440 - 0.001 C447 <= -0.001
 R650: - C440 - 12 C447 >= -12
 R651: - C441 - 0.001 C448 <= -0.001
 R652: - C441 - 12 C448 >= -12
 R653: - C442 - 0.001 C449 <= -0.001
 R654: - C442 - 12 C449 >= -12
 k_route_r3_r2_k0: dist_r0_r2 + onehop_r3_r0 - k_route_i3_k0_j2 = 0
 k_route_r3_r2_k1: dist_r1_r2 + onehop_r3_r1 - k_route_i3_k1_j2 = 0
 k_route_r3_r2_k2: dist_r2_r2 + onehop_r3_r2 - k_route_i3_k2_j2 = 0
 k_route_r3_r2_k3: C453 = 6
 k_route_r3_r2_k4: onehop_r3_r4 + dist_r4_r2 - k_route_i3_k4_j2 = 0
 k_route_r3_r2_k5: onehop_r3_r5 + dist_r5_r2 - k_route_i3_k5_j2 = 0
 R661: C456 >= 0
 R662: C457 >= 0
 R663: C458 >= 0
 R664: C459 >= 0
 R665: C460 >= 0
 R666: C461 >= 0
 R667: C462 >= 0
 min_kroute_zatmost_r3_r2: C463 + C464 + C465 + C466 + C467 + C468 + C469
   >= 1
 min_kroute_res_r3_r2_r0: - dist_r3_r2 + k_route_i3_k0_j2 - C456 = 0
 min_kroute_res_r3_r2_r1: - dist_r3_r2 + k_route_i3_k1_j2 - C457 = 0
 min_kroute_res_r3_r2_r2: - dist_r3_r2 + k_route_i3_k2_j2 - C458 = 0
 min_kroute_res_r3_r2_r3: - dist_r3_r2 + C453 - C459 = 0
 min_kroute_res_r3_r2_r4: - dist_r3_r2 + k_route_i3_k4_j2 - C460 = 0
 min_kroute_res_r3_r2_r5: - dist_r3_r2 + k_route_i3_k5_j2 - C461 = 0
 min_kroute_res_r3_r2_r6: - dist_r3_r2 - C462 = -12
 R676: - C456 - 0.001 C463 <= -0.001
 R677: - C456 - 12 C463 >= -12
 R678: - C457 - 0.001 C464 <= -0.001
 R679: - C457 - 12 C464 >= -12
 R680: - C458 - 0.001 C465 <= -0.001
 R681: - C458 - 12 C465 >= -12
 R682: - C459 - 0.001 C466 <= -0.001
 R683: - C459 - 12 C466 >= -12
 R684: - C460 - 0.001 C467 <= -0.001
 R685: - C460 - 12 C467 >= -12
 R686: - C461 - 0.001 C468 <= -0.001
 R687: - C461 - 12 C468 >= -12
 R688: - C462 - 0.001 C469 <= -0.001
 R689: - C462 - 12 C469 >= -12
 k_route_r3_r4_k0: dist_r0_r4 + onehop_r3_r0 - k_route_i3_k0_j4 = 0
 k_route_r3_r4_k1: dist_r1_r4 + onehop_r3_r1 - k_route_i3_k1_j4 = 0
 k_route_r3_r4_k2: dist_r2_r4 + onehop_r3_r2 - k_route_i3_k2_j4 = 0
 k_route_r3_r4_k3: C473 = 6
 k_route_r3_r4_k4: onehop_r3_r4 + dist_r4_r4 - k_route_i3_k4_j4 = 0
 k_route_r3_r4_k5: onehop_r3_r5 + dist_r5_r4 - k_route_i3_k5_j4 = 0
 R696: C476 >= 0
 R697: C477 >= 0
 R698: C478 >= 0
 R699: C479 >= 0
 R700: C480 >= 0
 R701: C481 >= 0
 R702: C482 >= 0
 min_kroute_zatmost_r3_r4: C483 + C484 + C485 + C486 + C487 + C488 + C489
   >= 1
 min_kroute_res_r3_r4_r0: - dist_r3_r4 + k_route_i3_k0_j4 - C476 = 0
 min_kroute_res_r3_r4_r1: - dist_r3_r4 + k_route_i3_k1_j4 - C477 = 0
 min_kroute_res_r3_r4_r2: - dist_r3_r4 + k_route_i3_k2_j4 - C478 = 0
 min_kroute_res_r3_r4_r3: - dist_r3_r4 + C473 - C479 = 0
 min_kroute_res_r3_r4_r4: - dist_r3_r4 + k_route_i3_k4_j4 - C480 = 0
 min_kroute_res_r3_r4_r5: - dist_r3_r4 + k_route_i3_k5_j4 - C481 = 0
 min_kroute_res_r3_r4_r6: - dist_r3_r4 - C482 = -12
 R711: - C476 - 0.001 C483 <= -0.001
 R712: - C476 - 12 C483 >= -12
 R713: - C477 - 0.001 C484 <= -0.001
 R714: - C477 - 12 C484 >= -12
 R715: - C478 - 0.001 C485 <= -0.001
 R716: - C478 - 12 C485 >= -12
 R717: - C479 - 0.001 C486 <= -0.001
 R718: - C479 - 12 C486 >= -12
 R719: - C480 - 0.001 C487 <= -0.001
 R720: - C480 - 12 C487 >= -12
 R721: - C481 - 0.001 C488 <= -0.001
 R722: - C481 - 12 C488 >= -12
 R723: - C482 - 0.001 C489 <= -0.001
 R724: - C482 - 12 C489 >= -12
 k_route_r3_r5_k0: dist_r0_r5 + onehop_r3_r0 - k_route_i3_k0_j5 = 0
 k_route_r3_r5_k1: dist_r1_r5 + onehop_r3_r1 - k_route_i3_k1_j5 = 0
 k_route_r3_r5_k2: dist_r2_r5 + onehop_r3_r2 - k_route_i3_k2_j5 = 0
 k_route_r3_r5_k3: C493 = 6
 k_route_r3_r5_k4: onehop_r3_r4 + dist_r4_r5 - k_route_i3_k4_j5 = 0
 k_route_r3_r5_k5: onehop_r3_r5 + dist_r5_r5 - k_route_i3_k5_j5 = 0
 R731: C496 >= 0
 R732: C497 >= 0
 R733: C498 >= 0
 R734: C499 >= 0
 R735: C500 >= 0
 R736: C501 >= 0
 R737: C502 >= 0
 min_kroute_zatmost_r3_r5: C503 + C504 + C505 + C506 + C507 + C508 + C509
   >= 1
 min_kroute_res_r3_r5_r0: - dist_r3_r5 + k_route_i3_k0_j5 - C496 = 0
 min_kroute_res_r3_r5_r1: - dist_r3_r5 + k_route_i3_k1_j5 - C497 = 0
 min_kroute_res_r3_r5_r2: - dist_r3_r5 + k_route_i3_k2_j5 - C498 = 0
 min_kroute_res_r3_r5_r3: - dist_r3_r5 + C493 - C499 = 0
 min_kroute_res_r3_r5_r4: - dist_r3_r5 + k_route_i3_k4_j5 - C500 = 0
 min_kroute_res_r3_r5_r5: - dist_r3_r5 + k_route_i3_k5_j5 - C501 = 0
 min_kroute_res_r3_r5_r6: - dist_r3_r5 - C502 = -12
 R746: - C496 - 0.001 C503 <= -0.001
 R747: - C496 - 12 C503 >= -12
 R748: - C497 - 0.001 C504 <= -0.001
 R749: - C497 - 12 C504 >= -12
 R750: - C498 - 0.001 C505 <= -0.001
 R751: - C498 - 12 C505 >= -12
 R752: - C499 - 0.001 C506 <= -0.001
 R753: - C499 - 12 C506 >= -12
 R754: - C500 - 0.001 C507 <= -0.001
 R755: - C500 - 12 C507 >= -12
 R756: - C501 - 0.001 C508 <= -0.001
 R757: - C501 - 12 C508 >= -12
 R758: - C502 - 0.001 C509 <= -0.001
 R759: - C502 - 12 C509 >= -12
 k_route_r4_r0_k0: dist_r0_r0 + onehop_r4_r0 - k_route_i4_k0_j0 = 0
 k_route_r4_r0_k1: dist_r1_r0 + onehop_r4_r1 - k_route_i4_k1_j0 = 0
 k_route_r4_r0_k2: dist_r2_r0 + onehop_r4_r2 - k_route_i4_k2_j0 = 0
 k_route_r4_r0_k3: dist_r3_r0 + onehop_r4_r3 - k_route_i4_k3_j0 = 0
 k_route_r4_r0_k4: C514 = 6
 k_route_r4_r0_k5: onehop_r4_r5 + dist_r5_r0 - k_route_i4_k5_j0 = 0
 R766: C516 >= 0
 R767: C517 >= 0
 R768: C518 >= 0
 R769: C519 >= 0
 R770: C520 >= 0
 R771: C521 >= 0
 R772: C522 >= 0
 min_kroute_zatmost_r4_r0: C523 + C524 + C525 + C526 + C527 + C528 + C529
   >= 1
 min_kroute_res_r4_r0_r0: - dist_r4_r0 + k_route_i4_k0_j0 - C516 = 0
 min_kroute_res_r4_r0_r1: - dist_r4_r0 + k_route_i4_k1_j0 - C517 = 0
 min_kroute_res_r4_r0_r2: - dist_r4_r0 + k_route_i4_k2_j0 - C518 = 0
 min_kroute_res_r4_r0_r3: - dist_r4_r0 + k_route_i4_k3_j0 - C519 = 0
 min_kroute_res_r4_r0_r4: - dist_r4_r0 + C514 - C520 = 0
 min_kroute_res_r4_r0_r5: - dist_r4_r0 + k_route_i4_k5_j0 - C521 = 0
 min_kroute_res_r4_r0_r6: - dist_r4_r0 - C522 = -12
 R781: - C516 - 0.001 C523 <= -0.001
 R782: - C516 - 12 C523 >= -12
 R783: - C517 - 0.001 C524 <= -0.001
 R784: - C517 - 12 C524 >= -12
 R785: - C518 - 0.001 C525 <= -0.001
 R786: - C518 - 12 C525 >= -12
 R787: - C519 - 0.001 C526 <= -0.001
 R788: - C519 - 12 C526 >= -12
 R789: - C520 - 0.001 C527 <= -0.001
 R790: - C520 - 12 C527 >= -12
 R791: - C521 - 0.001 C528 <= -0.001
 R792: - C521 - 12 C528 >= -12
 R793: - C522 - 0.001 C529 <= -0.001
 R794: - C522 - 12 C529 >= -12
 k_route_r4_r1_k0: dist_r0_r1 + onehop_r4_r0 - k_route_i4_k0_j1 = 0
 k_route_r4_r1_k1: dist_r1_r1 + onehop_r4_r1 - k_route_i4_k1_j1 = 0
 k_route_r4_r1_k2: dist_r2_r1 + onehop_r4_r2 - k_route_i4_k2_j1 = 0
 k_route_r4_r1_k3: dist_r3_r1 + onehop_r4_r3 - k_route_i4_k3_j1 = 0
 k_route_r4_r1_k4: C534 = 6
 k_route_r4_r1_k5: onehop_r4_r5 + dist_r5_r1 - k_route_i4_k5_j1 = 0
 R801: C536 >= 0
 R802: C537 >= 0
 R803: C538 >= 0
 R804: C539 >= 0
 R805: C540 >= 0
 R806: C541 >= 0
 R807: C542 >= 0
 min_kroute_zatmost_r4_r1: C543 + C544 + C545 + C546 + C547 + C548 + C549
   >= 1
 min_kroute_res_r4_r1_r0: - dist_r4_r1 + k_route_i4_k0_j1 - C536 = 0
 min_kroute_res_r4_r1_r1: - dist_r4_r1 + k_route_i4_k1_j1 - C537 = 0
 min_kroute_res_r4_r1_r2: - dist_r4_r1 + k_route_i4_k2_j1 - C538 = 0
 min_kroute_res_r4_r1_r3: - dist_r4_r1 + k_route_i4_k3_j1 - C539 = 0
 min_kroute_res_r4_r1_r4: - dist_r4_r1 + C534 - C540 = 0
 min_kroute_res_r4_r1_r5: - dist_r4_r1 + k_route_i4_k5_j1 - C541 = 0
 min_kroute_res_r4_r1_r6: - dist_r4_r1 - C542 = -12
 R816: - C536 - 0.001 C543 <= -0.001
 R817: - C536 - 12 C543 >= -12
 R818: - C537 - 0.001 C544 <= -0.001
 R819: - C537 - 12 C544 >= -12
 R820: - C538 - 0.001 C545 <= -0.001
 R821: - C538 - 12 C545 >= -12
 R822: - C539 - 0.001 C546 <= -0.001
 R823: - C539 - 12 C546 >= -12
 R824: - C540 - 0.001 C547 <= -0.001
 R825: - C540 - 12 C547 >= -12
 R826: - C541 - 0.001 C548 <= -0.001
 R827: - C541 - 12 C548 >= -12
 R828: - C542 - 0.001 C549 <= -0.001
 R829: - C542 - 12 C549 >= -12
 k_route_r4_r2_k0: dist_r0_r2 + onehop_r4_r0 - k_route_i4_k0_j2 = 0
 k_route_r4_r2_k1: dist_r1_r2 + onehop_r4_r1 - k_route_i4_k1_j2 = 0
 k_route_r4_r2_k2: dist_r2_r2 + onehop_r4_r2 - k_route_i4_k2_j2 = 0
 k_route_r4_r2_k3: dist_r3_r2 + onehop_r4_r3 - k_route_i4_k3_j2 = 0
 k_route_r4_r2_k4: C554 = 6
 k_route_r4_r2_k5: onehop_r4_r5 + dist_r5_r2 - k_route_i4_k5_j2 = 0
 R836: C556 >= 0
 R837: C557 >= 0
 R838: C558 >= 0
 R839: C559 >= 0
 R840: C560 >= 0
 R841: C561 >= 0
 R842: C562 >= 0
 min_kroute_zatmost_r4_r2: C563 + C564 + C565 + C566 + C567 + C568 + C569
   >= 1
 min_kroute_res_r4_r2_r0: - dist_r4_r2 + k_route_i4_k0_j2 - C556 = 0
 min_kroute_res_r4_r2_r1: - dist_r4_r2 + k_route_i4_k1_j2 - C557 = 0
 min_kroute_res_r4_r2_r2: - dist_r4_r2 + k_route_i4_k2_j2 - C558 = 0
 min_kroute_res_r4_r2_r3: - dist_r4_r2 + k_route_i4_k3_j2 - C559 = 0
 min_kroute_res_r4_r2_r4: - dist_r4_r2 + C554 - C560 = 0
 min_kroute_res_r4_r2_r5: - dist_r4_r2 + k_route_i4_k5_j2 - C561 = 0
 min_kroute_res_r4_r2_r6: - dist_r4_r2 - C562 = -12
 R851: - C556 - 0.001 C563 <= -0.001
 R852: - C556 - 12 C563 >= -12
 R853: - C557 - 0.001 C564 <= -0.001
 R854: - C557 - 12 C564 >= -12
 R855: - C558 - 0.001 C565 <= -0.001
 R856: - C558 - 12 C565 >= -12
 R857: - C559 - 0.001 C566 <= -0.001
 R858: - C559 - 12 C566 >= -12
 R859: - C560 - 0.001 C567 <= -0.001
 R860: - C560 - 12 C567 >= -12
 R861: - C561 - 0.001 C568 <= -0.001
 R862: - C561 - 12 C568 >= -12
 R863: - C562 - 0.001 C569 <= -0.001
 R864: - C562 - 12 C569 >= -12
 k_route_r4_r3_k0: dist_r0_r3 + onehop_r4_r0 - k_route_i4_k0_j3 = 0
 k_route_r4_r3_k1: dist_r1_r3 + onehop_r4_r1 - k_route_i4_k1_j3 = 0
 k_route_r4_r3_k2: dist_r2_r3 + onehop_r4_r2 - k_route_i4_k2_j3 = 0
 k_route_r4_r3_k3: dist_r3_r3 + onehop_r4_r3 - k_route_i4_k3_j3 = 0
 k_route_r4_r3_k4: C574 = 6
 k_route_r4_r3_k5: onehop_r4_r5 + dist_r5_r3 - k_route_i4_k5_j3 = 0
 R871: C576 >= 0
 R872: C577 >= 0
 R873: C578 >= 0
 R874: C579 >= 0
 R875: C580 >= 0
 R876: C581 >= 0
 R877: C582 >= 0
 min_kroute_zatmost_r4_r3: C583 + C584 + C585 + C586 + C587 + C588 + C589
   >= 1
 min_kroute_res_r4_r3_r0: - dist_r4_r3 + k_route_i4_k0_j3 - C576 = 0
 min_kroute_res_r4_r3_r1: - dist_r4_r3 + k_route_i4_k1_j3 - C577 = 0
 min_kroute_res_r4_r3_r2: - dist_r4_r3 + k_route_i4_k2_j3 - C578 = 0
 min_kroute_res_r4_r3_r3: - dist_r4_r3 + k_route_i4_k3_j3 - C579 = 0
 min_kroute_res_r4_r3_r4: - dist_r4_r3 + C574 - C580 = 0
 min_kroute_res_r4_r3_r5: - dist_r4_r3 + k_route_i4_k5_j3 - C581 = 0
 min_kroute_res_r4_r3_r6: - dist_r4_r3 - C582 = -12
 R886: - C576 - 0.001 C583 <= -0.001
 R887: - C576 - 12 C583 >= -12
 R888: - C577 - 0.001 C584 <= -0.001
 R889: - C577 - 12 C584 >= -12
 R890: - C578 - 0.001 C585 <= -0.001
 R891: - C578 - 12 C585 >= -12
 R892: - C579 - 0.001 C586 <= -0.001
 R893: - C579 - 12 C586 >= -12
 R894: - C580 - 0.001 C587 <= -0.001
 R895: - C580 - 12 C587 >= -12
 R896: - C581 - 0.001 C588 <= -0.001
 R897: - C581 - 12 C588 >= -12
 R898: - C582 - 0.001 C589 <= -0.001
 R899: - C582 - 12 C589 >= -12
 k_route_r4_r5_k0: dist_r0_r5 + onehop_r4_r0 - k_route_i4_k0_j5 = 0
 k_route_r4_r5_k1: dist_r1_r5 + onehop_r4_r1 - k_route_i4_k1_j5 = 0
 k_route_r4_r5_k2: dist_r2_r5 + onehop_r4_r2 - k_route_i4_k2_j5 = 0
 k_route_r4_r5_k3: dist_r3_r5 + onehop_r4_r3 - k_route_i4_k3_j5 = 0
 k_route_r4_r5_k4: C594 = 6
 k_route_r4_r5_k5: onehop_r4_r5 + dist_r5_r5 - k_route_i4_k5_j5 = 0
 R906: C596 >= 0
 R907: C597 >= 0
 R908: C598 >= 0
 R909: C599 >= 0
 R910: C600 >= 0
 R911: C601 >= 0
 R912: C602 >= 0
 min_kroute_zatmost_r4_r5: C603 + C604 + C605 + C606 + C607 + C608 + C609
   >= 1
 min_kroute_res_r4_r5_r0: - dist_r4_r5 + k_route_i4_k0_j5 - C596 = 0
 min_kroute_res_r4_r5_r1: - dist_r4_r5 + k_route_i4_k1_j5 - C597 = 0
 min_kroute_res_r4_r5_r2: - dist_r4_r5 + k_route_i4_k2_j5 - C598 = 0
 min_kroute_res_r4_r5_r3: - dist_r4_r5 + k_route_i4_k3_j5 - C599 = 0
 min_kroute_res_r4_r5_r4: - dist_r4_r5 + C594 - C600 = 0
 min_kroute_res_r4_r5_r5: - dist_r4_r5 + k_route_i4_k5_j5 - C601 = 0
 min_kroute_res_r4_r5_r6: - dist_r4_r5 - C602 = -12
 R921: - C596 - 0.001 C603 <= -0.001
 R922: - C596 - 12 C603 >= -12
 R923: - C597 - 0.001 C604 <= -0.001
 R924: - C597 - 12 C604 >= -12
 R925: - C598 - 0.001 C605 <= -0.001
 R926: - C598 - 12 C605 >= -12
 R927: - C599 - 0.001 C606 <= -0.001
 R928: - C599 - 12 C606 >= -12
 R929: - C600 - 0.001 C607 <= -0.001
 R930: - C600 - 12 C607 >= -12
 R931: - C601 - 0.001 C608 <= -0.001
 R932: - C601 - 12 C608 >= -12
 R933: - C602 - 0.001 C609 <= -0.001
 R934: - C602 - 12 C609 >= -12
 k_route_r5_r0_k0: dist_r0_r0 + onehop_r5_r0 - k_route_i5_k0_j0 = 0
 k_route_r5_r0_k1: dist_r1_r0 + onehop_r5_r1 - k_route_i5_k1_j0 = 0
 k_route_r5_r0_k2: dist_r2_r0 + onehop_r5_r2 - k_route_i5_k2_j0 = 0
 k_route_r5_r0_k3: dist_r3_r0 + onehop_r5_r3 - k_route_i5_k3_j0 = 0
 k_route_r5_r0_k4: dist_r4_r0 + onehop_r5_r4 - k_route_i5_k4_j0 = 0
 k_route_r5_r0_k5: C615 = 6
 R941: C616 >= 0
 R942: C617 >= 0
 R943: C618 >= 0
 R944: C619 >= 0
 R945: C620 >= 0
 R946: C621 >= 0
 R947: C622 >= 0
 min_kroute_zatmost_r5_r0: C623 + C624 + C625 + C626 + C627 + C628 + C629
   >= 1
 min_kroute_res_r5_r0_r0: - dist_r5_r0 + k_route_i5_k0_j0 - C616 = 0
 min_kroute_res_r5_r0_r1: - dist_r5_r0 + k_route_i5_k1_j0 - C617 = 0
 min_kroute_res_r5_r0_r2: - dist_r5_r0 + k_route_i5_k2_j0 - C618 = 0
 min_kroute_res_r5_r0_r3: - dist_r5_r0 + k_route_i5_k3_j0 - C619 = 0
 min_kroute_res_r5_r0_r4: - dist_r5_r0 + k_route_i5_k4_j0 - C620 = 0
 min_kroute_res_r5_r0_r5: - dist_r5_r0 + C615 - C621 = 0
 min_kroute_res_r5_r0_r6: - dist_r5_r0 - C622 = -12
 R956: - C616 - 0.001 C623 <= -0.001
 R957: - C616 - 12 C623 >= -12
 R958: - C617 - 0.001 C624 <= -0.001
 R959: - C617 - 12 C624 >= -12
 R960: - C618 - 0.001 C625 <= -0.001
 R961: - C618 - 12 C625 >= -12
 R962: - C619 - 0.001 C626 <= -0.001
 R963: - C619 - 12 C626 >= -12
 R964: - C620 - 0.001 C627 <= -0.001
 R965: - C620 - 12 C627 >= -12
 R966: - C621 - 0.001 C628 <= -0.001
 R967: - C621 - 12 C628 >= -12
 R968: - C622 - 0.001 C629 <= -0.001
 R969: - C622 - 12 C629 >= -12
 k_route_r5_r1_k0: dist_r0_r1 + onehop_r5_r0 - k_route_i5_k0_j1 = 0
 k_route_r5_r1_k1: dist_r1_r1 + onehop_r5_r1 - k_route_i5_k1_j1 = 0
 k_route_r5_r1_k2: dist_r2_r1 + onehop_r5_r2 - k_route_i5_k2_j1 = 0
 k_route_r5_r1_k3: dist_r3_r1 + onehop_r5_r3 - k_route_i5_k3_j1 = 0
 k_route_r5_r1_k4: dist_r4_r1 + onehop_r5_r4 - k_route_i5_k4_j1 = 0
 k_route_r5_r1_k5: C635 = 6
 R976: C636 >= 0
 R977: C637 >= 0
 R978: C638 >= 0
 R979: C639 >= 0
 R980: C640 >= 0
 R981: C641 >= 0
 R982: C642 >= 0
 min_kroute_zatmost_r5_r1: C643 + C644 + C645 + C646 + C647 + C648 + C649
   >= 1
 min_kroute_res_r5_r1_r0: - dist_r5_r1 + k_route_i5_k0_j1 - C636 = 0
 min_kroute_res_r5_r1_r1: - dist_r5_r1 + k_route_i5_k1_j1 - C637 = 0
 min_kroute_res_r5_r1_r2: - dist_r5_r1 + k_route_i5_k2_j1 - C638 = 0
 min_kroute_res_r5_r1_r3: - dist_r5_r1 + k_route_i5_k3_j1 - C639 = 0
 min_kroute_res_r5_r1_r4: - dist_r5_r1 + k_route_i5_k4_j1 - C640 = 0
 min_kroute_res_r5_r1_r5: - dist_r5_r1 + C635 - C641 = 0
 min_kroute_res_r5_r1_r6: - dist_r5_r1 - C642 = -12
 R991: - C636 - 0.001 C643 <= -0.001
 R992: - C636 - 12 C643 >= -12
 R993: - C637 - 0.001 C644 <= -0.001
 R994: - C637 - 12 C644 >= -12
 R995: - C638 - 0.001 C645 <= -0.001
 R996: - C638 - 12 C645 >= -12
 R997: - C639 - 0.001 C646 <= -0.001
 R998: - C639 - 12 C646 >= -12
 R999: - C640 - 0.001 C647 <= -0.001
 R1000: - C640 - 12 C647 >= -12
 R1001: - C641 - 0.001 C648 <= -0.001
 R1002: - C641 - 12 C648 >= -12
 R1003: - C642 - 0.001 C649 <= -0.001
 R1004: - C642 - 12 C649 >= -12
 k_route_r5_r2_k0: dist_r0_r2 + onehop_r5_r0 - k_route_i5_k0_j2 = 0
 k_route_r5_r2_k1: dist_r1_r2 + onehop_r5_r1 - k_route_i5_k1_j2 = 0
 k_route_r5_r2_k2: dist_r2_r2 + onehop_r5_r2 - k_route_i5_k2_j2 = 0
 k_route_r5_r2_k3: dist_r3_r2 + onehop_r5_r3 - k_route_i5_k3_j2 = 0
 k_route_r5_r2_k4: dist_r4_r2 + onehop_r5_r4 - k_route_i5_k4_j2 = 0
 k_route_r5_r2_k5: C655 = 6
 R1011: C656 >= 0
 R1012: C657 >= 0
 R1013: C658 >= 0
 R1014: C659 >= 0
 R1015: C660 >= 0
 R1016: C661 >= 0
 R1017: C662 >= 0
 min_kroute_zatmost_r5_r2: C663 + C664 + C665 + C666 + C667 + C668 + C669
   >= 1
 min_kroute_res_r5_r2_r0: - dist_r5_r2 + k_route_i5_k0_j2 - C656 = 0
 min_kroute_res_r5_r2_r1: - dist_r5_r2 + k_route_i5_k1_j2 - C657 = 0
 min_kroute_res_r5_r2_r2: - dist_r5_r2 + k_route_i5_k2_j2 - C658 = 0
 min_kroute_res_r5_r2_r3: - dist_r5_r2 + k_route_i5_k3_j2 - C659 = 0
 min_kroute_res_r5_r2_r4: - dist_r5_r2 + k_route_i5_k4_j2 - C660 = 0
 min_kroute_res_r5_r2_r5: - dist_r5_r2 + C655 - C661 = 0
 min_kroute_res_r5_r2_r6: - dist_r5_r2 - C662 = -12
 R1026: - C656 - 0.001 C663 <= -0.001
 R1027: - C656 - 12 C663 >= -12
 R1028: - C657 - 0.001 C664 <= -0.001
 R1029: - C657 - 12 C664 >= -12
 R1030: - C658 - 0.001 C665 <= -0.001
 R1031: - C658 - 12 C665 >= -12
 R1032: - C659 - 0.001 C666 <= -0.001
 R1033: - C659 - 12 C666 >= -12
 R1034: - C660 - 0.001 C667 <= -0.001
 R1035: - C660 - 12 C667 >= -12
 R1036: - C661 - 0.001 C668 <= -0.001
 R1037: - C661 - 12 C668 >= -12
 R1038: - C662 - 0.001 C669 <= -0.001
 R1039: - C662 - 12 C669 >= -12
 k_route_r5_r3_k0: dist_r0_r3 + onehop_r5_r0 - k_route_i5_k0_j3 = 0
 k_route_r5_r3_k1: dist_r1_r3 + onehop_r5_r1 - k_route_i5_k1_j3 = 0
 k_route_r5_r3_k2: dist_r2_r3 + onehop_r5_r2 - k_route_i5_k2_j3 = 0
 k_route_r5_r3_k3: dist_r3_r3 + onehop_r5_r3 - k_route_i5_k3_j3 = 0
 k_route_r5_r3_k4: dist_r4_r3 + onehop_r5_r4 - k_route_i5_k4_j3 = 0
 k_route_r5_r3_k5: C675 = 6
 R1046: C676 >= 0
 R1047: C677 >= 0
 R1048: C678 >= 0
 R1049: C679 >= 0
 R1050: C680 >= 0
 R1051: C681 >= 0
 R1052: C682 >= 0
 min_kroute_zatmost_r5_r3: C683 + C684 + C685 + C686 + C687 + C688 + C689
   >= 1
 min_kroute_res_r5_r3_r0: - dist_r5_r3 + k_route_i5_k0_j3 - C676 = 0
 min_kroute_res_r5_r3_r1: - dist_r5_r3 + k_route_i5_k1_j3 - C677 = 0
 min_kroute_res_r5_r3_r2: - dist_r5_r3 + k_route_i5_k2_j3 - C678 = 0
 min_kroute_res_r5_r3_r3: - dist_r5_r3 + k_route_i5_k3_j3 - C679 = 0
 min_kroute_res_r5_r3_r4: - dist_r5_r3 + k_route_i5_k4_j3 - C680 = 0
 min_kroute_res_r5_r3_r5: - dist_r5_r3 + C675 - C681 = 0
 min_kroute_res_r5_r3_r6: - dist_r5_r3 - C682 = -12
 R1061: - C676 - 0.001 C683 <= -0.001
 R1062: - C676 - 12 C683 >= -12
 R1063: - C677 - 0.001 C684 <= -0.001
 R1064: - C677 - 12 C684 >= -12
 R1065: - C678 - 0.001 C685 <= -0.001
 R1066: - C678 - 12 C685 >= -12
 R1067: - C679 - 0.001 C686 <= -0.001
 R1068: - C679 - 12 C686 >= -12
 R1069: - C680 - 0.001 C687 <= -0.001
 R1070: - C680 - 12 C687 >= -12
 R1071: - C681 - 0.001 C688 <= -0.001
 R1072: - C681 - 12 C688 >= -12
 R1073: - C682 - 0.001 C689 <= -0.001
 R1074: - C682 - 12 C689 >= -12
 k_route_r5_r4_k0: dist_r0_r4 + onehop_r5_r0 - k_route_i5_k0_j4 = 0
 k_route_r5_r4_k1: dist_r1_r4 + onehop_r5_r1 - k_route_i5_k1_j4 = 0
 k_route_r5_r4_k2: dist_r2_r4 + onehop_r5_r2 - k_route_i5_k2_j4 = 0
 k_route_r5_r4_k3: dist_r3_r4 + onehop_r5_r3 - k_route_i5_k3_j4 = 0
 k_route_r5_r4_k4: dist_r4_r4 + onehop_r5_r4 - k_route_i5_k4_j4 = 0
 k_route_r5_r4_k5: C695 = 6
 R1081: C696 >= 0
 R1082: C697 >= 0
 R1083: C698 >= 0
 R1084: C699 >= 0
 R1085: C700 >= 0
 R1086: C701 >= 0
 R1087: C702 >= 0
 min_kroute_zatmost_r5_r4: C703 + C704 + C705 + C706 + C707 + C708 + C709
   >= 1
 min_kroute_res_r5_r4_r0: - dist_r5_r4 + k_route_i5_k0_j4 - C696 = 0
 min_kroute_res_r5_r4_r1: - dist_r5_r4 + k_route_i5_k1_j4 - C697 = 0
 min_kroute_res_r5_r4_r2: - dist_r5_r4 + k_route_i5_k2_j4 - C698 = 0
 min_kroute_res_r5_r4_r3: - dist_r5_r4 + k_route_i5_k3_j4 - C699 = 0
 min_kroute_res_r5_r4_r4: - dist_r5_r4 + k_route_i5_k4_j4 - C700 = 0
 min_kroute_res_r5_r4_r5: - dist_r5_r4 + C695 - C701 = 0
 min_kroute_res_r5_r4_r6: - dist_r5_r4 - C702 = -12
 R1096: - C696 - 0.001 C703 <= -0.001
 R1097: - C696 - 12 C703 >= -12
 R1098: - C697 - 0.001 C704 <= -0.001
 R1099: - C697 - 12 C704 >= -12
 R1100: - C698 - 0.001 C705 <= -0.001
 R1101: - C698 - 12 C705 >= -12
 R1102: - C699 - 0.001 C706 <= -0.001
 R1103: - C699 - 12 C706 >= -12
 R1104: - C700 - 0.001 C707 <= -0.001
 R1105: - C700 - 12 C707 >= -12
 R1106: - C701 - 0.001 C708 <= -0.001
 R1107: - C701 - 12 C708 >= -12
 R1108: - C702 - 0.001 C709 <= -0.001
 R1109: - C702 - 12 C709 >= -12
 longdist_r0_r5: map_r0_r5 = 0
 longdist_r2_r3: map_r2_r3 = 0
 longdist_r3_r2: map_r3_r2 = 0
 longdist_r5_r0: map_r5_r0 = 0
 bw_var_constr0: sc_bw - 0.2 map_r0_r1 - 0.2 map_r0_r2 - 0.2 map_r0_r3
   - 0.2 map_r0_r4 - 0.2 map_r0_r5 <= 0
 bw_var_constr1: sc_bw - 0.2 map_r1_r0 - 0.2 map_r1_r2 - 0.2 map_r1_r3
   - 0.2 map_r1_r4 - 0.2 map_r1_r5 <= 0
 bw_var_constr2: sc_bw - 0.2 map_r2_r0 - 0.2 map_r2_r1 - 0.2 map_r2_r3
   - 0.2 map_r2_r4 - 0.2 map_r2_r5 <= 0
 bw_var_constr3: sc_bw - 0.2 map_r3_r0 - 0.2 map_r3_r1 - 0.2 map_r3_r2
   - 0.2 map_r3_r4 - 0.2 map_r3_r5 <= 0
 bw_var_constr4: sc_bw - 0.2 map_r4_r0 - 0.2 map_r4_r1 - 0.2 map_r4_r2
   - 0.2 map_r4_r3 - 0.2 map_r4_r5 <= 0
 bw_var_constr5: sc_bw - 0.2 map_r5_r0 - 0.2 map_r5_r1 - 0.2 map_r5_r2
   - 0.2 map_r5_r3 - 0.2 map_r5_r4 <= 0
 bw_var_constr6: sc_bw - 0.125 map_r0_r2 - 0.125 map_r0_r3
   - 0.125 map_r0_r4 - 0.125 map_r0_r5 - 0.125 map_r1_r2 - 0.125 map_r1_r3
   - 0.125 map_r1_r4 - 0.125 map_r1_r5 <= 0
 bw_var_constr7: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r3
   - 0.125 map_r0_r4 - 0.125 map_r0_r5 - 0.125 map_r2_r1 - 0.125 map_r2_r3
   - 0.125 map_r2_r4 - 0.125 map_r2_r5 <= 0
 bw_var_constr8: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r2
   - 0.125 map_r0_r4 - 0.125 map_r0_r5 - 0.125 map_r3_r1 - 0.125 map_r3_r2
   - 0.125 map_r3_r4 - 0.125 map_r3_r5 <= 0
 bw_var_constr9: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r2
   - 0.125 map_r0_r3 - 0.125 map_r0_r5 - 0.125 map_r4_r1 - 0.125 map_r4_r2
   - 0.125 map_r4_r3 - 0.125 map_r4_r5 <= 0
 bw_var_constr10: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r2
   - 0.125 map_r0_r3 - 0.125 map_r0_r4 - 0.125 map_r5_r1 - 0.125 map_r5_r2
   - 0.125 map_r5_r3 - 0.125 map_r5_r4 <= 0
 bw_var_constr11: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r3
   - 0.125 map_r1_r4 - 0.125 map_r1_r5 - 0.125 map_r2_r0 - 0.125 map_r2_r3
   - 0.125 map_r2_r4 - 0.125 map_r2_r5 <= 0
 bw_var_constr12: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r2
   - 0.125 map_r1_r4 - 0.125 map_r1_r5 - 0.125 map_r3_r0 - 0.125 map_r3_r2
   - 0.125 map_r3_r4 - 0.125 map_r3_r5 <= 0
 bw_var_constr13: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r2
   - 0.125 map_r1_r3 - 0.125 map_r1_r5 - 0.125 map_r4_r0 - 0.125 map_r4_r2
   - 0.125 map_r4_r3 - 0.125 map_r4_r5 <= 0
 bw_var_constr14: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r2
   - 0.125 map_r1_r3 - 0.125 map_r1_r4 - 0.125 map_r5_r0 - 0.125 map_r5_r2
   - 0.125 map_r5_r3 - 0.125 map_r5_r4 <= 0
 bw_var_constr15: sc_bw - 0.125 map_r2_r0 - 0.125 map_r2_r1
   - 0.125 map_r2_r4 - 0.125 map_r2_r5 - 0.125 map_r3_r0 - 0.125 map_r3_r1
   - 0.125 map_r3_r4 - 0.125 map_r3_r5 <= 0
 bw_var_constr16: sc_bw - 0.125 map_r2_r0 - 0.125 map_r2_r1
   - 0.125 map_r2_r3 - 0.125 map_r2_r5 - 0.125 map_r4_r0 - 0.125 map_r4_r1
   - 0.125 map_r4_r3 - 0.125 map_r4_r5 <= 0
 bw_var_constr17: sc_bw - 0.125 map_r2_r0 - 0.125 map_r2_r1
   - 0.125 map_r2_r3 - 0.125 map_r2_r4 - 0.125 map_r5_r0 - 0.125 map_r5_r1
   - 0.125 map_r5_r3 - 0.125 map_r5_r4 <= 0
 bw_var_constr18: sc_bw - 0.125 map_r3_r0 - 0.125 map_r3_r1
   - 0.125 map_r3_r2 - 0.125 map_r3_r5 - 0.125 map_r4_r0 - 0.125 map_r4_r1
   - 0.125 map_r4_r2 - 0.125 map_r4_r5 <= 0
 bw_var_constr19: sc_bw - 0.125 map_r3_r0 - 0.125 map_r3_r1
   - 0.125 map_r3_r2 - 0.125 map_r3_r4 - 0.125 map_r5_r0 - 0.125 map_r5_r1
   - 0.125 map_r5_r2 - 0.125 map_r5_r4 <= 0
 bw_var_constr20: sc_bw - 0.125 map_r4_r0 - 0.125 map_r4_r1
   - 0.125 map_r4_r2 - 0.125 map_r4_r3 - 0.125 map_r5_r0 - 0.125 map_r5_r1
   - 0.125 map_r5_r2 - 0.125 map_r5_r3 <= 0
 bw_var_constr21: sc_bw - 0.1111111111111111 map_r0_r3
   - 0.1111111111111111 map_r0_r4 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r1_r3 - 0.1111111111111111 map_r1_r4
   - 0.1111111111111111 map_r1_r5 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r2_r4 - 0.1111111111111111 map_r2_r5 <= 0
 bw_var_constr22: sc_bw - 0.1111111111111111 map_r0_r2
   - 0.1111111111111111 map_r0_r4 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r4
   - 0.1111111111111111 map_r1_r5 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r3_r5 <= 0
 bw_var_constr23: sc_bw - 0.1111111111111111 map_r0_r2
   - 0.1111111111111111 map_r0_r3 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r3
   - 0.1111111111111111 map_r1_r5 - 0.1111111111111111 map_r4_r2
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr24: sc_bw - 0.1111111111111111 map_r0_r2
   - 0.1111111111111111 map_r0_r3 - 0.1111111111111111 map_r0_r4
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r3
   - 0.1111111111111111 map_r1_r4 - 0.1111111111111111 map_r5_r2
   - 0.1111111111111111 map_r5_r3 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr25: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r4 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r4
   - 0.1111111111111111 map_r2_r5 - 0.1111111111111111 map_r3_r1
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r3_r5 <= 0
 bw_var_constr26: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r3 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r2_r5 - 0.1111111111111111 map_r4_r1
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr27: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r3 - 0.1111111111111111 map_r0_r4
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r2_r4 - 0.1111111111111111 map_r5_r1
   - 0.1111111111111111 map_r5_r3 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr28: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r2 - 0.1111111111111111 map_r0_r5
   - 0.1111111111111111 map_r3_r1 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r3_r5 - 0.1111111111111111 map_r4_r1
   - 0.1111111111111111 map_r4_r2 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr29: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r2 - 0.1111111111111111 map_r0_r4
   - 0.1111111111111111 map_r3_r1 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r5_r1
   - 0.1111111111111111 map_r5_r2 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr30: sc_bw - 0.1111111111111111 map_r0_r1
   - 0.1111111111111111 map_r0_r2 - 0.1111111111111111 map_r0_r3
   - 0.1111111111111111 map_r4_r1 - 0.1111111111111111 map_r4_r2
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r5_r1
   - 0.1111111111111111 map_r5_r2 - 0.1111111111111111 map_r5_r3 <= 0
 bw_var_constr31: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r4 - 0.1111111111111111 map_r1_r5
   - 0.1111111111111111 map_r2_r0 - 0.1111111111111111 map_r2_r4
   - 0.1111111111111111 map_r2_r5 - 0.1111111111111111 map_r3_r0
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r3_r5 <= 0
 bw_var_constr32: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r3 - 0.1111111111111111 map_r1_r5
   - 0.1111111111111111 map_r2_r0 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r2_r5 - 0.1111111111111111 map_r4_r0
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr33: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r3 - 0.1111111111111111 map_r1_r4
   - 0.1111111111111111 map_r2_r0 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r2_r4 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r3 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr34: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r5
   - 0.1111111111111111 map_r3_r0 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r3_r5 - 0.1111111111111111 map_r4_r0
   - 0.1111111111111111 map_r4_r2 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr35: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r4
   - 0.1111111111111111 map_r3_r0 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r2 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr36: sc_bw - 0.1111111111111111 map_r1_r0
   - 0.1111111111111111 map_r1_r2 - 0.1111111111111111 map_r1_r3
   - 0.1111111111111111 map_r4_r0 - 0.1111111111111111 map_r4_r2
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r2 - 0.1111111111111111 map_r5_r3 <= 0
 bw_var_constr37: sc_bw - 0.1111111111111111 map_r2_r0
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r5
   - 0.1111111111111111 map_r3_r0 - 0.1111111111111111 map_r3_r1
   - 0.1111111111111111 map_r3_r5 - 0.1111111111111111 map_r4_r0
   - 0.1111111111111111 map_r4_r1 - 0.1111111111111111 map_r4_r5 <= 0
 bw_var_constr38: sc_bw - 0.1111111111111111 map_r2_r0
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r4
   - 0.1111111111111111 map_r3_r0 - 0.1111111111111111 map_r3_r1
   - 0.1111111111111111 map_r3_r4 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r1 - 0.1111111111111111 map_r5_r4 <= 0
 bw_var_constr39: sc_bw - 0.1111111111111111 map_r2_r0
   - 0.1111111111111111 map_r2_r1 - 0.1111111111111111 map_r2_r3
   - 0.1111111111111111 map_r4_r0 - 0.1111111111111111 map_r4_r1
   - 0.1111111111111111 map_r4_r3 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r1 - 0.1111111111111111 map_r5_r3 <= 0
 bw_var_constr40: sc_bw - 0.1111111111111111 map_r3_r0
   - 0.1111111111111111 map_r3_r1 - 0.1111111111111111 map_r3_r2
   - 0.1111111111111111 map_r4_r0 - 0.1111111111111111 map_r4_r1
   - 0.1111111111111111 map_r4_r2 - 0.1111111111111111 map_r5_r0
   - 0.1111111111111111 map_r5_r1 - 0.1111111111111111 map_r5_r2 <= 0
 bw_var_constr41: sc_bw - 0.125 map_r0_r4 - 0.125 map_r0_r5
   - 0.125 map_r1_r4 - 0.125 map_r1_r5 - 0.125 map_r2_r4 - 0.125 map_r2_r5
   - 0.125 map_r3_r4 - 0.125 map_r3_r5 <= 0
 bw_var_constr42: sc_bw - 0.125 map_r0_r3 - 0.125 map_r0_r5
   - 0.125 map_r1_r3 - 0.125 map_r1_r5 - 0.125 map_r2_r3 - 0.125 map_r2_r5
   - 0.125 map_r4_r3 - 0.125 map_r4_r5 <= 0
 bw_var_constr43: sc_bw - 0.125 map_r0_r3 - 0.125 map_r0_r4
   - 0.125 map_r1_r3 - 0.125 map_r1_r4 - 0.125 map_r2_r3 - 0.125 map_r2_r4
   - 0.125 map_r5_r3 - 0.125 map_r5_r4 <= 0
 bw_var_constr44: sc_bw - 0.125 map_r0_r2 - 0.125 map_r0_r5
   - 0.125 map_r1_r2 - 0.125 map_r1_r5 - 0.125 map_r3_r2 - 0.125 map_r3_r5
   - 0.125 map_r4_r2 - 0.125 map_r4_r5 <= 0
 bw_var_constr45: sc_bw - 0.125 map_r0_r2 - 0.125 map_r0_r4
   - 0.125 map_r1_r2 - 0.125 map_r1_r4 - 0.125 map_r3_r2 - 0.125 map_r3_r4
   - 0.125 map_r5_r2 - 0.125 map_r5_r4 <= 0
 bw_var_constr46: sc_bw - 0.125 map_r0_r2 - 0.125 map_r0_r3
   - 0.125 map_r1_r2 - 0.125 map_r1_r3 - 0.125 map_r4_r2 - 0.125 map_r4_r3
   - 0.125 map_r5_r2 - 0.125 map_r5_r3 <= 0
 bw_var_constr47: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r5
   - 0.125 map_r2_r1 - 0.125 map_r2_r5 - 0.125 map_r3_r1 - 0.125 map_r3_r5
   - 0.125 map_r4_r1 - 0.125 map_r4_r5 <= 0
 bw_var_constr48: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r4
   - 0.125 map_r2_r1 - 0.125 map_r2_r4 - 0.125 map_r3_r1 - 0.125 map_r3_r4
   - 0.125 map_r5_r1 - 0.125 map_r5_r4 <= 0
 bw_var_constr49: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r3
   - 0.125 map_r2_r1 - 0.125 map_r2_r3 - 0.125 map_r4_r1 - 0.125 map_r4_r3
   - 0.125 map_r5_r1 - 0.125 map_r5_r3 <= 0
 bw_var_constr50: sc_bw - 0.125 map_r0_r1 - 0.125 map_r0_r2
   - 0.125 map_r3_r1 - 0.125 map_r3_r2 - 0.125 map_r4_r1 - 0.125 map_r4_r2
   - 0.125 map_r5_r1 - 0.125 map_r5_r2 <= 0
 bw_var_constr51: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r5
   - 0.125 map_r2_r0 - 0.125 map_r2_r5 - 0.125 map_r3_r0 - 0.125 map_r3_r5
   - 0.125 map_r4_r0 - 0.125 map_r4_r5 <= 0
 bw_var_constr52: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r4
   - 0.125 map_r2_r0 - 0.125 map_r2_r4 - 0.125 map_r3_r0 - 0.125 map_r3_r4
   - 0.125 map_r5_r0 - 0.125 map_r5_r4 <= 0
 bw_var_constr53: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r3
   - 0.125 map_r2_r0 - 0.125 map_r2_r3 - 0.125 map_r4_r0 - 0.125 map_r4_r3
   - 0.125 map_r5_r0 - 0.125 map_r5_r3 <= 0
 bw_var_constr54: sc_bw - 0.125 map_r1_r0 - 0.125 map_r1_r2
   - 0.125 map_r3_r0 - 0.125 map_r3_r2 - 0.125 map_r4_r0 - 0.125 map_r4_r2
   - 0.125 map_r5_r0 - 0.125 map_r5_r2 <= 0
 bw_var_constr55: sc_bw - 0.125 map_r2_r0 - 0.125 map_r2_r1
   - 0.125 map_r3_r0 - 0.125 map_r3_r1 - 0.125 map_r4_r0 - 0.125 map_r4_r1
   - 0.125 map_r5_r0 - 0.125 map_r5_r1 <= 0
 bw_var_constr56: sc_bw - 0.2 map_r0_r5 - 0.2 map_r1_r5 - 0.2 map_r2_r5
   - 0.2 map_r3_r5 - 0.2 map_r4_r5 <= 0
 bw_var_constr57: sc_bw - 0.2 map_r0_r4 - 0.2 map_r1_r4 - 0.2 map_r2_r4
   - 0.2 map_r3_r4 - 0.2 map_r5_r4 <= 0
 bw_var_constr58: sc_bw - 0.2 map_r0_r3 - 0.2 map_r1_r3 - 0.2 map_r2_r3
   - 0.2 map_r4_r3 - 0.2 map_r5_r3 <= 0
 bw_var_constr59: sc_bw - 0.2 map_r0_r2 - 0.2 map_r1_r2 - 0.2 map_r3_r2
   - 0.2 map_r4_r2 - 0.2 map_r5_r2 <= 0
 bw_var_constr60: sc_bw - 0.2 map_r0_r1 - 0.2 map_r2_r1 - 0.2 map_r3_r1
   - 0.2 map_r4_r1 - 0.2 map_r5_r1 <= 0
 bw_var_constr61: sc_bw - 0.2 map_r1_r0 - 0.2 map_r2_r0 - 0.2 map_r3_r0
   - 0.2 map_r4_r0 - 0.2 map_r5_r0 <= 0
Bounds
 bi_bw <= 24
 sc_bw <= 24
 dist_r0_r0 <= 6
 dist_r0_r1 <= 6
 dist_r0_r2 <= 6
 dist_r0_r3 <= 6
 dist_r0_r4 <= 6
 dist_r0_r5 <= 6
 dist_r1_r0 <= 6
 dist_r1_r1 <= 6
 dist_r1_r2 <= 6
 dist_r1_r3 <= 6
 dist_r1_r4 <= 6
 dist_r1_r5 <= 6
 dist_r2_r0 <= 6
 dist_r2_r1 <= 6
 dist_r2_r2 <= 6
 dist_r2_r3 <= 6
 dist_r2_r4 <= 6
 dist_r2_r5 <= 6
 dist_r3_r0 <= 6
 dist_r3_r1 <= 6
 dist_r3_r2 <= 6
 dist_r3_r3 <= 6
 dist_r3_r4 <= 6
 dist_r3_r5 <= 6
 dist_r4_r0 <= 6
 dist_r4_r1 <= 6
 dist_r4_r2 <= 6
 dist_r4_r3 <= 6
 dist_r4_r4 <= 6
 dist_r4_r5 <= 6
 dist_r5_r0 <= 6
 dist_r5_r1 <= 6
 dist_r5_r2 <= 6
 dist_r5_r3 <= 6
 dist_r5_r4 <= 6
 dist_r5_r5 <= 6
Binaries
 map_r0_r0 map_r0_r1 map_r0_r2 map_r0_r3 map_r0_r4 map_r0_r5 map_r1_r0
 map_r1_r1 map_r1_r2 map_r1_r3 map_r1_r4 map_r1_r5 map_r2_r0 map_r2_r1
 map_r2_r2 map_r2_r3 map_r2_r4 map_r2_r5 map_r3_r0 map_r3_r1 map_r3_r2
 map_r3_r3 map_r3_r4 map_r3_r5 map_r4_r0 map_r4_r1 map_r4_r2 map_r4_r3
 map_r4_r4 map_r4_r5 map_r5_r0 map_r5_r1 map_r5_r2 map_r5_r3 map_r5_r4
 map_r5_r5 C123 C124 C125 C126 C127 C128 C129 C143 C144 C145 C146 C147 C148
 C149 C163 C164 C165 C166 C167 C168 C169 C183 C184 C185 C186 C187 C188 C189
 C203 C204 C205 C206 C207 C208 C209 C223 C224 C225 C226 C227 C228 C229 C243
 C244 C245 C246 C247 C248 C249 C263 C264 C265 C266 C267 C268 C269 C283 C284
 C285 C286 C287 C288 C289 C303 C304 C305 C306 C307 C308 C309 C323 C324 C325
 C326 C327 C328 C329 C343 C344 C345 C346 C347 C348 C349 C363 C364 C365 C366
 C367 C368 C369 C383 C384 C385 C386 C387 C388 C389 C403 C404 C405 C406 C407
 C408 C409 C423 C424 C425 C426 C427 C428 C429 C443 C444 C445 C446 C447 C448
 C449 C463 C464 C465 C466 C467 C468 C469 C483 C484 C485 C486 C487 C488 C489
 C503 C504 C505 C506 C507 C508 C509 C523 C524 C525 C526 C527 C528 C529 C543
 C544 C545 C546 C547 C548 C549 C563 C564 C565 C566 C567 C568 C569 C583 C584
 C585 C586 C587 C588 C589 C603 C604 C605 C606 C607 C608 C609 C623 C624 C625
 C626 C627 C628 C629 C643 C644 C645 C646 C647 C648 C649 C663 C664 C665 C666
 C667 C668 C669 C683 C684 C685 C686 C687 C688 C689 C703 C704 C705 C706 C707
 C708 C709
Generals
 dist_r0_r0 onehop_r0_r0 dist_r0_r1 onehop_r0_r1 dist_r0_r2 onehop_r0_r2
 dist_r0_r3 onehop_r0_r3 dist_r0_r4 onehop_r0_r4 dist_r0_r5 onehop_r0_r5
 dist_r1_r0 onehop_r1_r0 dist_r1_r1 onehop_r1_r1 dist_r1_r2 onehop_r1_r2
 dist_r1_r3 onehop_r1_r3 dist_r1_r4 onehop_r1_r4 dist_r1_r5 onehop_r1_r5
 dist_r2_r0 onehop_r2_r0 dist_r2_r1 onehop_r2_r1 dist_r2_r2 onehop_r2_r2
 dist_r2_r3 onehop_r2_r3 dist_r2_r4 onehop_r2_r4 dist_r2_r5 onehop_r2_r5
 dist_r3_r0 onehop_r3_r0 dist_r3_r1 onehop_r3_r1 dist_r3_r2 onehop_r3_r2
 dist_r3_r3 onehop_r3_r3 dist_r3_r4 onehop_r3_r4 dist_r3_r5 onehop_r3_r5
 dist_r4_r0 onehop_r4_r0 dist_r4_r1 onehop_r4_r1 dist_r4_r2 onehop_r4_r2
 dist_r4_r3 onehop_r4_r3 dist_r4_r4 onehop_r4_r4 dist_r4_r5 onehop_r4_r5
 dist_r5_r0 onehop_r5_r0 dist_r5_r1 onehop_r5_r1 dist_r5_r2 onehop_r5_r2
 dist_r5_r3 onehop_r5_r3 dist_r5_r4 onehop_r5_r4 dist_r5_r5 onehop_r5_r5
End
