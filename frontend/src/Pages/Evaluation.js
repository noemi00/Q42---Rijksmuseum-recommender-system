import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Divider,
  Radio,
  notification,
  Row,
  Col,
  Modal,
  Select,
  Form,
} from "antd";

import useToken from "../Components/Token";
import "../Styles/evaluation.css";

function Evaluation() {
  const { token } = useToken();
  const [painting, setPainting] = useState({"painting": {
    "url": null,
    "description": null,
    "art_style": null,
    "title": null,
    "maker": null
  }});
  const [recommendations, setRecommendations] = useState([]);
  const navigate = useNavigate();
  const form = Form.useForm()[0];
  const features = [
    "Art style",
    "Color",
    "Description",
    "Visual similarity",
    "Combination"
  ]

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }

    setRecommendations([]);

    fetchRecommendations();
  }, [token, navigate]);

  async function fetchRecommendations() {
    await fetch(process.env.REACT_APP_FRONTEND_API_URL + "/evaluation/total/", {
        method: "GET",
        headers: new Headers({
          Authorization: "Bearer " + token,
        }),
      })
      .then((response) => {
        if (response.ok) {
          response.json().then(data => {
            if (data) {
                notification.info({
                    message: "evaluation complete thank you!"
                })
                navigate("/")
            }
          })
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


    setRecommendations([])
    setPainting({"painting": {
        "url": null,
        "description": null,
        "art_style": null,
        "title": null,
        "maker": null
      }})

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/painting/random/get/", {
      method: "GET",
      headers: new Headers({
        Authorization: "Bearer " + token,
      }),
    })
      .then((response) => {
        if (response.ok) {
          response.json().then((random_painting) => {
            fetch(
              process.env.REACT_APP_FRONTEND_API_URL +
                "/painting/" +
                random_painting.painting.object_number +
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
                    setPainting(painting);
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

            fetch(
              process.env.REACT_APP_FRONTEND_API_URL +
                "/painting/recommendations/" +
                random_painting.painting.object_number +
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
                  message: "Error while trying to fetch paintings!",
                });
                console.log(error);
              });
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

  function RegisterClick(painting_click, index) {
    let feature;

    if (painting.painting.color) {
        feature = index;
    } else if (index === 1) {
        feature = 0;
    } else {
        feature = index
    }

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/evaluation/click/", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + token,
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        painting_id: painting_click.object_number,
        actual_recommendation_feature: feature,
      }),
    })
      .then((response) => {
        if (response.ok) {
          response.json().then(data => {
            ShowFeatureQ(data)
          })
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

  function SubmitAnswers(data) {
    let t = []


    recommendations.forEach((recommendation, index) => {
        let form_index = recommendation.object_number
        let value = form.getFieldValue(form_index)

        t.push([
            recommendation.object_number,
            value,
            index,
            data.id
        ])
    })

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/evaluation/answers/", {
        method: "POST",
        headers: new Headers({
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        }),
        body: JSON.stringify({
          "result": t
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
            message: "Error while registering answers!",
          });
          console.log(error);
        })

    fetchRecommendations()
  }

  function ShowFeatureQ(data) {
    Modal.info({
      title: "Results",
      content: (
        <div className="images">
          <p>
            How good is the recommendation?
          </p>
          <Form className="form" form={form}>
            {recommendations.map((recommendation, index) => (
              <div className="evaluation_images">
                <Row key={index}>
                <Col span={6}>
                    <img
                      className="evaluation_image"
                      src={painting.painting.url}
                      alt=""
                    ></img>
                    Actual image:
                    {index == 2 ? <p>{painting.painting.description}</p>:<></>}

                  </Col>
                  <Col span={6}>
                    <img
                      className="evaluation_image"
                      src={recommendation.url}
                      alt=""
                    ></img>
                    recommendation image:
                    {index == 2 ? <p>{recommendation.description}</p>:<></>}
                  </Col>
                  <Col span={3}>
                    feature: {features[index]}
                  </Col>
                  <Col span={9}>
                    <Form.Item
                      name={recommendation.object_number}
                      rules={[
                        { required: true, message: "Please select a feature" },
                      ]}
                    >
                      <Radio.Group className="radio">
                        <Radio value="1">1</Radio>
                        <Radio value="2">2</Radio>
                        <Radio value="3">3</Radio>
                        <Radio value="4">4</Radio>
                        <Radio value="5">5</Radio>
                      </Radio.Group>
                    </Form.Item>
                  </Col>
                </Row>
              </div>
            ))}
          </Form>
        </div>
      ),
      okText: "Submit",
      onOk() {
        SubmitAnswers(data)
      },
      width: 1000,
    });
  }

  return (
    <div className="container">
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
            <h3 style={{ "margin-left": "20px" }}>Applicatie evaluation</h3>
            <p style={{ "margin-left": "20px" }}>
              Than you for helping us evaluate our application. Please select
              the painting that appeals to you the most. If the
              picture left is your reference.
              <br /> <br />
              title: {painting.painting.title} <br />
          description: {painting.painting.description} <br />
          maker: {painting.painting.maker} <br />
          art style: {painting.art_style} <br />
          dominant color: {painting.painting.color}<br />
            </p>
          </Col>
        </Row>

        <Divider />
        <Row className="images">
          {recommendations.map((painting, index) => (
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
          ))}
        </Row>
      </div>
    </div>
  );
}

export default Evaluation;
