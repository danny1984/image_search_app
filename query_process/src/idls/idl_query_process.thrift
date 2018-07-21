/*
* Query Process IDL
* input: image_url
* output: image_vector
*
* dehong.gdh 20180717
*/
namespace py query_process

// ========   Request  ==========
enum QPRequestType{
	IMAGE_2_VECTOR,
	IMAGE_2_VECTOR_DEBUG
}

struct QPRequest{
	1: required QPRequestType type;
	2: required list<string> img_urls;
	3: optional map<string, string> params;
}

// ========= Result ================
enum QPReturnStatus{
	SEARCH_OK,
	ERROR_1
}

struct QPReturnInfo{
	1: required i32	         img_cnt;
	2: required i32          img_dim;
	3: optional list<string> debug_info;
}

struct QPReturnVector{
	1: required list< list<double> > list_image_vectors;
}

struct QPSearchResult{
	1: required QPReturnStatus  ret_status;
	2: required QPReturnInfo	  ret_info;
	3: required QPReturnVector  ret_vec;
}

// ======   Exception ==========
exception QPRequestException{
	1: required i32 code;
	2: optional string excp;
}

// =======   Service  ===========
service QueryProcessService{
	// service function
	QPSearchResult doQueryProcess(1: QPRequest request) throws(1:QPRequestException qe);
}
