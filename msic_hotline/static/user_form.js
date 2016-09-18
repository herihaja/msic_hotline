$(document).ready(function(){
    var fac_selector = $("#id_facility_id, label[for='id_facility_id']");
    $("#id_group").change(function(){
        var selected = $(this).find("option:selected").text();

        if (["Garment Factory", "QAN Facility"].indexOf(selected) == -1) {
            fac_selector.hide();
        } else {
            fac_selector.show();
        }
    }).trigger("change");
    
});