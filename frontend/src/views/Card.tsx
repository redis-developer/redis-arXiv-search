/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { getSemanticallySimilarPapers } from "../api"
import  useCheckMobileScreen  from "../mobile"
import { Chip } from '@material-ui/core';



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
        <p className="card-text">
            <em>{props.authors}</em>
        </p>
        <div className="d-flex justify-content-between align-items-center">
         <div className="btn-group">
          <button
           type="button"
           className="btn btn-sm btn-outline-secondary"
           onClick={() => querySemanticallySimilarPapers()}
          >
           More Like This
          </button>
          <Chip
            style={{ margin: "auto 20px" }}
            label={`${props.categories}`}
            variant='outlined'
            color='primary'
          />
         </div>
        </div>
       </div>
      </div>
     </div>
    );
   };