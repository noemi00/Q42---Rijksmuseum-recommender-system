import { useState, useEffect } from "react";
import { Button, Divider, Form, Input, notification } from "antd";
import { useNavigate, Link } from "react-router-dom";

import Layout from "../Components/Layout";
import useToken from "../Components/Token";

import "../Styles/login.css";

function Login(props) {
  const [loading, setLoading] = useState(false);
  const { token, setToken } = useToken();
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      navigate("/");
    }
  }, [token, navigate]);

  function LoginUser(values) {
    if (loading) {
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("username", values.username);
    formData.append("password", values.password);

    fetch(process.env.REACT_APP_FRONTEND_API_URL + "/token/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          notification.success({
            message: "Login succesfull!",
          });
          response.json().then((data) => {
            console.log(data);
            setToken(data.access_token);
            navigate("/");
          });
          return;
        } else {
          throw new Error(response.text());
        }
      })
      .catch((error) => {
        notification.error({
          message: "Error while trying login!",
          description: "Check your user credentials",
        });
        console.log(error);
      });

    setLoading(false);
  }

  function LoginFailed(errorInfo) {
    console.log("Failed:", errorInfo);
    notification.error({
      message: "login failed",
    });
  }

  return (
    <Layout>
      <div className="login_container">
        <h1>Login</h1>
        <Form
          name="basic"
          labelAlign="left"
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
          initialValues={{ remember: true }}
          onFinish={LoginUser}
          onFinishFailed={LoginFailed}
          autoComplete="off"
        >
          <Form.Item
            label="Email"
            name="username"
            rules={[{ required: true, message: "Please input your email!" }]}
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
              Login
            </Button>
          </Form.Item>
        </Form>
        <Divider>OR</Divider>
        <p className="register_text">Need an account?</p>
        <p className="register_text">
          <Link className="register_link" to="/register">
            Register
          </Link>
        </p>
      </div>
    </Layout>
  );
}

export default Login;
