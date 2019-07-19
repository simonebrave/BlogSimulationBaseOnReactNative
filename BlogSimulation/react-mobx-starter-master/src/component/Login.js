import React from 'react';
import {Link} from 'react-router-dom';
import {Redirect} from 'react-router';
import login from '../css/login.css';
import {observer} from 'mobx-react';
import {message} from 'antd';
import 'antd/lib/message/style/css';

import service from '../service/userservice';
import inject from '../inject';

@inject({service})
@observer
export default class Login extends React.Component {

    handlerClick(event){
        event.preventDefault();
        let param = event.target.form
        let user = param[0].value;
        let pwd = param[1].value;
        this.props.service.login(user, pwd);
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
                    <form className="login-form">
                        <input type="text" placeholder="username" />
                        <input type="password" placeholder="password" />
                        <button onClick={this.handlerClick.bind(this)}>login</button>
                        <p className="message">Not registered? <Link to="/reg">Create an account</Link></p>
                    </form>
                </div>
            </div>
        );
    }
}