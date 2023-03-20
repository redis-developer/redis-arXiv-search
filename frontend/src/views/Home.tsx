import { useState, useEffect } from 'react';
import { getPapers, getSemanticallySimilarPapersbyText } from '../api';
import { Card } from "./Card"
import SearchBar from "material-ui-search-bar";


import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import ListItemText from '@mui/material/ListItemText';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import Tooltip from '@mui/material/Tooltip';

/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface Props {}

export const Home = (props: Props) => {
  const [error, setError] = useState<string>('');
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(15);
  const [papers, setPapers] = useState<any[]>([]);
  const [years, setYears] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [provider, setProvider] = useState<string>('huggingface');
  const [searchState, setSearchState] = useState<string>('');
  const [total, setTotal] = useState<number>(0);

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

  function EmbeddingModelOptions() {
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setProvider((event.target as HTMLInputElement).value);
    };
    return (
      <FormControl>
        <FormLabel id="demo-row-radio-buttons-group-label">Embedding Model</FormLabel>
        <RadioGroup
          row
          aria-labelledby="demo-controlled-radio-buttons-group"
          name="controlled-radio-buttons-group"
          value={provider}
          onChange={handleChange}
        >
          <FormControlLabel value="huggingface" control={<Radio />} label="HuggingFace" />
          <FormControlLabel value="openai" control={<Radio />} label="OpenAI" />
          <FormControlLabel value="cohere" control={<Radio />} label="Cohere"/>
        </RadioGroup>
      </FormControl>
    );
  }

  function YearOptions() {
    const handleChange = (event: SelectChangeEvent<typeof years>) => {
      const {
        target: { value },
      } = event;
      setYears(
        // On autofill we get a stringified value.
        typeof value === 'string' ? value.split(',') : value,
      );
      setSkip(0);
      console.log(years)
    };
    return (
        <FormControl sx={{ m: 1, width: 150 }}>
          <InputLabel id="demo-multiple-checkbox-label">Year</InputLabel>
          <Select
            labelId="demo-multiple-checkbox-label"
            id="demo-multiple-checkbox"
            multiple
            value={years}
            onChange={handleChange}
            input={<OutlinedInput label="Tag" />}
            renderValue={(selected) => selected.join(', ')}
            MenuProps={MenuProps}
          >
            {yearOptions.map((year) => (
              <MenuItem key={year} value={year}>
                <Checkbox checked={years.indexOf(year) > -1} />
                <ListItemText primary={year} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
    );
  }

  function CategoryOptions() {
    const handleChange = (event: SelectChangeEvent<typeof years>) => {
      const {
        target: { value },
      } = event;
      setCategories(
        // On autofill we get a stringified value.
        typeof value === 'string' ? value.split(',') : value,
      );
      setSkip(0);
      console.log(years)
    };
    return (
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">Category</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={categories}
          onChange={handleChange}
          input={<OutlinedInput label="Category" />}
          renderValue={(selected) => selected.join(', ')}
          MenuProps={MenuProps}
        >
          {categoryOptions.map((cat) => (
            <MenuItem key={cat} value={cat}>
              <Checkbox checked={categories.indexOf(cat) > -1} />
              <ListItemText primary={cat} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    );
  }

  const handleSearchChange = async (newValue: string) => {
    setSearchState(newValue);
  }

  const queryPapers = async () => {
    try {
      if ( searchState ) {
        const result = await getSemanticallySimilarPapersbyText(searchState, years, categories, provider)
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
    }
  };

  // Execute this one when the component loads up
  useEffect(() => {
    setPapers([]);
    setCategories([]);
    setYears([]);
    queryPapers();
  }, []);

  return (
    <>
      <main role="main">
      <section className="jumbotron text-center mb-0 bg-white" style={{ paddingTop: '40px', width: "95%"}}>
      <div className="container">
       <h1 className="jumbotron-heading">arXiv Paper Search</h1>
       <p className="lead text-muted">
           Redis is a real-time data platform that functions as a vector database, ML feature store, and low-latency data serving layer.
       </p>
       <p className="lead text-muted">
           <strong>Search with natural language (and other settings or filters) to discover <a href="https://arxiv.org/" target="_blank">arXiv</a> scholarly papers:</strong>
       </p>
       <div className="container">
        <SearchBar
          placeholder='Search'
          value={searchState}
          onChange={(newValue) => handleSearchChange(newValue)}
          onRequestSearch={() => queryPapers()}
          style={{
            margin: '20px 0',
          }}
        />
       </div>
       <div>
        <EmbeddingModelOptions></EmbeddingModelOptions>
        <YearOptions></YearOptions>
        <CategoryOptions></CategoryOptions>
    </div>
      </div>
     </section>
      <div className="album py-5 bg-light">
        <div className="container">
          <p style={{fontSize: 15}}>
            <Tooltip title="Filtered paper count" arrow>
              <em>{total} searchable arXiv papers</em>
            </Tooltip>
          </p>
        </div>
        <div className="container">
          {papers && (
            <div className="row">
              {papers.map((paper) => (
                 <Card
                  title={paper.title}
                  authors={paper.authors}
                  paperId={paper.paper_id}
                  numPapers={15}
                  paperCat={paper.categories}
                  paperYear={paper.year}
                  categories={categories}
                  years={years}
                  provider={provider}
                  similarity_score={paper.similarity_score}
                  setState={setPapers}
                  setTotal={setTotal}
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