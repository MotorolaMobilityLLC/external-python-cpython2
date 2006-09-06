#include "pgenheaders.h"
#include "grammar.h"
static arc arcs_0_0[3] = {
	{2, 1},
	{3, 1},
	{4, 2},
};
static arc arcs_0_1[1] = {
	{0, 1},
};
static arc arcs_0_2[1] = {
	{2, 1},
};
static state states_0[3] = {
	{3, arcs_0_0},
	{1, arcs_0_1},
	{1, arcs_0_2},
};
static arc arcs_1_0[3] = {
	{2, 0},
	{6, 0},
	{7, 1},
};
static arc arcs_1_1[1] = {
	{0, 1},
};
static state states_1[2] = {
	{3, arcs_1_0},
	{1, arcs_1_1},
};
static arc arcs_2_0[1] = {
	{9, 1},
};
static arc arcs_2_1[2] = {
	{2, 1},
	{7, 2},
};
static arc arcs_2_2[1] = {
	{0, 2},
};
static state states_2[3] = {
	{1, arcs_2_0},
	{2, arcs_2_1},
	{1, arcs_2_2},
};
static arc arcs_3_0[1] = {
	{11, 1},
};
static arc arcs_3_1[1] = {
	{12, 2},
};
static arc arcs_3_2[2] = {
	{13, 3},
	{2, 4},
};
static arc arcs_3_3[2] = {
	{14, 5},
	{15, 6},
};
static arc arcs_3_4[1] = {
	{0, 4},
};
static arc arcs_3_5[1] = {
	{15, 6},
};
static arc arcs_3_6[1] = {
	{2, 4},
};
static state states_3[7] = {
	{1, arcs_3_0},
	{1, arcs_3_1},
	{2, arcs_3_2},
	{2, arcs_3_3},
	{1, arcs_3_4},
	{1, arcs_3_5},
	{1, arcs_3_6},
};
static arc arcs_4_0[1] = {
	{10, 1},
};
static arc arcs_4_1[2] = {
	{10, 1},
	{0, 1},
};
static state states_4[2] = {
	{1, arcs_4_0},
	{2, arcs_4_1},
};
static arc arcs_5_0[2] = {
	{16, 1},
	{18, 2},
};
static arc arcs_5_1[1] = {
	{18, 2},
};
static arc arcs_5_2[1] = {
	{19, 3},
};
static arc arcs_5_3[1] = {
	{20, 4},
};
static arc arcs_5_4[1] = {
	{21, 5},
};
static arc arcs_5_5[1] = {
	{22, 6},
};
static arc arcs_5_6[1] = {
	{0, 6},
};
static state states_5[7] = {
	{2, arcs_5_0},
	{1, arcs_5_1},
	{1, arcs_5_2},
	{1, arcs_5_3},
	{1, arcs_5_4},
	{1, arcs_5_5},
	{1, arcs_5_6},
};
static arc arcs_6_0[1] = {
	{13, 1},
};
static arc arcs_6_1[2] = {
	{23, 2},
	{15, 3},
};
static arc arcs_6_2[1] = {
	{15, 3},
};
static arc arcs_6_3[1] = {
	{0, 3},
};
static state states_6[4] = {
	{1, arcs_6_0},
	{2, arcs_6_1},
	{1, arcs_6_2},
	{1, arcs_6_3},
};
static arc arcs_7_0[3] = {
	{24, 1},
	{28, 2},
	{29, 3},
};
static arc arcs_7_1[3] = {
	{25, 4},
	{27, 5},
	{0, 1},
};
static arc arcs_7_2[1] = {
	{19, 6},
};
static arc arcs_7_3[1] = {
	{19, 7},
};
static arc arcs_7_4[1] = {
	{26, 8},
};
static arc arcs_7_5[4] = {
	{24, 1},
	{28, 2},
	{29, 3},
	{0, 5},
};
static arc arcs_7_6[2] = {
	{27, 9},
	{0, 6},
};
static arc arcs_7_7[1] = {
	{0, 7},
};
static arc arcs_7_8[2] = {
	{27, 5},
	{0, 8},
};
static arc arcs_7_9[1] = {
	{29, 3},
};
static state states_7[10] = {
	{3, arcs_7_0},
	{3, arcs_7_1},
	{1, arcs_7_2},
	{1, arcs_7_3},
	{1, arcs_7_4},
	{4, arcs_7_5},
	{2, arcs_7_6},
	{1, arcs_7_7},
	{2, arcs_7_8},
	{1, arcs_7_9},
};
static arc arcs_8_0[2] = {
	{19, 1},
	{13, 2},
};
static arc arcs_8_1[1] = {
	{0, 1},
};
static arc arcs_8_2[1] = {
	{30, 3},
};
static arc arcs_8_3[1] = {
	{15, 1},
};
static state states_8[4] = {
	{2, arcs_8_0},
	{1, arcs_8_1},
	{1, arcs_8_2},
	{1, arcs_8_3},
};
static arc arcs_9_0[1] = {
	{24, 1},
};
static arc arcs_9_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_9_2[2] = {
	{24, 1},
	{0, 2},
};
static state states_9[3] = {
	{1, arcs_9_0},
	{2, arcs_9_1},
	{2, arcs_9_2},
};
static arc arcs_10_0[2] = {
	{3, 1},
	{4, 1},
};
static arc arcs_10_1[1] = {
	{0, 1},
};
static state states_10[2] = {
	{2, arcs_10_0},
	{1, arcs_10_1},
};
static arc arcs_11_0[1] = {
	{31, 1},
};
static arc arcs_11_1[2] = {
	{32, 2},
	{2, 3},
};
static arc arcs_11_2[2] = {
	{31, 1},
	{2, 3},
};
static arc arcs_11_3[1] = {
	{0, 3},
};
static state states_11[4] = {
	{1, arcs_11_0},
	{2, arcs_11_1},
	{2, arcs_11_2},
	{1, arcs_11_3},
};
static arc arcs_12_0[8] = {
	{33, 1},
	{34, 1},
	{35, 1},
	{36, 1},
	{37, 1},
	{38, 1},
	{39, 1},
	{40, 1},
};
static arc arcs_12_1[1] = {
	{0, 1},
};
static state states_12[2] = {
	{8, arcs_12_0},
	{1, arcs_12_1},
};
static arc arcs_13_0[1] = {
	{9, 1},
};
static arc arcs_13_1[3] = {
	{41, 2},
	{25, 3},
	{0, 1},
};
static arc arcs_13_2[2] = {
	{42, 4},
	{9, 4},
};
static arc arcs_13_3[2] = {
	{42, 5},
	{9, 5},
};
static arc arcs_13_4[1] = {
	{0, 4},
};
static arc arcs_13_5[2] = {
	{25, 3},
	{0, 5},
};
static state states_13[6] = {
	{1, arcs_13_0},
	{3, arcs_13_1},
	{2, arcs_13_2},
	{2, arcs_13_3},
	{1, arcs_13_4},
	{2, arcs_13_5},
};
static arc arcs_14_0[12] = {
	{43, 1},
	{44, 1},
	{45, 1},
	{46, 1},
	{47, 1},
	{48, 1},
	{49, 1},
	{50, 1},
	{51, 1},
	{52, 1},
	{53, 1},
	{54, 1},
};
static arc arcs_14_1[1] = {
	{0, 1},
};
static state states_14[2] = {
	{12, arcs_14_0},
	{1, arcs_14_1},
};
static arc arcs_15_0[1] = {
	{55, 1},
};
static arc arcs_15_1[3] = {
	{26, 2},
	{56, 3},
	{0, 1},
};
static arc arcs_15_2[2] = {
	{27, 4},
	{0, 2},
};
static arc arcs_15_3[1] = {
	{26, 5},
};
static arc arcs_15_4[2] = {
	{26, 2},
	{0, 4},
};
static arc arcs_15_5[2] = {
	{27, 6},
	{0, 5},
};
static arc arcs_15_6[1] = {
	{26, 7},
};
static arc arcs_15_7[2] = {
	{27, 8},
	{0, 7},
};
static arc arcs_15_8[2] = {
	{26, 7},
	{0, 8},
};
static state states_15[9] = {
	{1, arcs_15_0},
	{3, arcs_15_1},
	{2, arcs_15_2},
	{1, arcs_15_3},
	{2, arcs_15_4},
	{2, arcs_15_5},
	{1, arcs_15_6},
	{2, arcs_15_7},
	{2, arcs_15_8},
};
static arc arcs_16_0[1] = {
	{57, 1},
};
static arc arcs_16_1[1] = {
	{58, 2},
};
static arc arcs_16_2[1] = {
	{0, 2},
};
static state states_16[3] = {
	{1, arcs_16_0},
	{1, arcs_16_1},
	{1, arcs_16_2},
};
static arc arcs_17_0[1] = {
	{59, 1},
};
static arc arcs_17_1[1] = {
	{0, 1},
};
static state states_17[2] = {
	{1, arcs_17_0},
	{1, arcs_17_1},
};
static arc arcs_18_0[5] = {
	{60, 1},
	{61, 1},
	{62, 1},
	{63, 1},
	{64, 1},
};
static arc arcs_18_1[1] = {
	{0, 1},
};
static state states_18[2] = {
	{5, arcs_18_0},
	{1, arcs_18_1},
};
static arc arcs_19_0[1] = {
	{65, 1},
};
static arc arcs_19_1[1] = {
	{0, 1},
};
static state states_19[2] = {
	{1, arcs_19_0},
	{1, arcs_19_1},
};
static arc arcs_20_0[1] = {
	{66, 1},
};
static arc arcs_20_1[1] = {
	{0, 1},
};
static state states_20[2] = {
	{1, arcs_20_0},
	{1, arcs_20_1},
};
static arc arcs_21_0[1] = {
	{67, 1},
};
static arc arcs_21_1[2] = {
	{9, 2},
	{0, 1},
};
static arc arcs_21_2[1] = {
	{0, 2},
};
static state states_21[3] = {
	{1, arcs_21_0},
	{2, arcs_21_1},
	{1, arcs_21_2},
};
static arc arcs_22_0[1] = {
	{42, 1},
};
static arc arcs_22_1[1] = {
	{0, 1},
};
static state states_22[2] = {
	{1, arcs_22_0},
	{1, arcs_22_1},
};
static arc arcs_23_0[1] = {
	{68, 1},
};
static arc arcs_23_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_23_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_23_3[1] = {
	{26, 4},
};
static arc arcs_23_4[2] = {
	{27, 5},
	{0, 4},
};
static arc arcs_23_5[1] = {
	{26, 6},
};
static arc arcs_23_6[1] = {
	{0, 6},
};
static state states_23[7] = {
	{1, arcs_23_0},
	{2, arcs_23_1},
	{2, arcs_23_2},
	{1, arcs_23_3},
	{2, arcs_23_4},
	{1, arcs_23_5},
	{1, arcs_23_6},
};
static arc arcs_24_0[2] = {
	{69, 1},
	{70, 1},
};
static arc arcs_24_1[1] = {
	{0, 1},
};
static state states_24[2] = {
	{2, arcs_24_0},
	{1, arcs_24_1},
};
static arc arcs_25_0[1] = {
	{71, 1},
};
static arc arcs_25_1[1] = {
	{72, 2},
};
static arc arcs_25_2[1] = {
	{0, 2},
};
static state states_25[3] = {
	{1, arcs_25_0},
	{1, arcs_25_1},
	{1, arcs_25_2},
};
static arc arcs_26_0[1] = {
	{73, 1},
};
static arc arcs_26_1[2] = {
	{74, 2},
	{12, 3},
};
static arc arcs_26_2[3] = {
	{74, 2},
	{12, 3},
	{71, 4},
};
static arc arcs_26_3[1] = {
	{71, 4},
};
static arc arcs_26_4[3] = {
	{28, 5},
	{13, 6},
	{75, 5},
};
static arc arcs_26_5[1] = {
	{0, 5},
};
static arc arcs_26_6[1] = {
	{75, 7},
};
static arc arcs_26_7[1] = {
	{15, 5},
};
static state states_26[8] = {
	{1, arcs_26_0},
	{2, arcs_26_1},
	{3, arcs_26_2},
	{1, arcs_26_3},
	{3, arcs_26_4},
	{1, arcs_26_5},
	{1, arcs_26_6},
	{1, arcs_26_7},
};
static arc arcs_27_0[1] = {
	{19, 1},
};
static arc arcs_27_1[2] = {
	{77, 2},
	{0, 1},
};
static arc arcs_27_2[1] = {
	{19, 3},
};
static arc arcs_27_3[1] = {
	{0, 3},
};
static state states_27[4] = {
	{1, arcs_27_0},
	{2, arcs_27_1},
	{1, arcs_27_2},
	{1, arcs_27_3},
};
static arc arcs_28_0[1] = {
	{12, 1},
};
static arc arcs_28_1[2] = {
	{77, 2},
	{0, 1},
};
static arc arcs_28_2[1] = {
	{19, 3},
};
static arc arcs_28_3[1] = {
	{0, 3},
};
static state states_28[4] = {
	{1, arcs_28_0},
	{2, arcs_28_1},
	{1, arcs_28_2},
	{1, arcs_28_3},
};
static arc arcs_29_0[1] = {
	{76, 1},
};
static arc arcs_29_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_29_2[2] = {
	{76, 1},
	{0, 2},
};
static state states_29[3] = {
	{1, arcs_29_0},
	{2, arcs_29_1},
	{2, arcs_29_2},
};
static arc arcs_30_0[1] = {
	{78, 1},
};
static arc arcs_30_1[2] = {
	{27, 0},
	{0, 1},
};
static state states_30[2] = {
	{1, arcs_30_0},
	{2, arcs_30_1},
};
static arc arcs_31_0[1] = {
	{19, 1},
};
static arc arcs_31_1[2] = {
	{74, 0},
	{0, 1},
};
static state states_31[2] = {
	{1, arcs_31_0},
	{2, arcs_31_1},
};
static arc arcs_32_0[1] = {
	{79, 1},
};
static arc arcs_32_1[1] = {
	{19, 2},
};
static arc arcs_32_2[2] = {
	{27, 1},
	{0, 2},
};
static state states_32[3] = {
	{1, arcs_32_0},
	{1, arcs_32_1},
	{2, arcs_32_2},
};
static arc arcs_33_0[1] = {
	{80, 1},
};
static arc arcs_33_1[1] = {
	{26, 2},
};
static arc arcs_33_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_33_3[1] = {
	{26, 4},
};
static arc arcs_33_4[1] = {
	{0, 4},
};
static state states_33[5] = {
	{1, arcs_33_0},
	{1, arcs_33_1},
	{2, arcs_33_2},
	{1, arcs_33_3},
	{1, arcs_33_4},
};
static arc arcs_34_0[7] = {
	{81, 1},
	{82, 1},
	{83, 1},
	{84, 1},
	{85, 1},
	{17, 1},
	{86, 1},
};
static arc arcs_34_1[1] = {
	{0, 1},
};
static state states_34[2] = {
	{7, arcs_34_0},
	{1, arcs_34_1},
};
static arc arcs_35_0[1] = {
	{87, 1},
};
static arc arcs_35_1[1] = {
	{26, 2},
};
static arc arcs_35_2[1] = {
	{21, 3},
};
static arc arcs_35_3[1] = {
	{22, 4},
};
static arc arcs_35_4[3] = {
	{88, 1},
	{89, 5},
	{0, 4},
};
static arc arcs_35_5[1] = {
	{21, 6},
};
static arc arcs_35_6[1] = {
	{22, 7},
};
static arc arcs_35_7[1] = {
	{0, 7},
};
static state states_35[8] = {
	{1, arcs_35_0},
	{1, arcs_35_1},
	{1, arcs_35_2},
	{1, arcs_35_3},
	{3, arcs_35_4},
	{1, arcs_35_5},
	{1, arcs_35_6},
	{1, arcs_35_7},
};
static arc arcs_36_0[1] = {
	{90, 1},
};
static arc arcs_36_1[1] = {
	{26, 2},
};
static arc arcs_36_2[1] = {
	{21, 3},
};
static arc arcs_36_3[1] = {
	{22, 4},
};
static arc arcs_36_4[2] = {
	{89, 5},
	{0, 4},
};
static arc arcs_36_5[1] = {
	{21, 6},
};
static arc arcs_36_6[1] = {
	{22, 7},
};
static arc arcs_36_7[1] = {
	{0, 7},
};
static state states_36[8] = {
	{1, arcs_36_0},
	{1, arcs_36_1},
	{1, arcs_36_2},
	{1, arcs_36_3},
	{2, arcs_36_4},
	{1, arcs_36_5},
	{1, arcs_36_6},
	{1, arcs_36_7},
};
static arc arcs_37_0[1] = {
	{91, 1},
};
static arc arcs_37_1[1] = {
	{58, 2},
};
static arc arcs_37_2[1] = {
	{92, 3},
};
static arc arcs_37_3[1] = {
	{9, 4},
};
static arc arcs_37_4[1] = {
	{21, 5},
};
static arc arcs_37_5[1] = {
	{22, 6},
};
static arc arcs_37_6[2] = {
	{89, 7},
	{0, 6},
};
static arc arcs_37_7[1] = {
	{21, 8},
};
static arc arcs_37_8[1] = {
	{22, 9},
};
static arc arcs_37_9[1] = {
	{0, 9},
};
static state states_37[10] = {
	{1, arcs_37_0},
	{1, arcs_37_1},
	{1, arcs_37_2},
	{1, arcs_37_3},
	{1, arcs_37_4},
	{1, arcs_37_5},
	{2, arcs_37_6},
	{1, arcs_37_7},
	{1, arcs_37_8},
	{1, arcs_37_9},
};
static arc arcs_38_0[1] = {
	{93, 1},
};
static arc arcs_38_1[1] = {
	{21, 2},
};
static arc arcs_38_2[1] = {
	{22, 3},
};
static arc arcs_38_3[2] = {
	{94, 4},
	{95, 5},
};
static arc arcs_38_4[1] = {
	{21, 6},
};
static arc arcs_38_5[1] = {
	{21, 7},
};
static arc arcs_38_6[1] = {
	{22, 8},
};
static arc arcs_38_7[1] = {
	{22, 9},
};
static arc arcs_38_8[4] = {
	{94, 4},
	{89, 10},
	{95, 5},
	{0, 8},
};
static arc arcs_38_9[1] = {
	{0, 9},
};
static arc arcs_38_10[1] = {
	{21, 11},
};
static arc arcs_38_11[1] = {
	{22, 12},
};
static arc arcs_38_12[2] = {
	{95, 5},
	{0, 12},
};
static state states_38[13] = {
	{1, arcs_38_0},
	{1, arcs_38_1},
	{1, arcs_38_2},
	{2, arcs_38_3},
	{1, arcs_38_4},
	{1, arcs_38_5},
	{1, arcs_38_6},
	{1, arcs_38_7},
	{4, arcs_38_8},
	{1, arcs_38_9},
	{1, arcs_38_10},
	{1, arcs_38_11},
	{2, arcs_38_12},
};
static arc arcs_39_0[1] = {
	{96, 1},
};
static arc arcs_39_1[1] = {
	{26, 2},
};
static arc arcs_39_2[2] = {
	{97, 3},
	{21, 4},
};
static arc arcs_39_3[1] = {
	{21, 4},
};
static arc arcs_39_4[1] = {
	{22, 5},
};
static arc arcs_39_5[1] = {
	{0, 5},
};
static state states_39[6] = {
	{1, arcs_39_0},
	{1, arcs_39_1},
	{2, arcs_39_2},
	{1, arcs_39_3},
	{1, arcs_39_4},
	{1, arcs_39_5},
};
static arc arcs_40_0[1] = {
	{77, 1},
};
static arc arcs_40_1[1] = {
	{98, 2},
};
static arc arcs_40_2[1] = {
	{0, 2},
};
static state states_40[3] = {
	{1, arcs_40_0},
	{1, arcs_40_1},
	{1, arcs_40_2},
};
static arc arcs_41_0[1] = {
	{99, 1},
};
static arc arcs_41_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_41_2[2] = {
	{27, 3},
	{0, 2},
};
static arc arcs_41_3[1] = {
	{26, 4},
};
static arc arcs_41_4[1] = {
	{0, 4},
};
static state states_41[5] = {
	{1, arcs_41_0},
	{2, arcs_41_1},
	{2, arcs_41_2},
	{1, arcs_41_3},
	{1, arcs_41_4},
};
static arc arcs_42_0[2] = {
	{3, 1},
	{2, 2},
};
static arc arcs_42_1[1] = {
	{0, 1},
};
static arc arcs_42_2[1] = {
	{100, 3},
};
static arc arcs_42_3[1] = {
	{6, 4},
};
static arc arcs_42_4[2] = {
	{6, 4},
	{101, 1},
};
static state states_42[5] = {
	{2, arcs_42_0},
	{1, arcs_42_1},
	{1, arcs_42_2},
	{1, arcs_42_3},
	{2, arcs_42_4},
};
static arc arcs_43_0[1] = {
	{103, 1},
};
static arc arcs_43_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_43_2[1] = {
	{103, 3},
};
static arc arcs_43_3[2] = {
	{27, 4},
	{0, 3},
};
static arc arcs_43_4[2] = {
	{103, 3},
	{0, 4},
};
static state states_43[5] = {
	{1, arcs_43_0},
	{2, arcs_43_1},
	{1, arcs_43_2},
	{2, arcs_43_3},
	{2, arcs_43_4},
};
static arc arcs_44_0[2] = {
	{104, 1},
	{105, 1},
};
static arc arcs_44_1[1] = {
	{0, 1},
};
static state states_44[2] = {
	{2, arcs_44_0},
	{1, arcs_44_1},
};
static arc arcs_45_0[1] = {
	{106, 1},
};
static arc arcs_45_1[2] = {
	{23, 2},
	{21, 3},
};
static arc arcs_45_2[1] = {
	{21, 3},
};
static arc arcs_45_3[1] = {
	{103, 4},
};
static arc arcs_45_4[1] = {
	{0, 4},
};
static state states_45[5] = {
	{1, arcs_45_0},
	{2, arcs_45_1},
	{1, arcs_45_2},
	{1, arcs_45_3},
	{1, arcs_45_4},
};
static arc arcs_46_0[2] = {
	{104, 1},
	{107, 2},
};
static arc arcs_46_1[2] = {
	{87, 3},
	{0, 1},
};
static arc arcs_46_2[1] = {
	{0, 2},
};
static arc arcs_46_3[1] = {
	{104, 4},
};
static arc arcs_46_4[1] = {
	{89, 5},
};
static arc arcs_46_5[1] = {
	{26, 2},
};
static state states_46[6] = {
	{2, arcs_46_0},
	{2, arcs_46_1},
	{1, arcs_46_2},
	{1, arcs_46_3},
	{1, arcs_46_4},
	{1, arcs_46_5},
};
static arc arcs_47_0[1] = {
	{108, 1},
};
static arc arcs_47_1[2] = {
	{109, 0},
	{0, 1},
};
static state states_47[2] = {
	{1, arcs_47_0},
	{2, arcs_47_1},
};
static arc arcs_48_0[1] = {
	{110, 1},
};
static arc arcs_48_1[2] = {
	{111, 0},
	{0, 1},
};
static state states_48[2] = {
	{1, arcs_48_0},
	{2, arcs_48_1},
};
static arc arcs_49_0[2] = {
	{112, 1},
	{113, 2},
};
static arc arcs_49_1[1] = {
	{110, 2},
};
static arc arcs_49_2[1] = {
	{0, 2},
};
static state states_49[3] = {
	{2, arcs_49_0},
	{1, arcs_49_1},
	{1, arcs_49_2},
};
static arc arcs_50_0[1] = {
	{98, 1},
};
static arc arcs_50_1[2] = {
	{114, 0},
	{0, 1},
};
static state states_50[2] = {
	{1, arcs_50_0},
	{2, arcs_50_1},
};
static arc arcs_51_0[9] = {
	{115, 1},
	{116, 1},
	{117, 1},
	{118, 1},
	{119, 1},
	{120, 1},
	{92, 1},
	{112, 2},
	{121, 3},
};
static arc arcs_51_1[1] = {
	{0, 1},
};
static arc arcs_51_2[1] = {
	{92, 1},
};
static arc arcs_51_3[2] = {
	{112, 1},
	{0, 3},
};
static state states_51[4] = {
	{9, arcs_51_0},
	{1, arcs_51_1},
	{1, arcs_51_2},
	{2, arcs_51_3},
};
static arc arcs_52_0[1] = {
	{122, 1},
};
static arc arcs_52_1[2] = {
	{123, 0},
	{0, 1},
};
static state states_52[2] = {
	{1, arcs_52_0},
	{2, arcs_52_1},
};
static arc arcs_53_0[1] = {
	{124, 1},
};
static arc arcs_53_1[2] = {
	{125, 0},
	{0, 1},
};
static state states_53[2] = {
	{1, arcs_53_0},
	{2, arcs_53_1},
};
static arc arcs_54_0[1] = {
	{126, 1},
};
static arc arcs_54_1[2] = {
	{127, 0},
	{0, 1},
};
static state states_54[2] = {
	{1, arcs_54_0},
	{2, arcs_54_1},
};
static arc arcs_55_0[1] = {
	{128, 1},
};
static arc arcs_55_1[3] = {
	{129, 0},
	{56, 0},
	{0, 1},
};
static state states_55[2] = {
	{1, arcs_55_0},
	{3, arcs_55_1},
};
static arc arcs_56_0[1] = {
	{130, 1},
};
static arc arcs_56_1[3] = {
	{131, 0},
	{132, 0},
	{0, 1},
};
static state states_56[2] = {
	{1, arcs_56_0},
	{3, arcs_56_1},
};
static arc arcs_57_0[1] = {
	{133, 1},
};
static arc arcs_57_1[5] = {
	{28, 0},
	{134, 0},
	{135, 0},
	{136, 0},
	{0, 1},
};
static state states_57[2] = {
	{1, arcs_57_0},
	{5, arcs_57_1},
};
static arc arcs_58_0[4] = {
	{131, 1},
	{132, 1},
	{137, 1},
	{138, 2},
};
static arc arcs_58_1[1] = {
	{133, 2},
};
static arc arcs_58_2[1] = {
	{0, 2},
};
static state states_58[3] = {
	{4, arcs_58_0},
	{1, arcs_58_1},
	{1, arcs_58_2},
};
static arc arcs_59_0[1] = {
	{139, 1},
};
static arc arcs_59_1[3] = {
	{140, 1},
	{29, 2},
	{0, 1},
};
static arc arcs_59_2[1] = {
	{133, 3},
};
static arc arcs_59_3[1] = {
	{0, 3},
};
static state states_59[4] = {
	{1, arcs_59_0},
	{3, arcs_59_1},
	{1, arcs_59_2},
	{1, arcs_59_3},
};
static arc arcs_60_0[6] = {
	{13, 1},
	{142, 2},
	{145, 3},
	{19, 4},
	{148, 4},
	{149, 5},
};
static arc arcs_60_1[3] = {
	{42, 6},
	{141, 6},
	{15, 4},
};
static arc arcs_60_2[2] = {
	{143, 7},
	{144, 4},
};
static arc arcs_60_3[2] = {
	{146, 8},
	{147, 4},
};
static arc arcs_60_4[1] = {
	{0, 4},
};
static arc arcs_60_5[2] = {
	{149, 5},
	{0, 5},
};
static arc arcs_60_6[1] = {
	{15, 4},
};
static arc arcs_60_7[1] = {
	{144, 4},
};
static arc arcs_60_8[1] = {
	{147, 4},
};
static state states_60[9] = {
	{6, arcs_60_0},
	{3, arcs_60_1},
	{2, arcs_60_2},
	{2, arcs_60_3},
	{1, arcs_60_4},
	{2, arcs_60_5},
	{1, arcs_60_6},
	{1, arcs_60_7},
	{1, arcs_60_8},
};
static arc arcs_61_0[1] = {
	{26, 1},
};
static arc arcs_61_1[3] = {
	{150, 2},
	{27, 3},
	{0, 1},
};
static arc arcs_61_2[1] = {
	{0, 2},
};
static arc arcs_61_3[2] = {
	{26, 4},
	{0, 3},
};
static arc arcs_61_4[2] = {
	{27, 3},
	{0, 4},
};
static state states_61[5] = {
	{1, arcs_61_0},
	{3, arcs_61_1},
	{1, arcs_61_2},
	{2, arcs_61_3},
	{2, arcs_61_4},
};
static arc arcs_62_0[1] = {
	{26, 1},
};
static arc arcs_62_1[3] = {
	{151, 2},
	{27, 3},
	{0, 1},
};
static arc arcs_62_2[1] = {
	{0, 2},
};
static arc arcs_62_3[2] = {
	{26, 4},
	{0, 3},
};
static arc arcs_62_4[2] = {
	{27, 3},
	{0, 4},
};
static state states_62[5] = {
	{1, arcs_62_0},
	{3, arcs_62_1},
	{1, arcs_62_2},
	{2, arcs_62_3},
	{2, arcs_62_4},
};
static arc arcs_63_0[1] = {
	{106, 1},
};
static arc arcs_63_1[2] = {
	{23, 2},
	{21, 3},
};
static arc arcs_63_2[1] = {
	{21, 3},
};
static arc arcs_63_3[1] = {
	{26, 4},
};
static arc arcs_63_4[1] = {
	{0, 4},
};
static state states_63[5] = {
	{1, arcs_63_0},
	{2, arcs_63_1},
	{1, arcs_63_2},
	{1, arcs_63_3},
	{1, arcs_63_4},
};
static arc arcs_64_0[3] = {
	{13, 1},
	{142, 2},
	{74, 3},
};
static arc arcs_64_1[2] = {
	{14, 4},
	{15, 5},
};
static arc arcs_64_2[1] = {
	{152, 6},
};
static arc arcs_64_3[1] = {
	{19, 5},
};
static arc arcs_64_4[1] = {
	{15, 5},
};
static arc arcs_64_5[1] = {
	{0, 5},
};
static arc arcs_64_6[1] = {
	{144, 5},
};
static state states_64[7] = {
	{3, arcs_64_0},
	{2, arcs_64_1},
	{1, arcs_64_2},
	{1, arcs_64_3},
	{1, arcs_64_4},
	{1, arcs_64_5},
	{1, arcs_64_6},
};
static arc arcs_65_0[1] = {
	{153, 1},
};
static arc arcs_65_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_65_2[2] = {
	{153, 1},
	{0, 2},
};
static state states_65[3] = {
	{1, arcs_65_0},
	{2, arcs_65_1},
	{2, arcs_65_2},
};
static arc arcs_66_0[3] = {
	{74, 1},
	{26, 2},
	{21, 3},
};
static arc arcs_66_1[1] = {
	{74, 4},
};
static arc arcs_66_2[2] = {
	{21, 3},
	{0, 2},
};
static arc arcs_66_3[3] = {
	{26, 5},
	{154, 6},
	{0, 3},
};
static arc arcs_66_4[1] = {
	{74, 6},
};
static arc arcs_66_5[2] = {
	{154, 6},
	{0, 5},
};
static arc arcs_66_6[1] = {
	{0, 6},
};
static state states_66[7] = {
	{3, arcs_66_0},
	{1, arcs_66_1},
	{2, arcs_66_2},
	{3, arcs_66_3},
	{1, arcs_66_4},
	{2, arcs_66_5},
	{1, arcs_66_6},
};
static arc arcs_67_0[1] = {
	{21, 1},
};
static arc arcs_67_1[2] = {
	{26, 2},
	{0, 1},
};
static arc arcs_67_2[1] = {
	{0, 2},
};
static state states_67[3] = {
	{1, arcs_67_0},
	{2, arcs_67_1},
	{1, arcs_67_2},
};
static arc arcs_68_0[1] = {
	{98, 1},
};
static arc arcs_68_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_68_2[2] = {
	{98, 1},
	{0, 2},
};
static state states_68[3] = {
	{1, arcs_68_0},
	{2, arcs_68_1},
	{2, arcs_68_2},
};
static arc arcs_69_0[1] = {
	{26, 1},
};
static arc arcs_69_1[2] = {
	{27, 2},
	{0, 1},
};
static arc arcs_69_2[2] = {
	{26, 1},
	{0, 2},
};
static state states_69[3] = {
	{1, arcs_69_0},
	{2, arcs_69_1},
	{2, arcs_69_2},
};
static arc arcs_70_0[1] = {
	{26, 1},
};
static arc arcs_70_1[3] = {
	{21, 2},
	{27, 3},
	{0, 1},
};
static arc arcs_70_2[1] = {
	{26, 4},
};
static arc arcs_70_3[2] = {
	{26, 5},
	{0, 3},
};
static arc arcs_70_4[2] = {
	{27, 6},
	{0, 4},
};
static arc arcs_70_5[2] = {
	{27, 3},
	{0, 5},
};
static arc arcs_70_6[2] = {
	{26, 7},
	{0, 6},
};
static arc arcs_70_7[1] = {
	{21, 2},
};
static state states_70[8] = {
	{1, arcs_70_0},
	{3, arcs_70_1},
	{1, arcs_70_2},
	{2, arcs_70_3},
	{2, arcs_70_4},
	{2, arcs_70_5},
	{2, arcs_70_6},
	{1, arcs_70_7},
};
static arc arcs_71_0[1] = {
	{155, 1},
};
static arc arcs_71_1[1] = {
	{19, 2},
};
static arc arcs_71_2[2] = {
	{13, 3},
	{21, 4},
};
static arc arcs_71_3[2] = {
	{9, 5},
	{15, 6},
};
static arc arcs_71_4[1] = {
	{22, 7},
};
static arc arcs_71_5[1] = {
	{15, 6},
};
static arc arcs_71_6[1] = {
	{21, 4},
};
static arc arcs_71_7[1] = {
	{0, 7},
};
static state states_71[8] = {
	{1, arcs_71_0},
	{1, arcs_71_1},
	{2, arcs_71_2},
	{2, arcs_71_3},
	{1, arcs_71_4},
	{1, arcs_71_5},
	{1, arcs_71_6},
	{1, arcs_71_7},
};
static arc arcs_72_0[3] = {
	{156, 1},
	{28, 2},
	{29, 3},
};
static arc arcs_72_1[2] = {
	{27, 4},
	{0, 1},
};
static arc arcs_72_2[1] = {
	{26, 5},
};
static arc arcs_72_3[1] = {
	{26, 6},
};
static arc arcs_72_4[4] = {
	{156, 1},
	{28, 2},
	{29, 3},
	{0, 4},
};
static arc arcs_72_5[2] = {
	{27, 7},
	{0, 5},
};
static arc arcs_72_6[1] = {
	{0, 6},
};
static arc arcs_72_7[1] = {
	{29, 3},
};
static state states_72[8] = {
	{3, arcs_72_0},
	{2, arcs_72_1},
	{1, arcs_72_2},
	{1, arcs_72_3},
	{4, arcs_72_4},
	{2, arcs_72_5},
	{1, arcs_72_6},
	{1, arcs_72_7},
};
static arc arcs_73_0[1] = {
	{26, 1},
};
static arc arcs_73_1[3] = {
	{151, 2},
	{25, 3},
	{0, 1},
};
static arc arcs_73_2[1] = {
	{0, 2},
};
static arc arcs_73_3[1] = {
	{26, 2},
};
static state states_73[4] = {
	{1, arcs_73_0},
	{3, arcs_73_1},
	{1, arcs_73_2},
	{1, arcs_73_3},
};
static arc arcs_74_0[2] = {
	{150, 1},
	{158, 1},
};
static arc arcs_74_1[1] = {
	{0, 1},
};
static state states_74[2] = {
	{2, arcs_74_0},
	{1, arcs_74_1},
};
static arc arcs_75_0[1] = {
	{91, 1},
};
static arc arcs_75_1[1] = {
	{58, 2},
};
static arc arcs_75_2[1] = {
	{92, 3},
};
static arc arcs_75_3[1] = {
	{102, 4},
};
static arc arcs_75_4[2] = {
	{157, 5},
	{0, 4},
};
static arc arcs_75_5[1] = {
	{0, 5},
};
static state states_75[6] = {
	{1, arcs_75_0},
	{1, arcs_75_1},
	{1, arcs_75_2},
	{1, arcs_75_3},
	{2, arcs_75_4},
	{1, arcs_75_5},
};
static arc arcs_76_0[1] = {
	{87, 1},
};
static arc arcs_76_1[1] = {
	{103, 2},
};
static arc arcs_76_2[2] = {
	{157, 3},
	{0, 2},
};
static arc arcs_76_3[1] = {
	{0, 3},
};
static state states_76[4] = {
	{1, arcs_76_0},
	{1, arcs_76_1},
	{2, arcs_76_2},
	{1, arcs_76_3},
};
static arc arcs_77_0[2] = {
	{151, 1},
	{160, 1},
};
static arc arcs_77_1[1] = {
	{0, 1},
};
static state states_77[2] = {
	{2, arcs_77_0},
	{1, arcs_77_1},
};
static arc arcs_78_0[1] = {
	{91, 1},
};
static arc arcs_78_1[1] = {
	{58, 2},
};
static arc arcs_78_2[1] = {
	{92, 3},
};
static arc arcs_78_3[1] = {
	{104, 4},
};
static arc arcs_78_4[2] = {
	{159, 5},
	{0, 4},
};
static arc arcs_78_5[1] = {
	{0, 5},
};
static state states_78[6] = {
	{1, arcs_78_0},
	{1, arcs_78_1},
	{1, arcs_78_2},
	{1, arcs_78_3},
	{2, arcs_78_4},
	{1, arcs_78_5},
};
static arc arcs_79_0[1] = {
	{87, 1},
};
static arc arcs_79_1[1] = {
	{103, 2},
};
static arc arcs_79_2[2] = {
	{159, 3},
	{0, 2},
};
static arc arcs_79_3[1] = {
	{0, 3},
};
static state states_79[4] = {
	{1, arcs_79_0},
	{1, arcs_79_1},
	{2, arcs_79_2},
	{1, arcs_79_3},
};
static arc arcs_80_0[1] = {
	{26, 1},
};
static arc arcs_80_1[2] = {
	{27, 0},
	{0, 1},
};
static state states_80[2] = {
	{1, arcs_80_0},
	{2, arcs_80_1},
};
static arc arcs_81_0[1] = {
	{19, 1},
};
static arc arcs_81_1[1] = {
	{0, 1},
};
static state states_81[2] = {
	{1, arcs_81_0},
	{1, arcs_81_1},
};
static arc arcs_82_0[1] = {
	{163, 1},
};
static arc arcs_82_1[2] = {
	{9, 2},
	{0, 1},
};
static arc arcs_82_2[1] = {
	{0, 2},
};
static state states_82[3] = {
	{1, arcs_82_0},
	{2, arcs_82_1},
	{1, arcs_82_2},
};
static dfa dfas[83] = {
	{256, "single_input", 0, 3, states_0,
	 "\004\050\014\000\000\000\200\012\236\202\201\054\001\004\001\000\030\102\062\010\010"},
	{257, "file_input", 0, 2, states_1,
	 "\204\050\014\000\000\000\200\012\236\202\201\054\001\004\001\000\030\102\062\010\010"},
	{258, "eval_input", 0, 3, states_2,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{259, "decorator", 0, 7, states_3,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{260, "decorators", 0, 2, states_4,
	 "\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{261, "funcdef", 0, 7, states_5,
	 "\000\010\004\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{262, "parameters", 0, 4, states_6,
	 "\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{263, "varargslist", 0, 10, states_7,
	 "\000\040\010\060\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{264, "fpdef", 0, 4, states_8,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{265, "fplist", 0, 3, states_9,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{266, "stmt", 0, 2, states_10,
	 "\000\050\014\000\000\000\200\012\236\202\201\054\001\004\001\000\030\102\062\010\010"},
	{267, "simple_stmt", 0, 4, states_11,
	 "\000\040\010\000\000\000\200\012\236\202\001\000\000\004\001\000\030\102\062\000\010"},
	{268, "small_stmt", 0, 2, states_12,
	 "\000\040\010\000\000\000\200\012\236\202\001\000\000\004\001\000\030\102\062\000\010"},
	{269, "expr_stmt", 0, 6, states_13,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{270, "augassign", 0, 2, states_14,
	 "\000\000\000\000\000\370\177\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{271, "print_stmt", 0, 9, states_15,
	 "\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{272, "del_stmt", 0, 3, states_16,
	 "\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{273, "pass_stmt", 0, 2, states_17,
	 "\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{274, "flow_stmt", 0, 2, states_18,
	 "\000\000\000\000\000\000\000\000\036\000\000\000\000\000\000\000\000\000\000\000\010"},
	{275, "break_stmt", 0, 2, states_19,
	 "\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000\000"},
	{276, "continue_stmt", 0, 2, states_20,
	 "\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000\000\000\000"},
	{277, "return_stmt", 0, 3, states_21,
	 "\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000"},
	{278, "yield_stmt", 0, 2, states_22,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\010"},
	{279, "raise_stmt", 0, 7, states_23,
	 "\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\000\000\000\000\000"},
	{280, "import_stmt", 0, 2, states_24,
	 "\000\000\000\000\000\000\000\000\200\002\000\000\000\000\000\000\000\000\000\000\000"},
	{281, "import_name", 0, 3, states_25,
	 "\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000\000\000"},
	{282, "import_from", 0, 8, states_26,
	 "\000\000\000\000\000\000\000\000\000\002\000\000\000\000\000\000\000\000\000\000\000"},
	{283, "import_as_name", 0, 4, states_27,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{284, "dotted_as_name", 0, 4, states_28,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{285, "import_as_names", 0, 3, states_29,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{286, "dotted_as_names", 0, 2, states_30,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{287, "dotted_name", 0, 2, states_31,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{288, "global_stmt", 0, 3, states_32,
	 "\000\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000\000"},
	{289, "assert_stmt", 0, 5, states_33,
	 "\000\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000\000\000"},
	{290, "compound_stmt", 0, 2, states_34,
	 "\000\010\004\000\000\000\000\000\000\000\200\054\001\000\000\000\000\000\000\010\000"},
	{291, "if_stmt", 0, 8, states_35,
	 "\000\000\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000"},
	{292, "while_stmt", 0, 8, states_36,
	 "\000\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\000\000"},
	{293, "for_stmt", 0, 10, states_37,
	 "\000\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000"},
	{294, "try_stmt", 0, 13, states_38,
	 "\000\000\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000"},
	{295, "with_stmt", 0, 6, states_39,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\000"},
	{296, "with_var", 0, 3, states_40,
	 "\000\000\000\000\000\000\000\000\000\040\000\000\000\000\000\000\000\000\000\000\000"},
	{297, "except_clause", 0, 5, states_41,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000"},
	{298, "suite", 0, 5, states_42,
	 "\004\040\010\000\000\000\200\012\236\202\001\000\000\004\001\000\030\102\062\000\010"},
	{299, "testlist_safe", 0, 5, states_43,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{300, "old_test", 0, 2, states_44,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{301, "old_lambdef", 0, 5, states_45,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000"},
	{302, "test", 0, 6, states_46,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{303, "or_test", 0, 2, states_47,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\001\000\030\102\062\000\000"},
	{304, "and_test", 0, 2, states_48,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\001\000\030\102\062\000\000"},
	{305, "not_test", 0, 3, states_49,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\001\000\030\102\062\000\000"},
	{306, "comparison", 0, 2, states_50,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{307, "comp_op", 0, 4, states_51,
	 "\000\000\000\000\000\000\000\000\000\000\000\020\000\000\371\003\000\000\000\000\000"},
	{308, "expr", 0, 2, states_52,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{309, "xor_expr", 0, 2, states_53,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{310, "and_expr", 0, 2, states_54,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{311, "shift_expr", 0, 2, states_55,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{312, "arith_expr", 0, 2, states_56,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{313, "term", 0, 2, states_57,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{314, "factor", 0, 3, states_58,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{315, "power", 0, 4, states_59,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\100\062\000\000"},
	{316, "atom", 0, 9, states_60,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\100\062\000\000"},
	{317, "listmaker", 0, 5, states_61,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{318, "testlist_gexp", 0, 5, states_62,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{319, "lambdef", 0, 5, states_63,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000"},
	{320, "trailer", 0, 7, states_64,
	 "\000\040\000\000\000\000\000\000\000\004\000\000\000\000\000\000\000\100\000\000\000"},
	{321, "subscriptlist", 0, 3, states_65,
	 "\000\040\050\000\000\000\000\000\000\004\000\000\000\004\001\000\030\102\062\000\000"},
	{322, "subscript", 0, 7, states_66,
	 "\000\040\050\000\000\000\000\000\000\004\000\000\000\004\001\000\030\102\062\000\000"},
	{323, "sliceop", 0, 3, states_67,
	 "\000\000\040\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{324, "exprlist", 0, 3, states_68,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\000\000\000\030\102\062\000\000"},
	{325, "testlist", 0, 3, states_69,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{326, "dictsetmaker", 0, 8, states_70,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{327, "classdef", 0, 8, states_71,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\010\000"},
	{328, "arglist", 0, 8, states_72,
	 "\000\040\010\060\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{329, "argument", 0, 4, states_73,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{330, "list_iter", 0, 2, states_74,
	 "\000\000\000\000\000\000\000\000\000\000\200\010\000\000\000\000\000\000\000\000\000"},
	{331, "list_for", 0, 6, states_75,
	 "\000\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000"},
	{332, "list_if", 0, 4, states_76,
	 "\000\000\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000"},
	{333, "gen_iter", 0, 2, states_77,
	 "\000\000\000\000\000\000\000\000\000\000\200\010\000\000\000\000\000\000\000\000\000"},
	{334, "gen_for", 0, 6, states_78,
	 "\000\000\000\000\000\000\000\000\000\000\000\010\000\000\000\000\000\000\000\000\000"},
	{335, "gen_if", 0, 4, states_79,
	 "\000\000\000\000\000\000\000\000\000\000\200\000\000\000\000\000\000\000\000\000\000"},
	{336, "testlist1", 0, 2, states_80,
	 "\000\040\010\000\000\000\000\000\000\000\000\000\000\004\001\000\030\102\062\000\000"},
	{337, "encoding_decl", 0, 2, states_81,
	 "\000\000\010\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"},
	{338, "yield_expr", 0, 3, states_82,
	 "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\010"},
};
static label labels[164] = {
	{0, "EMPTY"},
	{256, 0},
	{4, 0},
	{267, 0},
	{290, 0},
	{257, 0},
	{266, 0},
	{0, 0},
	{258, 0},
	{325, 0},
	{259, 0},
	{50, 0},
	{287, 0},
	{7, 0},
	{328, 0},
	{8, 0},
	{260, 0},
	{261, 0},
	{1, "def"},
	{1, 0},
	{262, 0},
	{11, 0},
	{298, 0},
	{263, 0},
	{264, 0},
	{22, 0},
	{302, 0},
	{12, 0},
	{16, 0},
	{36, 0},
	{265, 0},
	{268, 0},
	{13, 0},
	{269, 0},
	{271, 0},
	{272, 0},
	{273, 0},
	{274, 0},
	{280, 0},
	{288, 0},
	{289, 0},
	{270, 0},
	{338, 0},
	{37, 0},
	{38, 0},
	{39, 0},
	{40, 0},
	{41, 0},
	{42, 0},
	{43, 0},
	{44, 0},
	{45, 0},
	{46, 0},
	{47, 0},
	{49, 0},
	{1, "print"},
	{35, 0},
	{1, "del"},
	{324, 0},
	{1, "pass"},
	{275, 0},
	{276, 0},
	{277, 0},
	{279, 0},
	{278, 0},
	{1, "break"},
	{1, "continue"},
	{1, "return"},
	{1, "raise"},
	{281, 0},
	{282, 0},
	{1, "import"},
	{286, 0},
	{1, "from"},
	{23, 0},
	{285, 0},
	{283, 0},
	{1, "as"},
	{284, 0},
	{1, "global"},
	{1, "assert"},
	{291, 0},
	{292, 0},
	{293, 0},
	{294, 0},
	{295, 0},
	{327, 0},
	{1, "if"},
	{1, "elif"},
	{1, "else"},
	{1, "while"},
	{1, "for"},
	{1, "in"},
	{1, "try"},
	{297, 0},
	{1, "finally"},
	{1, "with"},
	{296, 0},
	{308, 0},
	{1, "except"},
	{5, 0},
	{6, 0},
	{299, 0},
	{300, 0},
	{303, 0},
	{301, 0},
	{1, "lambda"},
	{319, 0},
	{304, 0},
	{1, "or"},
	{305, 0},
	{1, "and"},
	{1, "not"},
	{306, 0},
	{307, 0},
	{20, 0},
	{21, 0},
	{28, 0},
	{31, 0},
	{30, 0},
	{29, 0},
	{1, "is"},
	{309, 0},
	{18, 0},
	{310, 0},
	{33, 0},
	{311, 0},
	{19, 0},
	{312, 0},
	{34, 0},
	{313, 0},
	{14, 0},
	{15, 0},
	{314, 0},
	{17, 0},
	{24, 0},
	{48, 0},
	{32, 0},
	{315, 0},
	{316, 0},
	{320, 0},
	{318, 0},
	{9, 0},
	{317, 0},
	{10, 0},
	{26, 0},
	{326, 0},
	{27, 0},
	{2, 0},
	{3, 0},
	{331, 0},
	{334, 0},
	{321, 0},
	{322, 0},
	{323, 0},
	{1, "class"},
	{329, 0},
	{330, 0},
	{332, 0},
	{333, 0},
	{335, 0},
	{336, 0},
	{337, 0},
	{1, "yield"},
};
grammar _PyParser_Grammar = {
	83,
	dfas,
	{164, labels},
	256
};
