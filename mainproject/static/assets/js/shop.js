(function ($) {
    'use strict';
    /*Product Details*/
    var productDetails = function () {
        $('.product-image-slider').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: false,
            asNavFor: '.slider-nav-thumbnails',
        });

        $('.slider-nav-thumbnails').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            asNavFor: '.product-image-slider',
            dots: false,
            focusOnSelect: true,
            prevArrow: '<button type="button" class="slick-prev"><i class="fi-rs-angle-left"></i></button>',
            nextArrow: '<button type="button" class="slick-next"><i class="fi-rs-angle-right"></i></button>'
        });

        // Remove active class from all thumbnail slides
        $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');

        // Set active class to first thumbnail slides
        $('.slider-nav-thumbnails .slick-slide').eq(0).addClass('slick-active');

        // On before slide change match active thumbnail to current slide
        $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
            var mySlideNumber = nextSlide;
            $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');
            $('.slider-nav-thumbnails .slick-slide').eq(mySlideNumber).addClass('slick-active');
        });

        $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
            var img = $(slick.$slides[nextSlide]).find("img");
            $('.zoomWindowContainer,.zoomContainer').remove();
            $(img).elevateZoom({
                zoomType: "inner",
                cursor: "crosshair",
                zoomWindowFadeIn: 500,
                zoomWindowFadeOut: 750
            });
        });
        //Elevate Zoom
        if ( $(".product-image-slider").length ) {
            $('.product-image-slider .slick-active img').elevateZoom({
                zoomType: "inner",
                cursor: "crosshair",
                zoomWindowFadeIn: 500,
                zoomWindowFadeOut: 750
            });
        }
        //Filter color/Size
        $('.list-filter').each(function () {
            $(this).find('a').on('click', function (event) {
                event.preventDefault();
                $(this).parent().siblings().removeClass('active');
                $(this).parent().toggleClass('active');
                $(this).parents('.attr-detail').find('.current-size').text($(this).text());
                $(this).parents('.attr-detail').find('.current-color').text($(this).attr('data-color'));
            });
        });
        //Qty Up-Down
        $('.detail-qty').each(function () {
            var qtyval = parseInt($(this).find('.qty-val').text(), 10);
            $('.qty-up').on('click', function (event) {
                event.preventDefault();
                qtyval = qtyval + 1;
                $(this).prev().text(qtyval);
            });
            $('.qty-down').on('click', function (event) {
                event.preventDefault();
                qtyval = qtyval - 1;
                if (qtyval > 1) {
                    $(this).next().text(qtyval);
                } else {
                    qtyval = 1;
                    $(this).next().text(qtyval);
                }
            });
        });

        $('.dropdown-menu .cart_list').on('click', function (event) {
            event.stopPropagation();
        });
    };
    /* WOW active */
    new WOW().init();

    //Load functions
    $(document).ready(function () {
        productDetails();
    });

})(jQuery);






$(document).ready(function (){
    $(".filter-checkbox").on("click", function(){
        event.preventDefault();
        console.log("A box have been clicked");
        let filter_object ={}
        $(".filter-checkbox").each(function(){
            let filter_value=$(this).val()
            let filter_key = $(this).data("filter")
           

            filter_object[filter_key]=Array.from (document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function(element){
                return element.value
            })


        })
        console.log("filter object is: ",filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending data..");

            },
            success:function(response){
                console.log(response);
                console.log('data filtered suessgfuly');

                $("#filtered-product").html(response.data)
                console.log("Response Data:", response.data);

            }

        })

    })    

})

        

// $(document).ready(function() {
//     // Function to update products based on the selected price range
//     function updateProducts(minPrice, maxPrice) {
//         $.ajax({
//             url: '{% url "filter_products" %}',
//             data: { min_price: minPrice, max_price: maxPrice },
//             dataType: 'json',
//             success: function(data) {
//                 // Handle the updated product data
//                 console.log(data.products);
//                 // Implement logic to update the displayed products on the page
//             },
//             error: function(error) {
//                 console.log('Error fetching products:', error);
//             }
//         });
//     }

//     // Event listener for price range changes
//     $('#price-slider').on('slideStop', function(event) {
//         // Get the selected price range
//         var minPrice = event.value[0];
//         var maxPrice = event.value[1];

//         // Update products based on the selected price range
//         updateProducts(minPrice, maxPrice);
//     });
// });

    




// $(document).ready(function () {
//     $(document).on('change', '#size-selection', function () {
//         var selectedSize = $(this).val();
//         var productId = '{{ product.pid }}';

//         $.ajax({
//             url: '{% url "get_variant_details" product.pid %}',
//             type: 'GET',
//             data: {
//                 'product_id': productId,
//                 'variant': selectedSize
//             },
//             dataType: 'json',
//             success: function (data) {
//                 // Update the UI with variant details
//                 $('#stock-count-display').text('Stock Count: ' + data.stock_count);
//                 $('#price-display').text('Price: ' + data.price);
//                 // Update other UI elements as needed
//             },
//             error: function (error) {
//                 console.log('Error:', error);
//             }
//         });
//     });
// });

// document.addEventListener('DOMContentLoaded', function () {
//     var sizeSelection = document.getElementById('size-selection');
//     var variantDetails = document.querySelectorAll('.variant-details');

//     sizeSelection.addEventListener('change', function () {
//         var selectedSize = sizeSelection.value;

//         // Hide all variant details
//         variantDetails.forEach(function (variant) {
//             variant.style.display = 'none';
//         });

//         // Show the selected variant details
//         var selectedVariant = document.querySelector('.variant-details[data-size="' + selectedSize + '"]');
//         if (selectedVariant) {
//             selectedVariant.style.display = 'block';
//         }
//     });
// });



// $("#add-to-cart-btn").on("click", function(){

//     let quantity = $("#product-quantity").val()
//     let product_title=$(".product-title").val()
//     let product_id=$(".product-id").val()
//     let product_price =$("#current-product-price").text()
//     let this_value =$(this)


//     console.log("quantity:",quantity);
//     console.log("title:", product_title);
//     console.log("id:", product_id);
//     console.log("price:", product_price);
//     console.log("Current element:", this_value);
   

//     $.ajax({
//         url: '/add-to-cart',
//         data:{
//             'id':product_id,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         datatype: 'json',
//         beforeSend: function(){
//             console.log ("adding product to cart...");
//         },
//         success: function(response){
//             console.log(response);
//             this_value.html("item added to cart")
//             console.log("Added Product to Cart")
//             $(".cart-items-count").text(response.totalcartitems)
//         }
//     })
   
// })


$(".add-to-cart-btn").on("click", function(){

    let this_val =$(this)
    let index =this_val.attr("data-index")
    let quantity = $(".product-quantity-" + index).val()


    
    let product_title=$(".product-title-" + index).val()
    let product_id=$(".product-id-" + index).val()
    // let product_price =$(".current-product-price-" + index).text()
    let product_price = parseFloat($(".current-product-price-" + index).text());
    let product_pid =$(".product-pid-" + index).val()
    let product_image=$(".product-image-" + index).val()
    

    console.log("quantity:",quantity);
    console.log("title:", product_title);
    console.log("id:", product_id);
    console.log("pid:", product_pid);
    console.log("image:", product_image);
    console.log("price:", product_price);
    console.log("Current element:", this_val);
   

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id':product_id,
            'pid':product_pid,
            'image':product_image,
            'qty':quantity,
            'title':product_title,
            'price':product_price,
        },
        datatype: 'json',
        beforeSend: function(){
            console.log ("adding product to cart...");
        },
        success: function(response){
            console.log(response);
            this_val.html("✔")
            console.log("Added Product to Cart")
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
   
})



// delete product from cart

$(document).on("click", ".delete-product", function () {
    let thisVal = $(this);
    let productId = thisVal.attr("data-product");

    console.log("productId:", productId);

    $.ajax({
        url: "/delete-from-cart",
        data: {
            "id": productId
        },
        dataType: "json",
        beforeSend: function () {
            thisVal.hide();
        },
        success: function (response) {
            thisVal.show();
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });
});










// update cart


$(document).on("click", ".quantity-control .quantity-btn", function () {
    let action = $(this).data("action");
    let productId = $(this).data("product-id");
    let quantityInput = $(".product-qty-" + productId);
    let currentQty = parseInt(quantityInput.val());

    if (action === "increase") {
        quantityInput.val(currentQty + 1);
    } else if (action === "decrease" && currentQty > 1) {
        quantityInput.val(currentQty - 1);
    }

    updateCart(productId, quantityInput.val());
});

function updateCart(productId, newQuantity) {
    $.ajax({
        url: "/update-cart",
        data: {
            "id": productId,
            "qty": newQuantity
        },
        dataType: "json",
        beforeSend: function () {
            // Handle any actions before making the AJAX request, e.g., show loader
        },
        success: function (response) {
            // Handle success, e.g., update the UI with the new cart data
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
        },
        error: function (error) {
            // Handle error, e.g., show an alert or log the error
            console.log('Error:', error);
        },
        complete: function () {
            // Handle any actions after the AJAX request, e.g., hide loader
        }
    });
}



