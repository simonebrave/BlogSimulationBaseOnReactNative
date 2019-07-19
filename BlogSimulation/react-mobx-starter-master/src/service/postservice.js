import axios from 'axios';
import { log } from 'util';
import { observable } from 'mobx';
import { message } from 'antd';

class postService {
    @observable blogs = [];
    @observable page_info = { page: 0, size: 0, cout: 0, pages: 0 };
    @observable errMsg = "";
    @observable blog = {};

    list(page = 1, size = 20) {
        axios.get('/api/post/', {
            page: page,
            size: size
        })
            .then(response => {
                this.blogs = response.data.blogs;
                this.page_info = response.data.page_info;
            })
            .catch(error => {
                console.log(error);
                this.errMsg = "加载失败!";
            });
    }

    getBlog(blog_id) {
        axios.get('/api/post/' + blog_id)
            .then(response => {
                this.blog = response.data.blog;
            })
            .catch(error => {
                console.log(error);
                this.errMsg = "加载失败!";
            });
    }
}

const service = new postService();
export default service;