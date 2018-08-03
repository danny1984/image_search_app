/*
* image searcher IDL
* input: company_id, craft, style, image_vector
* output: product_list
*
* dehong.gdh 20180717
*/

namespace py image_searcher

// ========   Request  ==========
enum ISRequestType{
	IMAGE_SEARCH,
	SEARCH_DEBUG
}

struct ISRequest{
	1: required ISRequestType type;
	2: required i32		comp_id;
	3: required i32		craft_id;
	4: required set<i32>	styles;
	5: required list< list<double> > query_vecs;
	6: required i32     vec_dim;
	7: optional map<string, string> srch_params;
}
// 注: 一次检索发送多个图片检索

// ========    Result  ===========
enum ISReturnStatus{
	SEARCH_OK,
	ERROR_NO_COMP_ID,
	ERROR_NO_CRAFT_ID
}

struct ISReturnInfo{
	1: required i32	       srch_img_cnt;
	2: required i32	       srch_sample_cnt;
	3: optional list<string> debug_info;
}

struct ISReturnProduct{
	1: required list< list<i32> > list_prods;
}
// 注: 一次查询可能包含多个检索图片

struct ISSearchResult{
	1: required ISReturnStatus  ret_status;
	2: required ISReturnInfo	ret_info;
	3: required ISReturnProduct ret_prod;
}

// ======   Exception ==========
exception ISRequestException{
	1: required i32 code;
	2: optional string excp;
}

// =======   Service  ===========
service ImageSearcherService{
	// service function
	ISSearchResult doSearch(1: ISRequest request) throws(1:ISRequestException qe);
}
