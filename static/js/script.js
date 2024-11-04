$(document).ready(function() {
    // Функция для получения CSRF-токена из cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Настраиваем AJAX для отправки CSRF-токена
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Обновление корзины
    function cartUpdating(product_id, nmb, is_delete) {
        const data = {
            product_id: product_id,
            nmb: nmb,
            csrfmiddlewaretoken: csrftoken, // Передаем CSRF-токен здесь
        };

        if (is_delete) {
            data["is_delete"] = true;
        }

        const url = $('#form_buying_product').attr("action");

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            success: function(response) {
                console.log("OK");

              // Проверяем, если был удален товар, обновляем страницу
                if (is_delete) {
                    location.reload();
                } else {
                    $('#cart_total_nmb').text("(" + response.products_total_nmb + ")");
                    $('.cart-items tr').html("");

                    $.each(response.products, function(k, v) {
                        $('.cart-items').append(
                            `<tr><td>${v.name}</td><td>${v.nmb}</td><td>${v.price_per_item}</td>
                            <td><a href="#" class="delete-item" data-product_id="${v.id}">Удалить</a></td></tr>`
                        );
                    });
                }
            },
            error: function() {
                console.log("error");
            }
        });
    }

    // Обработчик для добавления товара в корзину
    $('#form_buying_product').on('submit', function(e) {
        e.preventDefault();
        const nmb = $('#number').val();
        const submit_btn = $('#submit_btn');
        const product_id = submit_btn.data("product_id");
        cartUpdating(product_id, nmb, false);
    });

    // Обработчик для удаления товара из корзины
    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        const product_id = $(this).data("product_id");
        cartUpdating(product_id, 0, true);
    });

    // Функция для пересчета общей суммы в корзине
    function calculatingCartAmount(){
        var total_order_amount = 0;
        $('.total-product-in-cart-amount').each(function() {
            var amount = parseFloat($(this).text().replace(',', '.')); // Замена запятой на точку
            if (!isNaN(amount)) {
                total_order_amount += amount;
            }
        });
        $('#total_order_amount').text(total_order_amount.toFixed(2)); // Приведение к 2 десятичным знакам
    }

    // Обработчик для изменения количества товара в корзине
    $(document).on('change', ".product-in-cart-nmb", function(){
        var current_nmb = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text().replace(',', '.')).toFixed(2);

        var total_amount = parseFloat(current_nmb * current_price).toFixed(2);
        current_tr.find('.total-product-in-cart-amount').text(total_amount);

        calculatingCartAmount();
    });

    calculatingCartAmount();
});

