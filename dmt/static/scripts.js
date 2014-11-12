var resource;

var list_template = '<ul id="files_list"></ul>';

var edit_template = function(data){
  var print_input = function(label, value, name){
    return '<label>' + label + ':</label><input type="text" value="' + value + '" name="' + name + '">';
  };
  var has_perms = function(){
    var _user_id = data.owner.split('/');
    _user_id = _user_id[_user_id.length - 2] * 1;
    if (user_id == _user_id){
      return '' +
          '<button type="submit">Update</button>' +
          '<button type="submit" id="delete" value="' + data.resource_uri + '">Delete</button>';
    }
    return '';
  };
  return '' +
      '<form id="update">' +
        '<h3>Created: ' + data.date + '</h3>' +
        print_input('Type', data.type, 'type') +
        '<h4>Size: ' +  data.size + '</h4>' +
        '<button type="submit" id="return">Return</button>' +
        has_perms() +
      '</form>';
};

var list = function(){
  resource = "/api/v1/file/";
  $('#page-title').html('Files list');
  $('#content').html(list_template);
  $.ajax({
    url: "/api/v1/file/" + meta,
    success: function(data) {
      if (data.hasOwnProperty('objects')) {
        var l = data.objects.length;
        if (l > 0) {
          for (var i=0; i<l; i++){
            var o = data.objects[i];
            $('#files_list').append('' +
                '<li>' +
                  '<a class="api_link" href="' + o.resource_uri + '">' +
                    o.type + ' : ' + o.date +
                  '</a>' +
                '</li>'
            );
          }

        } else {
          $('#files_list').append('<li>List is empty.</li>');
        }
      } else {
        $('#files_list').append('<li>Something goes wrong.</li>');
      }
    },
    error: function() {
      $('#files_list').append('<li>error</li>');
    }
  });
};

var edit = function(resource_uri){
  resource = resource_uri;
  $.ajax({
    url: resource + meta,
    type: "GET",
    success: function(data) {
      $('#page-title').html('File');
      $('#content').html(edit_template(data));
    }
  });
};

var create = function(data){
  $.ajax({
    url: "/api/v1/file/" + meta,
    type: "POST",
    dataType: "json",
    processData: false,
    data: JSON.stringify(data),
    success: function(data) {
      var files_list = $('#files_list');
      if (files_list.text()) {
        files_list.append('<li><a class="api_link" href="' + data.resource_uri + '">' + data.type + '</a></li>');
      } else {
        edit(data.resource_uri);
      }
    }
  });
};

var update = function(resource_uri, data){
  $.ajax({
    url: resource_uri + meta,
    type: "PUT",
    dataType: "json",
    processData: false,
    data: JSON.stringify(data)
  });
};

var _delete = function(resource_uri){
  $.ajax({
    url: resource_uri + meta,
    type: "DELETE",
    dataType: "json",
    processData: false,
    success: function() {
      list();
    }
  });
};

$(document).ready(function(){
  $('body').on('submit', '#upload_file', function(event){
    event.preventDefault();
    var data = {'type': this.type.value};
    create(data);
  });

  $('body').on('click', 'a.api_link', function(event){
    event.preventDefault();
    edit(this.href);
  });

  $('body').on('click', '#return', function(event){
    event.preventDefault();
    list();
  });

  $('body').on('submit', '#update', function(event){
    event.preventDefault();
    var data = {'type': this.type.value};
    update(resource, data);
  });

  $('body').on('click', '#delete', function(event){
    event.preventDefault();
    _delete(this.value);
  });

  list();
});