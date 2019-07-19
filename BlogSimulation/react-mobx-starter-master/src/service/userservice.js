import axios from 'axios';
import { log } from 'util';
import store from 'store';
import { observable } from 'mobx';
import { message } from 'antd';

class UserService {
  @observable success = false;
  @observable errMsg = "";

  login(email, password) {
    console.log(email, password);
    axios.post('/api/user/login', {
      email: email,
      password: password
    })
      .then(response => {
        console.log(response.status);
        console.log(response.data);
        console.log(response.headers);
        console.log(response.config);
        console.log(response.statusText);

        store.set('token', response.data.token, new Date().getTime() + (8 * 3600 * 1000));
        this.success = true;
      })
      .catch(error => {
        console.log(error);
        this.errMsg = "登录失败!";
      });
  }
  regist(name, email, password) {

    axios.post('/api/user/reg', {
      name: name,
      email: email,
      password: password
    })
      .then(response => {
        console.log(response.status);
        console.log(response.data);
        console.log(response.headers);
        console.log(response.config);
        console.log(response.statusText);

        store.set('token', response.data.token, new Date().getTime() + (8 * 3600 * 1000));
        this.success = true;
      })
      .catch(error => {
        console.log(error);
        this.errMsg = "注册失败!";
      });
  }
}

const service = new UserService();

export default service;