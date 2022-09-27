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

  // const categoryOptions: any = {
  //   'cs.AI': 'Artificial Intelligence',
  //   'cs.AR': 'Hardware Architecture',
  //   'cs.CC': 'Computational Complexity',
  //   'cs.CE': 'Computational Engineering, Finance, and Science',
  //   'cs.CG': 'Computational Geometry',
  //   'cs.CL': 'Computation and Language',
  //   'cs.CR': 'Cryptography and Security',
  //   'cs.CV': 'Computer Vision and Pattern Recognition',
  //   'cs.CY': 'Computers and Society',
  //   'cs.DB': 'Databases',
  //   'cs.DC': 'Distributed, Parallel, and Cluster Computing',
  //   'cs.DL': 'Digital Libraries',
  //   'cs.DM': 'Discrete Mathematics',
  //   'cs.DS': 'Data Structures and Algorithms',
  //   'cs.ET': 'Emerging Technologies',
  //   'cs.FL': 'Formal Languages and Automata Theory',
  //   'cs.GL': 'General Literature',
  //   'cs.GR': 'Graphics',
  //   'cs.GT': 'Computer Science and Game Theory',
  //   'cs.HC': 'Human-Computer Interaction',
  //   'cs.IR': 'Information Retrieval',
  //   'cs.IT': 'Information Theory',
  //   'cs.LG': 'Machine Learning',
  //   'cs.LO': 'Logic in Computer Science',
  //   'cs.MA': 'Multiagent Systems',
  //   'cs.MM': 'Multimedia',
  //   'cs.MS': 'Mathematical Software',
  //   'cs.NA': 'Numerical Analysis',
  //   'cs.NE': 'Neural and Evolutionary Computing',
  //   'cs.NI': 'Networking and Internet Architecture',
  //   'cs.OH': 'Other Computer Science',
  //   'cs.OS': 'Operating Systems',
  //   'cs.PF': 'Performance',
  //   'cs.PL': 'Programming Languages',
  //   'cs.RO': 'Robotics',
  //   'cs.SC': 'Symbolic Computation',
  //   'cs.SD': 'Sound',
  //   'cs.SE': 'Software Engineering',
  //   'cs.SI': 'Social and Information Networks',
  //   'cs.SY': 'Systems and Control',
  //   'econ.EM': 'Econometrics',
  //   'eess.AS': 'Audio and Speech Processing',
  //   'eess.IV': 'Image and Video Processing',
  //   'eess.SP': 'Signal Processing',
  //   'gr-qc': 'General Relativity and Quantum Cosmology',
  //   'hep-ex': 'High Energy Physics - Experiment',
  //   'hep-lat': 'High Energy Physics - Lattice',
  //   'hep-ph': 'High Energy Physics - Phenomenology',
  //   'hep-th': 'High Energy Physics - Theory',
  //   'math.AC': 'Commutative Algebra',
  //   'math.AG': 'Algebraic Geometry',
  //   'math.AP': 'Analysis of PDEs',
  //   'math.AT': 'Algebraic Topology',
  //   'math.CA': 'Classical Analysis and ODEs',
  //   'math.CO': 'Combinatorics',
  //   'math.CT': 'Category Theory',
  //   'math.CV': 'Complex Variables',
  //   'math.DG': 'Differential Geometry',
  //   'math.DS': 'Dynamical Systems',
  //   'math.FA': 'Functional Analysis',
  //   'math.GM': 'General Mathematics',
  //   'math.GN': 'General Topology',
  //   'math.GR': 'Group Theory',
  //   'math.GT': 'Geometric Topology',
  //   'math.HO': 'History and Overview',
  //   'math.IT': 'Information Theory',
  //   'math.KT': 'K-Theory and Homology',
  //   'math.LO': 'Logic',
  //   'math.MG': 'Metric Geometry',
  //   'math.MP': 'Mathematical Physics',
  //   'math.NA': 'Numerical Analysis',
  //   'math.NT': 'Number Theory',
  //   'math.OA': 'Operator Algebras',
  //   'math.OC': 'Optimization and Control',
  //   'math.PR': 'Probability',
  //   'math.QA': 'Quantum Algebra',
  //   'math.RA': 'Rings and Algebras',
  //   'math.RT': 'Representation Theory',
  //   'math.SG': 'Symplectic Geometry',
  //   'math.SP': 'Spectral Theory',
  //   'math.ST': 'Statistics Theory',
  //   'math-ph': 'Mathematical Physics',
  //   'nlin.AO': 'Adaptation and Self-Organizing Systems',
  //   'nlin.CD': 'Chaotic Dynamics',
  //   'nlin.CG': 'Cellular Automata and Lattice Gases',
  //   'nlin.PS': 'Pattern Formation and Solitons',
  //   'nlin.SI': 'Exactly Solvable and Integrable Systems',
  //   'nucl-ex': 'Nuclear Experiment',
  //   'nucl-th': 'Nuclear Theory',
  //   'physics.acc-ph': 'Accelerator Physics',
  //   'physics.ao-ph': 'Atmospheric and Oceanic Physics',
  //   'physics.app-ph': 'Applied Physics',
  //   'physics.atm-clus': 'Atomic and Molecular Clusters',
  //   'physics.atom-ph': 'Atomic Physics',
  //   'physics.bio-ph': 'Biological Physics',
  //   'physics.chem-ph': 'Chemical Physics',
  //   'physics.class-ph': 'Classical Physics',
  //   'physics.comp-ph': 'Computational Physics',
  //   'physics.data-an': 'Data Analysis, Statistics and Probability',
  //   'physics.ed-ph': 'Physics Education',
  //   'physics.flu-dyn': 'Fluid Dynamics',
  //   'physics.gen-ph': 'General Physics',
  //   'physics.geo-ph': 'Geophysics',
  //   'physics.hist-ph': 'History and Philosophy of Physics',
  //   'physics.ins-det': 'Instrumentation and Detectors',
  //   'physics.med-ph': 'Medical Physics',
  //   'physics.optics': 'Optics',
  //   'physics.plasm-ph': 'Plasma Physics',
  //   'physics.pop-ph': 'Popular Physics',
  //   'physics.soc-ph': 'Physics and Society',
  //   'physics.space-ph': 'Space Physics',
  //   'q-bio.BM': 'Biomolecules',
  //   'q-bio.CB': 'Cell Behavior',
  //   'q-bio.GN': 'Genomics',
  //   'q-bio.MN': 'Molecular Networks',
  //   'q-bio.NC': 'Neurons and Cognition',
  //   'q-bio.OT': 'Other Quantitative Biology',
  //   'q-bio.PE': 'Populations and Evolution',
  //   'q-bio.QM': 'Quantitative Methods',
  //   'q-bio.SC': 'Subcellular Processes',
  //   'q-bio.TO': 'Tissues and Organs',
  //   'q-fin.CP': 'Computational Finance',
  //   'q-fin.EC': 'Economics',
  //   'q-fin.GN': 'General Finance',
  //   'q-fin.MF': 'Mathematical Finance',
  //   'q-fin.PM': 'Portfolio Management',
  //   'q-fin.PR': 'Pricing of Securities',
  //   'q-fin.RM': 'Risk Management',
  //   'q-fin.ST': 'Statistical Finance',
  //   'q-fin.TR': 'Trading and Market Microstructure',
  //   'quant-ph': 'Quantum Physics',
  //   'stat.AP': 'Applications',
  //   'stat.CO': 'Computation',
  //   'stat.ME': 'Methodology',
  //   'stat.ML': 'Machine Learning',
  //   'stat.OT': 'Other Statistics',
  //   'stat.TH': 'Statistics Theory'
  // };


  const handleSearchChange = async (newValue: string) => {
    props.setSearchState(newValue);
    console.log(props.searchState);
  }

  const handleYearSelection = (event: SelectChangeEvent<typeof props.years>) => {
    const {
      target: { value },
    } = event;
    props.setYears(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',') : value,
    );
    console.log(props.years)
  };

  // const handleCatSelection = (event: SelectChangeEvent<typeof props.categories>) => {
  //   const {
  //     target: { value },
  //   } = event;
  //   props.setCategories(
  //     // On autofill we get a stringified value.
  //     typeof value === 'string' ? value.split(',') : value,
  //   );
  // };

  const queryPapers = async () => {
    try {
      // const categories = props.categories.map((cat: string) => categoryOptions[cat])
      // console.log(categories)
      console.log(props.searchState)

      if ( props.searchState ) {
        const paperJson = await getSemanticallySimilarPapersbyText(props.searchState, props.years, props.categories)
        props.setPapers(paperJson)
        console.log(props.searchState)
      } else {
        setSkip(skip + limit);
        const paperJson = await getPapers(limit, skip, props.years, props.categories);
        props.setPapers(paperJson)
        console.log(props.searchState)
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
        {/* <FormControl sx={{ m: 1, width: 300 }}>
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
            {Object.values(categoryOptions).map((cat) => (
              <MenuItem key={cat} value={cat}>
                <Checkbox checked={props.categories.indexOf(cat) > -1} />
                <ListItemText primary={cat} />
              </MenuItem>
            ))}
          </Select>
        </FormControl> */}
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
                  paperCat={paper.categories}
                  paperYear={paper.year}
                  categories={props.categories}
                  years={props.years}
                  similarity_score={paper.similarity_score}
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