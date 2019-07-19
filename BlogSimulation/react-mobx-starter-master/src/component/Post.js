import React from 'react';
import { observer } from 'mobx-react';
import { Card } from 'antd';
import 'antd/lib/message/style/css';
import 'antd/lib/card/style/css';

import service from '../service/postservice';
import inject from '../inject';

const postservice = service;

@inject({ postservice })
@observer
export default class Post extends React.Component {
    constructor(props){
        super(props);
        let blog_id = this.props.match.params.id;
        this.props.postservice.getBlog(blog_id);
    }

    render() {
        let blog = this.props.postservice.blog;
        return (
            <div style={{background: "#ECECEC", padding: "30px"}}>
                <Card title={blog.title} bordered={true}>
                    <p>{blog.author} {new Date(blog.post_date*1000).toLocaleDateString()}</p>
                    <p>{blog.content}</p>
                </Card>
            </div>
        );
    }
}