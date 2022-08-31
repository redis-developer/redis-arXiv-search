import { MASTER_URL } from './config';

export const fetchFromBackend = async (url: string, method: string, body?: any) => {
  const request = new Request(url, {
    method,
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json'
    },
  });

  const response = await fetch(request);

  if (response.status === 500) {
    throw new Error('Internal server error');
  }
  if (response.status === 401 || response.status === 403) {
    // redirect to home page
    window.location.href = "/";
  }

  const data = await response.json();

  if (response.status > 400 && response.status < 500) {
    if (data.detail) {
      throw data.detail;
    }
    throw data;
  }

  return data;
}
export const getPapers = async (limit=15, skip=0) => {
  return fetchFromBackend(`${MASTER_URL}?limit=${limit}&skip=${skip}`, 'GET');
}
// get papers from Redis through the FastAPI backend


export const getSemanticallySimilarPapers = async (paper_id: string,
                                                   search='KNN',
                                                   limit=15) => {
  console.log(paper_id);
  let body = {
    paper_id: paper_id,
    search_type: search,
    number_of_results: limit
  }

  const url = MASTER_URL + "vectorsearch/text";
  return fetchFromBackend(url, 'POST', body);
};


export const getSemanticallySimilarPapersbyText = async (text: string,
                                                         search='KNN',
                                                         limit=15) => {
  let body = {
    user_text: text,
    search_type: search,
    number_of_results: limit,
  }

  const url = MASTER_URL + "vectorsearch/text/user";
  return fetchFromBackend(url, 'POST', body);
};
