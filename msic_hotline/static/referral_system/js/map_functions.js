
var geocoder = null;
var map = null;
var direction;
var panel = document.getElementById('direction-panel');
var customerMarker = null;
var listeMarkers = _markers;
var markers = [];
var closest = [];
var referredServices = [];
var map;
var address_icon = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
var countryName = "Cambodia";
var garment_icon = "/referral_system/static/referral_system/css/pointer_factory green_2.png";

var address = "";

$(function($) {
    // Asynchronously Load the map API 
    var script = document.createElement('script');

    script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyDA3bMv4Elg98PcjCZkd5LiqqbzoaQ5e1Y&callback=initialize&libraries=geometry,places";
    document.body.appendChild(script);
});

function initialize() {
	geocoder = new google.maps.Geocoder();
    
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };
                    
    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);
    
    geocoder.geocode( { 'address': countryName }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
        } else {
            alert("Could not find location: " + location);
        }
    });
        
    // Multiple Markers
                        
    // Info Window Content
    var infoWindowContent = _infoWindowContent;
        
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    
    // Loop through our array of markers & place each one on the map  
    for( i = 0; i < listeMarkers.length; i++ ) {
        var position = new google.maps.LatLng(listeMarkers[i][1], listeMarkers[i][2]);
        bounds.extend(position);
        if(listeMarkers[i][21] == 'Garment factory infirmary' ) {
        	marker = new google.maps.Marker({
                position: position,
                map: map,
                icon: garment_icon,
                title: listeMarkers[i][19]
            });
        } else {
        	marker = new google.maps.Marker({
                position: position,
                map: map,
                title: listeMarkers[i][19]
            });
        }
        
        /*
        marker = new google.maps.Marker({
            position: pt,
            map: map,
            icon: locations[i][5],
            address: locations[i][2],
            title: locations[i][0],
            html: locations[i][0] + "<br>" + locations[i][2]
        });
        */
        markers.push(marker);
        
        // Allow each marker to have an info window    
        
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
            	selectClickedMarker(i);
                //infoWindow.setContent(infoWindowContent[i][0]);
                //infoWindow.open(map, marker);
            }
        })(marker, i));
        

        // Automatically center the map fitting all markers on the screen
         map.fitBounds(bounds);
    }

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        //this.setZoom(16);
        //google.maps.event.removeListener(boundsListener);
    });

    google.maps.event.addListenerOnce(map, 'idle', function(){
        // do something only the first time the map is loaded
        map.setZoom(7);
    });
    

    
}

function clearRoute(){
	if (direction != null) {
		direction.setMap(null);
		direction = null;
	}
	$("#direction-panel").html(" ");
	$("#selected-panel").html(" ");
	$("#id_selected_facility").val("");
	$("#btn-itineraire").hide();
}

function clearRouteAndFacility(){
	clearRoute();
	direction = new google.maps.DirectionsRenderer({
        map   : map, 
        panel : panel,
        suppressMarkers: true
    });
}

function getCheckedServices(){
	referredServices = [];
	$(".cb_services").each(function () {
		if (this.checked) {
			referredServices.push($( this ).val());
	    }
	});
	//alert(JSON.stringify(referredServices));
}
function codeAddress() {
	clearRouteAndFacility();
	getCheckedServices();
	
	// cr = client residence
	// gf = garment factory
	var search_type = $( "input:radio[name='searchtype']:checked" ).val();
	var infoWindow = new google.maps.InfoWindow();
	
	
	if(search_type == 'cr') {
		address = document.getElementById('adr_street').value;
        address += checkAndConcat(document.getElementById('adr_village').value);
        address += checkAndConcat(document.getElementById('adr_commune').value);
        address += checkAndConcat(document.getElementById('adr_district').value);
        address += checkAndConcat(document.getElementById('adr_province').value);
	} else {
		address = document.getElementById('gf_gps').value;
        if (!address) {
            alert("Please select a Garment Factory");
            return false;
        }
	}
    
    geocoder.geocode({
        'address': address //start point of the itinerary
    }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            if (customerMarker) customerMarker.setMap(null);
            
            if(search_type == 'gf') {
            	iconAddress = garment_icon;
            } else {
            	iconAddress = address_icon;
            }
            customerMarker = new google.maps.Marker({
                map: map,
                icon: iconAddress,
                position: results[0].geometry.location
            });
            
            if(search_type == 'gf') {
            	var garment_name = $("#garment option:selected"). text();
            	google.maps.event.addListener(customerMarker, 'click', (function(customerMarker, i) {
                    return function() {
                        infoWindow.setContent(garment_name);
                        infoWindow.open(map, customerMarker);
                    }
                })(customerMarker, i));
            }
            
            
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            var numResults = parseInt(document.getElementById('numberResults').value);
            closest = findClosestN(results[0].geometry.location, numResults);
            
            bounds_2 = new google.maps.LatLngBounds();
            bounds_2.extend(customerMarker.getPosition());
            
            var _closest_div = "";
            for (var i = 0; i < closest.length; i++) {
                closest[i].setMap(map);
                bounds_2.extend(closest[i].getPosition());
                
                
                var dist_km = Math.round(closest[i].distance / 1000).toFixed(2);
                
                //populate div
                _closest_div += "<li class='list-closest-marker' onclick='animateSpecificMarker(" + closest[i].distance+ ")'>" + closest[i].title + " </li>" ;
                //_closest_div += "<li class='list-closest-marker' onclick='animateSpecificMarker(" + closest[i].distance+ ")'>" + closest[i].title + " [" + dist_km +  "km ] </li>" ;
                
            }
            if(closest.length > 0) {
            	$("#closest-fac-div").html("<h6>Closest Facilities</h6><ol>" + _closest_div + "</ol>");
            }
            map.fitBounds(bounds_2);
        } else {
            alert("Please select at least a Province")
            //alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function filterFacilityByServices(){	
	
	filteredMarkersIndex = [];
	for (var i = 0; i < listeMarkers.length; i++) {
		facilityServices = listeMarkers[i][20].split(",");
		serviceFound = 0;
		
		for (var j = 0; j < referredServices.length; j++) {
			if(facilityServices.indexOf(referredServices[j]) > -1){
				serviceFound++ ;
			}
		}
		if(serviceFound > 0 || referredServices.length == 0){
			filteredMarkersIndex.push(i);
		}		
	}
	return filteredMarkersIndex;
}

function findClosestN(pt, numberOfResults) {
	filteredMarkersIndex = filterFacilityByServices();
    var closest = [];
    for (var i = 0; i < filteredMarkersIndex.length; i++) {
    	j = filteredMarkersIndex[i];
        markers[j].distance = google.maps.geometry.spherical.computeDistanceBetween(pt, markers[j].getPosition());
        markers[j].setMap(null);
        closest.push(markers[j]);
    }
    closest.sort(sortByDist);
    return closest.splice(0,numberOfResults);
}

function sortByDist(a, b) {
    return (a.distance - b.distance)
}

function selectClickedMarker(_index){
	
	for (var i = 0; i < markers.length; i++) {
		markers[i].setAnimation(null);
    }
	markers[_index].setAnimation(google.maps.Animation.BOUNCE);
	//calculate(markers[_index].getPosition());
	//clearRoute();
	displaySelectedFacility(_index);
	//$("#btn-itineraire").show();
}

function animateSpecificMarker(_distance) {
	_index = 0 ;
	for (var i = 0; i < markers.length; i++) {
        if(markers[i].distance == _distance) {
        	markers[i].setAnimation(google.maps.Animation.BOUNCE);
        	_index = i ;
        } else {
        	markers[i].setAnimation(null);
        }
    }
	calculate(markers[_index].getPosition());
	displaySelectedFacility(_index);
	$("#btn-itineraire").show();
}

function calculate(_destination){
    origin      = customerMarker.getPosition(); // Le point départ
    destination = _destination; // Le point d'arrivé
    if(origin && destination){
        var request = {
            origin      : origin,
            destination : destination,
            travelMode  : google.maps.DirectionsTravelMode.WALKING // Type de transport
        }
        var directionsService = new google.maps.DirectionsService(); // Service de calcul d'itinéraire
        directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
            if(status == google.maps.DirectionsStatus.OK){
                direction.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
            }
        });
    } //http://code.google.com/intl/fr-FR/apis/maps/documentation/javascript/reference.html#DirectionsRequest
};

function displaySelectedFacility(_index){
	var _selectedMarker = listeMarkers[_index] ;
	var _html_selected = "";
	
	_html_selected += " <span class='round label warning'><h6>" + _selectedMarker[19] + " <br/>" + _selectedMarker[0] + "</h6></span>";	
	
	_html_selected += "<h6>Address [KHMER]</h6>";
	_html_selected += "<p>" + _selectedMarker[18] + " ";
	_html_selected += "" + _selectedMarker[17] + " ";
	_html_selected += "" + _selectedMarker[16] + " ";
	_html_selected += "" + _selectedMarker[15] + " ";
	_html_selected += "" + _selectedMarker[14] + "</p> ";
	
	_html_selected += "<h6>Address [EN]</h6>";
	_html_selected += "<p>" + _selectedMarker[3] + " ";
	_html_selected += "" + _selectedMarker[4] + " ";
	_html_selected += "" + _selectedMarker[5] + " ";
	_html_selected += "" + _selectedMarker[6] + " ";
	_html_selected += "" + _selectedMarker[7] + "</p> ";
	
	_html_selected += "<h6>Telephones</h6>";
	_html_selected += "<p>" + _selectedMarker[8] + "</p>";
	_html_selected += "<h6>Opening Hours</h6>";
	_html_selected += "<p>" + _selectedMarker[9] + "</p>";
	_html_selected += "<h6>Available Services</h6>";
	_html_selected += "<p><b>Referred Services: </b>" + textToBulletList(_selectedMarker[20]) + "</p>";
	
	//alert(_selectedMarker[13]);
	$("#id_selected_facility").val(_selectedMarker[13]);
	$("#selected-panel").html(_html_selected);
	
}

function checkAndConcat(input) {
    if (input != "0" && input.length) {
        return " " + input;
    }
    return "";
}
