/* eslint-disable jsx-a11y/anchor-is-valid */
import { getSemanticallySimilarPapers } from "../api"
import Tooltip from '@mui/material/Tooltip';
import '../styles/Card.css'

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
    <div className="card">
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
      <div className="card-top">
        <Tooltip title="Search for more papers like this one">
          <button
            type="button"
            className="card-btn"
            onClick={() => querySemanticallySimilarPapers()}
          >
            More Like This
          </button>
        </Tooltip>
        <div className="card-btns-space"></div>
        <a href={`https://arxiv.org/pdf/${props.paperId}`} rel="noreferrer">
          <button
            type="button"
            className="card-btn"
          >Download
          </button>
        </a>
      </div>
    </div>
  );
};