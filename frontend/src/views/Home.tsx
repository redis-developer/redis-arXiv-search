import { useState, useEffect } from 'react';
import { getPapers, getSemanticallySimilarPapersbyText } from '../api';
import { Card } from "./Card"
import SearchBar from "material-ui-search-bar";


import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import Tooltip from '@mui/material/Tooltip';

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {
  papers: any[];
  setPapers: (state: any) => void;
  categories: string[];
  setCategories: (state: any) => void;
  years: string[];
  setYears: (state: any) => void;
  searchState: string;
  setSearchState: (state: any) => void;
  total: number;
  setTotal: (state: any) => void;
}

export const Home = (props: Props) => {
  const [error, setError] = useState<string>('');
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(15);

  const ITEM_HEIGHT = 48;
  const ITEM_PADDING_TOP = 8;
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        width: 150,
      },
    },
  };

  const yearOptions = [
    '2022',
    '2021',
    '2020',
    '2019',
    '2018',
    '2017',
    '2016',
    '2015',
    '2014',
    '2013',
    '2012',
    '2011'
  ];

  const categoryOptions = [
    'cs.LG',
    'math-ph',
    'quant-ph',
    'cond-mat.mes-hall',
    'hep-ph',
    'hep-th',
    'gr-qc',
    'cond-mat.mtrl-sci',
    'cond-mat.str-el',
    'cond-mat.stat-mech',
    'astro-ph.CO',
    'math.MP',
    'astro-ph.HE',
    'physics.optics',
    'astro-ph.GA'
  ]

  const handleSearchChange = async (newValue: string) => {
    props.setSearchState(newValue);
  }

  const handleYearSelection = (event: SelectChangeEvent<typeof props.years>) => {
    const {
      target: { value },
    } = event;
    props.setYears(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
    setSkip(0);
    console.log(props.years)
  };

  const handleCatSelection = (event: SelectChangeEvent<typeof props.categories>) => {
    const {
      target: { value },
    } = event;
    props.setCategories(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
    setSkip(0);
  };

  const queryPapers = async () => {
    try {
      if ( props.searchState ) {
        const result = await getSemanticallySimilarPapersbyText(props.searchState, props.years, props.categories)
        props.setPapers(result.papers)
        props.setTotal(result.total)
      } else {
        setSkip(skip + limit);
        const result = await getPapers(limit, skip, props.years, props.categories);
        props.setPapers(result.papers)
        props.setTotal(result.total)
      }
    } catch (err) {
      setError(String(err));
    }
  };

  // Execute this one when the component loads up
  useEffect(() => {
    props.setPapers([]);
    props.setCategories([]);
    props.setYears([]);
    queryPapers();
  }, []);

  return (
    <>
      <main role="main">
      <section className="jumbotron text-center mb-0 bg-white" style={{ paddingTop: '40px', width: "95%"}}>
      <div className="container">
       <h1 className="jumbotron-heading">arXiv Paper Search</h1>
       <p className="lead text-muted">
           This demo uses the built in Vector Search capabilities of Redis Enterprise
           to show how unstructured data, such as paper abstracts (text), can be used to create a powerful
           search engine.
       </p>
       <p className="lead text-muted">
           <strong>Enter a search query below to discover scholarly papers hosted by <a href="https://arxiv.org/" target="_blank">arXiv</a> (Cornell University).</strong>
       </p>
       <div className="container">
        <SearchBar
          placeholder='Search'
          value={props.searchState}
          onChange={(newValue) => handleSearchChange(newValue)}
          onRequestSearch={() => queryPapers()}
          style={{
            margin: '20px 0',
          }}
        />
       </div>
       <div>
        <FormControl sx={{ m: 1, width: 150 }}>
          <InputLabel id="demo-multiple-checkbox-label">Year</InputLabel>
          <Select
            labelId="demo-multiple-checkbox-label"
            id="demo-multiple-checkbox"
            multiple
            value={props.years}
            onChange={handleYearSelection}
            input={<OutlinedInput label="Tag" />}
            renderValue={(selected) => selected.join(', ')}
            MenuProps={MenuProps}
          >
            {yearOptions.map((year) => (
              <MenuItem key={year} value={year}>
                <Checkbox checked={props.years.indexOf(year) > -1} />
                <ListItemText primary={year} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, width: 300 }}>
          <InputLabel id="demo-multiple-checkbox-label">Category</InputLabel>
          <Select
            labelId="demo-multiple-checkbox-label"
            id="demo-multiple-checkbox"
            multiple
            value={props.categories}
            onChange={handleCatSelection}
            input={<OutlinedInput label="Category" />}
            renderValue={(selected) => selected.join(', ')}
            MenuProps={MenuProps}
          >
            {categoryOptions.map((cat) => (
              <MenuItem key={cat} value={cat}>
                <Checkbox checked={props.categories.indexOf(cat) > -1} />
                <ListItemText primary={cat} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
    </div>
      </div>
     </section>
      <div className="album py-5 bg-light">
        <div className="container">
          <p style={{fontSize: 15}}>
            <Tooltip title="Filtered paper count" arrow>
              <em>{props.total} searchable arXiv papers</em>
            </Tooltip>
          </p>
        </div>
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
                  paperCat={paper.categories}
                  paperYear={paper.year}
                  categories={props.categories}
                  years={props.years}
                  similarity_score={paper.similarity_score}
                  setState={props.setPapers}
                  setTotal={props.setTotal}
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