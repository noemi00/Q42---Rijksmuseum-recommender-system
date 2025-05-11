import React, { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import Layout from "../Components/Layout";
import { Divider, notification, Button, Row, Col } from "antd";

import useToken from "../Components/Token";
import "../Styles/painting.css";

function Painting() {
  const { token } = useToken();
  let { id } = useParams();
  const [painting, setPainting] = useState({"painting": {
    "url": null,
    "description": null,
    "art_style": null,
    "title": null,
    "maker": null
  }});
  const [recommendations, setRecommendations] = useState([]);
  const [offset, setOffset] = useState(1);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }

    setRecommendations([]);

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/painting/" + id + "/", {
      method: "GET",
      headers: new Headers({
        Authorization: "Bearer " + token,
      }),
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((painting) => {
            setPainting(painting);
          });

          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while trying to fetch painting!",
        });
        console.log(error);
      });

    fetch(
      process.env.REACT_APP_FRONTEND_API_URL +
        "/painting/recommendations/" +
        id +
        "/",
      {
        method: "GET",
        headers: new Headers({
          Authorization: "Bearer " + token,
        }),
      }
    )
      .then((response) => {
        if (response.ok) {
          response.json().then((painting) => {
            setRecommendations(painting);
          });

          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while trying to fetch paintings recommendaitions!",
        });
        console.log(error);
      });
  }, [id, token, navigate]);

  function RefreshPaintings() {
    setRecommendations([]);
    RegisterRefresh(id);

    fetch(
      process.env.REACT_APP_FRONTEND_API_URL +
        "/painting/recommendations/" +
        id +
        "/?offset=" +
        offset,
      {
        method: "GET",
        headers: new Headers({
          Authorization: "Bearer " + token,
        }),
      }
    )
      .then((response) => {
        if (response.ok) {
          response.json().then((painting) => {
            setRecommendations(painting);
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

    setOffset(offset + 1);
  }

  function RegisterClick(painting_click, index) {
    let feature;

    if (painting.painting.color) {
        feature = index;
    } else if (index === 1) {
        feature = 0;
    } else {
        feature = index
    }
    
    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/users/click/", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        painting_id: painting_click.object_number,
        frontend_click: false,
        recommendation_feature: feature,
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

  function RegisterRefresh(id) {
    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/users/refresh/", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        frontpage: false,
        painting_id: id,
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
      <link
        href="https://unpkg.com/boxicons@2.1.1/css/boxicons.min.css"
        rel="stylesheet"
      ></link>
      <div className="painting_container">
        <Row>
            <Col span={6}>
            <img className="painting_image" src={painting.painting.url} alt="" />
        </Col>
        <Col span={18}>
            <Row className="title_text2">
                <p>{painting.painting.title}</p>
            </Row>
            <Row className="description_text">
                <p>{painting.painting.description}</p>
            </Row>
            <Row className="description_text">
                <p>{painting.painting.maker}</p>
            </Row>
            <Row className="description_text">
                <p>{painting.art_style}</p>
            </Row>
            <Row className="color_text">
                <Col span={1} style={{ "background-color": painting.painting.color }}>
                </Col>
                <Col>
                    <p><Divider type="vertical"/>{painting.painting.color}</p>
                </Col>
            </Row>
        </Col>
        </Row>

        <Divider />
        <Row className="recommendation_title">
          <Col span={21}>
            <h1>You may also like?</h1>
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
        <Row className="images">
          {recommendations.map((painting, index) => (
            <Link to={"/painting/" + painting.object_number}>
              <div
                key={index}
                className="image-box"
                data-name={"image" + index}
                onClick={() => RegisterClick(painting, index)}
              >
                <img
                  className="recommendation_image"
                  src={painting.url}
                  alt=""
                ></img>
                <h6>
                  {painting.title} - {painting.maker}
                </h6>
              </div>
            </Link>
          ))}
        </Row>
      </div>
    </Layout>
  );
}

export default Painting;
