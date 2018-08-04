/*
* Search_Plan IDL
* input: company_id, craft, style, image_url
* output: offer_list
*
* dehong.gdh 20180715
*/

namespace py search_plan

// ========   Request  ==========
enum SPRequestType{
	IMAGE_SEARCH,
	SEARCH_DEBUG
}

struct SPRequest{
	1: required SPRequestType type;
	2: required i32		comp_id;
	3: required i32		craft_id;
	4: required set<i32>	styles;
	5: required list<string> img_urls; 
	6: optional map<string, string> srch_params; 
}

// ========    Result  ===========
enum SPReturnStatus{
	SEARCH_OK,
	ERROR_1
}

struct SPReturnInfo{
	1: required i32	       srch_img_cnt;
	2: required i32	       srch_sample_cnt;
	3: optional list<string> debug_info;
}

struct SPReturnProduct{
	1: required list< list<i32> > list_prods;
}

struct SPSearchResult{
	1: required SPReturnStatus  ret_status;
	2: required SPReturnInfo	  ret_info;
	3: required SPReturnProduct ret_prod;
}

// ======   Exception ==========
exception SPRequestException{
	1: required i32 code;
	2: optional string excp;
}

// =======   Service  ===========
service SearchPlanService{
	// service function
	SPSearchResult doImageSearch(1: SPRequest request) throws(1:SPRequestException qe);
}
