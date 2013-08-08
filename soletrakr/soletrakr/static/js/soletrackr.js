var user="sbuggay@gmail.com";
var api_key="95ff842a18a75c2c4898a1e2e45ccb782e44dcf4";
// var user;
// var api_key;
var map = new GMaps({
   div: '#map',
   lat: 32.605615,
   lng: -85.493685
 });
var devices = new Array();

function get_devices() {
  $.ajax({
    type: "GET",
    contentType: "application/json",
    url: "http://www.altoidengineer.com/api/devices/?username=" + user + "&api_key=" + api_key,
    data: "{}",  
    dataType: "jsonp",
    success: function(data) {
      for (var i=0, len=data.devices.length; i < len; i++) {
        devices.push(map.createMarker({
          lat: data.devices[i].location.coordinates[0],
          lng: data.devices[i].location.coordinates[1],
          title: data.devices[i].given_name,
          color: 'blue',
          infoWindow: {
            content: data.devices[i].given_name
          }
        }));
      }
      map.addMarkers(devices);
    },
    error: function (xhr, desc, err) {
      alert(desc);
      alert(err);
    }
  });
}

$(document).on('click', '.pan-to-marker', function(e) {
  e.preventDefault();
  var lat, lng;
  var $index = $(this).data('marker-index');
  var $lat = $(this).data('marker-lat');
  var $lng = $(this).data('marker-lng');
  if ($index != undefined) {
    // using indices
    var position = map.markers[$index].getPosition();
    lat = position.lat();
    lng = position.lng();
  }
  map.setCenter(lat, lng);
});


$(document).ready(function(){
  Dajaxice.users.set_user(Dajax.process);
  map.addControl({
    position: 'top_right',
    content: 'Center on you',
    style: {
      margin: '5px',
      padding: '1px 6px',
      border: 'solid 1px #717B87',
      background: '#fff'
    },
    events: {
      click: function(){
        GMaps.geolocate({
          success: function(position) {
            map.setCenter(position.coords.latitude, position.coords.longitude);
          },
          error: function(error) {
            alert('Geolocation failed: '+error.message);
          },
          not_supported: function() {
            alert("Your browser does not support geolocation");
          },
          always: function() {
          }
        });
      }
    }
  });

  get_devices();

  GMaps.on('marker_added', map, function(marker) {
    $('#markers-with-index').append('<li><a href="#" class="pan-to-marker" data-marker-index="' + map.markers.indexOf(marker) + '">' + marker.title + '</a></li>');
  });


});


