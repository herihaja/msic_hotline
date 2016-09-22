$(document).ready(function(){
    var fac_selector = $("#id_facility_id").parent().parent();
    var garment_selector = $("#id_garment_id").parent().parent();
    var facility_garment = $("#id_facility_id, #id_garment_id").parent().parent();
    $("#id_group").change(function(){
        var selected = $(this).find("option:selected").text();
        facility_garment.hide();
        if (selected == "Garment Factory") {
            garment_selector.show();
        } else if ( selected == "QAN Facility") {
            fac_selector.show();
        }
    }).trigger("change");
    
});