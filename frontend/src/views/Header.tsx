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
  //  const inputHandler = (event: React.ChangeEvent<HTMLInputElement>) => {
  //    const enteredText = event.target.value;
  //    setText(enteredText);
  // };

  return (
    <header>
      <div style={{ background: "black", display: "flex", justifyContent: "space-between", alignItems: "center", padding: "25px" }}>
        <img
          src={BASE_URL + `/data/redis-logo.png`}
          alt="Redis Logo"
          style={{
            height: '15%',
            width: '15%',
          }}>
        </img>
        {/* <h1 style={{ color: "white" }}>arXiv Paper Search</h1> */}
        <a className="btn" style={{ color: "white" }}>Talk with us!</a>
      </div>

      {/* <Navbar expand="lg" bg="dark" variant="dark" style={{ padding: '25px' }} >
        <Container fluid>
          <Navbar.Brand style={{ marginRight: "-30rem" }} href="#">
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll" style={{top: "5px"}}>
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '175px'}}
            navbarScroll
          >
            <NavDropdown title="About" id="navbarScrollingDropdown">
              <NavDropdown.Item href="https://github.com/RedisVentures/redis-arXiv-search">Code</NavDropdown.Item>
              <NavDropdown.Item href="https://datasciencedojo.com/blog/ai-powered-document-search/">Blog</NavDropdown.Item>
              <NavDropdown.Item href="https://github.com/RedisVentures/redis-ai-resources">Redis AI Resources List</NavDropdown.Item>
              <NavDropdown.Item href="https://redis.com/vss-meeting/" target="_blank">Talk With Us</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/">
                Vector Search Docs
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Nav.Link className="btn btn-primary m-2" href="https://redis.com/vss-meeting/" target="_blank">
              Talk With Us!
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
          <Nav>
            <Nav.Link href="https://redis.com/vss-meeting/" target="_blank">
              Talk With Us!
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar> */}
    </header>
  );
};
