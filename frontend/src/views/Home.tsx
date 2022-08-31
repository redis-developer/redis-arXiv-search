import React, { useState, useEffect } from 'react';
import { getPapers, getSemanticallySimilarPapersbyText } from '../api';
import { useNavigate } from 'react-router-dom';
import { Card } from "./Card"
import SearchBar from "material-ui-search-bar";

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {
  papers: any[];
  setPapers: (state: any) => void;
  category: string;
  setCategory: (state: any) => void;

}

export const Home = (props: Props) => {
  const [error, setError] = useState<string>('');
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(15);
  const Navigate = useNavigate();

  var state = {value: ''};

  const handleChange = async (newValue: string) => {
    state.value = newValue;
    console.log(state);
  }

  const queryPapers = async () => {
    try {
      // clear filters
      props.setCategory("");

      if ( state.value ) {
        const paperJson = await getSemanticallySimilarPapersbyText(state.value)
        props.setPapers(paperJson)
      } else {
        setSkip(skip + limit);
        const paperJson = await getPapers(limit, skip);
        props.setPapers(paperJson)
      }

    } catch (err) {
      setError(String(err));
    }
  };

  // Execute this one when the component loads up
  useEffect(() => {
    queryPapers();
  }, []);

  return (
    <>
      <main role="main">
      <section className="jumbotron text-center mb-0 bg-white" style={{ paddingTop: '40px'}}>
      <div className="container">
       <h1 className="jumbotron-heading">arXiv Paper Search</h1>
       <p className="lead text-muted">
           This demo uses the built in Vector Search capabilities of Redis Enterprise
           to show how unstructured data, such as paper abstracts (text), can be used to create a powerful
           search engine.
       </p>
       <p className="lead text-muted">
           <strong>Enter a search query below to discover scholarly papers hosted by <a href="https://arxiv.org/" target="_blank">arXiv</a> (Cornel University).</strong>
       </p>
       <div className="container">
        <SearchBar
          placeholder='Search'
          value={state.value}
          onChange={(newValue) => handleChange(newValue)}
          onRequestSearch={() => queryPapers()}
          style={{
            margin: '20px 0',
          }}
        />
       </div>
      </div>
     </section>
      <div className="album py-5 bg-light">
        <div className="container">
          {props.papers && (
            <div className="row">
              {props.papers.map((paper) => (
                 <Card
                  key={paper.pk}
                  title={paper.title}
                  authors={paper.authors}
                  paperId={paper.paper_id}
                  numPapers={15}
                  categories={paper.categories}
                  setState={props.setPapers}
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