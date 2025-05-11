import { useState } from "react";

function useToken() {
  const [token, setToken] = useState(getToken());

  function getToken() {
    const tokenString = sessionStorage.getItem("access_token");
    return tokenString;
  }

  function saveToken(userToken) {
    sessionStorage.setItem("access_token", userToken);
    setToken(userToken);
  }

  return {
    setToken: saveToken,
    token,
  };
}

export default useToken;
