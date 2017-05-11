#define JISX0213_ENCPAIRS 46
#ifdef EXTERN_JISX0213_PAIR
static const struct widedbcs_index *jisx0213_pair_decmap;
static const struct pair_encodemap *jisx0213_pair_encmap;
#else
static const ucs4_t __jisx0213_pair_decmap[49] = {
810234010,810365082,810496154,810627226,810758298,816525466,816656538,
816787610,816918682,817049754,817574042,818163866,818426010,838283418,
15074048,U,U,U,39060224,39060225,42730240,42730241,39387904,39387905,39453440,
39453441,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,48825061,48562921,
};

static const struct widedbcs_index jisx0213_pair_decmap[256] = {
{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{__jisx0213_pair_decmap
+0,119,123},{__jisx0213_pair_decmap+5,119,126},{__jisx0213_pair_decmap+13,120,
120},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{__jisx0213_pair_decmap+14,68,102},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,
0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{
0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0
},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},
};

static const struct pair_encodemap jisx0213_pair_encmap[JISX0213_ENCPAIRS] = {
{0x00e60000,0x295c},{0x00e60300,0x2b44},{0x02540000,0x2b38},{0x02540300,0x2b48
},{0x02540301,0x2b49},{0x02590000,0x2b30},{0x02590300,0x2b4c},{0x02590301,
0x2b4d},{0x025a0000,0x2b43},{0x025a0300,0x2b4e},{0x025a0301,0x2b4f},{
0x028c0000,0x2b37},{0x028c0300,0x2b4a},{0x028c0301,0x2b4b},{0x02e50000,0x2b60
},{0x02e502e9,0x2b66},{0x02e90000,0x2b64},{0x02e902e5,0x2b65},{0x304b0000,
0x242b},{0x304b309a,0x2477},{0x304d0000,0x242d},{0x304d309a,0x2478},{
0x304f0000,0x242f},{0x304f309a,0x2479},{0x30510000,0x2431},{0x3051309a,0x247a
},{0x30530000,0x2433},{0x3053309a,0x247b},{0x30ab0000,0x252b},{0x30ab309a,
0x2577},{0x30ad0000,0x252d},{0x30ad309a,0x2578},{0x30af0000,0x252f},{
0x30af309a,0x2579},{0x30b10000,0x2531},{0x30b1309a,0x257a},{0x30b30000,0x2533
},{0x30b3309a,0x257b},{0x30bb0000,0x253b},{0x30bb309a,0x257c},{0x30c40000,
0x2544},{0x30c4309a,0x257d},{0x30c80000,0x2548},{0x30c8309a,0x257e},{
0x31f70000,0x2675},{0x31f7309a,0x2678},
};
#endif
