$(document).ready(function () {
  $.ajax({
      type: 'GET',
      url: '/newsletter/api/users/',
    })

    .done(function (data) {
      for (var i in data) {
        var tableContent = '<tr>';
        tableContent += '<td>' + data[i]['mail'] + '</td>';
        tableContent += '<td>' + data[i]['registration_date'] + '</td>';
        tableContent += '<td>' + data[i]['source'] + '</td>';
        tableContent += '<td>' + data[i]['state'] + '</td>';
        tableContent +='</tr>';
        $('#user-table').append(tableContent);
      }
      $('#user-table').show();
      $('#loading-info').hide();
    });
});
