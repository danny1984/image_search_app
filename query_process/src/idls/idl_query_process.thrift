/*
* Query Process IDL
* input: image_url
* output: image_vector
*
* dehong.gdh 20180717
*/
namespace py query_process

// ========   Request  ==========
enum RequestType{
	IMAGE_2_VECTOR,
	IMAGE_2_VECTOR_DEBUG
}

struct Request{
	1: required RequestType type;
	2: required list<string> img_urls;
	3: optional map<string, string> params;
}

// ========= Result ================
enum ReturnStatus{
	SEARCH_OK,
	ERROR_1
}

struct ReturnInfo{
	1: required i32	         img_cnt;
	2: required i32          img_dim;
	3: optional list<string> debug_info;
}

struct ReturnVector{
	1: required list< list<double> > list_image_vectors;
}

struct SearchResult{
	1: required ReturnStatus  ret_status;
	2: required ReturnInfo	  ret_info;
	3: required ReturnVector  ret_vec;
}

// ======   Exception ==========
exception RequestException{
	1: required i32 code;
	2: optional string excp;
}

// =======   Service  ===========
service QueryProcessService{
	// service function
	SearchResult doQueryProcess(1: Request request) throws(1:RequestException qe);
}
