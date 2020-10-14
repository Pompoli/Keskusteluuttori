$(function() {
  $(".submit").click(() => $.post('',
    {'speaker': JSON.stringify(SPEAKER)},
    data => window.location.href = '/'));
  return $("#name").change(function() {
    return SPEAKER.name = $(this).val();
  });
});
