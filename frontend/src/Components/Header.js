import React from "react";

import { Divider, Row, Col, notification } from "antd";
import { Link, useNavigate } from "react-router-dom";

import "../Styles/header.css";
import useToken from "./Token";

function Header() {
  const navigate = useNavigate();
  const { token } = useToken();

  function Logout() {
    if (!token) {
      return;
    }

    sessionStorage.removeItem("access_token");
    navigate("/login");
    notification.info({
      message: "You have been logged out!",
    });
  }

  return (
    <div className="title_container">
      <Row>
        <Col>
          <Link className="title_link" to="/">
            <h1 className="title">Rijksstudio</h1>
          </Link>
        </Col>
        <Col>
          <Link className="title_link" to="/login">
            <h1 className="title">Login</h1>
          </Link>
        </Col>
        <Col>
          <button className="logout_link" onClick={() => Logout()}>
            <h1 className="title">Logout</h1>
          </button>
        </Col>
      </Row>
      <Divider className="title_divider" />
    </div>
  );
}

export default Header;
