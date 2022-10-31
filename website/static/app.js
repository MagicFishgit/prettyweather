function loadMap(){
    let params = {
        center: new google.maps.LatLng(53, -6), zoom :4,
        disableDefaultUI: true
    };

    let map = new google.maps.Map(document.getElementById("map-background"), params)
}