/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { getSemanticallySimilarPapers } from "../api"
import  useCheckMobileScreen  from "../mobile"
import Tooltip from '@mui/material/Tooltip';
import { makeStyles } from '@material-ui/core/styles';
import { useNavigate } from 'react-router';

interface Props {
    paperId: string;
    numPapers: number;
    title: string;
    authors: string;
    categories: string;
    setState: (state: any) => void;
}


const useStyles = makeStyles((theme) => ({
  btnGroup: {
    display: "float",
    position: "relative",
    left: "75%"
  },
  btnGroupMobile: {
    paddingTop: "5%",
    display: "float",
  },
  cardText: {
    display: "grid",
    fontSize: "14px"
  }
}));

export const Card = (props: Props) => {
    const classes = useStyles();
    const isMobile = useCheckMobileScreen();
    const navigate = useNavigate();

    const querySemanticallySimilarPapers = async () => {
        try {
          console.log(props.paperId);
          const productJson = await getSemanticallySimilarPapers(
              props.paperId,
              "KNN",
              props.numPapers);
          props.setState(productJson)
        } catch (err) {
          console.log(String(err));
        }
      };

    const getCardSize = () => {
      if (isMobile) {
        return '50%';
      }
      else {
        return '85%';
      }
    }
    const getCardClass = () => {
      if (isMobile) {
        return classes.btnGroupMobile;
      }
      else {
        return classes.btnGroup;
      }
    }
    const getButtonSpacing = () => {
      if (isMobile) {
        return {margin: "0px"}
      }
      else {
        return {margin: "5px"}
      }
    }

    return (
     <div className="col-md-2" style={{width: getCardSize()}}>
      <div className="card mb-2 border-dark box-shadow">
       <div className="card-body">
          <p className="card-text">
            <a href={`https://arxiv.org/abs/${props.paperId}`}>
              <strong>{props.title}</strong>
            </a>
          </p>
          <div className={classes.cardText}>
              <strong>Authors:</strong> <em>{props.authors}</em>
              <strong>Categories:</strong> <em>{props.categories}</em>
          </div>

         <div className={getCardClass()}>
              <Tooltip title="Search for more papers like this one">
                <button
                  type="button"
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => querySemanticallySimilarPapers()}
                  >
                  More Like This
                  </button>
              </Tooltip>
              <a href={`https://arxiv.org/pdf/${props.paperId}`} rel="noreferrer">
                <button
                  type="button"
                  style={getButtonSpacing()}
                  className="btn btn-sm btn-outline-secondary"
                  >Download
                </button>
              </a>
         </div>
       </div>
      </div>
     </div>
    );
   };