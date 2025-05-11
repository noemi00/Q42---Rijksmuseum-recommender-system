import Header from "./Header";
import "../Styles/layout.css";

function Layout(props) {
  return (
    <>
      <Header />
      <div className="container">{props.children}</div>
    </>
  );
}

export default Layout;
