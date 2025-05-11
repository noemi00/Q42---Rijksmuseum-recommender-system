import "../Styles/login.css";

import { useState, useEffect } from "react";
import { Button, Divider, Form, Input, notification } from "antd";
import { useNavigate, Link } from "react-router-dom";

import Layout from "../Components/Layout";
import useToken from "../Components/Token";

function Register() {
  const [loading, setLoading] = useState(false);
  const { token } = useToken();
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      navigate("/");
    }
  }, [token, navigate]);

  function RegisterUser(values) {
    console.log(values);
    if (loading) {
      return;
    }

    setLoading(true);

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/users/register/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: values.email,
        password: values.password,
      }),
    })
      .then((response) => {
        if (response.ok) {
          notification.success({
            message: "register succesfull!",
          });
          navigate("/login");
          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while trying register!",
        });
        console.log(error);
      });

    setLoading(false);
  }

  function RegisterFailed(errorInfo) {
    console.log("Failed:", errorInfo);
    notification.error({
      message: "register failed",
    });
  }

  return (
    <Layout>
      <div className="login_container">
        <h1>Register</h1>
        <Form
          name="basic"
          labelAlign="left"
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          initialValues={{ remember: true }}
          onFinish={RegisterUser}
          onFinishFailed={RegisterFailed}
          autoComplete="off"
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button className="submit_button" type="primary" htmlType="submit">
              Sign up
            </Button>
          </Form.Item>
        </Form>
        <Divider>OR</Divider>
        <p className="register_text">Already have an account</p>
        <p className="register_text">
          <Link className="register_link" to="/login">
            Login
          </Link>
        </p>
      </div>
    </Layout>
  );
}

export default Register;
