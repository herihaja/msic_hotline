   // hide garment if occupation not garment 		
	function updateGarmentList(){
		 if($("#occupation").val() != "1") {		 
			 $("#garment").val('0');	
			 updateGarmentLocation()
			 $("#garment_section").hide();
		 } else {
		  $("#garment_section").show();
		 }
	 }
	
	 function hideOrShowOtherServices(cb){
		 if ( $("#Other" ).prop( "checked" ) ) {
			 $("#service_other").show();
		 } else {
			 $("#service_other").val(" ");
			 $("#service_other").hide();
		 }
	 }
	 
	 function updateGarmentLocation() {
			var _gps = $("#garment option:selected").attr("class").substring(3);
			$("#gf_gps").val(_gps);
	}

    

	function updateLocalityDistrict(){
		_province = $("#adr_province").val();
		$.ajax({
		    url: '/referral_system/ajaxListLocalityDistrict/',
		    data: { province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option  value='" + dataJson[index].district + "'> ";
					_html +=  dataJson[index].district + " [" + dataJson[index].district_khmer + "]" ;
					_html += "</option> ";
		        });
				$("#adr_district").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function updateLocalityCommune(){
		var _province = $("#adr_province").val();
		var _district = $("#adr_district").val();
		$.ajax({
		    url: '/referral_system/ajaxListLocalityCommune/',
		    data: { district : _district , province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option value='" + dataJson[index].commune + "'> ";
					_html +=  dataJson[index].commune + " [" + dataJson[index].commune_khmer + "]" ;
					_html += "</option> ";
		        });
				$("#adr_commune").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function updateLocalityVillage(){
		var _province = $("#adr_province").val();
		var _district = $("#adr_district").val();
		var _commune  = $("#adr_commune").val();
		
		$.ajax({
		    url: '/referral_system/ajaxListLocalityVillage/',
		    data: { commune : _commune, province : _province, district : _district },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	 dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option  value='" + dataJson[index].village + "'> ";
					_html +=  dataJson[index].village  + " [" + dataJson[index].village_khmer + "]" ;
					_html += "</option> ";
		        });
				$("#adr_village").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	