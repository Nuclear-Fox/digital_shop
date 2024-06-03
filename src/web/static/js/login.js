(function($) {

    var web = window.location.origin;

    $('#loginButton').on('click', function(){
        var email = $("#emailLogin").val();
        var password = $("#passwordLogin").val()

        const req = new XMLHttpRequest();
        req.open("POST", `${web}/login_in`);
        req.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
        const body = JSON.stringify({
          email: email,
          password: password,
        });
        req.onload = () => {
          if (req.readyState == 4 && req.status == 200) {
            window.location.href = `${web}/my_account`;
          } else {
            alert(req.response);
          }
        };
        req.send(body);

    });

    $('#regButton').on('click', function(){
        var email = $("#emailReg").val();
        var password = $("#passwordReg").val()

        const req = new XMLHttpRequest();
        req.open("POST", `${web}/register`);
        req.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
        const body = JSON.stringify({
            email: email,
            password: password,
        });
        req.onload = () => {
            if (req.readyState == 4 && req.status == 200) {
                window.location.href = `${web}/my_account`;
            } else {
                alert(req.response);
            }
        };
        req.send(body);

    });

})(jQuery);