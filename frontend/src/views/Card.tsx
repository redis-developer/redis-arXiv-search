/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { getSemanticallySimilarPapers } from "../api"
import  useCheckMobileScreen  from "../mobile"
import { Chip } from '@material-ui/core';
import Tooltip from '@mui/material/Tooltip';


interface Props {
    paperId: string;
    numPapers: number;
    title: string;
    authors: string;
    categories: string;
    setState: (state: any) => void;
}


export const Card = (props: Props) => {

    const isMobile = useCheckMobileScreen();

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
        return '20%';
      }
    }

    return (
     <div className="col-md-2" style={{width: getCardSize()}}>
      <div className="card mb-2 box-shadow" style={{alignContent : 'center'}}>
       <div className="card-body">
        <p className="card-text">
          <strong>{props.title}</strong>
        </p>
        <div className="d-flex justify-content-between align-items-left">
         <div className="btn-group" style={{width: "100%"}}>

          <p className="card-text" style={{fontSize : 12, width: "50%", float: "left"}}>
            <a href={`https://arxiv.org/abs/${props.paperId}`} target="_blank">Read Me</a> 
          </p>
          <p className="card-text" style={{fontSize : 12, width: "50%", float: "right"}}>
            <a href={`https://arxiv.org/pdf/${props.paperId}`} target="_blank">Download</a> 
          </p>
          </div>
        </div>
        <p className="card-text" style={{fontSize : 12}}>
            <em>{props.authors}</em>
        </p>
        <div className="d-flex justify-content-between align-items-center">
         <div className="btn-group">
         <Tooltip title="Search for more papers like this one">
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary"
            onClick={() => querySemanticallySimilarPapers()}
            >
            More Like This
            </button>
         </Tooltip>

          {/* <Chip
            style={{ margin: "auto 20px" }}
            label={`${props.categories}`}
            color='primary'
            size="small"
          /> */}
         </div>
        </div>
       </div>
      </div>
     </div>
    );
   };