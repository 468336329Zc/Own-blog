var authCode;
    randomCode=$("#js5-authCode").eq(0);//获取验证码出现的方框dom
console.log(randomCode);

function createCode() {
    authCode="";//设置这个为空变量，然后往里面添加随机数
    var authCodeLength=4;//随机数的长度
    randomArray=[0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R', 'S','T','U','V','W','X','Y','Z'];
    //创建一个数组，随机数从里面选择四位数或者更多
    for(var i=0;i<authCodeLength;i++){
        var index=Math.floor(Math.random()*36);//随机取一位数
        authCode +=randomArray[index];//取四位数，并+相连
    }
    console.log(authCode);//取到四位随机数之后，跳出循环
    randomCode.val(authCode);//将四位随机数赋值给验证码出现的方框
    console.log(randomCode.val());
}

//以上是封装的获取验证码的函数

$(function () {//当文档加载结束后，运行这个函数
    createCode();//一开始先运行一遍取随机数的函数
    $("#js5-btn").click(function () {//这里是一个点击事件
        console.log(window.randomCode);
        //这里写了一个必报，window.randomCode是在文档里面找到这个dom，否则上文的四个随机数传不到这里来
        var randomCode=window.randomCode.val();
        console.log(randomCode);
        var authInput=$("#js5-form3-input").val().toUpperCase(),
            user=$("#js5-userNum").val(),
            psd=$('#js5-password').val();
        //上面三个是分别获取验证码输入框的值，账号的值，密码的值。
        //验证码输入框这里，最后toUpperCase()方法是把小写转换成大写
        console.log(authInput);
        console.log(randomCode);
        console.log(user,psd);
        if (randomCode===authInput) {
        //验证验证码，在验证码输入框与验证码的值不相等之前，是不会进入下面登录的步骤的，验证码是第一步关卡
            var firstAjax = new XMLHttpRequest();
            //创建ajax对象，这里是ajax跨域的部分
            firstAjax.open("POST", "这里是你url跨域的地址", true);
            //连接服务器，跨域。
            firstAjax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            //setRequestHeader() 方法指定了一个 HTTP 请求的头部，它应该包含在通过后续 send() 调用而发布的请求中。
            //可以理解为，这是http的请求头，固定格式，位置必须要在open之后，send之前。
            firstAjax.send("name=" + user + "&pwd=" + psd);
            //在使用POST方式时参数代表着向服务器发送的数据，前面两个是账号框和密码框
            firstAjax.onreadystatechange = function () {//当参数被传入服务器的时候，引用监听事件。
                if (firstAjax.readyState == 4) {//readyState四种状态，当执行四步完成之后
                    if (firstAjax.status == 200) {//返回的是200，代表成功，404未找到。
                        var returnValue = JSON.parse(firstAjax.responseText);//取回由服务器返回的数据
                        console.log(returnValue);
                        if (returnValue.code == 0) {//这里是后端定义的，当code==0的时候，代表登录正确。
                            window.location.href = "https://www.baidu.com/index.php?tn=98012088_3_dg&ch=1";
                            //后端返回的数据验证成功就跳转链接。
                        }
                        else {
                            $("#js5Message").text(returnValue.message);//当code不等于0时，返回出错信息
                        }
                    } else {
                        alert("出错咯，咯咯咯");//返回的不是200的时候，出错。
                    }
                }
            };
            createCode();//点击登录按钮，验证之后会刷新验证码
        }
        else {
            $("#js5Message").text("验证码错误，请重新输入");
            createCode();//验证码错误，刷新验证码。
        }
    })
});