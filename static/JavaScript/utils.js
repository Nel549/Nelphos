$(document).ready(function () {
    $('.addToCartBtn').click(function (e) {
        e.preventDefault();
    
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: 'POST',
            url: "add-to-cart",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType: "dataType",
            success: function (response){
                alert('asdfsadf');
            }
        });
    });
    $('.addToCartBtn2').click(function (e) {
        e.preventDefault();
    
        var product_id = $(this).closest('.product_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            method: 'POST',
            url: "/presets/" + product_id + "/add-to-cart2",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType: "dataType",
            success: function (response){
    
            }
        });
    });
    $('.RemoveFromCartBtn').click(function (e) {
        e.preventDefault()
    
        var product_id = $(this).closest('.cart_data').find('.product_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: "/presets/remove-from-cart/",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            success: function (response){
                //alert('Sldkjfasdlkfjasdlkfjalksdfmjsa');
                $(".cart_data").load(location.href + " .cart_data");
            }
        });
    });
    $("#file_input").on("change", function(e){
        var file = e.target.files;
        console.log(file);
        if (FileReader && file && file.length) {
            var fr = new FileReader();
            fr.onload = function () {
                $('.placeholder-image').attr('src', fr.result);
                $('.profile-image').attr('src', fr.result);
            }
            fr.readAsDataURL(file[0]);
        }

       
       });
});