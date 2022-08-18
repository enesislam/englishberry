//card
$("#id_card_owner").val("Test Tester");
$("#id_card_number").val("5555 5555 5555 5555");
$("#id_card_expiry").val("12/25");
$("#id_card_cvc").val("225");

//contact
$("#id_email").val(`test${Math.floor(Math.random() * 999) + 1}@gmail.com`);
$("#id_phone").val(`555${Math.floor(Math.random() * 9999999) + 1}`);
$('option[value="90"]').attr("selected", "selected");
$("#id_phone_code").trigger("change");

//find passenger count
count_pas =  $("label[for*='_surname']").length;

//passenger
for (var i = 0; i < count_pas; i++) {
    $("#id_passengers_" + i + "_name").val("Test");
    $("#id_passengers_" + i + "_surname").val("Tester");
    $('option[value="90"]').attr("selected", "selected");
    $("#id_passengers_" + i + "_birth_date").val("1989-03-16");
    $("#id_passengers_" + i + "_man").prop("checked", true);
    $("#id_passengers_" + i + "_foregein_citizen").click();
    $("#id_passengers_" + i + "_passport").val(`U${Math.floor(Math.random() * 99999999) + 1}`);
    $("#id_passengers_" + i + "_passport_expiry_date").val("2028-12-12");
}
$("#id_condition").prop("checked", true);
