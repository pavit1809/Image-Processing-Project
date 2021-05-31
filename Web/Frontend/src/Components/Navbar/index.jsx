import React from "react";
import { Menu } from "antd";
import { useHistory } from "react-router-dom";
import { KeyOutlined, UnlockOutlined } from "@ant-design/icons";

export default function Navbar(props) {
  const [current, setCurrent] = React.useState("");
  const history = useHistory();

  const handleClick = (e) => {
    console.log("click ", e);
    setCurrent(e.key);
  };

  React.useEffect(() => {
    setCurrent(props.current);
  }, []);

  return (
    <Menu
      onClick={handleClick}
      theme="dark"
      selectedKeys={[current]}
      mode="horizontal"
    >
      <Menu.Item
        key="encrypt"
        icon={<KeyOutlined />}
        onClick={() => history.push("/")}
        style={{ cursor: "pointer" }}
      >
        Encrypt
      </Menu.Item>
      <Menu.Item
        key="decrypt"
        icon={<UnlockOutlined />}
        onClick={() => history.push("/decrypt")}
        style={{ cursor: "pointer" }}
      >
        Decrypt
      </Menu.Item>
    </Menu>
  );
}
