// todo: Add MicroInteractions to all add to Cart Buttons
$('.search-query').keypress(function (e) {
    let key = e.which;
    if (key === 13) {
        $('.search-query').submit()
    }
})

function update_side_cart(book_id) {
    let book_data = {
        'book_id': book_id,
    }
    $.ajax({
        url: '/app/side_cart/',
        data: book_data,
        dataType: 'json',
        success: function (response) {
            $('.holder').html(response.data)
        }

    })
}


// Checks the cart is empty data in session storag as a function
function check_cart() {
    $.ajax({
        url: '/app/check_cart/',
        dataType: 'json',

        success: function (response) {
            sessionStorage.setItem('cart_is_empty', response.data.cart_is_empty)
        }
    })

    let dataFromSession = sessionStorage.getItem('cart_is_empty');
    if (Number(dataFromSession) === 0) {
        $('.cart-not-empty').show()
    } else {
        $('.cart-not-empty').hide()
    }
}

// frequently checks if the cart is empty
setInterval(check_cart, 1000)


//filter js
$(document).ready(function () {
    $(".filter-checkbox, #filterBtn, #radio").on("click", function () {

        let filter_object = {}

        let min_price = $('#min_price').val()
        let max_price = $('#max_price').val()
        filter_object['min_price'] = min_price
        filter_object['max_price'] = max_price

        let radios = document.querySelectorAll("#radio")
        let radio_value = true
        radios.forEach(radio => {
            if (radio.checked) {
                radio_value = radio.value
            }
        })
        filter_object['radio'] = radio_value

        $('.filter-checkbox').each(function () {
            let filter_key = $(this).data('filter')

            filter_object[filter_key] = Array.from(document.querySelectorAll(`input[data-filter='${filter_key}']:checked`)).map(function (element) {
                return element.value
            })
        })

        $.ajax({
            url: '/app/filter/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log('Sending Data>>>>>>>')
            },
            success: function (response) {
                $('#filtered-products').html(response.data)
            }
        })
    })

    $("#m_filterBtn, .filter-checkbox, #radio").on("click", function () {
        let filter_object = {}

        let min_price = $('#m_min_price').val()
        let max_price = $('#m_max_price').val()
        filter_object['min_price'] = min_price
        filter_object['max_price'] = max_price

        let radios = document.querySelectorAll("#radio")
        let radio_value = true
        radios.forEach(radio => {
            if (radio.checked) {
                radio_value = radio.value
            }
        })
        filter_object['radio'] = radio_value

        $('.filter-checkbox').each(function () {
            let filter_key = $(this).data('filter')

            filter_object[filter_key] = Array.from(document.querySelectorAll(`input[data-filter='${filter_key}']:checked`)).map(function (element) {
                return element.value
            })
        })

        $.ajax({
            url: '/app/filter/',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log('Sending Data>>>>>>>');
            },
            success: function (response) {
                $('#filtered-products').html(response.data)
            }
        })
    })

    // For Price Range Filter
    $("#max_price, #m_max_price").on("blur", function () {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert(`Please enter a price between ${min_price} and ${max_price}`)
            $(this).val(max_price)
            $('#range').val(min_price)
            return false
        }
    })

    $("#min_price, #m_min_price").on("blur", function () {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert(`Please enter a price between ${min_price} and ${max_price}`)
            $(this).val(min_price)
            $('#range').val(min_price)
            return false
        }
    })

//     Add to Cart Button
    $('#add_to_cart_btn').on('click', function () {
        let book_id = $(this).data('id')
        let book_price = $(this).data('price')
        let book_title = $(this).data('title')
        let book_image = $(this).data('image')
        let book_author = $(this).data('author')
        let book_category = $(this).data('category')
        let quantity = $('#quan').val()
        let book_data = {
            'book_id': book_id,
            'book_price': book_price,
            'book_title': book_title,
            'book_image': book_image,
            'book_author': book_author,
            'book_category': book_category,
            'quantity': quantity
        }

        $.ajax({
            url: $(this).data('url'),
            data: book_data,
            dataType: "json",
            beforeSend: function () {
                console.log("Adding Product to Cart")
            },
            success: function (response) {
                console.log("Added Product to Cart!!")
                // get the text in the span element under the add to cart button and change it to "Book Added to Cart"
                cart_button_span = document.querySelector('#add_to_cart_btn span')
                cart_button_span.innerHTML = "Book Added to Cart"
                $('.cart-not-empty').show()
                update_side_cart(book_data.book_id)
            }
        })
    })

    $(document).on('click', '#cart_btn', function () {
        let quantity = 1
        let book_id = $(this).data('id')
        let book_price = $(this).data('price')
        let book_title = $(this).data('title')
        let book_image = $(this).data('image')
        let book_author = $(this).data('author')
        let book_category = $(this).data('category')

        let book_data = {
            'book_id': book_id,
            'book_price': book_price,
            'book_title': book_title,
            'book_image': book_image,
            'book_author': book_author,
            'book_category': book_category,
            'quantity': quantity
        }

        $.ajax({
            url: $(this).data('url'),
            data: book_data,
            dataType: "json",
            success: function (response) {
                // get the text in the span element under the add to cart button and change it to "Book Added to Cart
                update_side_cart(book_data.book_id)
            }
        })
    })


    // Use event delegation for dynamically added elements
    $(document).on('click', '#cart_quan', function () {
        let quantity = $(`#${$(this).data('id')}`).val()
        let book_id = $(this).data('id')

        let book_data = {
            'book_id': book_id,
            'quantity': quantity
        }
        console.log(book_data)

        $.ajax({
            url: '/app/update_cart/',
            data: book_data,
            dataType: "json",
            beforeSend: function () {
                console.log("Increasing Product Quantity in Cart")
            },
            success: function (response) {
                $('.the-cart').html(response.data);
                update_side_cart(book_data.book_id)

                // Re-attach the click event after updating the content
                $('#cart_quan').off('click').on('click', function () {
                    // Your existing click event logic here
                });
            }
        });
    });

    $(document).on('click', '.delete-item', function () {
        let book_id = $(this).data('item')
        let book_data = {
            'book_id': book_id
        }

        $.ajax({
            url: '/app/delete_cart_item/',
            data: book_data,
            dataType: "json",
            beforeSend: function () {
                console.log("Successfully Deleted..")
            },
            success: function (response) {
                $('.the-cart').html(response.data);
                update_side_cart(book_data.book_id)

            }
        })
    })
})
