/* eslint-disable jsx-a11y/anchor-is-valid */
import { getSemanticallySimilarPapers } from "../api"
import useCheckMobileScreen from "../mobile"
import Tooltip from '@mui/material/Tooltip';
import Chip from '@mui/material/Chip';
// import '../styles/Card.css'
import { makeStyles } from '@material-ui/core/styles';
import { useNavigate } from 'react-router';

interface Props {
  paperId: string;
  numPapers: number;
  title: string;
  authors: string;
  paperCat: string;
  paperYear: number;
  categories: string[];
  years: string[];
  provider: string;
  similarity_score: number;
  setState: (state: any) => void;
  setTotal: (state: any) => void;
}

export const Card = (props: Props) => {
  const querySemanticallySimilarPapers = async () => {
    try {
      const results = await getSemanticallySimilarPapers(
        props.paperId,
        props.years,
        props.categories,
        props.provider,
        "KNN",
        props.numPapers);
      props.setState(results.papers)
      props.setTotal(results.total)
    } catch (err) {
      console.log(String(err));
    }
  };

  return (
    <div style={{ border: "1px solid black", padding: "1rem", margin: "1rem", width: "30rem" }}>
      <a href={`https://arxiv.org/abs/${props.paperId}`}>
        <strong>{props.title}</strong>
      </a>
      <div>
        <div><strong>Authors:</strong> <em>{props.authors}</em></div>
        <div><strong>Categories:</strong> <em>{props.paperCat.replaceAll("|", ", ")}</em></div>
        <div><strong>Year:</strong> <em>{props.paperYear}</em></div>
        <div>
          {props.similarity_score ? (<div><strong>Vector search similarity score:</strong> <em>{props.similarity_score.toFixed(2)}</em></div>) : <></>}
        </div>
      </div>
      <div style={{ paddingTop: "1rem" }}>
        <Tooltip title="Search for more papers like this one">
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary"
            onClick={() => querySemanticallySimilarPapers()}
          >
            More Like This
          </button>
        </Tooltip>
        <div style={{ width: "0.5rem", display: "inline-block" }}></div>
        <a href={`https://arxiv.org/pdf/${props.paperId}`} rel="noreferrer">
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary"
          >Download
          </button>
        </a>
      </div>
    </div>
  );
};