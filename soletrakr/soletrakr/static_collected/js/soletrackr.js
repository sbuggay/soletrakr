// show login modal
// $(window).load(function(){
// 	$('#myModal').modal('show');
// });


function get_devices() {
  var url = 'http://www.altoidengineer.com/api/devices/?format=json&username=sbuggay@gmail.com&api_key=95ff842a18a75c2c4898a1e2e45ccb782e44dcf4';

  $.get(url, function(data,status) {
    alert(data);
    alert(status);
  });
}

function set_map() {
  var map = new GMaps({
  	div: '#map',
  	lat: -12.043333,
  	lng: -77.028333
  });
  var devices = new Array();

  // Loop this shit.
  devices[0] = map.createMarker({
    lat: -12.043333,
    lng: -77.028333,
    title: 'Marker',
    click: function(e) {
      $(this).lat = -12.06,
      $(this).lng = -77.05
    }
  });
  //
  map.addMarkers(devices);

  var latlng = new google.maps.LatLng(-12.05, -77.03);
  devices[0].setPosition(latlng)
}