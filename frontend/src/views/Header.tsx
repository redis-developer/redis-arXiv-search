import React, { useState } from 'react';
import { Navbar, Container, NavDropdown, Nav } from 'react-bootstrap';
import { BASE_URL } from "../config";
import { useNavigate } from 'react-router-dom';

interface Props {
}


/* eslint-disable jsx-a11y/anchor-is-valid */
export const Header = (props: Props) => {
  const [searchText, setText] = useState("");
  const Navigate = useNavigate();

   // This function is called when the input changes
   const inputHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
     const enteredText = event.target.value;
     setText(enteredText);
  };

  return (
   <header>
    <Navbar expand="lg" bg="dark" variant="dark" style={{ padding: '25px'}} >
      <Container fluid>
        <Navbar.Brand style={{marginRight: "-30rem"}} href="#">
            <img
              src={BASE_URL + `/data/redis-logo.png`}
              alt="Redis Logo"
              style={{
                height: '7%',
                width: '7%',
                paddingRight: '10px',
                }}>
            </img>
          Redis Vector Search Demo
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll" style={{top: "5px"}}>
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '175px'}}
            navbarScroll
          >
            <NavDropdown title="About" id="navbarScrollingDropdown">
              <NavDropdown.Item href="https://github.com/Spartee/redis-vector-search">Code</NavDropdown.Item>
              <NavDropdown.Item href="https://mlops.community/vector-similarity-search-from-basics-to-production/">Blog</NavDropdown.Item>
              <NavDropdown.Item href="https://forms.gle/ANpHTe2Da5CVGHty7" target="_blank">Talk With Us</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="https://redis.io/docs/stack/search/reference/vectors/">
                Docs: Redis Vector Search
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Nav.Link className="btn btn-primary m-2" href="https://forms.gle/ANpHTe2Da5CVGHty7" target="_blank">
              Talk With Us!
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
   </header>
  );
 };
