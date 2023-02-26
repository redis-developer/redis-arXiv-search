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

export const getPapers = async (limit = 15, skip = 0, years: string[] = [], categories: string[] = []) => {
  var params: string;
  if (!years.length && !categories.length) {
    var params = `?limit=${limit}&skip=${skip}`
  } else {
    if (years.length && categories.length) {
      var params = `?limit=${limit}&skip=${skip}&years=${years.join()}&categories=${categories.join()}`
    } else if (years.length) {
      var params = `?limit=${limit}&skip=${skip}&years=${years.join()}`
    } else {
      var params = `?limit=${limit}&skip=${skip}&categories=${categories.join()}`
    }
  }
  return fetchFromBackend(`${MASTER_URL}${params}`, 'GET');
}
// get papers from Redis through the FastAPI backend


interface PaperSearchRequest {
  years: string[];
  categories: string[];
  search?: 'KNN' | 'ANN'
  limit?: number;
  matchExactCategories?: boolean;
}

interface SimilarPaperSearchRequest extends PaperSearchRequest {
  paper_id: string;
}

export const getSemanticallySimilarPapers = async ({
  paper_id,
  years,
  categories,
  search = 'KNN',
  limit = 15,
  matchExactCategories = false
}: SimilarPaperSearchRequest) => {
  let body = {
    paper_id: paper_id,
    search_type: search,
    number_of_results: limit,
    years: years,
    categories: categories,
    categories_operator: matchExactCategories ? 'AND' : 'OR'
  }

  const url = MASTER_URL + "vectorsearch/text";
  return fetchFromBackend(url, 'POST', body);
};

interface TextPaperSearchRequest extends PaperSearchRequest {
  searchItems: string[],
}

export const getSemanticallySimilarPapersbyText = async ({
  searchItems,
  years,
  categories,
  search = 'KNN',
  limit = 15,
  matchExactCategories = false
}: TextPaperSearchRequest) => {
  let body = {
    articles: searchItems.map(text => ({ text })),
    search_type: search,
    number_of_results: limit,
    years: years,
    categories,
    categories_operator: matchExactCategories ? 'AND' : 'OR'
  }

  const url = MASTER_URL + "vectorsearch/text/user";
  return fetchFromBackend(url, 'POST', body);
};


export const getSuggestedCategories = async (
  articles: string[]
) => {
  let body = { articles }

  const url = MASTER_URL + "predict-categories"
  const { categories } = await fetchFromBackend(url, 'POST', body)
  return categories || []
};
