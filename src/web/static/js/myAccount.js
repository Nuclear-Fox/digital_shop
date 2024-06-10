(function($) {

    var web = window.location.origin;

    function getCoinBalance() {
        const req = new XMLHttpRequest();
        req.open("GET", `${web}/getCoinBalance`, true);
        req.addEventListener("load", () => {
            var result = req.responseText;
            $("#bonusBalance").text(result);
        });
        req.send(null);
    }

    function getCoinAccount() {
        const req = new XMLHttpRequest();
        req.open("GET", `${web}/getCoinAccount`, true);
        req.addEventListener("load", () => {
            var result = req.responseText;
            $("#account").text(result);
            getCoinBalance();
        });
        req.send(null);
    }
    getCoinAccount();

})(jQuery);