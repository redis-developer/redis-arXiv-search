import { BASE_URL } from "../config";
import '../styles/Header.css';


/* eslint-disable jsx-a11y/anchor-is-valid */
export const Header = () => {
  return (
    <header>
      <div className="header">
        <img
          src={BASE_URL + `/data/redis-logo.png`}
          alt="Redis Logo"
          className="header-logo">
        </img>
        <div>
          <a href='https://x.com/Redisinc'>
            <img
              src={"x-logo.svg"}
              className="header-icon-link"
            ></img>
          </a>
          <a href='https://github.com/redis-developer/redis-arXiv-search'>
            <img
              src={"github-mark-white.svg"}
              className="header-icon-link"
            ></img>
          </a>
          <a className="btn header-cta">Talk with us!</a>
        </div>
      </div>
    </header>
  );
};
