import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Layout from "../Components/Layout";
import { Button, Col, notification, Row } from "antd";

import useToken from "../Components/Token";
import "../Styles/index.css";

function Index() {
  const { token } = useToken();
  const [images, setImages] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }

    fetch(
      process.env.REACT_APP_FRONTEND_API_URL + "/users/paintings/overview/",
      {
        method: "GET",
        headers: new Headers({
          Authorization: "Bearer " + token,
        }),
      }
    )
      .then((response) => {
        if (response.ok) {
          response.json().then((paintings) => {
            setImages(paintings);
          });

          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        if (token) {
          notification.error({
            message: "Error while trying to fetch paintings!",
          });
        }
        console.log(error);
      });

      console.log(images)
  }, [token, navigate]);

  function RefreshPaintings() {
    setImages([]);
    fetch(
      process.env.REACT_APP_FRONTEND_API_URL + "/users/paintings/overview/",
      {
        method: "GET",
        headers: new Headers({
          Authorization: "Bearer " + token,
        }),
      }
    )
      .then((response) => {
        if (response.ok) {
          response.json().then((paintings) => {
            setImages(paintings);
            RegisterRefresh();
          });
          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while trying to fetch paintings!",
        });
        console.log(error);
      });
  }

  function RegisterClick(object_number) {
    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/users/click/", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        painting_id: object_number,
        frontend_click: true,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while registering click!",
        });
        console.log(error);
      });
  }

  function RegisterRefresh() {
    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/users/refresh/", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        frontpage: true,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while registering click!",
        });
        console.log(error);
      });
  }

  return (
    <Layout>
      <Row class="title_text">
        <Col span={21}>
          <h1>What are you looking for?</h1>
        </Col>
        <Col span={3}>
          <Button
            className="submit_button refresh_button"
            type="submit"
            onClick={() => RefreshPaintings()}
          >
            Refresh overview
          </Button>
        </Col>
      </Row>
      <link
        href="https://unpkg.com/boxicons@2.1.1/css/boxicons.min.css"
        rel="stylesheet"
      ></link>

      <div className="images">
        {images.map((painting, index) => (
          <Link to={"/painting/" + painting.object_number}>
            <div
              key={index}
              className="image-box"
              data-name={"image" + index}
              onClick={() => RegisterClick(painting.object_number)}
            >
              <img src={painting.url} alt=""></img>
              <h6>
                {painting.title} - {painting.maker}
              </h6>
            </div>
          </Link>
        ))}
      </div>
    </Layout>
  );
}

export default Index;
