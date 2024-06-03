(function($) {

    function getProductElement(id, name, price, amount, total) {
        return `<tr class="product">
                    <td class="product-remove" id="${id}"><a style="cursor: pointer;"><i class="fa fa-trash-o"></i></a></td>
                    <td class="product-thumb"><img src="category/getImage/${id}.png" alt="${name}"></td>
                    <td class="product-name">${name}</a></td>
                    <td class="product-price">${price} ₽</td>
                    <td class="product-quantity"><input class="amount" id="${id}" min="1" max="100" value="1" type="number"></td>
                    <td class="product-price">${total} ₽</td>
                </tr>`;
    }

    var web = window.location.origin;

    function getTotal() {
        const req = new XMLHttpRequest();
        req.open("GET", `${web}/getTotal`, true);
        req.addEventListener("load", () => {
            var result = JSON.parse(req.responseText);
            $("#cart_total").text(result["cart_total"]);
            $("#bonus").text(result["bonus"]);
            $("#total").text(result["total"]);
        });
        req.send(null);
    }

    function getList() {
        const req = new XMLHttpRequest();
        req.open("GET", `${web}/getCartList`, true);
        req.addEventListener("load", () => {
            var list = JSON.parse(req.responseText);

            $(".cart-content").empty()
            list.forEach((product) => {
                var id = product[0];
                var name = product[1]
                var price = product[2];
                var amount = product[3];
                var total = product[4];

                var prObj = $(getProductElement(id, name, price, amount, total));

                prObj.find(".amount").val(amount);

//                prObj.find(".product-quantity").value = amount;

                $(".cart-content").append(prObj);

                prObj.find('.amount').change(function() {
                     id = $(this).attr('id');
                     amount = $(this).val();
                     const req = new XMLHttpRequest();
                     req.open("POST", `${web}/setAmountInCart/${id}?amount=${amount}`);
                     req.onload = () => {
                      if (req.readyState == 4 && req.status == 200) {
                        getList();
                      } else {
                        alert(req.response);
                      }
                    };
                    req.send();
                });

                prObj.find(".product-remove").on( "click", function() {
                    id = $(this).attr('id');
                    const req = new XMLHttpRequest();
                    req.open("POST", `${web}/delFromCart/${id}`);
                        //req.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
        //                    const body = JSON.stringify({
        //                      email: email,
        //                      password: password,
        //                    });
                    req.onload = () => {
                        if (req.readyState == 4 && req.status == 200) {
                            getList();
                        } else {
                            alert(req.response);
                        }
                    };
                    req.send();
                } );





            });
        });
        req.send(null);

        getTotal();
    }

    $(".checkout_btn").on( "click", function() {
        const req = new XMLHttpRequest();
        req.open("POST", `${web}/confirm_order`);
        req.onload = () => {
            if (req.readyState == 4 && req.status == 200) {
                alert(req.response);
                window.setTimeout('location.reload()', 500);
            } else {
                alert(req.response);
            }
        };
    req.send();
    } );

    getList();

})(jQuery);