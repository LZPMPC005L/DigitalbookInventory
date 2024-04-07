document.getElementById('create-button').addEventListener('click', function() {
    // 获取表单中的数据
    var title = document.getElementById('title').value;
    var author = document.getElementById('author').value;
    var description = document.getElementById('description').value;
    var date_published = document.getElementById('date_published').value;
    var price = document.getElementById('price').value;
    var subject = document.getElementById('subject').value;

    // 创建一个包含新书籍信息的对象
    var book = {
        title: title,
        author: author,
        description: description,
        date_published: date_published,
        price: price,
        subject: subject
    };

    // 将对象转换为JSON
    var jsonBook = JSON.stringify(book);

    //获取CSRF令牌
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // 创建一个新的XHR对象
    var xhr = new XMLHttpRequest();

    // 配置XHR对象
    xhr.open("POST", "/book/new/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    //在请求头中设置CSRF令牌
    xhr.setRequestHeader("X-CSRFToken",csrftoken);

    // 发送请求
    xhr.send(jsonBook);

    // 当收到响应时，打印响应的内容
    xhr.onload = function() {
        console.log(xhr.responseText);
    };
});
