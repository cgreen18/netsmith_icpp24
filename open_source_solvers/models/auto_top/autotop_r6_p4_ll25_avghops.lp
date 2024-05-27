\ Model auto_top_gurobi
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 bi_bw + 0 sc_bw + 0.0333333333333333 dist_r0_r1
   + 0.0333333333333333 dist_r0_r2 + 0.0333333333333333 dist_r0_r3
   + 0.0333333333333333 dist_r0_r4 + 0.0333333333333333 dist_r0_r5
   + 0.0333333333333333 dist_r1_r0 + 0.0333333333333333 dist_r1_r2
   + 0.0333333333333333 dist_r1_r3 + 0.0333333333333333 dist_r1_r4
   + 0.0333333333333333 dist_r1_r5 + 0.0333333333333333 dist_r2_r0
   + 0.0333333333333333 dist_r2_r1 + 0.0333333333333333 dist_r2_r3
   + 0.0333333333333333 dist_r2_r4 + 0.0333333333333333 dist_r2_r5
   + 0.0333333333333333 dist_r3_r0 + 0.0333333333333333 dist_r3_r1
   + 0.0333333333333333 dist_r3_r2 + 0.0333333333333333 dist_r3_r4
   + 0.0333333333333333 dist_r3_r5 + 0.0333333333333333 dist_r4_r0
   + 0.0333333333333333 dist_r4_r1 + 0.0333333333333333 dist_r4_r2
   + 0.0333333333333333 dist_r4_r3 + 0.0333333333333333 dist_r4_r5
   + 0.0333333333333333 dist_r5_r0 + 0.0333333333333333 dist_r5_r1
   + 0.0333333333333333 dist_r5_r2 + 0.0333333333333333 dist_r5_r3
   + 0.0333333333333333 dist_r5_r4
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
 k_route_r0_r1_k0: C110 = 6
 k_route_r0_r1_k1: onehop_r0_r1 + dist_r1_r1 - k_route_i0_k1_j1 = 0
 k_route_r0_r1_k2: onehop_r0_r2 + dist_r2_r1 - k_route_i0_k2_j1 = 0
 k_route_r0_r1_k3: onehop_r0_r3 + dist_r3_r1 - k_route_i0_k3_j1 = 0
 k_route_r0_r1_k4: onehop_r0_r4 + dist_r4_r1 - k_route_i0_k4_j1 = 0
 k_route_r0_r1_k5: onehop_r0_r5 + dist_r5_r1 - k_route_i0_k5_j1 = 0
 k_route_r0_r2_k0: C116 = 6
 k_route_r0_r2_k1: onehop_r0_r1 + dist_r1_r2 - k_route_i0_k1_j2 = 0
 k_route_r0_r2_k2: onehop_r0_r2 + dist_r2_r2 - k_route_i0_k2_j2 = 0
 k_route_r0_r2_k3: onehop_r0_r3 + dist_r3_r2 - k_route_i0_k3_j2 = 0
 k_route_r0_r2_k4: onehop_r0_r4 + dist_r4_r2 - k_route_i0_k4_j2 = 0
 k_route_r0_r2_k5: onehop_r0_r5 + dist_r5_r2 - k_route_i0_k5_j2 = 0
 k_route_r0_r3_k0: C122 = 6
 k_route_r0_r3_k1: onehop_r0_r1 + dist_r1_r3 - k_route_i0_k1_j3 = 0
 k_route_r0_r3_k2: onehop_r0_r2 + dist_r2_r3 - k_route_i0_k2_j3 = 0
 k_route_r0_r3_k3: onehop_r0_r3 + dist_r3_r3 - k_route_i0_k3_j3 = 0
 k_route_r0_r3_k4: onehop_r0_r4 + dist_r4_r3 - k_route_i0_k4_j3 = 0
 k_route_r0_r3_k5: onehop_r0_r5 + dist_r5_r3 - k_route_i0_k5_j3 = 0
 k_route_r0_r4_k0: C128 = 6
 k_route_r0_r4_k1: onehop_r0_r1 + dist_r1_r4 - k_route_i0_k1_j4 = 0
 k_route_r0_r4_k2: onehop_r0_r2 + dist_r2_r4 - k_route_i0_k2_j4 = 0
 k_route_r0_r4_k3: onehop_r0_r3 + dist_r3_r4 - k_route_i0_k3_j4 = 0
 k_route_r0_r4_k4: onehop_r0_r4 + dist_r4_r4 - k_route_i0_k4_j4 = 0
 k_route_r0_r4_k5: onehop_r0_r5 + dist_r5_r4 - k_route_i0_k5_j4 = 0
 k_route_r0_r5_k0: C134 = 6
 k_route_r0_r5_k1: onehop_r0_r1 + dist_r1_r5 - k_route_i0_k1_j5 = 0
 k_route_r0_r5_k2: onehop_r0_r2 + dist_r2_r5 - k_route_i0_k2_j5 = 0
 k_route_r0_r5_k3: onehop_r0_r3 + dist_r3_r5 - k_route_i0_k3_j5 = 0
 k_route_r0_r5_k4: onehop_r0_r4 + dist_r4_r5 - k_route_i0_k4_j5 = 0
 k_route_r0_r5_k5: onehop_r0_r5 + dist_r5_r5 - k_route_i0_k5_j5 = 0
 k_route_r1_r0_k0: dist_r0_r0 + onehop_r1_r0 - k_route_i1_k0_j0 = 0
 k_route_r1_r0_k1: C141 = 6
 k_route_r1_r0_k2: onehop_r1_r2 + dist_r2_r0 - k_route_i1_k2_j0 = 0
 k_route_r1_r0_k3: onehop_r1_r3 + dist_r3_r0 - k_route_i1_k3_j0 = 0
 k_route_r1_r0_k4: onehop_r1_r4 + dist_r4_r0 - k_route_i1_k4_j0 = 0
 k_route_r1_r0_k5: onehop_r1_r5 + dist_r5_r0 - k_route_i1_k5_j0 = 0
 k_route_r1_r2_k0: dist_r0_r2 + onehop_r1_r0 - k_route_i1_k0_j2 = 0
 k_route_r1_r2_k1: C147 = 6
 k_route_r1_r2_k2: onehop_r1_r2 + dist_r2_r2 - k_route_i1_k2_j2 = 0
 k_route_r1_r2_k3: onehop_r1_r3 + dist_r3_r2 - k_route_i1_k3_j2 = 0
 k_route_r1_r2_k4: onehop_r1_r4 + dist_r4_r2 - k_route_i1_k4_j2 = 0
 k_route_r1_r2_k5: onehop_r1_r5 + dist_r5_r2 - k_route_i1_k5_j2 = 0
 k_route_r1_r3_k0: dist_r0_r3 + onehop_r1_r0 - k_route_i1_k0_j3 = 0
 k_route_r1_r3_k1: C153 = 6
 k_route_r1_r3_k2: onehop_r1_r2 + dist_r2_r3 - k_route_i1_k2_j3 = 0
 k_route_r1_r3_k3: onehop_r1_r3 + dist_r3_r3 - k_route_i1_k3_j3 = 0
 k_route_r1_r3_k4: onehop_r1_r4 + dist_r4_r3 - k_route_i1_k4_j3 = 0
 k_route_r1_r3_k5: onehop_r1_r5 + dist_r5_r3 - k_route_i1_k5_j3 = 0
 k_route_r1_r4_k0: dist_r0_r4 + onehop_r1_r0 - k_route_i1_k0_j4 = 0
 k_route_r1_r4_k1: C159 = 6
 k_route_r1_r4_k2: onehop_r1_r2 + dist_r2_r4 - k_route_i1_k2_j4 = 0
 k_route_r1_r4_k3: onehop_r1_r3 + dist_r3_r4 - k_route_i1_k3_j4 = 0
 k_route_r1_r4_k4: onehop_r1_r4 + dist_r4_r4 - k_route_i1_k4_j4 = 0
 k_route_r1_r4_k5: onehop_r1_r5 + dist_r5_r4 - k_route_i1_k5_j4 = 0
 k_route_r1_r5_k0: dist_r0_r5 + onehop_r1_r0 - k_route_i1_k0_j5 = 0
 k_route_r1_r5_k1: C165 = 6
 k_route_r1_r5_k2: onehop_r1_r2 + dist_r2_r5 - k_route_i1_k2_j5 = 0
 k_route_r1_r5_k3: onehop_r1_r3 + dist_r3_r5 - k_route_i1_k3_j5 = 0
 k_route_r1_r5_k4: onehop_r1_r4 + dist_r4_r5 - k_route_i1_k4_j5 = 0
 k_route_r1_r5_k5: onehop_r1_r5 + dist_r5_r5 - k_route_i1_k5_j5 = 0
 k_route_r2_r0_k0: dist_r0_r0 + onehop_r2_r0 - k_route_i2_k0_j0 = 0
 k_route_r2_r0_k1: dist_r1_r0 + onehop_r2_r1 - k_route_i2_k1_j0 = 0
 k_route_r2_r0_k2: C172 = 6
 k_route_r2_r0_k3: onehop_r2_r3 + dist_r3_r0 - k_route_i2_k3_j0 = 0
 k_route_r2_r0_k4: onehop_r2_r4 + dist_r4_r0 - k_route_i2_k4_j0 = 0
 k_route_r2_r0_k5: onehop_r2_r5 + dist_r5_r0 - k_route_i2_k5_j0 = 0
 k_route_r2_r1_k0: dist_r0_r1 + onehop_r2_r0 - k_route_i2_k0_j1 = 0
 k_route_r2_r1_k1: dist_r1_r1 + onehop_r2_r1 - k_route_i2_k1_j1 = 0
 k_route_r2_r1_k2: C178 = 6
 k_route_r2_r1_k3: onehop_r2_r3 + dist_r3_r1 - k_route_i2_k3_j1 = 0
 k_route_r2_r1_k4: onehop_r2_r4 + dist_r4_r1 - k_route_i2_k4_j1 = 0
 k_route_r2_r1_k5: onehop_r2_r5 + dist_r5_r1 - k_route_i2_k5_j1 = 0
 k_route_r2_r3_k0: dist_r0_r3 + onehop_r2_r0 - k_route_i2_k0_j3 = 0
 k_route_r2_r3_k1: dist_r1_r3 + onehop_r2_r1 - k_route_i2_k1_j3 = 0
 k_route_r2_r3_k2: C184 = 6
 k_route_r2_r3_k3: onehop_r2_r3 + dist_r3_r3 - k_route_i2_k3_j3 = 0
 k_route_r2_r3_k4: onehop_r2_r4 + dist_r4_r3 - k_route_i2_k4_j3 = 0
 k_route_r2_r3_k5: onehop_r2_r5 + dist_r5_r3 - k_route_i2_k5_j3 = 0
 k_route_r2_r4_k0: dist_r0_r4 + onehop_r2_r0 - k_route_i2_k0_j4 = 0
 k_route_r2_r4_k1: dist_r1_r4 + onehop_r2_r1 - k_route_i2_k1_j4 = 0
 k_route_r2_r4_k2: C190 = 6
 k_route_r2_r4_k3: onehop_r2_r3 + dist_r3_r4 - k_route_i2_k3_j4 = 0
 k_route_r2_r4_k4: onehop_r2_r4 + dist_r4_r4 - k_route_i2_k4_j4 = 0
 k_route_r2_r4_k5: onehop_r2_r5 + dist_r5_r4 - k_route_i2_k5_j4 = 0
 k_route_r2_r5_k0: dist_r0_r5 + onehop_r2_r0 - k_route_i2_k0_j5 = 0
 k_route_r2_r5_k1: dist_r1_r5 + onehop_r2_r1 - k_route_i2_k1_j5 = 0
 k_route_r2_r5_k2: C196 = 6
 k_route_r2_r5_k3: onehop_r2_r3 + dist_r3_r5 - k_route_i2_k3_j5 = 0
 k_route_r2_r5_k4: onehop_r2_r4 + dist_r4_r5 - k_route_i2_k4_j5 = 0
 k_route_r2_r5_k5: onehop_r2_r5 + dist_r5_r5 - k_route_i2_k5_j5 = 0
 k_route_r3_r0_k0: dist_r0_r0 + onehop_r3_r0 - k_route_i3_k0_j0 = 0
 k_route_r3_r0_k1: dist_r1_r0 + onehop_r3_r1 - k_route_i3_k1_j0 = 0
 k_route_r3_r0_k2: dist_r2_r0 + onehop_r3_r2 - k_route_i3_k2_j0 = 0
 k_route_r3_r0_k3: C203 = 6
 k_route_r3_r0_k4: onehop_r3_r4 + dist_r4_r0 - k_route_i3_k4_j0 = 0
 k_route_r3_r0_k5: onehop_r3_r5 + dist_r5_r0 - k_route_i3_k5_j0 = 0
 k_route_r3_r1_k0: dist_r0_r1 + onehop_r3_r0 - k_route_i3_k0_j1 = 0
 k_route_r3_r1_k1: dist_r1_r1 + onehop_r3_r1 - k_route_i3_k1_j1 = 0
 k_route_r3_r1_k2: dist_r2_r1 + onehop_r3_r2 - k_route_i3_k2_j1 = 0
 k_route_r3_r1_k3: C209 = 6
 k_route_r3_r1_k4: onehop_r3_r4 + dist_r4_r1 - k_route_i3_k4_j1 = 0
 k_route_r3_r1_k5: onehop_r3_r5 + dist_r5_r1 - k_route_i3_k5_j1 = 0
 k_route_r3_r2_k0: dist_r0_r2 + onehop_r3_r0 - k_route_i3_k0_j2 = 0
 k_route_r3_r2_k1: dist_r1_r2 + onehop_r3_r1 - k_route_i3_k1_j2 = 0
 k_route_r3_r2_k2: dist_r2_r2 + onehop_r3_r2 - k_route_i3_k2_j2 = 0
 k_route_r3_r2_k3: C215 = 6
 k_route_r3_r2_k4: onehop_r3_r4 + dist_r4_r2 - k_route_i3_k4_j2 = 0
 k_route_r3_r2_k5: onehop_r3_r5 + dist_r5_r2 - k_route_i3_k5_j2 = 0
 k_route_r3_r4_k0: dist_r0_r4 + onehop_r3_r0 - k_route_i3_k0_j4 = 0
 k_route_r3_r4_k1: dist_r1_r4 + onehop_r3_r1 - k_route_i3_k1_j4 = 0
 k_route_r3_r4_k2: dist_r2_r4 + onehop_r3_r2 - k_route_i3_k2_j4 = 0
 k_route_r3_r4_k3: C221 = 6
 k_route_r3_r4_k4: onehop_r3_r4 + dist_r4_r4 - k_route_i3_k4_j4 = 0
 k_route_r3_r4_k5: onehop_r3_r5 + dist_r5_r4 - k_route_i3_k5_j4 = 0
 k_route_r3_r5_k0: dist_r0_r5 + onehop_r3_r0 - k_route_i3_k0_j5 = 0
 k_route_r3_r5_k1: dist_r1_r5 + onehop_r3_r1 - k_route_i3_k1_j5 = 0
 k_route_r3_r5_k2: dist_r2_r5 + onehop_r3_r2 - k_route_i3_k2_j5 = 0
 k_route_r3_r5_k3: C227 = 6
 k_route_r3_r5_k4: onehop_r3_r4 + dist_r4_r5 - k_route_i3_k4_j5 = 0
 k_route_r3_r5_k5: onehop_r3_r5 + dist_r5_r5 - k_route_i3_k5_j5 = 0
 k_route_r4_r0_k0: dist_r0_r0 + onehop_r4_r0 - k_route_i4_k0_j0 = 0
 k_route_r4_r0_k1: dist_r1_r0 + onehop_r4_r1 - k_route_i4_k1_j0 = 0
 k_route_r4_r0_k2: dist_r2_r0 + onehop_r4_r2 - k_route_i4_k2_j0 = 0
 k_route_r4_r0_k3: dist_r3_r0 + onehop_r4_r3 - k_route_i4_k3_j0 = 0
 k_route_r4_r0_k4: C234 = 6
 k_route_r4_r0_k5: onehop_r4_r5 + dist_r5_r0 - k_route_i4_k5_j0 = 0
 k_route_r4_r1_k0: dist_r0_r1 + onehop_r4_r0 - k_route_i4_k0_j1 = 0
 k_route_r4_r1_k1: dist_r1_r1 + onehop_r4_r1 - k_route_i4_k1_j1 = 0
 k_route_r4_r1_k2: dist_r2_r1 + onehop_r4_r2 - k_route_i4_k2_j1 = 0
 k_route_r4_r1_k3: dist_r3_r1 + onehop_r4_r3 - k_route_i4_k3_j1 = 0
 k_route_r4_r1_k4: C240 = 6
 k_route_r4_r1_k5: onehop_r4_r5 + dist_r5_r1 - k_route_i4_k5_j1 = 0
 k_route_r4_r2_k0: dist_r0_r2 + onehop_r4_r0 - k_route_i4_k0_j2 = 0
 k_route_r4_r2_k1: dist_r1_r2 + onehop_r4_r1 - k_route_i4_k1_j2 = 0
 k_route_r4_r2_k2: dist_r2_r2 + onehop_r4_r2 - k_route_i4_k2_j2 = 0
 k_route_r4_r2_k3: dist_r3_r2 + onehop_r4_r3 - k_route_i4_k3_j2 = 0
 k_route_r4_r2_k4: C246 = 6
 k_route_r4_r2_k5: onehop_r4_r5 + dist_r5_r2 - k_route_i4_k5_j2 = 0
 k_route_r4_r3_k0: dist_r0_r3 + onehop_r4_r0 - k_route_i4_k0_j3 = 0
 k_route_r4_r3_k1: dist_r1_r3 + onehop_r4_r1 - k_route_i4_k1_j3 = 0
 k_route_r4_r3_k2: dist_r2_r3 + onehop_r4_r2 - k_route_i4_k2_j3 = 0
 k_route_r4_r3_k3: dist_r3_r3 + onehop_r4_r3 - k_route_i4_k3_j3 = 0
 k_route_r4_r3_k4: C252 = 6
 k_route_r4_r3_k5: onehop_r4_r5 + dist_r5_r3 - k_route_i4_k5_j3 = 0
 k_route_r4_r5_k0: dist_r0_r5 + onehop_r4_r0 - k_route_i4_k0_j5 = 0
 k_route_r4_r5_k1: dist_r1_r5 + onehop_r4_r1 - k_route_i4_k1_j5 = 0
 k_route_r4_r5_k2: dist_r2_r5 + onehop_r4_r2 - k_route_i4_k2_j5 = 0
 k_route_r4_r5_k3: dist_r3_r5 + onehop_r4_r3 - k_route_i4_k3_j5 = 0
 k_route_r4_r5_k4: C258 = 6
 k_route_r4_r5_k5: onehop_r4_r5 + dist_r5_r5 - k_route_i4_k5_j5 = 0
 k_route_r5_r0_k0: dist_r0_r0 + onehop_r5_r0 - k_route_i5_k0_j0 = 0
 k_route_r5_r0_k1: dist_r1_r0 + onehop_r5_r1 - k_route_i5_k1_j0 = 0
 k_route_r5_r0_k2: dist_r2_r0 + onehop_r5_r2 - k_route_i5_k2_j0 = 0
 k_route_r5_r0_k3: dist_r3_r0 + onehop_r5_r3 - k_route_i5_k3_j0 = 0
 k_route_r5_r0_k4: dist_r4_r0 + onehop_r5_r4 - k_route_i5_k4_j0 = 0
 k_route_r5_r0_k5: C265 = 6
 k_route_r5_r1_k0: dist_r0_r1 + onehop_r5_r0 - k_route_i5_k0_j1 = 0
 k_route_r5_r1_k1: dist_r1_r1 + onehop_r5_r1 - k_route_i5_k1_j1 = 0
 k_route_r5_r1_k2: dist_r2_r1 + onehop_r5_r2 - k_route_i5_k2_j1 = 0
 k_route_r5_r1_k3: dist_r3_r1 + onehop_r5_r3 - k_route_i5_k3_j1 = 0
 k_route_r5_r1_k4: dist_r4_r1 + onehop_r5_r4 - k_route_i5_k4_j1 = 0
 k_route_r5_r1_k5: C271 = 6
 k_route_r5_r2_k0: dist_r0_r2 + onehop_r5_r0 - k_route_i5_k0_j2 = 0
 k_route_r5_r2_k1: dist_r1_r2 + onehop_r5_r1 - k_route_i5_k1_j2 = 0
 k_route_r5_r2_k2: dist_r2_r2 + onehop_r5_r2 - k_route_i5_k2_j2 = 0
 k_route_r5_r2_k3: dist_r3_r2 + onehop_r5_r3 - k_route_i5_k3_j2 = 0
 k_route_r5_r2_k4: dist_r4_r2 + onehop_r5_r4 - k_route_i5_k4_j2 = 0
 k_route_r5_r2_k5: C277 = 6
 k_route_r5_r3_k0: dist_r0_r3 + onehop_r5_r0 - k_route_i5_k0_j3 = 0
 k_route_r5_r3_k1: dist_r1_r3 + onehop_r5_r1 - k_route_i5_k1_j3 = 0
 k_route_r5_r3_k2: dist_r2_r3 + onehop_r5_r2 - k_route_i5_k2_j3 = 0
 k_route_r5_r3_k3: dist_r3_r3 + onehop_r5_r3 - k_route_i5_k3_j3 = 0
 k_route_r5_r3_k4: dist_r4_r3 + onehop_r5_r4 - k_route_i5_k4_j3 = 0
 k_route_r5_r3_k5: C283 = 6
 k_route_r5_r4_k0: dist_r0_r4 + onehop_r5_r0 - k_route_i5_k0_j4 = 0
 k_route_r5_r4_k1: dist_r1_r4 + onehop_r5_r1 - k_route_i5_k1_j4 = 0
 k_route_r5_r4_k2: dist_r2_r4 + onehop_r5_r2 - k_route_i5_k2_j4 = 0
 k_route_r5_r4_k3: dist_r3_r4 + onehop_r5_r3 - k_route_i5_k3_j4 = 0
 k_route_r5_r4_k4: dist_r4_r4 + onehop_r5_r4 - k_route_i5_k4_j4 = 0
 k_route_r5_r4_k5: C289 = 6
 map2onehop_pos_r0_r1: map_r0_r1 = 1 -> onehop_r0_r1 = 1
 map2onehop_neg_r0_r1: map_r0_r1 = 0 -> onehop_r0_r1 = 6
 map2hop_pos_r0_r1: map_r0_r1 = 1 -> dist_r0_r1 = 1
 map2hop_neg_r0_r1: map_r0_r1 = 0 -> dist_r0_r1 >= 2
 map2onehop_pos_r0_r2: map_r0_r2 = 1 -> onehop_r0_r2 = 1
 map2onehop_neg_r0_r2: map_r0_r2 = 0 -> onehop_r0_r2 = 6
 map2hop_pos_r0_r2: map_r0_r2 = 1 -> dist_r0_r2 = 1
 map2hop_neg_r0_r2: map_r0_r2 = 0 -> dist_r0_r2 >= 2
 map2onehop_pos_r0_r3: map_r0_r3 = 1 -> onehop_r0_r3 = 1
 map2onehop_neg_r0_r3: map_r0_r3 = 0 -> onehop_r0_r3 = 6
 map2hop_pos_r0_r3: map_r0_r3 = 1 -> dist_r0_r3 = 1
 map2hop_neg_r0_r3: map_r0_r3 = 0 -> dist_r0_r3 >= 2
 map2onehop_pos_r0_r4: map_r0_r4 = 1 -> onehop_r0_r4 = 1
 map2onehop_neg_r0_r4: map_r0_r4 = 0 -> onehop_r0_r4 = 6
 map2hop_pos_r0_r4: map_r0_r4 = 1 -> dist_r0_r4 = 1
 map2hop_neg_r0_r4: map_r0_r4 = 0 -> dist_r0_r4 >= 2
 map2onehop_pos_r0_r5: map_r0_r5 = 1 -> onehop_r0_r5 = 1
 map2onehop_neg_r0_r5: map_r0_r5 = 0 -> onehop_r0_r5 = 6
 map2hop_pos_r0_r5: map_r0_r5 = 1 -> dist_r0_r5 = 1
 map2hop_neg_r0_r5: map_r0_r5 = 0 -> dist_r0_r5 >= 2
 map2onehop_pos_r1_r0: map_r1_r0 = 1 -> onehop_r1_r0 = 1
 map2onehop_neg_r1_r0: map_r1_r0 = 0 -> onehop_r1_r0 = 6
 map2hop_pos_r1_r0: map_r1_r0 = 1 -> dist_r1_r0 = 1
 map2hop_neg_r1_r0: map_r1_r0 = 0 -> dist_r1_r0 >= 2
 map2onehop_pos_r1_r2: map_r1_r2 = 1 -> onehop_r1_r2 = 1
 map2onehop_neg_r1_r2: map_r1_r2 = 0 -> onehop_r1_r2 = 6
 map2hop_pos_r1_r2: map_r1_r2 = 1 -> dist_r1_r2 = 1
 map2hop_neg_r1_r2: map_r1_r2 = 0 -> dist_r1_r2 >= 2
 map2onehop_pos_r1_r3: map_r1_r3 = 1 -> onehop_r1_r3 = 1
 map2onehop_neg_r1_r3: map_r1_r3 = 0 -> onehop_r1_r3 = 6
 map2hop_pos_r1_r3: map_r1_r3 = 1 -> dist_r1_r3 = 1
 map2hop_neg_r1_r3: map_r1_r3 = 0 -> dist_r1_r3 >= 2
 map2onehop_pos_r1_r4: map_r1_r4 = 1 -> onehop_r1_r4 = 1
 map2onehop_neg_r1_r4: map_r1_r4 = 0 -> onehop_r1_r4 = 6
 map2hop_pos_r1_r4: map_r1_r4 = 1 -> dist_r1_r4 = 1
 map2hop_neg_r1_r4: map_r1_r4 = 0 -> dist_r1_r4 >= 2
 map2onehop_pos_r1_r5: map_r1_r5 = 1 -> onehop_r1_r5 = 1
 map2onehop_neg_r1_r5: map_r1_r5 = 0 -> onehop_r1_r5 = 6
 map2hop_pos_r1_r5: map_r1_r5 = 1 -> dist_r1_r5 = 1
 map2hop_neg_r1_r5: map_r1_r5 = 0 -> dist_r1_r5 >= 2
 map2onehop_pos_r2_r0: map_r2_r0 = 1 -> onehop_r2_r0 = 1
 map2onehop_neg_r2_r0: map_r2_r0 = 0 -> onehop_r2_r0 = 6
 map2hop_pos_r2_r0: map_r2_r0 = 1 -> dist_r2_r0 = 1
 map2hop_neg_r2_r0: map_r2_r0 = 0 -> dist_r2_r0 >= 2
 map2onehop_pos_r2_r1: map_r2_r1 = 1 -> onehop_r2_r1 = 1
 map2onehop_neg_r2_r1: map_r2_r1 = 0 -> onehop_r2_r1 = 6
 map2hop_pos_r2_r1: map_r2_r1 = 1 -> dist_r2_r1 = 1
 map2hop_neg_r2_r1: map_r2_r1 = 0 -> dist_r2_r1 >= 2
 map2onehop_pos_r2_r3: map_r2_r3 = 1 -> onehop_r2_r3 = 1
 map2onehop_neg_r2_r3: map_r2_r3 = 0 -> onehop_r2_r3 = 6
 map2hop_pos_r2_r3: map_r2_r3 = 1 -> dist_r2_r3 = 1
 map2hop_neg_r2_r3: map_r2_r3 = 0 -> dist_r2_r3 >= 2
 map2onehop_pos_r2_r4: map_r2_r4 = 1 -> onehop_r2_r4 = 1
 map2onehop_neg_r2_r4: map_r2_r4 = 0 -> onehop_r2_r4 = 6
 map2hop_pos_r2_r4: map_r2_r4 = 1 -> dist_r2_r4 = 1
 map2hop_neg_r2_r4: map_r2_r4 = 0 -> dist_r2_r4 >= 2
 map2onehop_pos_r2_r5: map_r2_r5 = 1 -> onehop_r2_r5 = 1
 map2onehop_neg_r2_r5: map_r2_r5 = 0 -> onehop_r2_r5 = 6
 map2hop_pos_r2_r5: map_r2_r5 = 1 -> dist_r2_r5 = 1
 map2hop_neg_r2_r5: map_r2_r5 = 0 -> dist_r2_r5 >= 2
 map2onehop_pos_r3_r0: map_r3_r0 = 1 -> onehop_r3_r0 = 1
 map2onehop_neg_r3_r0: map_r3_r0 = 0 -> onehop_r3_r0 = 6
 map2hop_pos_r3_r0: map_r3_r0 = 1 -> dist_r3_r0 = 1
 map2hop_neg_r3_r0: map_r3_r0 = 0 -> dist_r3_r0 >= 2
 map2onehop_pos_r3_r1: map_r3_r1 = 1 -> onehop_r3_r1 = 1
 map2onehop_neg_r3_r1: map_r3_r1 = 0 -> onehop_r3_r1 = 6
 map2hop_pos_r3_r1: map_r3_r1 = 1 -> dist_r3_r1 = 1
 map2hop_neg_r3_r1: map_r3_r1 = 0 -> dist_r3_r1 >= 2
 map2onehop_pos_r3_r2: map_r3_r2 = 1 -> onehop_r3_r2 = 1
 map2onehop_neg_r3_r2: map_r3_r2 = 0 -> onehop_r3_r2 = 6
 map2hop_pos_r3_r2: map_r3_r2 = 1 -> dist_r3_r2 = 1
 map2hop_neg_r3_r2: map_r3_r2 = 0 -> dist_r3_r2 >= 2
 map2onehop_pos_r3_r4: map_r3_r4 = 1 -> onehop_r3_r4 = 1
 map2onehop_neg_r3_r4: map_r3_r4 = 0 -> onehop_r3_r4 = 6
 map2hop_pos_r3_r4: map_r3_r4 = 1 -> dist_r3_r4 = 1
 map2hop_neg_r3_r4: map_r3_r4 = 0 -> dist_r3_r4 >= 2
 map2onehop_pos_r3_r5: map_r3_r5 = 1 -> onehop_r3_r5 = 1
 map2onehop_neg_r3_r5: map_r3_r5 = 0 -> onehop_r3_r5 = 6
 map2hop_pos_r3_r5: map_r3_r5 = 1 -> dist_r3_r5 = 1
 map2hop_neg_r3_r5: map_r3_r5 = 0 -> dist_r3_r5 >= 2
 map2onehop_pos_r4_r0: map_r4_r0 = 1 -> onehop_r4_r0 = 1
 map2onehop_neg_r4_r0: map_r4_r0 = 0 -> onehop_r4_r0 = 6
 map2hop_pos_r4_r0: map_r4_r0 = 1 -> dist_r4_r0 = 1
 map2hop_neg_r4_r0: map_r4_r0 = 0 -> dist_r4_r0 >= 2
 map2onehop_pos_r4_r1: map_r4_r1 = 1 -> onehop_r4_r1 = 1
 map2onehop_neg_r4_r1: map_r4_r1 = 0 -> onehop_r4_r1 = 6
 map2hop_pos_r4_r1: map_r4_r1 = 1 -> dist_r4_r1 = 1
 map2hop_neg_r4_r1: map_r4_r1 = 0 -> dist_r4_r1 >= 2
 map2onehop_pos_r4_r2: map_r4_r2 = 1 -> onehop_r4_r2 = 1
 map2onehop_neg_r4_r2: map_r4_r2 = 0 -> onehop_r4_r2 = 6
 map2hop_pos_r4_r2: map_r4_r2 = 1 -> dist_r4_r2 = 1
 map2hop_neg_r4_r2: map_r4_r2 = 0 -> dist_r4_r2 >= 2
 map2onehop_pos_r4_r3: map_r4_r3 = 1 -> onehop_r4_r3 = 1
 map2onehop_neg_r4_r3: map_r4_r3 = 0 -> onehop_r4_r3 = 6
 map2hop_pos_r4_r3: map_r4_r3 = 1 -> dist_r4_r3 = 1
 map2hop_neg_r4_r3: map_r4_r3 = 0 -> dist_r4_r3 >= 2
 map2onehop_pos_r4_r5: map_r4_r5 = 1 -> onehop_r4_r5 = 1
 map2onehop_neg_r4_r5: map_r4_r5 = 0 -> onehop_r4_r5 = 6
 map2hop_pos_r4_r5: map_r4_r5 = 1 -> dist_r4_r5 = 1
 map2hop_neg_r4_r5: map_r4_r5 = 0 -> dist_r4_r5 >= 2
 map2onehop_pos_r5_r0: map_r5_r0 = 1 -> onehop_r5_r0 = 1
 map2onehop_neg_r5_r0: map_r5_r0 = 0 -> onehop_r5_r0 = 6
 map2hop_pos_r5_r0: map_r5_r0 = 1 -> dist_r5_r0 = 1
 map2hop_neg_r5_r0: map_r5_r0 = 0 -> dist_r5_r0 >= 2
 map2onehop_pos_r5_r1: map_r5_r1 = 1 -> onehop_r5_r1 = 1
 map2onehop_neg_r5_r1: map_r5_r1 = 0 -> onehop_r5_r1 = 6
 map2hop_pos_r5_r1: map_r5_r1 = 1 -> dist_r5_r1 = 1
 map2hop_neg_r5_r1: map_r5_r1 = 0 -> dist_r5_r1 >= 2
 map2onehop_pos_r5_r2: map_r5_r2 = 1 -> onehop_r5_r2 = 1
 map2onehop_neg_r5_r2: map_r5_r2 = 0 -> onehop_r5_r2 = 6
 map2hop_pos_r5_r2: map_r5_r2 = 1 -> dist_r5_r2 = 1
 map2hop_neg_r5_r2: map_r5_r2 = 0 -> dist_r5_r2 >= 2
 map2onehop_pos_r5_r3: map_r5_r3 = 1 -> onehop_r5_r3 = 1
 map2onehop_neg_r5_r3: map_r5_r3 = 0 -> onehop_r5_r3 = 6
 map2hop_pos_r5_r3: map_r5_r3 = 1 -> dist_r5_r3 = 1
 map2hop_neg_r5_r3: map_r5_r3 = 0 -> dist_r5_r3 >= 2
 map2onehop_pos_r5_r4: map_r5_r4 = 1 -> onehop_r5_r4 = 1
 map2onehop_neg_r5_r4: map_r5_r4 = 0 -> onehop_r5_r4 = 6
 map2hop_pos_r5_r4: map_r5_r4 = 1 -> dist_r5_r4 = 1
 map2hop_neg_r5_r4: map_r5_r4 = 0 -> dist_r5_r4 >= 2
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
 map_r5_r5
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
General Constraints
 min_constr_r0_r1: dist_r0_r1 = MIN ( C110 , k_route_i0_k1_j1 ,
   k_route_i0_k2_j1 , k_route_i0_k3_j1 , k_route_i0_k4_j1 ,
   k_route_i0_k5_j1 )
 min_constr_r0_r2: dist_r0_r2 = MIN ( C116 , k_route_i0_k1_j2 ,
   k_route_i0_k2_j2 , k_route_i0_k3_j2 , k_route_i0_k4_j2 ,
   k_route_i0_k5_j2 )
 min_constr_r0_r3: dist_r0_r3 = MIN ( C122 , k_route_i0_k1_j3 ,
   k_route_i0_k2_j3 , k_route_i0_k3_j3 , k_route_i0_k4_j3 ,
   k_route_i0_k5_j3 )
 min_constr_r0_r4: dist_r0_r4 = MIN ( C128 , k_route_i0_k1_j4 ,
   k_route_i0_k2_j4 , k_route_i0_k3_j4 , k_route_i0_k4_j4 ,
   k_route_i0_k5_j4 )
 min_constr_r0_r5: dist_r0_r5 = MIN ( C134 , k_route_i0_k1_j5 ,
   k_route_i0_k2_j5 , k_route_i0_k3_j5 , k_route_i0_k4_j5 ,
   k_route_i0_k5_j5 )
 min_constr_r1_r0: dist_r1_r0 = MIN ( k_route_i1_k0_j0 , C141 ,
   k_route_i1_k2_j0 , k_route_i1_k3_j0 , k_route_i1_k4_j0 ,
   k_route_i1_k5_j0 )
 min_constr_r1_r2: dist_r1_r2 = MIN ( k_route_i1_k0_j2 , C147 ,
   k_route_i1_k2_j2 , k_route_i1_k3_j2 , k_route_i1_k4_j2 ,
   k_route_i1_k5_j2 )
 min_constr_r1_r3: dist_r1_r3 = MIN ( k_route_i1_k0_j3 , C153 ,
   k_route_i1_k2_j3 , k_route_i1_k3_j3 , k_route_i1_k4_j3 ,
   k_route_i1_k5_j3 )
 min_constr_r1_r4: dist_r1_r4 = MIN ( k_route_i1_k0_j4 , C159 ,
   k_route_i1_k2_j4 , k_route_i1_k3_j4 , k_route_i1_k4_j4 ,
   k_route_i1_k5_j4 )
 min_constr_r1_r5: dist_r1_r5 = MIN ( k_route_i1_k0_j5 , C165 ,
   k_route_i1_k2_j5 , k_route_i1_k3_j5 , k_route_i1_k4_j5 ,
   k_route_i1_k5_j5 )
 min_constr_r2_r0: dist_r2_r0 = MIN ( k_route_i2_k0_j0 , k_route_i2_k1_j0 ,
   C172 , k_route_i2_k3_j0 , k_route_i2_k4_j0 , k_route_i2_k5_j0 )
 min_constr_r2_r1: dist_r2_r1 = MIN ( k_route_i2_k0_j1 , k_route_i2_k1_j1 ,
   C178 , k_route_i2_k3_j1 , k_route_i2_k4_j1 , k_route_i2_k5_j1 )
 min_constr_r2_r3: dist_r2_r3 = MIN ( k_route_i2_k0_j3 , k_route_i2_k1_j3 ,
   C184 , k_route_i2_k3_j3 , k_route_i2_k4_j3 , k_route_i2_k5_j3 )
 min_constr_r2_r4: dist_r2_r4 = MIN ( k_route_i2_k0_j4 , k_route_i2_k1_j4 ,
   C190 , k_route_i2_k3_j4 , k_route_i2_k4_j4 , k_route_i2_k5_j4 )
 min_constr_r2_r5: dist_r2_r5 = MIN ( k_route_i2_k0_j5 , k_route_i2_k1_j5 ,
   C196 , k_route_i2_k3_j5 , k_route_i2_k4_j5 , k_route_i2_k5_j5 )
 min_constr_r3_r0: dist_r3_r0 = MIN ( k_route_i3_k0_j0 , k_route_i3_k1_j0 ,
   k_route_i3_k2_j0 , C203 , k_route_i3_k4_j0 , k_route_i3_k5_j0 )
 min_constr_r3_r1: dist_r3_r1 = MIN ( k_route_i3_k0_j1 , k_route_i3_k1_j1 ,
   k_route_i3_k2_j1 , C209 , k_route_i3_k4_j1 , k_route_i3_k5_j1 )
 min_constr_r3_r2: dist_r3_r2 = MIN ( k_route_i3_k0_j2 , k_route_i3_k1_j2 ,
   k_route_i3_k2_j2 , C215 , k_route_i3_k4_j2 , k_route_i3_k5_j2 )
 min_constr_r3_r4: dist_r3_r4 = MIN ( k_route_i3_k0_j4 , k_route_i3_k1_j4 ,
   k_route_i3_k2_j4 , C221 , k_route_i3_k4_j4 , k_route_i3_k5_j4 )
 min_constr_r3_r5: dist_r3_r5 = MIN ( k_route_i3_k0_j5 , k_route_i3_k1_j5 ,
   k_route_i3_k2_j5 , C227 , k_route_i3_k4_j5 , k_route_i3_k5_j5 )
 min_constr_r4_r0: dist_r4_r0 = MIN ( k_route_i4_k0_j0 , k_route_i4_k1_j0 ,
   k_route_i4_k2_j0 , k_route_i4_k3_j0 , C234 , k_route_i4_k5_j0 )
 min_constr_r4_r1: dist_r4_r1 = MIN ( k_route_i4_k0_j1 , k_route_i4_k1_j1 ,
   k_route_i4_k2_j1 , k_route_i4_k3_j1 , C240 , k_route_i4_k5_j1 )
 min_constr_r4_r2: dist_r4_r2 = MIN ( k_route_i4_k0_j2 , k_route_i4_k1_j2 ,
   k_route_i4_k2_j2 , k_route_i4_k3_j2 , C246 , k_route_i4_k5_j2 )
 min_constr_r4_r3: dist_r4_r3 = MIN ( k_route_i4_k0_j3 , k_route_i4_k1_j3 ,
   k_route_i4_k2_j3 , k_route_i4_k3_j3 , C252 , k_route_i4_k5_j3 )
 min_constr_r4_r5: dist_r4_r5 = MIN ( k_route_i4_k0_j5 , k_route_i4_k1_j5 ,
   k_route_i4_k2_j5 , k_route_i4_k3_j5 , C258 , k_route_i4_k5_j5 )
 min_constr_r5_r0: dist_r5_r0 = MIN ( k_route_i5_k0_j0 , k_route_i5_k1_j0 ,
   k_route_i5_k2_j0 , k_route_i5_k3_j0 , k_route_i5_k4_j0 , C265 )
 min_constr_r5_r1: dist_r5_r1 = MIN ( k_route_i5_k0_j1 , k_route_i5_k1_j1 ,
   k_route_i5_k2_j1 , k_route_i5_k3_j1 , k_route_i5_k4_j1 , C271 )
 min_constr_r5_r2: dist_r5_r2 = MIN ( k_route_i5_k0_j2 , k_route_i5_k1_j2 ,
   k_route_i5_k2_j2 , k_route_i5_k3_j2 , k_route_i5_k4_j2 , C277 )
 min_constr_r5_r3: dist_r5_r3 = MIN ( k_route_i5_k0_j3 , k_route_i5_k1_j3 ,
   k_route_i5_k2_j3 , k_route_i5_k3_j3 , k_route_i5_k4_j3 , C283 )
 min_constr_r5_r4: dist_r5_r4 = MIN ( k_route_i5_k0_j4 , k_route_i5_k1_j4 ,
   k_route_i5_k2_j4 , k_route_i5_k3_j4 , k_route_i5_k4_j4 , C289 )
End
