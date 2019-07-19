import React from 'react';
import ReactDom from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'
import { Menu, Icon } from 'antd';
import 'antd/lib/menu/style/css';

import Login from './component/Login';
import Reg from './component/Reg';
import BlogList from './component/BlogList';
import Post from './component/Post';

const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const About = () => (
  <div>
    <h2>About</h2>
  </div>
);

const App = () => (
  <Router>
    <div>
      <div>
        <Menu mode="horizontal">
          <Menu.Item key="home">
            <Link to="/" ><Icon type="home" />主页</Link>
          </Menu.Item>
          <Menu.Item key="login">
            <Link to="/login" >登录</Link>
          </Menu.Item>
          <Menu.Item key="reg">
            <Link to="/reg" >注册</Link>
          </Menu.Item>
          <Menu.Item key="list">
            <Link to="/list" >查看列表</Link>
          </Menu.Item>
          <Menu.Item key="about">
            <Link to="/about" >关于</Link>
          </Menu.Item>
        </Menu>
      </div>
      <Route exact path="/" component={Home} />
      <Route path="/about" component={About} />
      <Route path="/login" component={Login} />
      <Route path="/reg" component={Reg} />
      <Route path="/list" component={BlogList} />
      <Route exact path="/post/:id" component={Post} />
    </div>
  </Router>
);

ReactDom.render(<App />, document.getElementById('root'));
