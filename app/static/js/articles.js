function comments() {

    var comments = $("#comment_content").val();
    my_data = {"comments": comments};
    $.ajax({
        url: '/comment/html css急速入门',
        data: my_data,
        type: 'POST',
        success: function (data) {
            if (data['status'] === '0') {
                alert('请先注册并登录后再评论,即将跳转到注册界面...');
                window.location.href = '/register/';

            }
        },
        statusCode: {
            500: function () {
                alert('后台错误')
            }
        },
        error: function () {
            alert('连接服务器失败');
        },

    })
}

//跳转控制
function delayURL(url, time) {
    setTimeout("top.location.href='" + url + "'", time);
}
//根据博文数量隐藏博文多少次
function yincang(){
    $.ajax({
        url:"/get-blogsums",
        success:function (blogsums) {
            for(var i=0;i<blogsums;i++)
                document.getElementById('blog').style.display='none';
        }
     });
}
//后台获取blog
function get_blog_title() {
    $.ajax({
        url: '/admin/get-blog',
        type: 'get',
        success: function (blogs_arr) {
            yincang();
            creat(blogs_arr['blogs_arr']);

        }
    });
}



//前端模糊搜索，
function creat(blogs) {
    var input = document.getElementById("key");
    var ul = document.getElementById("sousuo-blog");
    var value = input.value;
    var html = "";
    var newData = blogs.filter(item => {
        if (item.indexOf(value) > -1) {//indexOf方法中如果xxx.indexOf("")返回值为0
            return item
        }
        return newData
    });
    if (newData.length > 0) {
        for (var i = 0; i < newData.length; i++) {
            html += `<a>${newData[i]}</a>`
        }
    } else {
        html += `<a>暂无数据</a>`
    }
    ul.innerHTML = html;
    input.onchange = function (e) {
        get_blog_title();
    }
}


/* Display table of contents */
function show_toc(toc_selector, wrap_id, min_nr)
{
    var wrap = document.getElementById(wrap_id);

    var hlist = document.querySelectorAll(toc_selector);

    if (!wrap)
        return;

    if (!hlist || hlist.length <= min_nr) {
        wrap.style.display = 'none';
        return;
    }

    var ul = document.createElement('ul'), li, link;

    for (i = 0; i < hlist.length; i++) {
        hlist[i].id = 'i_' + i;

        li = document.createElement('li');

        link = document.createElement('a');
        link.href = '#' + hlist[i].id;
        link.className = 'toc_link';
        link.innerHTML = hlist[i].innerHTML;

        li.appendChild(link);
        ul.appendChild(li);
    }

    wrap.appendChild(ul);
}
show_toc('show_toc',)