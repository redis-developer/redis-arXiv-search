import { useEffect } from 'react';
import { useImmer } from "use-immer";
import { getPapers, getSemanticallySimilarPapersbyText, getSuggestedCategories } from '../api';
import { Card } from "./Card"

import {
  Tooltip,
  SelectChangeEvent,
} from '@mui/material';


import { SearchStates } from '../types/search';
import { Search } from '../components/Search';
import { AddItemButton } from '../ui/AddItemButton';

import { useSearchParams } from 'react-router-dom';
import { getArrayParam, parseURLSearchParams } from '../utils/query_string';
import { useDebounce } from '../hooks/useDebounce';
import { SuggestedCategories } from '../components/SuggestedCategories';
import { LoadingButton } from '../ui/LoadingButton';
import { SearchFilters } from '../components/SearchFilters';
import CopyToClipboardButton from '../ui/CopyToClipboard';
import { CATEGORY_HUMAN_NAMES } from '../constants/search_filter';

export const Home = () => {
  const [urlParams, setUrlParams] = useSearchParams();

  const parsed_params = parseURLSearchParams(urlParams)

  const [papers, setPapers] = useImmer<any[]>([]);
  const [isLoadingPapers, setIsLoadingPapers] = useImmer<boolean>(false);
  const [categories, setCategories] = useImmer<string[]>(getArrayParam(parsed_params, 'categories', []));
  const [suggestedCategories, setSuggestedCategories] = useImmer<string[]>([]);
  const [matchExactCategories, setMatchExactCategories] = useImmer<boolean>(false)
  const [years, setYears] = useImmer<string[]>(getArrayParam(parsed_params, 'years', []));
  const [searchStates, setSearchStates] = useImmer<SearchStates>(getArrayParam(parsed_params, 'searchStates', ['']));
  const [total, setTotal] = useImmer<number>(0);
  const [_error, setError] = useImmer<string>('');
  const [skip, setSkip] = useImmer(0);
  const [limit, _setLimit] = useImmer(15);

  const changeSuggestedCategories = async () => {
    const newSuggestedCategories = await getSuggestedCategories(searchStates)

    setSuggestedCategories(newSuggestedCategories)
  }
  const changeSuggestedCategoriesDebounced = useDebounce(changeSuggestedCategories, 500)

  const queryPapers = async () => {
    setIsLoadingPapers(true)
    try {
      if (searchStates) {
        const result = await getSemanticallySimilarPapersbyText({ searchItems: searchStates, years, categories })
        setPapers(result.papers)
        setTotal(result.total)
      } else {
        setSkip(skip + limit);
        const result = await getPapers(limit, skip, years, categories);
        setPapers(result.papers)
        setTotal(result.total)
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setIsLoadingPapers(false)
    }
  };

  // Execute this one when the component loads up
  useEffect(() => {
    queryPapers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setUrlParams({
      years,
      categories,
      searchStates
    })
  }, [years, categories, searchStates, setUrlParams])

  const handleYearSelection = (event: SelectChangeEvent<typeof years>) => {
    const {
      target: { value },
    } = event;
    setYears(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
    setSkip(0)
  };

  const handleCategorySelection = (event: SelectChangeEvent<typeof categories>) => {
    const {
      target: { value },
    } = event;
    setCategories(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
    setSkip(0)
  };

  const handleSearchChange = (index: number, newText: string) => {
    setSearchStates(searchStates => {
      searchStates[index] = newText
    })

    changeSuggestedCategoriesDebounced()
  }

  const handleSearchItemAdd = () => {
    setSearchStates(searchStates => {
      searchStates.push('')
    })
  }

  const handleSearchItemRemove = (index: number) => {
    setSearchStates(searchStates => {
      searchStates.splice(index, 1)
    })
  }

  const applySuggestedCategories = () => {
    const mergedCategories = new Set([...categories, ...suggestedCategories])

    setCategories(Array.from(mergedCategories))
  }

  const handleMatchExactCategoriesChange = () => {
    setMatchExactCategories((el) => !el)
  }

  return (
    <>
      <main role="main">
        <section className="jumbotron text-center bg-white" style={{ paddingTop: '40px' }}>
          <div className="container">
            <h1 className="jumbotron-heading">arXiv Paper Search</h1>
            <p className="lead text-muted">
              This demo uses the built in Vector Search capabilities of Redis Enterprise
              to show how unstructured data, such as paper abstracts (text), can be used to create a powerful
              search engine.
            </p>
            <p className="lead text-muted">
              <strong>Enter a search query below to discover scholarly papers hosted by <a href="https://arxiv.org/" target="_blank" rel="noreferrer">arXiv</a> (Cornell University).</strong>
            </p>
            <div className="container pb-4">

              <SearchFilters
                {...{
                  years,
                  onYearSelection: handleYearSelection,
                  categories,
                  onCategorySelection: handleCategorySelection,
                  matchExactCategories,
                  onMatchExactCategoriesChange: handleMatchExactCategoriesChange
                }}
              />

              <Search
                {...{
                  searchStates,
                  onSearchStateChange: handleSearchChange,
                  onSearchItemRemove: handleSearchItemRemove,
                }}
              />

              <AddItemButton text="Add another paper" onClick={handleSearchItemAdd} />

              <div className="pt-4">
                <LoadingButton loading={isLoadingPapers} onClick={queryPapers}> Search!</LoadingButton>
              </div>

              <SuggestedCategories
                options={suggestedCategories.map((slug) => `${slug} (${CATEGORY_HUMAN_NAMES[slug as keyof typeof CATEGORY_HUMAN_NAMES]})`)}
                onClick={applySuggestedCategories}
              />
            </div>

          </div>
        </section>
        <div className="album py-5 bg-light">
          <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <p style={{ fontSize: 15 }}>
                <Tooltip title="Filtered paper count" arrow>
                  <em>{total} searchable arXiv papers</em>
                </Tooltip>
              </p>
              <div>
                <CopyToClipboardButton />
              </div>
            </div>

          </div>
          <div className="container">
            {papers && (
              <div className="row">
                {papers.map((paper) => (
                  <Card
                    {...{
                      key: paper.pk,
                      title: paper.title,
                      authors: paper.authors,
                      paperId: paper.paper_id,
                      numPapers: 15,
                      paperCat: paper.categories,
                      paperYear: paper.year,
                      categories,
                      years,
                      similarity_score: paper.similarity_score,
                      setState: setPapers,
                      setTotal,
                      matchExactCategories,
                    }}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
};
