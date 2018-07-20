/*
* image searcher IDL
* input: company_id, craft, style, image_vector
* output: product_list
*
* dehong.gdh 20180717
*/

namespace py image_searcher

// ========   Request  ==========
enum RequestType{
	IMAGE_SEARCH,
	SEARCH_DEBUG
}

struct Request{
	1: required RequestType type;
	2: required i32		comp_id;
	3: required i32		craft_id;
	4: required set<i32>	styles;
	5: required list< list<double> > img_urls;
	6: required i32     vec_dim;
	7: optional map<string, string> srch_params;
}

// ========    Result  ===========
enum ReturnStatus{
	SEARCH_OK,
	ERROR_1
}

struct ReturnInfo{
	1: required i32	       srch_img_cnt;
	2: required i32	       srch_sample_cnt;
	3: optional list<string> debug_info;
}

struct ReturnProduct{
	1: required list<i32> list_prods;
}

struct SearchResult{
	1: required ReturnStatus  ret_status;
	2: required ReturnInfo	  ret_info;
	3: required ReturnProduct ret_prod;
}

// ======   Exception ==========
exception RequestException{
	1: required i32 code;
	2: optional string excp;
}

// =======   Service  ===========
service ImageSearcherService{
	// service function
	SearchResult doSearch(1: Request request) throws(1:RequestException qe);
}