document.body.firstElementChild.tabIndex = 1
/**
*#################################
* AMOUNT INPUTS AND LABELS FORMAT
*#################################
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
 * ############
 * DATA TABLES
 * ############
 */
$('#operations_table_desktop').DataTable({
    searching: false,
    lengthMenu: [
        [5, 10, 25, 50, -1],
        [5, 10, 25, 50, "All"]
    ],
    "initComplete": function(settings, json) {
        $('#loadingSpinner2').hide();
    },
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

$('#operations_table_mobile').DataTable({
    searching: false,
    ordering: false,
    lengthMenu: [
        [5, 10, 25, 50, -1],
        [5, 10, 25, 50, "All"]
    ],
    "initComplete": function(settings, json) {
        $('#loadingSpinner3').hide();
    },
    "drawCallback": function(settings) {
        $("#operations_table_mobile thead").remove();
    },
    "pagingType": "full",
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
 * ###############
 *  SETTINGS FORM
 * ###############
 * Update exchange rates from values to form input
 **/
function updateExchangeRates(e, currencyDescription) {
    let exchangeRates = $('#exchange_rates_user_settings').val();
    let exchangeRatesJson = JSON.parse(exchangeRates);
    exchangeRatesJson[currencyDescription] = $(e).val();
    $('#exchange_rates_user_settings').val(JSON.stringify(exchangeRatesJson));
}

/**
 * #################
 *  OPERATION FORMS
 * #################
 * 
 * New Operation saving dropdown visible for all operation types
 * New Operation saving section visible for operation type = 15 (Ingreso)
 */
function verifyOperationTypeDropdown(e, index, version) {
    if ($(e).children("option:selected").val() == '17') {
        $('.generalFromSavingSection').hide();
    } else if ($(e).children("option:selected").val() == '15') {
        $('.generalFromSavingSection').show();
    } else {
        if (version == 'mobile') {
            $("#fromSavingIdMobileEd_" + index).parent().click();
        } else if (version == 'desktop_edit') {
            $("#fromSavingIdEd_" + index).parent().click();
        } else if (version == 'desktop_create') {
            $("#fromSavingId").parent().click();
        }
        $('.generalFromSavingSection').hide();
    }
};

/**
 * Checking for checkbox true to display currency dropdown
 */
$(".savingCheck").parent().click(function() {
    // The classes are before the click, so the condition is negative
    if (!$(".savingCheck").parent().hasClass('btn-success')) {
        $('.operationCurrencySection').show();
    } else {
        $('.operationCurrencySection').hide();
    }
});

/**
 * Check if the checkbox from_saving is not null to show it.
 * @param {boolean} isFromSaving 
 */
function checkSaving(typeId, isFromSaving, loopIndex, isMobile) {
    let locator = "";
    if (isMobile) {
        $("#type_id_" + loopIndex + "_mobile").val(typeId);
        locator = "#fromSavingIdMobileEd_" + loopIndex;
    } else {
        $("#type_id_" + loopIndex).val(typeId);
        locator = "#fromSavingIdEd_" + loopIndex;
    }

    if (isFromSaving) {
        $(locator).bootstrapToggle('on');
    } else {
        $(locator).bootstrapToggle('off');
    }
    
    if (typeId == 15) {
        $('.generalFromSavingSection').show();
    } else {
        if (typeId == 17) {
            $('.operationCurrencySection').show();
        } else {
            $('.operationCurrencySection').hide();

        }

        $('.generalFromSavingSection').hide();
    }
}

/**
 * ##############
 * EXCHANGE FORM
 * ##############
 * 
 * 
* Calculate the amount of the current exchange
*/
 $('#exchangeValueId').keyup(function() {
        var originAmount = 0.0;
        var destinationAmount = 0.0;

        if ($("#originAmountId").val() != "" && $("#originAmountId").val() != undefined &&
            $("#exchangeValueId").val() != "" && $("#exchangeValueId").val() != undefined) {
            originAmount = parseFloat($("#originAmountId").val().replace("$","").replace(",",""));
            destinationAmount = parseFloat($("#exchangeValueId").val().replace("$","").replace(",",""));
    
            if ($("#originDropdownId option:selected").html() == 'ARS' && $("#destinationDropdownId option:selected").html() != 'ARS')  {
                // Divido por que el peso argentino es menor que todo el resto de monedas
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "/"));
    
            } else if (($("#originDropdownId option:selected").html() == 'USD' && $("#destinationDropdownId option:selected").html() == 'EUR') ||
                        ($("#originDropdownId option:selected").html() == 'USD' && $("#destinationDropdownId option:selected").html() == 'GBP')) {
                // Divido por el que dolar es menor al euro y a la libra
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "/"));
    
            } else if (($("#originDropdownId option:selected").html() == 'USD' && $("#destinationDropdownId option:selected").html() == 'ARS')) {
                // Multiplico por que el dolar es mayor al peso argentino
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "*"));
    
            } else if (($("#originDropdownId option:selected").html() == 'EUR' && $("#destinationDropdownId option:selected").html() == 'USD') ||
                        ($("#originDropdownId option:selected").html() == 'EUR' && $("#destinationDropdownId option:selected").html() == 'ARS')) {
                // Multiplico por que el euro es mayor al dolar y al peso
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "*"));
    
            } else if ($("#originDropdownId option:selected").html() == 'EUR' && $("#destinationDropdownId option:selected").html() != 'GBP') {
                // Divido por que el euro es menor a la libra
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "/"));
    
            } else if ($("#originDropdownId option:selected").html() == 'GBP' && $("#destinationDropdownId option:selected").html() != 'GBP') {
                // Multiplico por que la libra es mas grande que todas las monedas
                $("#totalExchangedId").text(operateAndFormat(originAmount, destinationAmount, "*"));
            }

            $("#totalAmountExchanged").val($("#totalExchangedId").text());
        } else {
            $("#totalExchangedId").text(0.0);
        }

        if ($("#totalExchangedId").text() != "0") {
            $(".totalLabel").css("border", "1px solid rgb(11, 168, 63)");
        } else {
            $(".totalLabel").css("border", "none");
        }
 });

 /***
  * Make operation with 2 numbers based on specific operator
  * @returns String formatted with 2 decimals
  */
 function operateAndFormat(number1, number2, operator) {
    var result = 0.0; 

    switch(operator) {
         case "*":
             result = number1 * number2;
             break;
        case "/":
            if (number1 > 0) {
                result = number1 / number2;
            }
            break;
     }

     return result.toFixed(2);
 }

 /***
  * Check that both dropdown have different currencies
  */
 $('#originDropdownId').change(function() {
    controlCurrenciesForExchange();
 });

 $('#destinationDropdownId').change(function() {
    controlCurrenciesForExchange();
});

/***
 * Make exchange currency button disabled if the condition is true
 */
function controlCurrenciesForExchange() {
    if ($("#originDropdownId option:selected").html() == $("#destinationDropdownId option:selected").html()) {
        $("#exchangeCurrencySubmit").prop('disabled', true);
        $("#exchangeCurrencySubmitAsIncome").prop('disabled', true);
    } else {
        $("#exchangeCurrencySubmit").prop('disabled', false);
        $("#exchangeCurrencySubmitAsIncome").prop('disabled', false);
    }
    // Check if destination currency is ARS to use configuration values
    if ($("#destinationDropdownId option:selected").val() == '1') {
        let exchangeVal = $("[name='exchange_rate_" + $("#originDropdownId option:selected").text().toLowerCase() + "']").val()
        $("#exchangeValueId").val(exchangeVal !== 'undefined' ? exchangeVal : "1.0");
    }else {
        $("#exchangeValueId").val("1.0");
    }

    $("#originAmountId").val("");
}

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

$(document).ready(function() {
    $(function() {
        $('[data-toggle="popover"]').popover({
            trigger: 'focus'
        })

        $("#loadingSpinner").hide()
    })
});

function changeResponsiveElements(window) {
    if (window.width() <= 768) {
        $('#currentUserNav').addClass('mt-4 mb-2');
        $('#mobileTitle').removeClass('d-none');
        $('#mobileTitle').addClass('d-block');
        $('.homeChoicesRow').addClass('pl-4');
        $('#customFilterForm').removeClass('form-row');
        $('#customFilterForm').addClass('form');
        $('#customMonthField').removeClass('col-3');
        $('#customMonthField').addClass('col');
        $('#customYearField').removeClass('col-3');
        $('#customYearField').addClass('col');
        $('#customOpTypeField').removeClass('col-3');
        $('#customOpTypeField').addClass('col');
        $('#customFilterSubmit').removeClass('col-3 align-self-end');
        $('#customFilterSubmit').addClass('col');
        $('.custom-info-buttons').removeClass('mr-3');
        $('.custom-info-buttons').addClass('text-center');
        $('.custom-danger-buttons').addClass('text-center');
        $('.iconRow').removeClass('justify-content-center');
        $('.iconRow').addClass('justify-content-end');
        $('.iconContent').removeClass('col-4');
        $('.iconContent').addClass('col-2');
        $('.customDashboardAmountSeparator').removeClass('d-none');
        $('.customDashboardAmountSeparator').addClass('d-block');
        $('[data-toggle="popover"]').removeAttr("data-placement");
        $('[data-toggle="popover"]').attr("data-placement", "bottom");
        $('.savingCard').addClass('col-6');
        $('.savingCard').removeClass('col-4');
    } else {
        $('#currentUserNav').removeClass('mt-4 mb-2');
        $('#mobileTitle').removeClass('d-block');
        $('#mobileTitle').addClass('d-none');
        $('.homeChoicesRow').removeClass('pl-4');
        $('#customFilterForm').removeClass('form');
        $('#customFilterForm').addClass('form-row');
        $('#customMonthField').removeClass('col');
        $('#customMonthField').addClass('col-3');
        $('#customYearField').removeClass('col');
        $('#customYearField').addClass('col-3');
        $('#customOpTypeField').removeClass('col');
        $('#customOpTypeField').addClass('col-3');
        $('#customFilterSubmit').removeClass('col');
        $('#customFilterSubmit').addClass('col-3 align-self-end');
        $('.custom-info-buttons').removeClass('text-center');
        $('.custom-info-buttons').addClass('mr-3');
        $('.custom-danger-buttons').removeClass('text-center');
        $('.iconRow').removeClass('justify-content-end');
        $('.iconRow').addClass('justify-content-center');
        $('.iconContent').removeClass('col-2');
        $('.iconContent').addClass('col-4');
        $('.customDashboardAmountCols').removeClass('col-6');
        $('.customDashboardAmountCols').addClass('col-4');
        $('.customDashboardAmountSeparator').removeClass('d-block');
        $('.customDashboardAmountSeparator').addClass('d-none');
        $('[data-toggle="popover"]').removeAttr("data-placement");
        $('[data-toggle="popover"]').attr("data-placement", "right");
        $('.savingCard').removeClass('col-6');
        $('.savingCard').addClass('col-4');
    }
}
