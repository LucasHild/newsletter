$(document).ready(function () {
  $('.input-field').keyup(function () {
    var id = $(this).attr('id');
    var value = $(this).val();

    // Get section
    if ((id.indexOf('blog') > -1)) {
      var section = 'blog';
    } else if ((id.indexOf('top') > -1)) {
      var section = 'top';
    } else if ((id.indexOf('introduction') > -1)) {
      $('.lucas-newsletter #introduction').text(value);
      return true;
    }

    // Get number
    var expression = /[1-9]/gi;
    var number = id.match(expression)[0];

    // Set value
    if ((id.indexOf('heading') > -1)) {
      $('.lucas-newsletter #' + section + '-article-' + number + ' h4').text(value);
    } else if ((id.indexOf('image') > -1)) {
      $('.lucas-newsletter #' + section + '-article-' + number + ' img').attr('src', value);
    } else if ((id.indexOf('summary') > -1)) {
      $('.lucas-newsletter #' + section + '-article-' + number + ' p').text(value);
    } else if ((id.indexOf('link') > -1)) {
      $('.lucas-newsletter #' + section + '-article-' + number + ' a').attr('href', value);
    }

    showAndHideArticles();
  });

  function showAndHideArticles() {
    var sections = ['blog', 'top'];

    // For blog and top
    for (var i in sections) {
      var section = sections[i];

      // Set length of articles
      if (section == 'blog') {
        var numbers = 4;
      } else if (section == 'top') {
        var numbers = 3;
      }

      // For every article
      for (var j = 0; j < numbers; j++) {
        var number = j + 1;
        var hasContent = false;

        var types = ['heading', 'image', 'summary', 'link'];

        // For every input field of one article
        for (var k in types) {
          var type = types[k];

          // If input has value
          if ($('#' + section + '-article-' + number + '-' + type).val()) {
            hasContent = true;
          }
        }

        if (hasContent) {
          // Show article
          $('.lucas-newsletter #' + section + '-article-' + number).css('display', 'block');

          // Show it, because MS Outlook doesn't support display: none
          $('.lucas-newsletter #' + section + '-article-' + number).css('width', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('max-height', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('overflow', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('mso-hide', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('height', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('font-size', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('line-height', 'initial');
          $('.lucas-newsletter #' + section + '-article-' + number).css('margin', 'initial');
        } else {
          // Hide article
          $('.lucas-newsletter #' + section + '-article-' + number).css('display', 'none');

          // Hide it, because MS Outlook doesn't support display: none
          $('.lucas-newsletter #' + section + '-article-' + number).css('width', '0px');
          $('.lucas-newsletter #' + section + '-article-' + number).css('max-height', '0px');
          $('.lucas-newsletter #' + section + '-article-' + number).css('overflow', 'hidden');
          $('.lucas-newsletter #' + section + '-article-' + number).css('mso-hide', 'all');
          $('.lucas-newsletter #' + section + '-article-' + number).css('height', '0');
          $('.lucas-newsletter #' + section + '-article-' + number).css('font-size', '0');
          $('.lucas-newsletter #' + section + '-article-' + number).css('line-height', '0');
          $('.lucas-newsletter #' + section + '-article-' + number).css('margin', '0');

        }
      }
    }
  }

  $('#send-test-mail').click(function () {
    // Get HTML
    var html = $('#output-area').html();

    // Change button text
    $('#send-test-mail').text('Nachricht wird verschickt ...');

    // Post data to api
    $.ajax({
        data: {
          html: $('#output-area').html(),
          type: 'test'
        },
        type: 'POST',
        url: '/newsletter/api/send/',
      })

      .done(function (data) {
        if (data.success) {
          // Change button text
          $('#send-test-mail').text('Mail gesendet');
          // Change button text after 3 seconds
          setTimeout(function functionName() {
            $('#send-test-mail').text('Sende Test Mail');
          }, 3000);
        } else {
          // Change button text
          $('#send-test-mail').text('Fehler beim Versenden');
          // Change button text after 3 seconds
          setTimeout(function functionName() {
            $('#send-test-mail').text('Sende Test Mail');
          }, 3000);

          // If API sent error show it
          if (data.error) {
            alert(data.error);
          }
        }
      });
  });

  $('#send-mail').click(function () {
    // Get HTML
    var html = $('#output-area').html();

    // Verify
    if (prompt('Überprüfung: Schreibe "Ich bin mir sicher, dass ich diese Mail schicken möchte!"') != 'Ich bin mir sicher, dass ich diese Mail schicken möchte!') {
      // Stop function
      return false;
    }

    // Change button text
    $('#send-mail').text('Nachricht wird verschickt ...');

    // Post data to api
    $.ajax({
        data: {
          html: $('#output-area').html(),
          type: 'all'
        },
        type: 'POST',
        url: '/newsletter/api/send/',
      })

      .done(function (data) {
        if (data.success) {
          // Change button text
          $('#send-mail').text('Mail gesendet');
          // Change button text after 3 seconds
          setTimeout(function functionName() {
            $('#send-mail').text('Sende Test Mail');
          }, 3000);
        } else if (data.success) {
          // Change button text
          $('#send-mail').text('Fehler beim Versenden');
          // Change button text after 3 seconds
          setTimeout(function functionName() {
            $('#send-mail').text('Sende Test Mail');
          }, 3000);

          // If API sent error show it
          if (data.error) {
            alert(data.error);
          }
        }
      });
  });
});
