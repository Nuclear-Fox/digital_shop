 /*mini cart slideToggle*/

    $(".cart_link > a").on("click", function() {
        $('.mini_cart').slideToggle('medium');
    });

    /*categories slideToggle*/
    $(".categories_title").on("click", function() {
        $(this).toggleClass('active');
        $('.categories_menu_inner').slideToggle('medium');
    });


    /*------addClass/removeClass categories-------*/
   $(".categories_menu_inner > ul > li > a, #cat_toggle.has-sub > a").on("click", function() {
        $(this).removeAttr('href');
        $(this).toggleClass('open').next('.categories_mega_menu,.categorie_sub').toggleClass('open');
        $(this).parents().siblings().find('.categories_mega_menu,#cat_toggle.has-sub > a').removeClass('open');
    });

    $('body').on('click', function (e) {
        var target = e.target;
        if (!$(target).is('.categories_menu_inner > ul > li > a') ) {
            $('.categories_mega_menu').removeClass('open');
        }
    });

$(document).ready(function(){
    $(".categories_menu_inner").css("width", $(".logo").width());
    $(".categories_menu_inner").css("left", 0 - $(".logo-item").eq(0).width());
});