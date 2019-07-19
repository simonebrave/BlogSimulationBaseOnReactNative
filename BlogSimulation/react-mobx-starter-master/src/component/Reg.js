import React from 'react';
import { Link } from 'react-router-dom';
import {Redirect} from 'react-router';
import login from '../css/login.css';
import {observer} from 'mobx-react';
import { message } from 'antd';
import 'antd/lib/message/style/css';

import service from '../service/userservice';
import inject from '../inject';


@inject({service})
@observer
export default class Reg extends React.Component {
    handleClick(event){
        event.preventDefault();
        let params = event.target.form;
        let name = params[0].value;
        let email = params[1].value;
        let fpwd = params[2].value;
        let spwd = params[3].value;
        if (fpwd === ""){
            message.info("密码不可以为空");
            return;
        } 
        if (fpwd === spwd){
            this.props.service.regist(name, email, fpwd);
        }
        else{
            message.info("请确认两次输入的密码相同!");
        }
    }
    render() {
        if (this.props.service.success){
            return (<Redirect to="/" />);
        }
        if (this.props.service.errMsg){
            message.error(this.props.service.errMsg, 3, () => {this.props.service.errMsg = ""});
        }
        return (
            <div className="login-page">
                <div className="form">
                    <form className="register-form">
                        <input type="text" placeholder="name" />
                        <input type="text" placeholder="email address" />
                        <input type="password" placeholder="password" />
                        <input type="password" placeholder="confirm password" />
                        <button onClick={this.handleClick.bind(this)}>create</button>
                        <p className="message">Already registered? <Link to="/login">Sign In</Link></p>
                    </form>
                </div>
            </div>
        );
    }
}