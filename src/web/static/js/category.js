(function($) {

    function getProductElement(id, name, price, info) {
        return `<div class="single_product list_item">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-md-5">
                        <img src="getImage/${id}.png" alt="${name}">
                    </div>
                    <div class="col-lg-8 col-md-7">
                        <div class="product_content">
                            <h3>${name}</h3>
                            <div class="product_price">
                                <span class="current_price">${price} ₽</span>
                            </div>
                            <div class="product_description">
                                <p>${info}</p>
                            </div>
                            <div class="product_action">
                                <ul>
                                    <li class="product_cart" id="${id}" style="cursor: pointer;"><a >В корзину</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
    }

    var orderType = "1";
    var web = window.location.origin;
    var category = window.category;

    function getList() {
        const req = new XMLHttpRequest();
        req.open("GET", `${web}/getCategoryList/${category.code}?orderType=${orderType}`, true);
        req.addEventListener("load", () => {
            var list = JSON.parse(req.responseText);

            $(".tab-pane").empty()
            list.forEach((product) => {
                var id = product[0];
                var name = product[1]
                var price = product[2];
                var info = product[3];
                var brand = product[4];

                var prObj = $(getProductElement(id, name, price, info));

                $(".tab-pane").append(prObj);

                prObj.find(".product_cart").on( "click", function() {
                  id = $(this).attr('id');
                  const req = new XMLHttpRequest();
                    req.open("POST", `${web}/addToCart/${id}`);
                    //req.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
//                    const body = JSON.stringify({
//                      email: email,
//                      password: password,
//                    });
                    req.onload = () => {
                      if (req.readyState == 4 && req.status == 200) {
                        alert(req.response)
                      } else {
                        alert(req.response);
                      }
                    };
                    req.send();
                } );



            });
        });
        req.send(null);
    }

    $('#short1').change(() => {
         orderType = $(".nice-select").find(".selected").get(0).dataset.value;
         getList();

    });

    getList();

})(jQuery);