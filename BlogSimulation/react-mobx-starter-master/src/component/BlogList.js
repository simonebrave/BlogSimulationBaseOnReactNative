import React from 'react';
import { Link } from 'react-router-dom';
import { observer } from 'mobx-react';
import { List } from 'antd';
import 'antd/lib/message/style/css';
import 'antd/lib/list/style/css';

import service from '../service/postservice';
import inject from '../inject';
const postservice = service;

@inject({ postservice })
@observer
export default class BlogList extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props.location);
        let params = new URLSearchParams(this.props.location.search);
        this.props.postservice.list(params.get("page"), params.get("size"));
    }

    render() {
        let blogs = this.props.postservice.blogs;
        return (
            <div>
                <List
                    bordered={true}
                    style={{background: "#ECECEC", padding: "30px"}}
                    dataSource={blogs}
                    renderItem={item => (
                        <List.Item>
                            <List.Item.Meta
                                title={<Link to={"/post/" + item.blog_id}>{item.title}</Link>}
                            />
                        </List.Item>
                    )}
                />
            </div>
        );
    }
}