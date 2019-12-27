document.body.firstElementChild.tabIndex = 1

/**
 * *******************************
 * AMOUNT INPUTS AND LABELS FORMAT
 * *******************************
 */

$("input[data-type='currency']").on({
    keyup: function() {
        formatCurrency($(this));
    },
    blur: function() {
        formatCurrency($(this), "blur");
    }
});

function formatNumber(n) {
    // format number 1000000 to 1,234,567
    return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

function formatCurrency(input, blur) {
    // appends $ to value, validates decimal side
    // and puts cursor back in right position.

    // get input value
    var input_val = input.val();

    // don't validate empty input
    if (input_val === "") { return; }

    // original length
    var original_len = input_val.length;

    // initial caret position 
    var caret_pos = input.prop("selectionStart");

    // check for decimal
    if (input_val.indexOf(".") >= 0) {

        // get position of first decimal
        // this prevents multiple decimals from
        // being entered
        var decimal_pos = input_val.indexOf(".");

        // split number by decimal point
        var left_side = input_val.substring(0, decimal_pos);
        var right_side = input_val.substring(decimal_pos);

        // add commas to left side of number
        left_side = formatNumber(left_side);

        // validate right side
        right_side = formatNumber(right_side);

        // On blur make sure 2 numbers after decimal
        if (blur === "blur") {
            right_side += "00";
        }

        // Limit decimal to only 2 digits
        right_side = right_side.substring(0, 2);

        // join number by .
        input_val = "$" + left_side + "." + right_side;

    } else {
        // no decimal entered
        // add commas to number
        // remove all non-digits
        input_val = formatNumber(input_val);
        input_val = "$" + input_val;

        // final formatting
        if (blur === "blur") {
            input_val += ".00";
        }

        $(this).next().focus();
    }

    // send updated string to input
    input.val(input_val);

    // put caret back in the right position
    var updated_len = input_val.length;
    caret_pos = updated_len - original_len + caret_pos;
    input[0].setSelectionRange(caret_pos, caret_pos);
}

/**
 * ###########
 * DATA TABLES
 * ###########
 */

$('#operations_table').DataTable({
    searching: false,
    lengthMenu: [
        [5, 10, 25, 50, -1],
        [5, 10, 25, 50, "All"]
    ],
    "language": {
        "lengthMenu": "Mostrar _MENU_ registros por página",
        "zeroRecords": "No se han encontrado registros",
        "info": "Página _PAGE_ de _PAGES_",
        "infoEmpty": "",
        "infoFiltered": "(filtrado de _MAX_ total registros)",
        "oPaginate": {
            "sFirst": "Primero",
            "sLast": "Último",
            "sNext": "Siguiente",
            "sPrevious": "Anterior"
        }
    },
    "dom": '<"row justify-content-start"<"col text-left"l>>rt<"row justify-content-between"<"col text-left"i><"col text-right"p>>'
});

/**
 ********************
 * RESPONSIVE CLASSES
 ********************
 */

$(window).on({
    load: function() {
        changeResponsiveElements($(this));
    },
    resize: function() {
        changeResponsiveElements($(this));
    }
});

function changeResponsiveElements(window) {
    if (window.width() < 768) {
        $('.homeChoicesRow').removeClass('mr-5');
        $('.homeChoicesRow').addClass('pl-4');
        $('#monthInfoTitle').removeClass('col-4');
        $('#monthInfoTitle').addClass('col-6');
        $('#customFilterForm').removeClass('form-row');
        $('#customFilterForm').addClass('form');
        $('#customMonthField').removeClass('col-4');
        $('#customMonthField').addClass('col');
        $('#customOpTypeField').removeClass('col-4');
        $('#customOpTypeField').addClass('col');
        $('#customFilterSubmit').removeClass('col-4 align-self-end');
        $('#customFilterSubmit').addClass('col');
        $('#operations_table').removeClass('table-striped');
        $('.custom-info-buttons').removeClass('mr-3');
        $('.custom-info-buttons').addClass('text-center');
        $('.custom-danger-buttons').addClass('text-center');
        $('.iconRow').removeClass('justify-content-center');
        $('.iconRow').addClass('justify-content-end');
        $('.iconContent').removeClass('col-4');
        $('.iconContent').addClass('col-2');
    } else {
        $('.homeChoicesRow').addClass('mr-5');
        $('.homeChoicesRow').removeClass('pl-4');
        $('#monthInfoTitle').removeClass('col-6');
        $('#monthInfoTitle').addClass('col-4');
        $('#customFilterForm').removeClass('form');
        $('#customFilterForm').addClass('form-row');
        $('#customMonthField').removeClass('col');
        $('#customMonthField').addClass('col-4');
        $('#customOpTypeField').removeClass('col');
        $('#customOpTypeField').addClass('col-4');
        $('#customFilterSubmit').removeClass('col');
        $('#customFilterSubmit').addClass('col-4 align-self-end');
        $('#operations_table').addClass('table-striped');
        $('.custom-info-buttons').removeClass('text-center');
        $('.custom-info-buttons').addClass('mr-3');
        $('.custom-danger-buttons').removeClass('text-center');
        $('.iconRow').removeClass('justify-content-end');
        $('.iconRow').addClass('justify-content-center');
        $('.iconContent').removeClass('col-2');
        $('.iconContent').addClass('col-4');
    }
}