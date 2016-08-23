$(document).ready(function() {
  $('#get-data').click(function() {
    var showImagesData = $('#show-images-data');


    $.getJSON('http://127.0.0.1:5000/img/api/v1.0/images', function (data) {
      console.log(data);

      var items = data.images.map(function(item) {
        return item.title + ': ' + item.url;
      });
      showImagesData.empty();

      if (items.length) {
        var content = '<li>' + items.join('</li><li>') + '</li>';
        var list = $('<ul />').html(content);
        showImagesData.append(list);
      }
    });
    showImagesData.text('Loading the JSON file.');
  })
  // $('#put-data').click(function() {
  //   var putImageData = $('#put-image-data');
  //     $.getJSON('http://127.0.0.1:5000/img/api/v1.0/images/3', function (data) {
  //     console.log(data);
  //
  //     var items = data.images.map(function(item) {
  //       return item.title + ': ' + item.url;
  //     });
  //     showImagesData.empty();
  //
  //     if (items.length) {
  //       var content = '<li>' + items.join('</li><li>') + '</li>';
  //       var list = $('<ul />').html(content);
  //       showImagesData.append(list);
  //     }
  //   });
  //   showImagesData.text('Loading the JSON file.');
  // })
  $('#delete-data').click(function() {
    var deleteImageData = $('#delete-image-data');
      $.ajax({
      url: 'http://127.0.0.1:5000/img/api/v1.0/images/3',
      type: 'DELETE',
      success: function(result) {
        console.log(result);
        return "success"
        }
      });
      showImagesData.text('Loading the JSON file.');
    })
});
