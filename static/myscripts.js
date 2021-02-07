$(document).ready(function() {
  $('li:not(.header)').hide();

  $('li.header').click(function() {
    $(this).find('span').text(function(_, value) {
      return value == '-' ? '+' : '-'
    });
    
    $(this).nextUntil('li.header').slideToggle(100, function() {});
  });
});